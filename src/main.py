"""
Main Flask application for Chowdeck Restaurant API
"""
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from flask import Flask, jsonify, render_template
from flask_cors import CORS
from dotenv import load_dotenv

# Import with proper path handling
try:
    from src.restaurants.service import RestaurantService
except ModuleNotFoundError:
    from restaurants.service import RestaurantService

# Load environment variables
load_dotenv()

# Initialize Flask app with custom template and static folders
app = Flask(
    __name__,
    template_folder='../templates',
    static_folder='../static'
)
app.config['JSON_SORT_KEYS'] = False

# Enable CORS
CORS(app)

# Configuration
app.config['CHOWDECK_URL'] = os.getenv(
    'CHOWDECK_URL',
    'https://help.chowdeck.com/en/articles/5769156-what-is-chowdeck'
)
app.config['CACHE_TIMEOUT'] = int(os.getenv('CACHE_TIMEOUT', 3600))
app.config['DEBUG'] = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'

# Initialize restaurant service
restaurant_service = RestaurantService()


@app.route('/')
def index():
    """Homepage with restaurant listings"""
    restaurants = restaurant_service.get_all_restaurants()

    # Calculate statistics
    cities = list(set(r.get('city') for r in restaurants if r.get('city')))
    ratings = [r.get('rating') for r in restaurants if r.get('rating')]
    avg_rating = round(sum(ratings) / len(ratings), 2) if ratings else 0

    return render_template(
        'index.html',
        restaurants=restaurants,
        cities=cities,
        avg_rating=avg_rating
    )


@app.route('/restaurant/<restaurant_id>')
def restaurant_detail(restaurant_id):
    """Restaurant detail page"""
    restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)

    if not restaurant:
        return render_template('404.html'), 404

    return render_template('restaurant.html', restaurant=restaurant)


@app.route('/health')
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'service': 'chowdeck-api'
    })


# Import and register blueprints
try:
    from src.restaurants.handlers import restaurants_bp
except ModuleNotFoundError:
    from restaurants.handlers import restaurants_bp
app.register_blueprint(restaurants_bp, url_prefix='/api')


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )
