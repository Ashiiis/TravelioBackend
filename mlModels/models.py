from django.db import models

class CityData(models.Model):
    city = models.CharField(max_length=100)
    name = models.CharField(max_length=100, default='Unknown') 
    G_rating = models.FloatField()
    reviews = models.FloatField()
    fee = models.FloatField()
    significance = models.CharField(max_length=100)
    place_img = models.URLField(max_length=500, null=True, blank=True)
    place_img_1 = models.URLField(max_length=500, null=True, blank=True)
    place_img_2 = models.URLField(max_length=500, null=True, blank=True)
    place_img_3 = models.URLField(max_length=500, null=True, blank=True)
    place_img_4 = models.URLField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.city
    
class Hotel(models.Model):
    city = models.ForeignKey(CityData, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=200)
    hotel_price = models.FloatField()
    stars = models.FloatField(null=True, blank=True)
    hotel_rating = models.FloatField()
    # Add other relevant fields from hotel.csv

    def __str__(self):
        return self.hotel_name
