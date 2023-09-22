from django.urls import path

from server.apps.pictures.views import DashboardView, FavouritePicturesView, FavouriteDeleteView

app_name = 'pictures'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('favourites', FavouritePicturesView.as_view(), name='favourites'),
    path('favourites/<int:picture_id>', FavouriteDeleteView.as_view(), name='remove_favourite'),
]
