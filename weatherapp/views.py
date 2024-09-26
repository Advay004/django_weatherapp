from django.shortcuts import render

import requests
from django.conf import settings
# Create your views here.
API_KEY=settings.API_KEY
def index(request):
    
    
    current_weather_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}"


    if request.method=="POST":
        city1=request.POST['city1']
        city2=request.POST.get('city2',None)
        weatherdata1=fetch_weather_and_forecast(city1,API_KEY,current_weather_url)
        if city2:
            weatherdata2=fetch_weather_and_forecast(city2,API_KEY,current_weather_url)
        else:
            weatherdata2=None
            
        context={
            "weatherdata1":weatherdata1,
            
            "weatherdata2":weatherdata2,
            
        }
        return render(request,'index.html',context)

    else:
        return render(request,'index.html')
def fetch_weather_and_forecast(city, api_key, current_weather_url):
    try:
        # Fetch current weather data
        response = requests.get(current_weather_url.format(city, api_key)).json()

        # Check if the response contains the expected data
        if 'coord' not in response:
            print(f"Error: Unable to fetch coordinates for city: {city}")
            return None, None

        lat = response['coord']['lat']
        lon = response['coord']['lon']

    

        weatherdata = {
            "city": city,
            "temperature": round(response['main']['temp'] - 273.15, 2),
            "description": response['weather'][0]['description'],
            "icon": response['weather'][0]['icon']
        }


        return weatherdata

    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None



