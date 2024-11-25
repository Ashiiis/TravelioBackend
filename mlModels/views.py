import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from fuzzywuzzy import process
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import CityData, Hotel
import json
import logging
from django.db.models import F

@csrf_exempt
def get_city_and_hotel_data(request):
    logging.info(f"Request method: {request.method}")

    if request.method == 'POST':
        # Handling POST requests
        try:
            data = json.loads(request.body)
            user_input = data.get('city_name', '').lower().strip()
            logging.info(f"User input: {user_input}")

            response_data = {}

            # Fetch available cities and hotels from the database
            available_cities = CityData.objects.values_list('city', flat=True)
            avail_hotels = Hotel.objects.values_list('city__city', flat=True).distinct()

            # Find best matches using fuzzy matching
            place_match = process.extractOne(user_input, available_cities)
            hotel_match = process.extractOne(user_input, avail_hotels)

            # For city data
            if place_match and place_match[1] > 50:
                city_filter = place_match[0]
                filtered_cities = CityData.objects.filter(city=city_filter)
                df_filtered = pd.DataFrame(list(filtered_cities.values()))
                df_filtered = df_filtered[df_filtered['G_rating'] < 5]

                df_sorted = df_filtered.sort_values(by=['G_rating', 'reviews', 'fee'], ascending=[False, False, True])
                grouped = df_filtered.groupby('significance').apply(
                    lambda x: x.sort_values(by=['G_rating', 'reviews', 'fee'], ascending=[False, False, True])
                ).reset_index(drop=True)

                response_data['grouped_places'] = grouped.to_dict(orient='records')
            else:
                response_data['grouped_places'] = "No close city match found."

            # For hotel data
            if hotel_match and hotel_match[1] > 50:
                hotel_filter = hotel_match[0]
                filtered_hotels = Hotel.objects.filter(city__city=hotel_filter)
                df_hotels = pd.DataFrame(list(filtered_hotels.values()))

                df_hotels['stars'] = df_hotels['stars'].fillna(df_hotels['stars'].mean())

                X = df_hotels[['hotel_price', 'stars', 'hotel_rating']]
                y = df_hotels['hotel_name']
                y_encoded, labels = pd.factorize(y)

                X_train, X_test, y_train, y_test = train_test_split(X, y_encoded, test_size=0.2, random_state=42)
                rf = RandomForestClassifier(n_estimators=100, random_state=0)
                rf.fit(X_train, y_train)

                y_pred = rf.predict(X_test)
                accuracy = accuracy_score(y_test, y_pred)
                logging.info(f'Accuracy: {accuracy * 100:.2f}%')

                predicted_hotel_names = labels[y_pred]
                predicted_df = X_test.copy()
                predicted_df['Predicted_Hotel_Name'] = predicted_hotel_names

                response_data['hotel_data'] = predicted_df.to_dict(orient='records')
            else:
                response_data['hotel_data'] = "No close hotel match found."

            return JsonResponse(response_data)

        except json.JSONDecodeError:
            logging.error("Invalid JSON format received.")
            return JsonResponse({"error": "Invalid JSON format"}, status=400)

        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    elif request.method == 'GET':
        # Optionally handle GET requests if needed for testing
        return JsonResponse({"message": "GET request received, but this endpoint expects POST requests."}, status=400)

    else:
        return JsonResponse({"error": "Invalid request method"}, status=400)


@csrf_exempt
def recommend_top_10_cities(request):
    logging.info(f"Request method: {request.method}")

    if request.method == 'GET':
        try:
            # Fetch all city data including images
            city_data = CityData.objects.all()
            df = pd.DataFrame(list(city_data.values()))

            # Calculate average footfall and rating
            city_footfall = df.groupby('city')['reviews'].sum()
            city_counts = df['city'].value_counts()
            avg_footfall = city_footfall / city_counts
            city_Greviews = df.groupby('city')['G_rating'].sum()
            avg_rating = city_Greviews / city_counts

            # Combine results into a DataFrame
            city_scores = pd.DataFrame({
                'avg_footfall': avg_footfall,
                'avg_rating': avg_rating
            })

            # Sort by average footfall and rating (descending) to get the top 10 cities
            top_10_cities = city_scores.sort_values(by=['avg_footfall', 'avg_rating'], ascending=[False, False]).head(10)

            # Merge with original dataframe to include all necessary info
            merged_df = pd.merge(top_10_cities.reset_index(), df[['city', 'place_img_1']], on='city')


            # Return top 10 cities as a list of dictionaries
            merged_df['image'] = merged_df['place_img_1']
            response_data = merged_df[['city', 'avg_footfall', 'avg_rating', 'image']].to_dict(orient='records')

            return JsonResponse({'top_10_cities': response_data})
    
        except Exception as e:
            logging.error(f"An error occurred: {str(e)}")
            return JsonResponse({"error": str(e)}, status=500)

    else:
        return JsonResponse({"error": "Invalid request method, only GET requests are allowed."}, status=400)
