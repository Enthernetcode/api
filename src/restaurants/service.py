"""
Restaurant service layer
"""
from datetime import datetime, timedelta
from src.clients.chowdeck import ChowdeckClient
from src.data.seed_restaurants import get_all_seed_restaurants
from src.data.mega_lagos_restaurants import get_mega_lagos_restaurants


class RestaurantService:
    """Service for managing restaurant data"""

    def __init__(self):
        self.client = ChowdeckClient()
        self._cache = None
        self._cache_time = None
        self._cache_timeout = 3600  # 1 hour in seconds

    def get_all_restaurants(self):
        """
        Get all restaurants with caching
        Returns cached data if available and not expired
        Combines seed database with blog-scraped data
        """
        if self._is_cache_valid():
            return self._cache

        # Fetch fresh data - combine Lagos DB + seed database + blog scraping
        all_restaurants = []
        seen_ids = set()

        # 1. Load Lagos restaurants (24,000+ mega Lagos database)
        try:
            lagos_restaurants = get_mega_lagos_restaurants()
            for restaurant in lagos_restaurants:
                all_restaurants.append(restaurant)
                seen_ids.add(restaurant['id'])
        except Exception as e:
            print(f"Error loading Lagos restaurants: {str(e)}")

        # 2. Load other seed restaurants (Abuja, etc.)
        try:
            seed_restaurants = get_all_seed_restaurants()
            for restaurant in seed_restaurants:
                # Only add if not Lagos (since we already added Lagos above)
                if restaurant['id'] not in seen_ids and restaurant.get('state') != 'Lagos':
                    all_restaurants.append(restaurant)
                    seen_ids.add(restaurant['id'])
        except Exception as e:
            print(f"Error loading seed restaurants: {str(e)}")

        # 3. Fetch from blog posts (additional data)
        try:
            blog_restaurants = self.client.fetch_restaurants()
            for restaurant in blog_restaurants:
                if restaurant['id'] not in seen_ids:
                    all_restaurants.append(restaurant)
                    seen_ids.add(restaurant['id'])
        except Exception as e:
            print(f"Error fetching blog restaurants: {str(e)}")

        self._update_cache(all_restaurants)
        return all_restaurants

    def get_restaurant_by_id(self, restaurant_id):
        """Get a specific restaurant by ID"""
        restaurants = self.get_all_restaurants()

        for restaurant in restaurants:
            if str(restaurant.get('id')) == str(restaurant_id):
                return restaurant

        return None

    def clear_cache(self):
        """Clear the cached restaurant data"""
        self._cache = None
        self._cache_time = None

    def _is_cache_valid(self):
        """Check if cache is still valid"""
        if self._cache is None or self._cache_time is None:
            return False

        age = datetime.now() - self._cache_time
        return age.total_seconds() < self._cache_timeout

    def _update_cache(self, data):
        """Update cache with fresh data"""
        self._cache = data
        self._cache_time = datetime.now()
