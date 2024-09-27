from django.urls import path
from .views import get_city_and_hotel_data


urlpatterns = [
    path('get-data/', get_city_and_hotel_data, name='get_city_and_hotel_data'),


]
