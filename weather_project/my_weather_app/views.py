from django.shortcuts import render
from django.http import HttpResponse
import requests

# Create your views here.
def index(request):

    #Seoul data
    seoul_weather_data = fetch_weather('Seoul')

    #Cities lists
    cities = ['Yakutsk', 'Oymyakon', 'Ulaanbaatar', 'Dudinka', 'Yellowknife', 'Harbin', 'Winnipeg', 'International Falls', 'Fairbanks', 'Irkutsk']


    if request.method == "POST":
        compare_city = request.POST['compare_city']
        compare_city_weather_data = fetch_weather(compare_city)

        context = {
            "seoul_weather_data":seoul_weather_data,
            "compare_city_weather_data":compare_city_weather_data,
            "cities":cities
        }
    else:
        context = {
            "seoul_weather_data":seoul_weather_data,
            "cities":cities
        }
    
    return render(request, 'my_weather_app/index.html', context)

def fetch_weather(city):
    API_KEY = open("C:/Users/pomel/Documents/001/00/weather_project/my_weather_app/API_KEY.txt", "r").read()
    geocoding_api = "http://api.openweathermap.org/geo/1.0/direct?q={}&appid={}"
    current_weather_data_api = "https://api.openweathermap.org/data/2.5/weather?lat={}&lon={}&appid={}"

    response = requests.get(geocoding_api.format(city, API_KEY)).json()
    lat, lon = response[0]['lat'], response[0]['lon']
    country = response[0]['country']

    response = requests.get(current_weather_data_api.format(lat, lon, API_KEY)).json()

    weather_data = {
        "city": city,
        "country":country,
        "temp":round(response["main"]["temp"] - 273.15, 2),
        "description":response["weather"][0]["description"],
        "icon":response["weather"][0]["icon"]
    }

    return weather_data
