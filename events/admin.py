from django.contrib import admin
from .models import Event, Signup, Search

# Register your models here.
admin.site.register(Event)
admin.site.register(Signup)
admin.site.register(Search)
