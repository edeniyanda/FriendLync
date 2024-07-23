from django.urls import path 
from . import views


urlpatterns =[
    path("", views.index, name="home_page"),
    path("settings", views.settings, name="settings"),
    path("upload", views.upload, name="upload"),
    path("profile/<str:pk>", views.profile, name="profile"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("logout/", views.logout, name="logout"),
    path("like_post/", views.like_post, name="like_post"),
]