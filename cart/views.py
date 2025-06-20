from django.views import View

from products.models import Product
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem
import json


class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.items.all()
            data = {
                'items': [{'id': item.id, 'product': item.product.name, 'quantity': item.quantity,
                           'price': item.total_price()} for item in cart_items],
                'total': sum(item.total_price() for item in cart_items) if cart_items.exists() else 0.00
            }
            return JsonResponse({'success': True, 'cart': data})
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)

            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product,
                                                                defaults={'quantity': quantity})

            if not created:
                return JsonResponse(
                    {'success': False, 'action': 'exists', 'message': 'Siz bu mahsulotni allaqachon qo\'shdingiz!'})
            else:
                if not created:  # Agar yangi emas bo'lsa, miqdorni oshirish
                    cart_item.quantity += quantity
                    cart_item.save()
                return JsonResponse({'success': True, 'action': 'added', 'message': ''})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mahsulot topilmadi!'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Noto‘g‘ri JSON format!'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class RemoveFromCartView(LoginRequiredMixin, View):
    def delete(self, request, item_id, *args, **kwargs):
        try:
            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            cart_item.delete()
            return JsonResponse({'success': True, 'action': 'removed', 'message': ''})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item topilmadi!'}, status=404)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)
