from django.shortcuts import render
import json
import urllib.request
import requests
import math
from datetime import date, timedelta

from .models import Forecast

# Create your views here.
def index(request):

    if request.method == 'POST':
        try:
            city = request.POST.get('city', False) #['city']
            country_code = request.POST.get('country-code', False) 
            api_key = '68bc131971ee152eb1a65e6df7737770'

            # Direct Geocoding: Geographical coordinates (lat, lon)
            direct_geocode_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country_code}&appid={api_key}"
            geocode_json_data = requests.get(direct_geocode_url).json()
            geocode_data = {
                'lat': str(geocode_json_data[0]['lat']),
                'lon': str(geocode_json_data[0]['lon']),
            }
            # Grab weather for the next 7 days
            forecast_5_url = f"http://api.openweathermap.org/data/2.5/forecast?lat={geocode_data['lat']}&lon={geocode_data['lon']}&units=metric&appid={api_key}"
            json_data = requests.get(forecast_5_url).json()
            
            # Get the date for the next 5 days
            today = date.today()

            # Get Location
            location = {
                'city':json_data['city']['name'],
                'country': json_data['city']['country']
            }
            # Get the forecast for the next 5 days
            forecasts = []
            for i in range(len(json_data)):
                # Set date
                td = timedelta(i)
                today = today + td

                day = Forecast()
                day.day = today.strftime('%A')
                day.date = today.strftime('%B %d, %Y') 
                day.icon = str(json_data['list'][i]['weather'][0]['icon'])
                day.temp = math.ceil(int(json_data['list'][i]['main']['temp']))
                day.feels_like = math.ceil(int(json_data['list'][i]['main']['feels_like']))
                day.high = math.ceil(int(json_data['list'][i]['main']['temp_max']))
                day.low = math.ceil(int(json_data['list'][i]['main']['temp_min']))
                day.description = str(json_data['list'][i]['weather'][0]['description'])
                day.clouds = str(json_data['list'][i]['clouds']['all'])
                day.pop = math.ceil(float(json_data['list'][i]['pop'])*100)
                forecasts.append(day)
                
                # Reset date
                today = date.today()
        except KeyError:
            city = ''
            location = []
            forecasts = []
    
    return render(request, 'index.html', {'city':city, 'location':location, 'forecasts': forecasts})