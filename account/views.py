from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_POST
from django.views.generic import FormView, RedirectView, TemplateView, ListView, DetailView

from images.models import Image
from winkle_social_network.common.decorators import ajax_required
from .forms import LoginForm, UserEditForm, ProfileEditForm
from .models import CustomUser, Contact


class WincleBaseView(TemplateView):
    template_name = 'base.html'


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


class UserProfileListView(LoginRequiredMixin, ListView):
    template_name = 'account/profiles.html'
    paginate_by = settings.USER_PROFILE_PER_PAGE

    def get_queryset(self):
        return CustomUser.objects.all()

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(UserProfileListView, self).get_context_data(**kwargs)
        users = self.get_queryset()

        page = self.request.GET.get('page')
        paginator = Paginator(users, self.paginate_by)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)

        context['users'] = users
        return context


class UserProfileDetailsView(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'account/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(self.model, slug=self.kwargs.get('slug'))
        images = Image.objects.filter(user=user)
        context['user'] = user
        context['images'] = images
        return context


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


@ajax_required
@require_POST
@login_required
def user_follow(request):
    user_id = request.POST.get('id')
    action = request.POST.get('action')
    if user_id and action:
        try:
            user = get_object_or_404(CustomUser, id=user_id)
            if action == 'follow':
                Contact.objects.get_or_create(user_from=request.user, user_to=user)
            else:
                Contact.objects.filter(user_from=request.user, user_to=user).delete()
            return JsonResponse({'status': 'ok'})
        except CustomUser.DoesNotExist:
            return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'ok'})
