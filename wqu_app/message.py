import requests


def retrieve_local_ip_adress():
    """Return IP address of our computer."""
    response = requests.get('https://api.ipify.org')

    return response.text


def get_geolocation(ip_address):
    """Return gelociaton of an IP address."""
    response = requests.get(f'https://ipinfo.io/{ip_address}')
    data = response.json()
    city = data['city']
    coords = [float(coord) for coord in data['loc'].split(',')]

    return coords, city


def get_weather(coords):
    """Return weather data for a given set of coordinates."""
    url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
    params = {'lat': coords[0], 'lon': coords[1]}

    response = requests.get(url, params=params)
    data = response.json()

    return data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']


def greet(ip_address):
    coords = get_geolocation(ip_address)[0]
    temperature = get_weather(coords)
    city = get_geolocation(ip_address)[1]

    return f"Hello, the temperature in {city}(where your internet provider is located) is {temperature} deg C"


if __name__ == '__main__':
    print(greet())
