from django.shortcuts import render, redirect
from allauth.account.views import SignupView
from .forms import ArtistForm, FanForm, ArtistSignUpForm, FanSignUpForm
from django.contrib.auth import logout as logout_function
import q1.functions as functions
from django.contrib import messages
from events.views import index
from django.contrib.auth.models import User
from .models import Artist, Fan

# Create your views here.
class ArtistSignUp(SignupView):
    '''
    Present Signup form for artists
    '''
    template_name = 'custom_allauth/signup_artist.html'
    form_class = ArtistSignUpForm
    redirect_field_name = 'next'
    view_name = 'artist_sign_up'

    def get_context_data(self, **kwargs):
        ret = super(ArtistSignUp, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

class FanSignUp(SignupView):
    '''
    Present signup form for fans
    '''
    template_name = 'custom_allauth/signup_fan.html'
    form_class = FanSignUpForm
    redirect_field_name = 'next'
    view_name = 'fan_sign_up'

    def get_context_data(self, **kwargs):
        ret = super(FanSignUp, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

#This view lists all artists
def artists(request):
    '''
    Get and present all artists
    '''
    context = {}

    genre_list = Genre.objects.all()
    for genre in genre_list:
        artists = Artist.objects.filter(valid_profile=True, is_active=True)
        temp_dict = {}
        for artist in artists:
            events = Event.objects.filter(artist=artist, is_active=True, is_accepted=True, is_hidden=False)
            events = [event for event in events if event.has_happened == False]
            temp_dict[artist.name] = events
        context[genre.name] = temp_dict

    artists = Artist.objects.filter(valid_profile=True, is_active=True)

    return render(request, 'artists_page.html', context={'context':context})

#This view lists all artists of a certain genre
def artists_genre(request, genre):
    '''
    Get and present all artist of a specific genre

    genre: String | Name of the genre we are filtering with
    '''
    context = {}

    try:
        genre = Genre.objects.get(name=genre)
        artists = Artist.objects.filter(genres=genre, valid_profile=True, is_active=True)
        temp_dict = {}
        for artist in artists:
            events = Event.objects.filter(artist=artist, is_active=True, is_accepted=True, is_hidden=False)
            events = [event for event in events if event.has_happened == False]
            temp_dict[artist.name] = events
        contect[genre.name] = temp_dict

    except Genre.DoesNotExist:
        pass

    return render(request, 'artists_page.html', context={'context':context})

#This view presents the user's own profile
def my_profile(request):
    '''
    Get and present the profile of the current user
    '''
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == 'not valid':
            request.method = "GET"
            messages.error(request, 'There is still missing info about you.')
            return edit_profile(request)
        elif status == 'not activated':
            messages.error(request, 'Your account is not activated.')
            return logout(request)

        user = request.user

        if functions.is_artist(request) or functions.is_fan(request):
            return profile_id(request, user.id)
        else:
            messages.error(request, 'Something went wrong, please try again.')
            return logout(request)
    else:
        messages.error(request, 'You are not logged in')
        return redirect('account_login')
def profile_id(request, id):
    '''
    Get and present the profile of the user with a specific id

    id: Integer | Primary key used to find the user
    '''
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == 'not valid':
            request.method = "GET"
            message = 'There is still information missing about you.'
            return edit_profile(request)
        elif status == 'not active':
            messages.error(request, 'Your account has not been activated')
            return logout(request)

    user = request.user

    try:
        user = User.objects.get(pk=user.id)
    except User.DoesNotExist:
        messages.error(request, 'This profile no longer exists')
        return render(request, 'profile_page.html')

    if functions.is_artist(request):
        profile = Artist.objects.get(user=user)
    elif functions.is_fan(request):
        profile = Fan.objects.get(user=user)
    else:
        message = 'This profile no longer exists.'
        return render(request, 'profile_page.html')

    if profile.is_active == False:
        message = 'This profile is no longer active'
        return render(request, 'profile_page.html')

    if profile.is_artist:
        genre_list = Genre.objects.filter(artist=profile)
    else:
        genre_list = []

    return render(request, 'profile_page.html', context={'genre_list': genre_list, 'profile':profile, 'user':user})


def edit_profile(request):
    '''
    Present edit profile form for both fans and artists
    '''

    user = functions.get_authenticated_user(request)

    if user != None:
        if functions.is_artist(request):
            form_type = ArtistForm
            form_obj = user.artist
        elif functions.is_fan(request):
            form_type = FanForm
            form_obj = user.fan
        else:
            return index(request)

        #If request method is POST, try to save the form data into the database
        if request.method == "POST":
            form = form_type(request.POST, request.FILES, instance=form_obj)
            if form.is_valid():
                form.save()
                form_obj.valid_profile = True
                form_obj.save()
                messages.success(request, 'Your profile has been saved')
                request.method = "GET"
                return my_profile(request)
            else:
                messages.error(request, 'Your profile was not changed')
                return render(request, 'edit_profile_page.html', context={'form': form})
        #If it is not POST, generate a new form with all the infromation already in the form
        else:
            form = form_type(None, instance=form_obj)
            return render(request, 'edit_profile_page.html', context={'form':form})

    else:
        messages.error(request, 'You are not logged in')
        return redirect('account_login')

def logout(request):
    '''
    Logout the current user
    '''
    logout_function(request)
    messages.info(request, 'You have been logged out')
    return index(request)

def boost(request):
    '''
    Lets a user boost an artist
    '''
    pass

def follow(request):
    '''
    Lets a user follow an artist
    '''
    user = get_authenticated_user(request)
    if user != None:
        if user.is_artist:
            profile = user.artist
        elif user.is_fan:
            profile = user.fan
        else:
            profile = None

        if request.method == "POST":
            user_id = request.method.POST.get('user_id')
        else:
            return my_profile(request)

        try:
            artist = User.objects.get(pk=user_Id)
            if artist.is_artist == False:
                messages.error(request, 'You can only follow other artists')
                return profile_id(request, user_id)

        except User.DoesNotExist:
            messages.error(request, 'This profile does not exist anymore')
            return profile_id(request, user_id)

        try:
            Follower.objects.get(instructor=artist.artist, follower=user)
            messages.error(request, 'You are already following %s.' % (artist.artist.name))

        except Follower.DoesNotExist:
            pass

        if profile == None:
            messages.error(request, 'You do not have the authority to follow artists')
            return profile_id(request, user_id)

        else:
            if user == artist:
                messages.error(request, 'You cannot follow yourself')
                return profile_id(request, user_id)
            else:
                Follower.objects.create(artist=artist.artist, follower=user)
                messages.success(request, 'You are now following %s.' % (artist.artist))
                return profile_id(request, user_id)
    else:
        messages.error(request, 'You have to be logged in')
        return profile_id(request, user_id)

def unfollow(request):
    '''
    Lets a user unfollow an artist
    '''
    if request.user.is_authenticated:
        user = functions.get_authenticated_user(request)
        if user.is_artist:
            profile = user.artist
        elif user.is_fan:
            profile = user.fan
        else:
            profile = None

        if request.method == "POST":
            user_id = request.POST.get('user_id')
        else:
            return my_profile(request)

        try:
            artist = User.objects.get(pk=user_id)
            if artist.is_artist == False:
                messages.error(request, 'You can only unfollow artists')
                return profile_id(request, user_id)

        except User.DoesNotExist:
            messages.error(request, 'This profile no longer exists')
            return profile_id(request, user_id)

        if profile == None:
            messages.error(request, 'You are not authorized to unfollow artists')
            return profile_id(request, user_id)
        else:
            if user == artist:
                messages.error(request, 'You cannot unfollow yourself')
                return profile_id(request, user_id)
            else:
                follows = Follower.objects.filter(artist=artist.artist, follower=user)
                if len(follow) == 0:
                    messages.error(request, 'You are not currently following this artist')
                    return profile_id(request, user_id)
                else:
                    for follow in follows:
                        follow.delete()
                message.info(request, 'You have now unfollowed %s.' (artist.artist.name))
                return profile_id(request, user_id)
    else:
        message.error(request, 'You have to be logged in')
        return profile_id(request, user_id)

def settings(request):
    user = functions.get_authenticated_user(request)
    if user != None:
        return render(request, 'settings_page.html', {'this_user': user})
    else:
        return index(request)

def terms_of_use(request):
    pass

def integrity(request):
    pass
