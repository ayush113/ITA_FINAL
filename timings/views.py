from django.shortcuts import render

from django.db import connection
from notes.utils import namedtuplefetchall
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
from weather.models import City
import requests

@csrf_exempt
def timings(request):
    cities = City.objects.all()  # return all the cities in the database

    url = 'http://api.openweathermap.org/data/2.5/weather?q={}&units=imperial&appid=271d1234d3f497eed5b1d80a07b3fcd1'


    weather_data = []

    for city in cities:
        city_weather = requests.get(url.format(city)).json()  # request the API data and convert the JSON to Python data types

        weather = {
            'city': city,
            'temperature': round(5 * ((city_weather['main']['temp'] - 32) / 9), 2),
            'description': city_weather['weather'][0]['description'],
            'icon': city_weather['weather'][0]['icon']
        }

        if weather['temperature'] > float(25):
            weather['colour'] = 1
        else:
            weather['colour'] = 0

     # add the data for the current city into our list

    context = {'weather': weather}
    timings = None
    if(request.method == 'POST'):
        data = request.POST
        place = data.get('places')
        with connection.cursor() as curr:
            curr.execute("SELECT open_time,close_time,days_closed from timings where place_name=%s",[place])
            timings = namedtuplefetchall(curr)
    with connection.cursor() as curr:
        curr.execute("Select * from timings")
        res = namedtuplefetchall(curr)

    context['timings'] = res

    return render(request,'timings/index.html',context)