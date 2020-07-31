import tmdb_client
from unittest.mock import Mock
import requests


def test_get_poster_url_uses_default_size():
    # Przygotowanie danych
    poster_api_path = "/w342/e1mjopzAS2KNsvpbpahQ1a6SkSn.jpg"
    expected_default_size = 'w342'
    # Wywołanie kodu, który testujemy
    poster_url = tmdb_client.get_poster_url(poster_api_path=poster_api_path)
    # Porównanie wyników
    assert expected_default_size in poster_url


def test_get_movies_list(monkeypatch):
    # Lista, którą będzie zwracać przysłonięte "zapytanie do API"
    mock_movies_list = ['Movie 1', 'Movie 2']

    requests_mock = Mock()
    # Wynik wywołania zapytania do API
    response = requests_mock.return_value
    # Przysłaniamy wynik wywołania metody .json()
    response.json.return_value = mock_movies_list
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)

    movies_list = tmdb_client.get_movies_list(list_type="popular")
    assert movies_list == mock_movies_list


def test_get_single_movie(monkeypatch):
    mock_movie = ['mov1', 'mov2', 'mov3', 'mov4', 'mov5']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = mock_movie
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movie = tmdb_client.get_single_movie(movie_id=1)
    assert movie == mock_movie


def test_get_sinle_movie_images(monkeypatch):
    movie_images_mock = ['img1', 'img2', 'img3', 'img4']
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = movie_images_mock
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movie_images = tmdb_client.get_single_movie_images(movie_id=1)
    assert movie_images == movie_images_mock


class MockResponse():
    @staticmethod
    def json():
        return {"mock_key": "mock_response"}


def test_get_json(monkeypatch):
    def mock_get(*args, **kwargs):
        return MockResponse.json()

    monkeypatch.setattr(requests, "get", mock_get)
    result = tmdb_client.requests.get("https://fakeurl")
    assert result["mock_key"] == "mock_response"


def test_get_single_movie_cast(monkeypatch):
    movie_cast_mock = {'cast': 'Ja'}
    requests_mock = Mock()
    response = requests_mock.return_value
    response.json.return_value = movie_cast_mock
    monkeypatch.setattr("tmdb_client.requests.get", requests_mock)
    movie = tmdb_client.get_single_movie_cast(movie_id=1, how_many=2)
    assert movie == movie_cast_mock['cast']

