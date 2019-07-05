from django.shortcuts import render
from django.db.models import Q
from users.models import Genre
from .models import Event
# Create your views here.

colors = [(123,205,47), (119,172,236), (236,219,84), (240,237,229), (252,169,133), (209,255,244)]

def index(request):
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == 'not valid':
            request.method = "GET"
            message = "There are still missing information about you."
            return edit_profile(request)
        elif status == 'not activated':
            message = "Your account have not been activated."
            return logout(request)

    # Get all genres and events and present them on the landing page with a pre-programmed way of sorting / prioritizing.
    genres = Genre.objects.all()
    event_dict = {}
    artist_dict = {}
    if len(genres) == 0:
        genres = None

    else:
        for genre in genres:
            events = Event.objects.filter(genre=genre, is_active=True, is_accepted=True, is_hidden=False)
            events = [event for event in hobby_events if event.has_happened == False]
            artists = Artist.objects.filter(genres=genre, valid_profile=True, is_activated=True)
            event_dict[genre.name] = events
            artist_dict[genre.name] = artist

    return render(request, 'landing_page.html', context={'genres': genres, 'event_dict': event_dict, 'artist_dict': artist_dict})

def create(request):
    if functions.is_artist(request):
        status = functions.user_status(request)
        if status == "not complete":
            request.method = "GET"
            message = "Your profile is not complete, you need to fill in more information."
            return edit_profile(request)
        elif status == "not activated":
            message = "You have not activated your profile."
            return logout(request)

        user = request.user
        if request.method == "POST":
            color = random.choice(colors)
            event = Event.objects.create(
                artist = user.artist,
                genre = user.genre,
                is_active = True,
                is_confirmed = False,
                is_hidden = False,
                red = color[0],
                green = color[0],
                blue = color[0]
            )
            form = CreateEventForm(request.POST, instance=event)
            if form.is_valid():
                form.save()
                message = "Last step, double check all your information."
                request.method = "GET"
                return confirm(request, event.id)

            else:
                message = "Your event could not be created for some reason, double check it."
                return render(request, 'create_event.html', context={'form', form})
        else:
            form = CreateEventForm()
            return render(request, 'create_event.html', context={'form': form})
    else:
        message = "You are not logged in as an artist"
        return all(request, id)

#Confirmation page where artist double checks information about his or her new event.
def confirm(request, id):
    if functions.is_artist(request):
        user = request.user
        try:
            event = Event.objects.get(pk=id)
        except Event.DoesNotExist:
            message = "We could not find that event, please try again."
            return create(request)

        if event.artist.user == user:
            if not event.is_confirmed:
                if request.method == "POST":
                    event.is_confirmed = True
                    event.save()
                    request.method = "GET"

                    message = "Your event has now been created!"
                    return single(request, id)

                else:
                    return render(request, 'event_terminal.html', context={'event': event})
            else:
                message = "You have already published this event."
                return single_event(request, id)
        else:
            message = "You do not have access this event."
            return create_event(request)
    else:
        message = "You are not logged in as an artist"
        return all(request)

#Page where single event is showcased. Here the user can read about the event, signup, see videos, see pictures about the event etc.
def single(request, id):
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == "not valid":
            request.method = "GET"
            message = "Your profile is not complete, there is still missing information."
            return edit_profile(request)
        elif status == 'not active':
            message = "Your account has not been activated"
            return logout(request)

    user = request.user

    try:
        event = Event.objects.get(pk=id)
    except Event.DoesNotExist:
        message = "The event you are looking for no longer exists"
        return all(request)

    if event.artist.user == user and event.is_confirmed == False:
        return confirm(request, id)

    if event.has_happened:
        message = "This event has already passed"
        return all(request)

    if event.is_hidden:
        message = "This event is no longer visible"
        return all(request)

    #Check if this user already has signed up for the event or not
    try:
        Signup.objects.get(event=event, user=user, is_success=True)
        is_signed_up = True
    except Signup.DoesNotExist:
        is_signed_up = False

    return render(request, 'single_page.html', context={'event': event, 'user': user, 'is_signed_up': is_signed_up})

