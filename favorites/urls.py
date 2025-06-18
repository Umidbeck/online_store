from django.urls import path

from .views import *


urlpatterns = [
    path('add-to-favorite/', AddToFavoriteView.as_view(), name='add_to_favorite'),
    path('', FavoritesView.as_view(), name='favorites'),
    path('remove-from-favorites/<int:pk>/', RemoveFromFavoritesView.as_view(), name='remove_from_favorites'),
]