from django.urls import path, include
from . import views

urlpatterns = [
    path('artists/', views.artists, name="artists"),
    path('artists/<str:genre>', views.artists_genre, name="artists_genre"),
    path('my_profile/', views.my_profile, name="my_profile"),
    path('profile/<int:id>/', views.profile_id, name="profile_id"),
    path('edit_profile/', views.edit_profile, name="edit_profile"),
    path('artist_signup/', views.ArtistSignup.as_view(), name="artist_signup"),
    path('fan_signup/', views.FanSignup.as_view(), name="fan_signup"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('boost/', views.boost, name="boost"),
    path('follow/', views.follow, name="follow"),
    path('unfollow/', views.unfollow, name="unfollow"),
    path('terms_of_use/', views.terms_of_use, name="terms_of_use"),
    path('integrity/', views.integrity, name="integrity"),
]
