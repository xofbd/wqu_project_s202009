import json
import os
from unittest.mock import Mock, patch

import pytest

from wqu_app.app import app

DATA_DIR = os.path.join('tests', 'data')


@pytest.fixture
def mock_greet():
    with patch('wqu_app.app.greet') as mock_greet:
        mock_greet.return_value = (
            "Hello, the temperature in X (based on your IP address) is 10.5 deg C",
            '{"data": []}')
        yield mock_greet


@pytest.fixture
def mock_retrieve_local_ip_address():
    with patch('wqu_app.app.retrieve_local_ip_adress') as mock:
        mock.return_value = '157.245.254.219'
        yield mock


@pytest.fixture
def test_client():
    with app.test_client() as test_client:
        return test_client


@pytest.fixture
def response():
    """Fixture for a mocked response object with a given JSON response."""
    def wrapper(path_json):
        mock_response = Mock()
        with open(path_json, 'r') as f:
            mock_response.json.return_value = json.load(f)
        return mock_response
    return wrapper


@pytest.fixture
def forecast():
    """Fixture of forecast JSON."""
    with open(os.path.join(DATA_DIR, 'forecast.json'), 'r') as f:
        return json.load(f)


@pytest.fixture
def coords():
    """Fixture of coordinates."""
    return (40.8043, -74.0121)
