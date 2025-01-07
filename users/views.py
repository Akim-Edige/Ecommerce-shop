from django.contrib import messages
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView, UpdateView

from common.views import TitleMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm

from .models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    title = 'Store - Авторизация'

    def form_valid(self, form):
        # Check if the user is verified
        user = form.get_user()
        if user.is_verified:
            # Proceed with the normal login process
            return super().form_valid(form)
        else:
            # Add a message and redirect to the login page
            messages.error(self.request, "Please go to your email and verify your account.")
            return redirect('users:login')  # Replace 'login' with the name of your login URL pattern


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
    success_message = 'Success. Please verify your email address.'
    title = 'Store - Registration'


class VerifyUserView(TitleMixin, TemplateView):
    title = 'Store - Verify'
    template_name = 'users/email_verification.html'

    def get_context_data(self, **kwargs):
        instance = EmailVerification.objects.get(code=kwargs['code'])
        is_not_expired = timezone.now() < instance.expire_at
        if is_not_expired:
            instance.user.is_verified = True
            instance.user.save()
            instance.delete()
        else:
            instance.user.delete()

        context = {'not_expired': is_not_expired}
        return context


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name = 'users/profile.html'
    success_url = reverse_lazy('users:profile')
    title = 'Store - Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', kwargs={'pk': self.object.pk})
