from django.views.generic import TemplateView, DetailView
from products.models import Category, Product
import random


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()[:8]
        context['bestsellers'] = Product.objects.order_by('-stock')[:8]  # Stock bo'yicha tartiblangan
        context['featured_products'] = random.sample(list(Product.objects.all()), 2)  # Tasodifiy 10 ta mahsulot
        context['most_popular_products'] = Product.objects.all()
        context['latest_products'] = Product.objects.order_by('-created_at')[:2]
        # context['blogs'] = Blog.objects.order_by('-created_at')[:3]
        return context


class CategoryDetailView(DetailView):
    model = Category
    template_name = 'category_detail.html'  # Yangi template kerak bo'ladi
    slug_url_kwarg = 'slug'
    context_object_name = 'category'
