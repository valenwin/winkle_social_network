from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import CreateView, DetailView, ListView, DeleteView, UpdateView

from winkle_social_network.common.decorators import ajax_required
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
    template_name = 'images/dashboard.html'
    context_object_name = 'images'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        return Image.objects.filter(user=self.request.user)

    def get_context_data(self, *, object_list=None, **kwargs):
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

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        image = get_object_or_404(self.model, slug=self.kwargs.get('slug'))
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


class ImageUpdateView(LoginRequiredMixin, UpdateView):
    model = Image
    form_class = ImageCreateForm
    template_name = 'images/image/update.html'

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can update posts """
        obj = self.get_object()
        if obj.user != self.request.user:
            messages.error(request, 'Restricted access. You are not owner of this image.')
            return redirect(obj)
        return super(ImageUpdateView, self).dispatch(request, *args, **kwargs)


class ImageDeleteView(LoginRequiredMixin, DeleteView):
    model = Image
    template_name = 'images/image/delete.html'
    success_url = reverse_lazy('images:dashboard')

    def dispatch(self, request, *args, **kwargs):
        """ Making sure that only authors can delete posts """
        obj = self.get_object()
        if obj.user != self.request.user and not request.user.is_superuser:
            messages.error(request, 'Restricted access. You are not owner of this image.')
            return redirect(obj)
        return super(ImageDeleteView, self).dispatch(request, *args, **kwargs)


@ajax_required
@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except:
            pass
    return JsonResponse({'status': 'ok'})
