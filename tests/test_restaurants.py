"""
Tests for restaurant API endpoints
"""
import pytest
from src.main import app


@pytest.fixture
def client():
    """Create a test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_index(client):
    """Test the index endpoint"""
    response = client.get('/')
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Chowdeck Restaurant API'
    assert 'endpoints' in data


def test_health(client):
    """Test the health check endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert data['service'] == 'chowdeck-api'


def test_get_restaurants(client):
    """Test getting all restaurants"""
    response = client.get('/api/restaurants')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'count' in data
    assert 'data' in data
    assert isinstance(data['data'], list)


def test_get_restaurants_with_city_filter(client):
    """Test filtering restaurants by city"""
    response = client.get('/api/restaurants?city=Lagos')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    # Verify all returned restaurants are from Lagos
    for restaurant in data['data']:
        assert restaurant['city'] == 'Lagos'


def test_get_restaurants_with_limit(client):
    """Test limiting restaurant results"""
    response = client.get('/api/restaurants?limit=5')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert len(data['data']) <= 5


def test_get_restaurant_by_id(client):
    """Test getting a specific restaurant"""
    # First get all restaurants
    response = client.get('/api/restaurants')
    restaurants = response.get_json()['data']

    if restaurants:
        # Get the first restaurant by ID
        restaurant_id = restaurants[0]['id']
        response = client.get(f'/api/restaurants/{restaurant_id}')
        assert response.status_code == 200
        data = response.get_json()
        assert data['success'] is True
        assert data['data']['id'] == restaurant_id


def test_get_nonexistent_restaurant(client):
    """Test getting a restaurant that doesn't exist"""
    response = client.get('/api/restaurants/nonexistent_id')
    assert response.status_code == 404
    data = response.get_json()
    assert data['success'] is False
    assert 'error' in data


def test_refresh_restaurants(client):
    """Test refreshing restaurant data"""
    response = client.post('/api/restaurants/refresh')
    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] is True
    assert 'count' in data
