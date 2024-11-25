from django.urls import path
from .views import get_city_and_hotel_data, recommend_top_10_cities


urlpatterns = [
    path('get-data/', get_city_and_hotel_data, name='get_city_and_hotel_data'),
    path('top-10/', recommend_top_10_cities, name='recommend_top_10_cities'),


]
