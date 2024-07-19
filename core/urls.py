from django.urls import path 
from . import views


urlpatterns =[
    path("", views.index, name="home_page"),
    path("settings", views.settings, name="settings"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),
]