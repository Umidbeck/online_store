from django.views import View
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Cart, CartItem
import json


class CartView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_items = cart.items.all()
        data = {
            'items': [
                {'id': item.id, 'product': item.product.name, 'quantity': item.quantity, 'price': item.total_price()}
                for item in cart_items],
            'total': sum(item.total_price() for item in cart_items)
        }
        return JsonResponse({'success': True, 'cart': data})


class AddToCartView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            product_id = data.get('product_id')
            if not product_id:
                return JsonResponse({'success': False, 'error': 'Product ID is required'}, status=400)

            product = Product.objects.get(id=product_id)
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product, defaults={'quantity': 1})

            if not created:
                cart_item.quantity += 1
                cart_item.save()
            return JsonResponse({'success': True, 'action': 'added', 'message': ''})
        except Product.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Mahsulot topilmadi!'}, status=404)
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Noto‘g‘ri JSON format!'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


class UpdateCartItemView(LoginRequiredMixin, View):
    def post(self, request, *args, **kwargs):
        try:
            data = json.loads(request.body.decode('utf-8'))
            item_id = data.get('item_id')
            quantity = data.get('quantity')
            if not item_id or quantity is None:
                return JsonResponse({'success': False, 'error': 'Item ID and quantity are required'}, status=400)

            cart_item = CartItem.objects.get(id=item_id, cart__user=request.user)
            if quantity <= 0:
                cart_item.delete()
            else:
                cart_item.quantity = quantity
                cart_item.save()
            return JsonResponse({'success': True, 'action': 'updated', 'message': ''})
        except CartItem.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Cart item topilmadi!'}, status=404)
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
