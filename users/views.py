from django.shortcuts import render
from allauth.account.views import SignupView
from .forms import ArtistForm, FanForm, ArtistSignupForm, FanSignupForm

# Create your views here.
class ArtistSignup(SignupView):
    template_name = 'custom_allauth/signup_artist.html'
    form_class = ArtistSignupForm
    redirect_field_name = 'next'
    view_name = 'artist_signup'

    def get_context_data(self, **kwargs):
        ret = super(ArtistSignup, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

class FanSignup(SignupView):
    template_name = 'custom_allauth/signup_fan.html'
    form_class = FanSignupForm
    redirect_field_name = 'next'
    view_name = 'fan_sign_up'

    def get_context_data(self, **kwargs):
        ret = super(FanSignup, self).get_context_data(**kwargs)
        ret.update(self.kwargs)
        return ret

def artists(request):
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

def artists_genre(request, genre):
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

def my_profile(request):
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == 'not valid':
            request.method = "GET"
            message = "There is still missing info about you"
            return edit_profile(request)
        elif status == 'not activated':
            message = 'Your account is not activated.'
            return logout(request)
        else:
            if functions.is_artist(request) or functions.is_fan(request):
                return profile_id(request, user.id)
            else:
                message = 'Something went wrong, please try again.'
                return logout(request)

def profile_id(request, id):
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
        user = User.objects.get(pk=user_id)
    except:
        messages.error(request, 'This profile no longer exists')
        return render(request, 'profile_page.html')

    if user.is_artist:
        profile = Artist.objects.get(user=user)
    elif user.is_fan:
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
    pass

def login(request):
    pass

def logout(request):
    pass

def boost(request):
    pass

def follow(request):
    pass

def unfollow(request):
    pass

def terms_of_use(request):
    pass

def integrity(request):
    pass
