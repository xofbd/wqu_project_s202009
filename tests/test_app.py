import pytest

from wqu_app.app import app


@pytest.fixture
def test_client():
    with app.test_client() as test_client:
        return test_client


def test_app(test_client):
    """
    GIVEN a test client
    WHEN it visits '/'
    THEN the response has a 200 status code
    """
    response = test_client.get('/')

    assert response.status_code == 200
