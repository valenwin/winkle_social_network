from django.urls import path

from .views import ImageCreateView, ImageDashboardListView, ImageDetailsView
from .views import ImageUpdateView, ImageDeleteView
from .views import image_like, image_ranking

urlpatterns = [
    path('create/', ImageCreateView.as_view(), name='create'),
    path('dashboard/', ImageDashboardListView.as_view(), name='dashboard'),
    path('image/<str:slug>/', ImageDetailsView.as_view(), name='image_details'),
    path('image/<str:slug>/update/', ImageUpdateView.as_view(), name='update'),
    path('image/<str:slug>/delete/', ImageDeleteView.as_view(), name='delete'),

    path('like', image_like, name='like'),
    path('ranking/', image_ranking, name='create'),

]
