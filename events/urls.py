from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create_event"),
    path('<int:id>/confirm', views.confirm, name="confirm"),
    path('<int:id>/', views.single, name="single"),
    path('all/', views.all_events, name="all_events"),
    path('edit/<int:id>/', views.edit, name="edit"),
    path('my/', views.my_events, name="my_events"),
    path('participants/<int:id>/', views.participants, name="participants"),
    path('hide_show/<int:id>/', views.hide_show, name="hide_show"),
    path('signup/<int:id>/', views.signup, name="signup")
]
