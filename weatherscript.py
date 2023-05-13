import argparse
import requests
import colorama
import datetime
from prettytable import PrettyTable

api_key = 'api-key'
base_url = 'http://api.openweathermap.org/data/2.5/weather'

emojis = {
    'clear': '☀️',
    'clouds': '☁️',
    'rain': '🌧️',
    'snow': '❄️',
    'thunderstorm': '⛈️',
    'mist': '🌫️'
}

def get_weather_data(city_name, table):
    params = {
        'q': city_name,
        'units': 'metric',
        'appid': api_key
    }

    response = requests.get(base_url, params=params)
    weather_data = response.json()

    temperature = weather_data['main']['temp']
    description = weather_data['weather'][0]['description']
    last_updated = datetime.datetime.fromtimestamp(weather_data['dt'])

    for key in emojis:
        if key in description.lower():
            emoji = emojis[key]
            break
    else:
        emoji = ''

    if temperature >= 25:
        color = colorama.Fore.RED
    elif temperature >= 20:
        color = colorama.Fore.YELLOW
    elif temperature >= 15:
        color = colorama.Fore.GREEN
    else:
        color = colorama.Fore.BLUE

    table.add_row([city_name.capitalize(), f"{color}{temperature:.1f}°C {emoji}{colorama.Style.RESET_ALL}", description, last_updated])

parser = argparse.ArgumentParser()
parser.add_argument('city_names', nargs='+')

args = parser.parse_args()

colorama.init()

table = PrettyTable()
table.field_names = ["City", "Temperature", "Weather Condition", "Last Updated"]

for city_name in args.city_names:
    get_weather_data(city_name, table)

print(table)
