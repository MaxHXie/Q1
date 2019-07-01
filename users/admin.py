from django.contrib import admin
from .models import Genre, Artist, Fan, Boost, Follow, Visit

admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Fan)
admin.site.register(Boost)
admin.site.register(Follow)
admin.site.register(Visit)