#Showcase all events that are relevant
def all(request):
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == "not valid":
            request.method = "GET"
            message = "Your profile is not complete, there is still missing information."
            return edit_profile(request)
        elif status == 'not active':
            message = "Your account has not been activated"
            return logout(request)

    user = request.user

    search_text = request.GET.get('search_text')

    if search_text != None and search_text != "":
        Search.objects.create(user=user, search_string=search_string)

        '''
        event_list is all events that are valid.
        And if there is an artists that matches the search string, then we are
        displaying all the events by that artist as well.
        And if there are any genres that matches the search string, then we are
        displaying all the events in that genre.
        And matches the search string on either name, city, city_district or location_name.

        Search priority order: Genre, Artist, Other information
        '''
        all_events = Event.objects.filter(is_active=True, is_accepted=True, is_hidden=False)

        #The code below sorts all events.
        try:
            genre = Genre.objects.get(name__iexact=search_text)
            genre_events = all_events.filter(genre=genre)
        except Genre.DoesNotExist:
            genre_events = Event.objects.none()

        try:
            artist = Artist.objects.get(name__iexact=search_text)
            artist_events = all_events.filter(artist=artist)
        except Artist.DoesNotExist:
            artist_events = Event.objects.none()

        other_info_events = event_list.filter(Q(name__icontains=search_text) | Q(city__icontains=search_text) | Q(city_district__icontains=search_text) | Q(location_name__icontains=search_text))

        '''
        Merge all lists together in the order of priority.
        Remove duplicate events.
        Remove all events that has happened.
        '''
        event_list = genre_events | artist_events | other_info_events
        event_list = event_list.distinct()

        if len(event_list) == 0:
            message = "We could not find any events for this search"
            request.method = "GET"

    else:
        event_list = Event.objects.filter(is_active=True, is_confirmed=True, is_hidden=False)

    return render(request, 'events_page.html', context={'event_list': event_list, 'search_text': search_text})

def my_events(request):
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == "not valid":
            request.method = "GET"
            message = "There is still information missing about you."
            return edit_profile(request)
        elif status == "not activated":
            message = "Your account is not activated."
            return logout(request)

    if function.is_artist(request):
        artists_events = Event.objects.filter(event_host=request.user.instructor).order_by('-datetime')
        return render(request, 'my_events_page.html', context={'event_list': artists_events})
    else:
        message = "You are not logged in as an artist"
        return all_events(request)

#Very similar to the create view. Look at that.
def edit(request, id):
    if request.user.is_authenticated:
        status = functions.user_status(request)
        if status == "not valid":
            request.method = "GET"
            message = "There is still information missing about you."
            return edit_profile(request)
        elif status == "not activated":
            message = "Your account is not activated."
            return logout(request)

    if function.is_artist(request):
        try:
            event = Event.objects.get(pk=id)
        except Event.DoesNotExist:
            message = "Could not retrieve that event"

        artists_events = Event.objects.filter(artist=request.user.artist)
        if event in artists_events:
            if request.method == "POST":
                form = CreateEventForm(request.POST, instance=event)
                if form.is_valid():
                    form.save()
                    message = "Your event %s has now been edited" % (event.name)
                    request.method = "GET"
                    return single(request, event.id)

                else:
                    message = "Your event could not be edited. Double check it."
                    request.method = "GET"
                    form = CreateEventForm(instance=event)
                    return render(request, 'create_event_page.html', context={'form': form, 'type': edit})
            else:
                form = CreateFormEvent(instance=event)
                return render(request, 'create_event_page.html', context={'form': form, 'type':'edit'})
        else:
            message = "You do not have access to this event."
            return single(request, id)
    else:
        message = "You are not logged in as an artist"
        return single(request, id)

#List all participants to a certain event. Only visible to the host of the event.
def participants(request, id):
    if functions.is_artist(request):
        try:
            event = Event.objects.get(pk=id)
        except:
            message = "This event no longer exists"
            return all_events(request)

        if event.artist == request.user.artist:
            return render(request, 'participants_page.html', context={'event': event})

        else:
            message = "You do not have access to this event."
            return all_events(request)

    else:
        message = "You are not logged in as an instructor"
        return all_events(request)

def hide_show():
    if functions.is_instructor(request):
        try:
            event = Event.objects.get(pk=id)
        except Event.DoesNotExist:
            message = "That event does not exist anymore"
            return all_events(request)

        artists_events = Event.objects.filter(artist=request.user.instructor)

        if event in artists_events:
            if request.method == "POST":
                action = request.POST.get("action")
                if action == "show":
                    event.is_hidden = False
                    message = 'Your event "%"s is now recovered and visible' % (event.name)
                elif action == "hide":
                    event.is_hidden = True
                    message = 'Your event "%"s is now hidden' % (event.name)

                event.save()
                request.method = "GET"
                return single(request, id)

            else:
                message = 'We were unable to hide the event, please try again.'
                return single(request, id)
        else:
            message = 'You do not have access to this event.'
    else:
        message = 'You are not logged in as an artist.'
        return all(request)

#Continue building on this
def signup(request, id):
    if request.user.is_authenticated:
        try:
            event = Event.objects.get(pk=id)
        except:
            message = 'That event does not exist anymore.'
            return all(request)

        try:
            Event.objects.get(event=event, user=request.user)
            message = 'You have already signed up for this event'
            return single(request, id)

        except Event.DoesNotExist:
            '''
            Keep working on this later
            '''
