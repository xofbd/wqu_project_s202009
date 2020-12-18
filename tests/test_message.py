import json
import os
from unittest.mock import patch

from wqu_app.message import get_forecast, get_geolocation, get_weather
from .conftest import DATA_DIR


def test_get_geolocation(response):
    """
    GIVEN an IP address for North Bergen, NJ
    WHEN get_geolocation is called
    THEN return the proper coordinates and city name
    """
    path_response = os.path.join(DATA_DIR, 'geolocation_response.json')
    with patch('wqu_app.message.requests.get') as mock_get:
        mock_get.return_value = response(path_response)
        coords, city = get_geolocation('157.245.254.219')

    mock_get.assert_called_once()
    assert coords == [40.8043, -74.0121]
    assert city == 'North Bergen'


def test_get_weather(response, coords):
    """
    GIVEN a tuple of coordinates
    WHEN get_weather is called for that tuple
    THEN the correct current temperature and forecast is returned
    """
    current_temp_expected = -6.0
    with open(os.path.join(DATA_DIR, 'forecast.json'), 'r') as f:
        forecast_expected = json.load(f)

    path_response = os.path.join(DATA_DIR, 'weather_response.json')
    with patch('wqu_app.message.requests.get') as mock_get:
        mock_get.return_value = response(path_response)
        current_temp, forecast = get_weather(coords)

    mock_get.assert_called_once()
    assert current_temp == current_temp_expected
    assert forecast == forecast_expected


def test_get_forecast(forecast):
    """
    GIVEN a forecast series JSON
    WHEN get_forecast is called with that JSON
    THEN an iterable of tuples of hourly timestamps and temperature is returned
    """

    # Loading the JSON results in a list of lists but we need a zip object,
    # which is in iterable of tuples. The code below properly formats the
    # result for comparison. Further, to compare the functions output, the
    # objects are converted to lists in which an actual element-by-element
    # comparison can be made.
    with open(os.path.join(DATA_DIR, 'next_24h.json'), 'r') as f:
        next_24h_expect = json.load(f)
    next_24h_expect = zip(*zip(*next_24h_expect))

    assert list(get_forecast(forecast)) == list(next_24h_expect)
