from django.shortcuts import render
from django.http import JsonResponse
from .ml_engine import train_and_predict # The file we created earlier
import datetime

def forecast_view(request):
    # These would ideally come from your Weather API
    current_temp = 31 
    current_day = datetime.datetime.now().weekday() 

    # Get the "Scientific" prediction
    predicted_cups = train_and_predict(current_temp, current_day)

    # Fallback if there isn't enough data yet
    if predicted_cups is None:
        predicted_cups = "Need more data"

    return render(request, 'PAGES/forecast.html', {
        'predicted_cups': predicted_cups
    })

def get_prediction_api(request):
    temp     = float(request.GET.get('temp', 30))
    humidity = float(request.GET.get('humidity', 60))
    day      = datetime.datetime.now().weekday()

    prediction = train_and_predict(temp, day)

    reason = "Normal demand expected."
    if temp < 20:   reason = "Cold weather detected — hot drink demand is elevated."
    elif temp > 30: reason = "High heat detected — iced drink demand is elevated."
    if humidity > 80: reason += " High humidity may reduce foot traffic."

    return JsonResponse({
        'prediction': prediction if prediction else "Need Data",
        'reason': reason,
        'accuracy': 0.87,      # Replace with real model.score(X, y) from ml_engine
        'row_count': 34,       # Replace with real len(df) from ml_engine
        'products': [          # Replace with real per-product predictions
            {'name': 'Hot Coffee',  'qty': 95,  'trend': 'down'},
            {'name': 'Iced Coffee', 'qty': 130, 'trend': 'up'},
        ]
    })