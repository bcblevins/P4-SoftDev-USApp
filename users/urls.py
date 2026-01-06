"""URL routing for user authentication and profile actions."""

from django.urls import path
from django.contrib.auth import views as auth_views

from .views import (
    signup,
    profile,
    public_profile,
    follow,
    unfollow,
    search_users,
    CustomLoginView,
)

urlpatterns = [
    path("signup/", signup, name="signup"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(next_page="login"), name="logout"),
    path("profile/", profile, name="profile"),
    path("user/<int:user_id>/", public_profile, name="public_profile"),
    path("follow/<int:user_id>/", follow, name="follow"),
    path("unfollow/<int:user_id>/", unfollow, name="unfollow"),
    path("search/", search_users, name="search_users"),
]
