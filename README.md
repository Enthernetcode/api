# Chowdeck Restaurant API

A Flask-based REST API to fetch and serve restaurant data from Chowdeck.

## Project Overview

This API scrapes restaurant information from Chowdeck's website and provides RESTful endpoints to access the data. It includes caching, filtering capabilities, and follows best practices for API development.

## Features

- REST API with multiple endpoints
- Web scraping with BeautifulSoup
- In-memory caching (1-hour TTL)
- City-based filtering
- CORS support
- Comprehensive test coverage
- Type hints and documentation

## Project Structure

```
api/
├── src/
│   ├── __init__.py
│   ├── main.py                 # Flask application entry point
│   ├── clients/
│   │   ├── __init__.py
│   │   └── chowdeck.py         # Web scraper for Chowdeck
│   └── restaurants/
│       ├── __init__.py
│       ├── handlers.py          # API route handlers
│       └── service.py           # Business logic layer
├── tests/
│   ├── __init__.py
│   ├── test_restaurants.py     # API endpoint tests
│   └── fixtures/               # Test data
├── scripts/                    # Utility scripts
├── .env.example                # Environment variable template
├── requirements.txt            # Python dependencies
├── Makefile                    # Development commands
├── AGENTS.md                   # Development guidelines
└── README.md                   # This file
```

## Installation

### Prerequisites

- Python 3.8+
- pip

### Setup

1. Install dependencies:
```bash
make install
# or
pip install -r requirements.txt
```

2. Create environment file:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Running the Server

```bash
# Development mode
make serve
# or
python3 -m src.main

# Production mode with Gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

The API will be available at `http://localhost:5000`

### API Endpoints

#### GET /
Get API information and available endpoints

```bash
curl http://localhost:5000/
```

#### GET /health
Health check endpoint

```bash
curl http://localhost:5000/health
```

#### GET /api/restaurants
Get all restaurants with optional filtering

**Query Parameters:**
- `city` (optional) - Filter by city name
- `limit` (optional) - Limit number of results

```bash
# Get all restaurants
curl http://localhost:5000/api/restaurants

# Filter by city
curl http://localhost:5000/api/restaurants?city=Lagos

# Limit results
curl http://localhost:5000/api/restaurants?limit=5

# Combine filters
curl http://localhost:5000/api/restaurants?city=Abuja&limit=10
```

**Response:**
```json
{
  "success": true,
  "count": 10,
  "data": [
    {
      "id": "rest_1",
      "name": "Sample Restaurant 1",
      "city": "Lagos",
      "description": "A popular restaurant in Lagos",
      "cuisine": "Nigerian",
      "rating": 4.0,
      "delivery_time": "20-30 mins"
    }
  ]
}
```

#### GET /api/restaurants/<id>
Get a specific restaurant by ID

```bash
curl http://localhost:5000/api/restaurants/rest_1
```

**Response:**
```json
{
  "success": true,
  "data": {
    "id": "rest_1",
    "name": "Sample Restaurant 1",
    "city": "Lagos",
    "description": "A popular restaurant in Lagos",
    "cuisine": "Nigerian",
    "rating": 4.0,
    "delivery_time": "20-30 mins"
  }
}
```

#### POST /api/restaurants/refresh
Force refresh cached restaurant data

```bash
curl -X POST http://localhost:5000/api/restaurants/refresh
```

**Response:**
```json
{
  "success": true,
  "message": "Restaurant data refreshed",
  "count": 10
}
```

## Development

### Code Quality

```bash
# Format code
make format

# Run linter
make lint
```

### Testing

```bash
# Run all tests with coverage
make test

# Run specific test file
pytest tests/test_restaurants.py -v

# Run with coverage report
pytest --cov=src --cov-report=html
```

### Clean Up

```bash
# Remove cache and build files
make clean
```

## Configuration

Environment variables (set in `.env`):

| Variable | Description | Default |
|----------|-------------|---------|
| `FLASK_DEBUG` | Enable debug mode | `False` |
| `PORT` | Server port | `5000` |
| `SECRET_KEY` | Flask secret key | Required |
| `CHOWDECK_URL` | Chowdeck source URL | Help article URL |
| `CACHE_TIMEOUT` | Cache duration in seconds | `3600` |

## Customizing the Scraper

The current implementation in `src/clients/chowdeck.py` includes placeholder logic. To scrape actual restaurant data:

1. Find the correct Chowdeck URL with restaurant listings
2. Update `CHOWDECK_URL` in `.env`
3. Modify `_parse_restaurants()` method to match the HTML structure:

```python
def _parse_restaurants(self, soup: BeautifulSoup) -> List[Dict]:
    restaurants = []

    # Example: Update selectors based on actual HTML
    restaurant_cards = soup.find_all('div', class_='restaurant-card')

    for card in restaurant_cards:
        name = card.find('h3', class_='name').text.strip()
        city = card.find('span', class_='city').text.strip()
        # ... extract other fields

        restaurants.append({
            'id': generate_id(name),
            'name': name,
            'city': city,
            # ... other fields
        })

    return restaurants
```

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message description"
}
```

HTTP status codes:
- `200` - Success
- `404` - Resource not found
- `500` - Server error

## Contributing

1. Follow the guidelines in `AGENTS.md`
2. Use conventional commits (`feat:`, `fix:`, `chore:`)
3. Add tests for new features
4. Ensure `make lint` and `make test` pass
5. Keep PRs focused and well-documented

## License

This project is for educational/personal use.

## Support

For questions or issues, please check:
- Project documentation in `AGENTS.md`
- Test files in `tests/` for usage examples
- Chowdeck website: https://chowdeck.com
