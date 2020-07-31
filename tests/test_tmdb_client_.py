from main import app
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize('n, result', (
    ('movie/popular', 200),
    ('movie/now_playing', 200),
    ('movie/top_rated', 200),
    ('movie/upcoming', 200),
))
def test_homepage(monkeypatch, n, result):
    api_mock = Mock(return_value={'results': []})
    monkeypatch.setattr("tmdb_client.call_tmdb_api", api_mock)

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == result