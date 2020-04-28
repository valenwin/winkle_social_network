from django.urls import path

from .views import ImageCreateView, ImageDashboardListView, ImageDetailsView
from .views import image_like

urlpatterns = [
    path('create/', ImageCreateView.as_view(), name='create'),
    path('dashboard/', ImageDashboardListView.as_view(), name='dashboard'),
    path('image/<str:slug>/', ImageDetailsView.as_view(), name='image_details'),
    path('like', image_like, name='like')

]
