"""
Restaurant API handlers
"""
from flask import Blueprint, jsonify, request, send_file
from src.restaurants.service import RestaurantService
from src.data.locations import get_all_states, get_lgas_for_state
from src.clients.location_scraper import LocationBasedScraper
from src.utils.excel_export import create_restaurants_excel
from datetime import datetime

restaurants_bp = Blueprint('restaurants', __name__)
restaurant_service = RestaurantService()
location_scraper = LocationBasedScraper()


@restaurants_bp.route('/restaurants', methods=['GET'])
def get_restaurants():
    """
    Get all restaurants
    Query params:
        - city: Filter by city (optional)
        - limit: Limit results (optional)
    """
    try:
        city = request.args.get('city')
        limit = request.args.get('limit', type=int)

        restaurants = restaurant_service.get_all_restaurants()

        # Filter by city if provided
        if city:
            restaurants = [
                r for r in restaurants
                if r.get('city') and r.get('city').lower() == city.lower()
            ]

        # Limit results if provided
        if limit:
            restaurants = restaurants[:limit]

        return jsonify({
            'success': True,
            'count': len(restaurants),
            'data': restaurants
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@restaurants_bp.route('/restaurants/<restaurant_id>', methods=['GET'])
def get_restaurant(restaurant_id):
    """Get a specific restaurant by ID"""
    try:
        restaurant = restaurant_service.get_restaurant_by_id(restaurant_id)

        if not restaurant:
            return jsonify({
                'success': False,
                'error': 'Restaurant not found'
            }), 404

        return jsonify({
            'success': True,
            'data': restaurant
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@restaurants_bp.route('/restaurants/refresh', methods=['POST'])
def refresh_restaurants():
    """Force refresh restaurant data from Chowdeck"""
    try:
        restaurant_service.clear_cache()
        restaurants = restaurant_service.get_all_restaurants()

        return jsonify({
            'success': True,
            'message': 'Restaurant data refreshed',
            'count': len(restaurants)
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@restaurants_bp.route('/locations/states', methods=['GET'])
def get_states():
    """Get all available states"""
    try:
        states = get_all_states()

        return jsonify({
            'success': True,
            'count': len(states),
            'data': states
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@restaurants_bp.route('/locations/lgas/<state>', methods=['GET'])
def get_lgas(state):
    """Get all LGAs for a specific state"""
    try:
        lgas = get_lgas_for_state(state)

        if not lgas:
            return jsonify({
                'success': False,
                'error': 'State not found or no LGAs available'
            }), 404

        return jsonify({
            'success': True,
            'state': state,
            'count': len(lgas),
            'data': lgas
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@restaurants_bp.route('/restaurants/location', methods=['GET'])
def get_restaurants_by_location():
    """
    Get restaurants for a specific state and LGA
    Query params:
        - state: State name (required)
        - lga: LGA name (optional)
        - page: Page number (default: 1)
        - per_page: Results per page (default: 15)
    """
    try:
        state = request.args.get('state')
        lga = request.args.get('lga')
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 15, type=int)

        if not state:
            return jsonify({
                'success': False,
                'error': 'State parameter is required'
            }), 400

        # Fetch restaurants for the location
        restaurants = location_scraper.fetch_for_location(state, lga)

        # Calculate pagination
        total = len(restaurants)
        start = (page - 1) * per_page
        end = start + per_page

        paginated = restaurants[start:end]

        return jsonify({
            'success': True,
            'state': state,
            'lga': lga,
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page,
            'count': len(paginated),
            'data': paginated
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@restaurants_bp.route('/restaurants/download/excel', methods=['GET'])
def download_restaurants_excel():
    """
    Download all restaurants as Excel file
    Query params:
        - state: Filter by state (optional, default: Lagos)
        - lga: Filter by LGA (optional)
    """
    try:
        state = request.args.get('state', 'Lagos')
        lga = request.args.get('lga')

        # Get restaurants
        if lga:
            restaurants = location_scraper.fetch_for_location(state, lga)
            filename = f"{state}_{lga}_Restaurants_{datetime.now().strftime('%Y%m%d')}.xlsx"
        else:
            restaurants = location_scraper.fetch_for_location(state)
            filename = f"{state}_Restaurants_{datetime.now().strftime('%Y%m%d')}.xlsx"

        # Generate Excel file
        excel_file = create_restaurants_excel(restaurants, state)

        return send_file(
            excel_file,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name=filename
        )

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
