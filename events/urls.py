from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('create/', views.create, name="create"),
    path('<int:id>/confirm', views.confirm, name="confirm"),
    path('<int:id>/', views.single, name="single"),
    path('all/', views.all_events, name="all_events"),
    path('edit/<int:id>/', views.edit, name="edit"),
    path('my/', views.my_events, name="my_events"),
    path('<int:id>/participants', views.participants, name="participants"),
    path('<int:id>/hide_show', views.hide_show, name="hide_show"),
    path('<int:id>/signup', views.signup, name="signup")
]
