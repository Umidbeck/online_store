from django.shortcuts import render
from django.views.generic import ListView, TemplateView


# Create your views here.

class ProductListView(TemplateView):
    template_name = 'favorites/favorit.html'