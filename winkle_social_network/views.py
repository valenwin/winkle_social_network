from django.views.generic import TemplateView


class ProfilesBaseView(TemplateView):
    template_name = 'find_profiles.html'


class MyProfileBaseView(TemplateView):
    template_name = 'my_profile_account.html'
