from django.conf import settings
from django.core.management.base import BaseCommand
from ...models import CityData, Hotel  # Adjust to your app name
import csv
import os

class Command(BaseCommand):
    help = 'Load data from CSV files into the CityData and Hotel models'

    def handle(self, *args, **kwargs):
        # Load City Data
        city_csv_path = os.path.join(settings.CSV_FILES_DIR, 'cities.csv')
        with open(city_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city, created = CityData.objects.get_or_create(
                    city=row['City'],
                    name=row.get('Name', 'Unknown'),  # Add the name field
                    G_rating=row['G_rating'],
                    reviews=row['reviews'],
                    fee=row['fee'],
                    significance=row['Significance'],
                    place_img=row.get('Place_img', None),
                    place_img_1=row.get('Place_img_1', None),
                    place_img_2=row.get('Place_img_2', None),
                    place_img_3=row.get('Place_img_3', None),
                    place_img_4=row.get('Place_img_4', None),
                )

        # Load Hotel Data
        hotel_csv_path = os.path.join(settings.CSV_FILES_DIR, 'hotel.csv')
        with open(hotel_csv_path, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                city, created = CityData.objects.get_or_create(
                    city=row['City'],
                    defaults={
                        'G_rating': 0,
                        'reviews': 0,
                        'fee': 0,
                        'significance': 'Unknown',
                        'name': 'Unknown',  # Add default name here as well
                    }
                )

                hotel, created = Hotel.objects.get_or_create(
                    city=city,
                    hotel_name=row['Hotel_Name'],
                    hotel_price=row['Hotel_Price'],
                    stars=row.get('Stars', None),
                    hotel_rating=row['Hotel_Rating']
                )
