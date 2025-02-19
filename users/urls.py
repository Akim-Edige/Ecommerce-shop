from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from django.urls import path

from users.views import (UserLoginView, UserProfileView, UserRegistrationView,
                         VerifyUserView)

app_name = 'users'
urlpatterns = [
    path("profile/<int:pk>/", login_required(UserProfileView.as_view()), name='profile'),
    path("register/", UserRegistrationView.as_view(), name='registration'),
    path("login/", UserLoginView.as_view(), name='login'),

    path("logout/", LogoutView.as_view(), name='logout'),

    path("verify/<uuid:code>", VerifyUserView.as_view(), name='verify'),
]
