import requests
import pandas as pd
from datetime import datetime, timedelta
import altair as alt


HEADERS = {'User-Agent': 'WQU weather application', 'Accept': 'application/json'}


def retrieve_local_ip_adress():
    """Return IP address of our computer."""
    response = requests.get('https://api.ipify.org', headers=HEADERS)

    return response.text


def get_geolocation(ip_address):
    """Return gelociaton of an IP address."""
    response = requests.get(f'https://ipinfo.io/{ip_address}', headers=HEADERS)
    data = response.json()
    city = data['city']
    coords = [float(coord) for coord in data['loc'].split(',')]

    return coords, city


def get_weather(coords):
    """Return current temperature and forecast for a given set of coordinates."""
    url = 'https://api.met.no/weatherapi/locationforecast/2.0/compact'
    params = {'lat': coords[0], 'lon': coords[1]}
    response = requests.get(url, params=params, headers=HEADERS)
    data_forecast = response.json()['properties']['timeseries']
    current_temp = data_forecast[0]['data']['instant']['details']['air_temperature']

    return current_temp, data_forecast


def get_forecast(forecast_series):
    """Return iterable of time-temp tuple pairs for the next 24 hours."""
    time = [forecast_series[i]['time'] for i in range(3, 27)]
    temperature = [
        forecast_series[i]['data']['instant']['details']['air_temperature']
        for i in range(3, 27)
    ]

    return zip(time, temperature)


def generate_chart(next_24h):
    """Return JSON of Vega visualization of 24 hour forecast."""
    df = pd.DataFrame(next_24h, columns=['time', 'Temperature'])
    min_scaler = min(df['Temperature']) * 1.1
    max_scaler = max(df['Temperature']) * 1.1
    df['Time'] = [
        datetime.strptime(df['time'][i], '%Y-%m-%dT%H:%M:%Sz')
        for i in range(len(df))
    ]
    df['Time'] = df['Time'].apply(lambda x: x + timedelta(minutes=59)
                                  if x.hour == 23 else x)
    df['Day'] = [df['Time'][i].strftime("%A") for i in range(len(df))]

    hour_chart = (alt.Chart(df)
                  .mark_line(point={'filled': False, 'fill': 'white'})
                  .encode(alt.X('Time', sort=None),
                          alt.Y('Temperature',
                                scale=alt.Scale(domain=(min_scaler, max_scaler))),
                          tooltip=['Temperature', 'Time'],
                          color='Day').properties(width=600, height=400)
                  .interactive(name=None, bind_x=True, bind_y=True))
    chart_json = hour_chart.to_json()
    return chart_json


def greet(ip_address):
    coords, city = get_geolocation(ip_address)
    temperature, forecast_series = get_weather(coords)
    next_24h = get_forecast(forecast_series)
    chart_forecast = generate_chart(next_24h)
    msg_str = (f"Hello, the temperature in {city} (based on your IP address)"
               f" is {temperature} deg C")

    return msg_str, chart_forecast


if __name__ == '__main__':
    ip_address = retrieve_local_ip_adress()
    msg_str, chart_forecast = greet(ip_address)
    print(msg_str)
