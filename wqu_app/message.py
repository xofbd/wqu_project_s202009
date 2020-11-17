import requests

def retrieve_local_ip_adress():
    """Return IP address of our computer."""
    response = requests.get('https://api.ipify.org')
    
    return response.text
    

def get_geolocation(ip_address):
    """Return gelociaton of an IP address."""
    response = requests.get(f'https://ipinfo.io/{ip_address}')
    data = response.json()
    coords = [float(coord) for coord in data['loc'].split(',')]

    return coords


def get_weather(coords):
    """Return weather data for a given set of coordinates."""
    url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
    params = {'lat': coords[0], 'lon': coords[1]}

    response = requests.get(url, params=params)
    data = response.json()
    
    return data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature']

def greet(ip_address):
    coords = get_geolocation(ip_address)
    temperature = get_weather(coords)
    
    return f"Hello, the temperature is {temperature} deg C"
    

if __name__ == '__main__':
    print(greet())