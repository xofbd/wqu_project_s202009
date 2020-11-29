import requests
import pandas as pd
from datetime import datetime, timedelta
import altair as alt
import altair_viewer


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
    headers = {'User-Agent': 'WQU weather application'}
    response = requests.get(url, params=params, headers=headers)
    data = response.json()

    return data['properties']['timeseries'][0]['data']['instant']['details']['air_temperature'], data['properties']['timeseries']

def get_forecast(forecast_series):
    forecast_list = []
    for i in range(3, 27):
        forecast_list.append([forecast_series[i]['time'],forecast_series[i]['data']['instant']['details']['air_temperature']])
    return forecast_list

def generate_chart(next_24h):
    df = pd.DataFrame(next_24h, columns=['time', 'Temperature'])
    min_scaler = min(df['Temperature'])*1.1
    max_scaler = max(df['Temperature'])*1.1
    df['Time'] = [datetime.strptime(df['time'][i],'%Y-%m-%dT%H:%M:%Sz') for i in range(0,len(df))]
    df['Time'] = df['Time'].apply(lambda x: x + timedelta(minutes=59) 
                      if x.hour == 23 else x)
    df['Day'] = [df['Time'][i].strftime("%A") for i in range(0,len(df))]
    
   
    hour_chart = alt.Chart(df[['Time', 'Temperature', 'Day']]).mark_line(point={'filled':False,'fill':'white'}).encode(alt.X('Time', sort=None),
                                                    alt.Y('Temperature', scale=alt.Scale(domain=(min_scaler,max_scaler))),
                                                    tooltip=['Temperature', 'Time'],
                                                    color = 'Day').properties(width=600,height=400).interactive(
                                                        name=None, bind_x=True, bind_y=True)
    
    chart_json = hour_chart.to_json()
    return chart_json

def greet(ip_address):
    coords, city = get_geolocation(ip_address)
    temperature, forecast_series = get_weather(coords)
    next_24h = get_forecast(forecast_series)
    chartForecast = generate_chart(next_24h)
    return f"Hello, the temperature in {city} (based on your IP address) is {temperature} deg C", chartForecast


if __name__ == '__main__':
    print(greet())
