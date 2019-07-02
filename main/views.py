from django.shortcuts import render
from .models import City
from .forms import CityForm
import requests


def index(request):
    app_id = '5fed592c4901dc15bdf14c25066cdc15'
    url = 'https://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=' + app_id

    if request.method == 'POST':
        form = CityForm(request.POST)
        form.save()

    form = CityForm()  # Clear form
    cities = City.objects.all()
    all_cities = []

    for city in cities:
        response = requests.get(url.format(city.name)).json()  # we using .json for convert JSON format to Py {Dictionary}
        city_info = {
            'city': city.name,
            'country': response['sys']['country'],
            'temperature': response['main']['temp'],
            'pressure': response['main']['pressure'],
            'icon': response['weather'][0]['icon']
        }
        all_cities.append(city_info)

    context = {'all_info': all_cities, 'form': form}
    return render(request, 'main/index.html', context)


#  Json
'''{"coord":{"lon":24.03,"lat":49.84},"weather":[{"id":800,"main":"Clear","description":"clear sky","icon":"01n"}],"base":"stations","main":{"temp":25,"pressure":1013,"humidity":61,"temp_mi
n":25,"temp_max":25},"visibility":10000,"wind":{"speed":2,"deg":210},"clouds":{"all":0},"dt":1562007420,"sys":{"type":1,"id":8909,"message":0.0071,"country":"UA","sunrise":1561947558,"su
nset":1562006142},"timezone":10800,"id":702550,"name":"Lviv","cod":200}
'''
