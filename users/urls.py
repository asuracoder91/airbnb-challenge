from django.urls import path
from . import views

urlpatterns = [
    path("", views.Users.as_view()),
    path("me", views.Me.as_view()),
    path("password", views.ChangePassword.as_view()),
    path("login", views.LogIn.as_view()),
    path("logout", views.LogOut.as_view()),
    path("<int:pk>", views.OneUser.as_view()),
    path("<int:pk>/tweets", views.UserTweets.as_view()),
]
