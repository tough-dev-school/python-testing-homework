from django.urls import path

from server.apps.pictures.views import DashboardView, FavouritePicturesView

app_name = 'pictures'

urlpatterns = [
    path('dashboard', DashboardView.as_view(), name='dashboard'),
    path('favourites', FavouritePicturesView.as_view(), name='favourites'),
]
