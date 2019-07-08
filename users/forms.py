from .models import Artist, Fan, Genre
from django.forms import ModelForm
from django.db import models
from django.utils.safestring import mark_safe
from django import forms
from allauth.account.forms import SignupForm
from django.forms import TextInput, Select, Textarea, RadioSelect, NumberInput
from django.core.files.images import get_image_dimensions
from django.utils.translation import gettext as _
import q1.functions as functions
import re


class RadioSelect(RadioSelect):
    def render(self, *args, **kwargs):
        output = super(RadioSelect, self).render(*args, **kwargs)
        output = output.replace(u'<li>', u'')
        output = output.replace(u'</li>', u'<br />')
        return mark_safe(output.replace(u'<ul id="id_hobbies">', u''))

class ArtistSignUpForm(SignupForm):
    def save(self, request):
        user = super(ArtistSignUpForm, self).save(request)
        user.save()
        functions.create_artist(user)
        return user

class FanSignUpForm(SignupForm):
    def save(self, request):
        user = super(FanSignUpForm, self).save(request)
        user.save()
        functions.create_fan(user)
        return user

class ArtistForm(ModelForm):
    honeypot = forms.CharField(required=False,widget=forms.HiddenInput)
    class Meta:
        model = Artist
        fields = ['profile_picture', 'name', 'genres', 'first_name', 'last_name', 'city', 'city_district', 'description']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Förnamn'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Efternamn'}),
            'genres': RadioSelect(),
            'city': TextInput(attrs={'class': 'form-control', 'placeholder': 'Stad... ex. Stockholm, Göteborg...'}),
            'city_district': TextInput(attrs={'class': 'form-control', 'placeholder': 'Kommun: ex. Sollentuna, Täby...'}),
            'description': Textarea(attrs={'class': 'form-control', 'placeholder': 'Kort biografi om dig själv: Hej...', 'rows':20}),
        }
        #Check for errors on a database level
        error_messages = {
            'first_name': {
                'required': _('Du måste fylla i ditt förnamn'),
                'max_length': _('Texten du skrev in här var för långt'),
            },
            'last_name': {
                'required': _('Du måste fylla i ditt efternamn'),
                'max_length': _('Texten du skrev in här var för långt'),
            },
            'genres': {
                'required': _('Du måste välja en genre'),
            },
            'city': {
                'required': _('Du måste fylla i din stad'),
                'max_length': _('Texten du skrev in här var för långt'),
            },
            'city_district': {
                'required': _('Du måste fylla i din kommun/stadsdel'),
                'max_length': _('Texten du skrev in här var för långt'),
            },
            'description': {
                'max_length': _('Texten du skrev in här var för långt, max 2500 tecken'),
            },
        }

    #Check for errors on a application level
    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[a-zA-ZåäöÅÄÖØ ]*$', first_name):
            raise forms.ValidationError(("Du har använt ogiltiga tecken i det här fältet"), code="invalid_first_name")
        else:
            return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[a-zA-ZåäöÅÄÖØ ]*$', last_name):
            raise forms.ValidationError(("Du har använt ogiltiga tecken i det här fältet"), code="invalid_last_name")
        else:
            return last_name

    def clean_city(self):
        city = self.cleaned_data['city']
        if not re.match(r'^[a-zA-ZåäöÅÄÖØ ]*$', city):
            raise forms.ValidationError(("Du har använt ogiltiga tecken i det här fältet"), code="invalid_city")
        else:
            return city

    def clean_city_district(self):
        city_district = self.cleaned_data['city_district']
        if not re.match(r'^[a-zA-ZåäöÅÄÖØ ]*$', city_district):
            raise forms.ValidationError(("Du har använt ogiltiga tecken i det här fältet"), code="invalid_city_district")
        else:
            return city_district

    def clean_profile_picture(self):
        try:
            profile_picture = self.cleaned_data['profile_picture']

            try:
                w, h = get_image_dimensions(profile_picture)

                #validate dimensions
                max_width = 1080
                max_height = 1080
                if w > max_width or h > max_height:
                    raise forms.ValidationError(_('Din profilbild får inte vara större än pixlar på höjden eller %s på bredden') % (max_width, max_height))

                #validate content type
                main, sub = profile_picture.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'jpg', 'png']):
                    raise forms.ValidationError(_('Du måste ladda upp en .jpg eller .png fil.'))

                #validate file size
                if len(profile_picture) > (1000 * 1024):
                    raise forms.ValidationError(_('Din profilbild får inte vara större än 1 Megabyte i storlek.'))

            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new profile_picture
                """
                pass

            return profile_picture

        except:
            pass

    #Not important
    def clean_honeypot(self):
        honeypot = self.cleaned_data['honeypot']
        if len(honeypot):
            raise forms.ValidationError()
        else:
            return honeypot

    #Please ignore
    def clean(self):
        cleaned_data=super(ArtistForm, self).clean()

class FanForm(ModelForm):
    honeypot = forms.CharField(required=False,widget=forms.HiddenInput)
    class Meta:
        model = Fan
        fields = ['profile_picture', 'first_name', 'last_name', 'telephone']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Förnamn'}),
            'last_name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Efternamn'}),
            'telephone': TextInput(attrs={'class': 'form-control', 'placeholder': 'Telefonnummer'}),
        }
        error_messages = {
            'first_name': {
                'required': _('Du måste fylla i ditt förnamn'),
                'max_length': _('Texten du skrev in här var för långt'),
            },
            'last_name': {
                'required': _('Du måste fylla i ditt efternamn'),
                'max_length': _('Texten du skrev in här var för långt'),
            },
            'telephone': {
                'required': _('Du måste fylla i ett telefonnummer'),
                'max_length': _('Texten du skrev in här var för långt'),
            },
        }

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not re.match(r'^[a-zA-ZåäöÅÄÖØ ]*$', first_name):
            raise forms.ValidationError(_("Du har använt ogiltiga tecken i det här fältet"), code="invalid_first_name")
        else:
            return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not re.match(r'^[a-zA-ZåäöÅÄÖØ ]*$', last_name):
            raise forms.ValidationError(_("Du har använt ogiltiga tecken i det här fältet"), code="invalid_last_name")
        else:
            return last_name

    def clean_telephone(self):
        telephone = self.cleaned_data['telephone']
        mobile_regex = r'^(\+46|0|\(\+46\)) *(7[0236])( |-|)(\d{4} \d{3}|\d{3} \d{4}|\d{3} \d{2} \d{2}|\d{2} \d{2} \d{3}|\d{7})$'
        home_phone_regex = r'^(\+46|0|\(\+46\)) *(8)( |-|)(\d{4} \d{2}|\d{2} \d{4}|\d{3} \d{3}|\d{2} \d{2} \d{2}|\d{6})$'
        if re.match(mobile_regex, telephone) or re.match(home_phone_regex, telephone):
            return telephone
        else:
            raise forms.ValidationError(_("Du måste ange ett giltigt telefonnummer"), code="invalid_telephone")

    def clean_profile_picture(self):
        try:
            profile_picture = self.cleaned_data['profile_picture']

            try:
                w, h = get_image_dimensions(profile_picture)

                #validate dimensions
                max_width = 1080
                max_height = 1080
                if w > max_width or h > max_height:
                    raise forms.ValidationError(_('Din profilbild får inte vara större än pixlar på höjden eller %s på bredden') % (max_width, max_height))

                #validate content type
                main, sub = profile_picture.content_type.split('/')
                if not (main == 'image' and sub in ['jpeg', 'jpg', 'png']):
                    raise forms.ValidationError(_('Du måste ladda upp en .jpg eller .png fil.'))

                #validate file size
                if len(profile_picture) > (1000 * 1024):
                    raise forms.ValidationError(_('Din profilbild får inte vara större än 1 Megabyte i storlek.'))

            except AttributeError:
                """
                Handles case when we are updating the user profile
                and do not supply a new profile_picture
                """
                pass

            return profile_picture

        except:
            pass
