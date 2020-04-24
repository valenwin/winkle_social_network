from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, TemplateView

from .forms import LoginForm, UserEditForm, ProfileEditForm


class WincleBaseView(TemplateView):
    template_name = 'base.html'


class DashboardBaseView(LoginRequiredMixin, TemplateView):
    template_name = 'account/my_dashboard.html'


class RegistrationCompleteView(TemplateView):
    template_name = 'django_registration/registration_complete.html'


class LoginView(SuccessMessageMixin, FormView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    success_url = reverse_lazy('home_page')
    success_message = ''

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        """Sets a test cookie to make sure the user has cookies enabled"""
        request.session.set_test_cookie()
        return super(LoginView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        cd = form.cleaned_data
        user = authenticate(self.request,
                            username=cd.get('username'),
                            password=cd.get('password'))
        if user is not None:
            if user.is_active:
                login(self.request, user)
                self.success_message = 'Authenticated successfully.'
            else:
                self.success_message = 'Disabled accounts.'
        else:
            self.success_message = 'Invalid credentials.'

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super(LoginView, self).form_valid(form)


class LogoutView(SuccessMessageMixin, RedirectView):
    url = reverse_lazy('home_page')
    success_message = ''

    def get(self, request, *args, **kwargs):
        logout(request)
        self.success_message = 'Logout successfully.'
        return super(LogoutView, self).get(request, *args, **kwargs)


@login_required
def update_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile,
                                       data=request.POST,
                                       files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully.')
        else:
            messages.error(request, 'Error updating your profile.')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/update_user_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form
    })
