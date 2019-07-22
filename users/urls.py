from django.urls import path, include
from . import views

urlpatterns = [
    path('artists/', views.artists, name="artists"),
    path('artists/<str:genre_name>', views.artists_genre, name="artists_genre"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('profile/<int:id>/', views.profile_id, name="profile_id"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('artist_signup/', views.ArtistSignUp.as_view(), name="artist_signup"),
    path('fan_signup/', views.FanSignUp.as_view(), name="fan_signup"),
    path('settings/', views.settings, name="settings"),
    path('logout/', views.logout, name="logout"),
    path('boost/', views.boost, name="boost"),
    path('unboost/',views.unboost,name="unboost"),
    path('follow/', views.follow, name="follow"),
    path('unfollow/', views.unfollow, name="unfollow"),
    path('data/', views.data, name="data"),
    path('terms_of_use/', views.terms_of_use, name="terms_of_use"),
    path('integrity/', views.integrity, name="integrity"),
]
