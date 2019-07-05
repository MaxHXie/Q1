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

def user_status(request):
    user = request.user
    if is_artist(request):
        try:
            artist = Artist.objects.get(user=user)
            if artist.valid_profile:
                if artist.is_active:
                    return 'success'
                else:
                    return 'not_active'
            else:
                return 'not_valid'
        except Artist.DoesNotExist:
            artist = Artist.objects.create(user=user)
            artist.save()
            return False

    elif is_fan(request):
        try:
            fan = Fan.objects.get(user=user)
            if fan.valid_profile:
                if fan.is_active:
                    return 'success'
                else:
                    return 'not_active'
            else:
                return 'not_valid'
        except Fan.DoesNotExist:
            fan = Fan.objects.get(user=user)
            fan.save()
            return False
