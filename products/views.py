
from django.shortcuts import render
from django.views.generic import TemplateView, DetailView
from .models import Product


# Create your views here.
class ProductDetailView(DetailView):
    model = Product
    template_name = 'product/products_detail.html'
    slug_url_kwarg = 'slug'
    context_object_name = 'product'

class ProductList(TemplateView):
    template_name = 'products/products_detail.html'