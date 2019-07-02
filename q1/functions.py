from users.models import Artist, Fan

def is_artist(request):
    if request.user.is_authenticated:
        try:
            Artist.objects.get(user=request.user)
            return True
        except Artist.DoesNotExist:
            return False
    else:
        return False

def is_fan(request):
    if request.user.is_authenticated:
        try:
            Fan.objects.get(user=request.user)
            return True
        except Fan.DoesNotExist:
            return False
    else:
        return False

def get_authenticated_user(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None

    return user

def user_status(request):
    user = request.user
    if is_artist(request):
        try:
            artist = Artist.objects.get(user=user)
            if artist.valid_profile:
                if artist.is_activated:
                    return 'success'
                else:
                    return 'not active'
            else:
                return 'not valid'
        except Artist.DoesNotExist:
            artist = Artist.objects.create(user=user)
            artist.save()
            return False

    elif is_fan(request):
        try:
            fan = Fan.objects.get(user=user)
            if fan.valid_profile:
                if fan.is_activated:
                    return 'success'
                else:
                    return 'not active'
            else:
                return 'not valid'
        except Fan.DoesNotExist:
            fan = Fan.objects.get(user=user)
            fan.save()
            return False

def create_artist(user):
    artist = Artist.objects.create(user=user)
    artist.save()
    return artist

def create_fan(user):
    fan = Fan.objects.create(user=user)
    fan.save()
    return fan
