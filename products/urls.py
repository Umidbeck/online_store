from core.views import HomeView
from .views import *
from django.urls import path

urlpatterns = [
    path('product/detail/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('product/list/', ProductList.as_view(), name='product_list'),
]
