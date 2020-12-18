from bs4 import BeautifulSoup


def create_soup(html):
    """Return soup object given HTML string."""
    return BeautifulSoup(html, 'html.parser')


def test_app(test_client, mock_greet, mock_retrieve_local_ip_address):
    """
    GIVEN a test client
    WHEN it visits '/'
    THEN the response is OK and is the main project page
    """
    response = test_client.get('/')
    soup = create_soup(response.data)
    expected_greeting = mock_greet.return_value[0]

    mock_greet.assert_called_once()
    mock_retrieve_local_ip_address.assert_called_once()
    assert response.status_code == 200
    assert soup.select_one('title').text == 'WQU Project'
    assert soup.select_one('div.text-content > p').text.strip() == expected_greeting
