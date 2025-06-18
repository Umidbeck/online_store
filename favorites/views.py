from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, ListView

from .models import Favorite, Product
import json



class AddToFavoriteView(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            product_id = data.get('product_id')
            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)

            product = Product.objects.get(id=product_id)
            favorite, created = Favorite.objects.get_or_create(user=request.user, product=product)

            if created:
                return JsonResponse({'success': True, 'action': 'added', 'message': ''})
            else:
                favorite.delete()
                return JsonResponse({'success': True, 'action': 'removed', 'message': ''})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mahsulot topilmadi!'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Noto‘g‘ri JSON format!'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class FavoritesView(LoginRequiredMixin, TemplateView):
    template_name = 'favorites/favorit.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites'] = Favorite.objects.filter(user=self.request.user)
        return context


class RemoveFromFavoritesView(LoginRequiredMixin, View):
    """
    Remove a product from the user's favorites list via DELETE request.
    CSRF protection is enabled; ensure tokens are sent via HTMX or AJAX.
    """
    def _remove_favorite(self, pk):
        """Helper method to handle the removal logic."""
        try:
            favorite = Favorite.objects.get(id=pk, user=self.request.user)
            favorite.delete()
            return {'success': True, 'action': 'removed', 'message': ''}
        except Favorite.DoesNotExist:
            return {'success': False, 'error': 'Mahsulot topilmadi!', 'status': 404}

    def delete(self, request, pk, *args, **kwargs):
        """Handle DELETE request to remove a favorite."""
        response_data = self._remove_favorite(pk)
        return JsonResponse(response_data, status=response_data.get('status', 200))