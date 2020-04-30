from django.views.generic import TemplateView


class ProfilesBaseView(TemplateView):
    template_name = 'account/profiles.html'


class MyProfileBaseView(TemplateView):
    template_name = 'account/user_profile.html'
