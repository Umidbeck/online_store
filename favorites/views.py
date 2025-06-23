from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from .models import Favorite, Product
import json


class AddToFavoriteView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            product_id = data.get('product_id')
            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)

            product = Product.objects.get(id=product_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)
            if not created:
                return JsonResponse({'success': False, 'error': 'Already in favorites!'}, status=400)
            return JsonResponse({'success': True})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Product not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'favorites/favorit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.filter(user=self.request.user)
        return context


class RemoveFavoriteByIdView(LoginRequiredMixin, View):
    def delete(self, request, favorite_id, *args, **kwargs):
        try:
            favorite = Favorite.objects.get(id=favorite_id, user=request.user)
            favorite.delete()
            return JsonResponse({'success': True})
        except Favorite.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Favorite not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class RemoveFavoriteByProductView(LoginRequiredMixin, View):
    def delete(self, request, *args, **kwargs):
        product_id = request.GET.get('product_id')
        if not product_id:
            return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)
        try:
            favorite = Favorite.objects.get(product_id=product_id, user=request.user)
            favorite.delete()
            return JsonResponse({'success': True})
        except Favorite.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Favorite not found!'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class CheckFavoriteView(LoginRequiredMixin, View):
    def get(self, request, product_id, *args, **kwargs):
        try:
            favorite = Favorite.objects.filter(user=request.user, product_id=product_id).first()
            is_favorite = favorite is not None
            favorite_id = favorite.id if favorite else None
            return JsonResponse({'success': True, 'is_favorite': is_favorite, 'favorite_id': favorite_id})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)