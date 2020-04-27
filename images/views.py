from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView

from .models import Image
from .forms import ImageCreateForm, CommentForm


class ImageCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Image
    form_class = ImageCreateForm
    template_name = 'images/image/create.html'
    success_url = reverse_lazy('images:dashboard')
    success_message = ''

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            'form': self.form_class(request.GET)
        })

    def form_valid(self, form):
        form.instance.user = self.request.user
        self.success_message = 'Image added successfully'
        return super().form_valid(form)


class ImageDashboardListView(LoginRequiredMixin, ListView):
    queryset = Image.objects.all()
    template_name = 'images/dashboard.html'
    context_object_name = 'images'
    paginate_by = settings.POSTS_PER_PAGE

    def get_context_data(self, **kwargs):
        """With pagination for posts list view"""
        context = super(ImageDashboardListView, self).get_context_data(**kwargs)
        images = self.get_queryset()

        page = self.request.GET.get('page')
        paginator = Paginator(images, self.paginate_by)
        try:
            images = paginator.page(page)
        except PageNotAnInteger:
            images = paginator.page(1)
        except EmptyPage:
            images = paginator.page(paginator.num_pages)

        context['images'] = images
        return context


class ImageDetailsView(DetailView):
    model = Image
    context_object_name = 'images'
    template_name = 'images/image/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.model.objects.get(slug=self.kwargs.get('slug'))
        context['image'] = image
        context['form'] = CommentForm()
        context['comments'] = image.comments.filter(active=True)
        return context

    def post(self, request, *args, **kwargs):
        try:
            form = CommentForm(request.POST)
            form.instance.image = self.model.objects.get(slug=self.kwargs.get('slug'))
            form.instance.user = self.request.user
            form.save()
            return redirect('images:image_details', slug=self.kwargs.get('slug'))
        except ValueError:
            return redirect(reverse_lazy('account:django_registration_register'))
