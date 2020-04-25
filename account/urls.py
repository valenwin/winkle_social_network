from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from django_registration.backends.one_step.views import RegistrationView

from .forms import CustomSignUpForm
from .views import RegistrationCompleteView
from .views import update_user

urlpatterns = [
    path('accounts/register/', RegistrationView.as_view(
        form_class=CustomSignUpForm, success_url='/'), name='django_registration_register'),
    path('register/complete', RegistrationCompleteView.as_view(), name='django_registration_register_complete'),

    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(
        success_url=reverse_lazy('account:password_change_done')), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('password_reset/', auth_views.PasswordResetView.as_view(
        success_url=reverse_lazy('account:password_reset_done')), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        success_url=reverse_lazy('account:password_reset_complete')), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('update/', update_user, name='update_profile'),

]
