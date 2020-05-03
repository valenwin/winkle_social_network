import redis
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
from winkle_social_network.utils import pagination
from .forms import ImageCreateForm, CommentForm
from .models import Image


redis_connect = redis.StrictRedis(host=settings.REDIS_HOST,
                                  port=settings.REDIS_PORT,
                                  db=settings.REDIS_DB)


class WincleBaseView(ListView):
    template_name = 'base.html'
    paginate_by = settings.POSTS_PER_PAGE

    def get_queryset(self):
        images_by_popularity = Image.objects.order_by('-total_likes')
        return images_by_popularity

    def get_context_data(self, *, object_list=None, **kwargs):
        """With pagination for posts list view"""
        context = super(WincleBaseView, self).get_context_data(**kwargs)
        images_by_popularity = self.get_queryset()
        context['images_by_popularity'] = pagination(self.request,
                                                     images_by_popularity,
                                                     self.paginate_by)
        return context


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
        total_views = redis_connect.incr('image:{}:views'.format(image.id))
        redis_connect.zincrby('img_ranking', image.id, 1)
        context['image'] = image
        context['form'] = CommentForm()
        context['comments'] = image.comments.filter(active=True)
        context['total_views'] = total_views
        context['section'] = 'images'
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


@login_required
def image_ranking(request):
    # get image ranking dictionary
    img_ranking = redis_connect.zrange('img_ranking', 0, -1, desc=True)[:10]
    image_ranking_ids = [int(id) for id in img_ranking]
    # get most viewed images
    most_viewed = list(Image.objects.filter(
                           id__in=image_ranking_ids))
    most_viewed.sort(key=lambda x: image_ranking_ids.index(x.id))
    return render(request, 'images/image/ranking.html', {
                      'section': 'images',
                      'most_viewed': most_viewed
                  })
