from django.urls import path

from .views import *

urlpatterns = [
    path('', FavoritesView.as_view(), name='favorites'),
    path('add-to-favorite/', AddToFavoriteView.as_view(), name='add_to_favorite'),
    path('remove-from-favorites-by-id/<int:favorite_id>/', RemoveFavoriteByIdView.as_view(), name='remove_favorite_by_id'),
    path('check/<int:product_id>/', CheckFavoriteView.as_view(), name='check_favorite'),
    path('remove-from-favorites-by-product/', RemoveFavoriteByProductView.as_view(), name='remove_favorite_by_product'),
]
