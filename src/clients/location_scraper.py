"""
Location-based restaurant scraper for Chowdeck
Fetches restaurants on-demand based on state and LGA selection
"""
import re
import hashlib
import requests
from bs4 import BeautifulSoup
from typing import List, Dict
from src.data.locations import get_areas_for_lga, get_chowdeck_url_for_area
from src.data.seed_restaurants import get_all_seed_restaurants
from src.data.mega_lagos_restaurants import get_mega_lagos_restaurants


class LocationBasedScraper:
    """Scrapes restaurants from Chowdeck blog posts for specific locations"""

    # Known blog posts mapping food types to URLs
    BLOG_POSTS = {
        'jollof_rice': 'https://chowdeck.com/blog/get-it-here-jollof-rice-on-chowdeck',
        'pizza': 'https://chowdeck.com/blog/get-it-here-pizza-on-chowdeck',
        'chinese': 'https://chowdeck.com/blog/get-it-here-chinese-food-on-chowdeck',
        'shawarma': 'https://chowdeck.com/blog/get-it-here-shawarma-on-chowdeck',
        'suya': 'https://chowdeck.com/blog/get-it-here-suya-on-chowdeck',
    }

    def __init__(self):
        self.timeout = 30

    def fetch_for_location(self, state: str, lga: str = None) -> List[Dict]:
        """
        Fetch restaurants for a specific state and optionally LGA
        Returns list of restaurant dictionaries
        """
        all_restaurants = []
        seen_ids = set()

        # 1. Load mega Lagos database if state is Lagos (24,000+ restaurants)
        if state == 'Lagos':
            try:
                lagos_restaurants = get_mega_lagos_restaurants()

                # Filter by LGA if specified
                for restaurant in lagos_restaurants:
                    if not lga or restaurant.get('lga') == lga:
                        all_restaurants.append(restaurant)
                        seen_ids.add(restaurant['id'])

                print(f"Loaded {len(all_restaurants)} Lagos restaurants" + (f" for {lga}" if lga else ""))
            except Exception as e:
                print(f"Error loading Lagos restaurants: {str(e)}")
        else:
            # For other states, use general seed database
            try:
                seed_restaurants = get_all_seed_restaurants()

                # Filter by location
                for restaurant in seed_restaurants:
                    if self._matches_location(restaurant, state, lga):
                        all_restaurants.append(restaurant)
                        seen_ids.add(restaurant['id'])

                print(f"Loaded {len(all_restaurants)} seed restaurants for {state}" + (f", {lga}" if lga else ""))
            except Exception as e:
                print(f"Error loading seed restaurants: {str(e)}")

        # 2. Fetch from all blog posts (additional dynamic data)
        for food_type, url in self.BLOG_POSTS.items():
            try:
                restaurants = self._scrape_blog_post(url, state, lga)

                # Deduplicate
                for restaurant in restaurants:
                    if restaurant['id'] not in seen_ids:
                        all_restaurants.append(restaurant)
                        seen_ids.add(restaurant['id'])

            except Exception as e:
                print(f"Error scraping {food_type}: {str(e)}")
                continue

        return all_restaurants

    def _scrape_blog_post(self, url: str, state: str, lga: str = None) -> List[Dict]:
        """Scrape a single blog post and filter by location"""
        restaurants = []

        try:
            response = requests.get(url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')
            restaurant_headings = soup.find_all('h2')

            for heading in restaurant_headings:
                try:
                    link = heading.find('a')
                    if not link:
                        continue

                    name = link.get_text(strip=True)
                    if not name or name.lower() in ['chowdeck', 'get it here']:
                        continue

                    # Initialize restaurant data
                    restaurant_data = {
                        'id': self._generate_id(name),
                        'name': name,
                        'url': link.get('href', ''),
                        'city': None,
                        'state': None,
                        'lga': None,
                        'location': None,
                        'rating': None,
                        'delivery_areas': [],
                        'opening_hours': None,
                        'cuisine': 'Nigerian',
                        'specialties': []
                    }

                    # Parse details
                    current = heading.find_next_sibling()

                    while current and current.name != 'h2' and current.name != 'hr':
                        if current.name == 'p':
                            text = current.get_text(strip=True)

                            # Extract rating
                            rating_match = re.search(r'(\d+\.\d+)\s*out of\s*5', text)
                            if rating_match:
                                restaurant_data['rating'] = float(rating_match.group(1))

                            # Extract location
                            if 'Where:' in text or text.startswith('Where'):
                                location_text = text.replace('Where:', '').strip()
                                restaurant_data['location'] = location_text

                                # Parse location data
                                self._parse_location(restaurant_data, location_text)

                            # Extract delivery areas
                            if 'Delivering To:' in text or 'Delivering to:' in text:
                                delivery_text = re.sub(r'Delivering [Tt]o:\s*', '', text).strip()
                                areas = [area.strip() for area in delivery_text.split(',') if area.strip()]
                                restaurant_data['delivery_areas'] = areas

                            # Extract opening hours
                            if 'Opening Hours:' in text or 'Hours:' in text:
                                hours_text = re.sub(r'Opening Hours:\s*|Hours:\s*', '', text).strip()
                                restaurant_data['opening_hours'] = hours_text

                        current = current.find_next_sibling()

                    # Filter by state and LGA
                    if self._matches_location(restaurant_data, state, lga):
                        restaurants.append(restaurant_data)

                except Exception:
                    continue

        except Exception as e:
            raise Exception(f"Failed to fetch from {url}: {str(e)}")

        return restaurants

    def _parse_location(self, restaurant_data: Dict, location_text: str):
        """Parse location text and extract city, state, LGA"""
        location_lower = location_text.lower()

        # Lagos areas
        if any(area in location_lower for area in ['lagos', 'ikeja', 'lekki', 'yaba', 'surulere', 'ikoyi', 'victoria island']):
            restaurant_data['state'] = 'Lagos'
            restaurant_data['city'] = 'Lagos'

            # Map to LGA
            lga_mapping = {
                'ikeja': 'Ikeja', 'allen': 'Ikeja', 'ogba': 'Ikeja', 'alausa': 'Ikeja',
                'lekki': 'Eti-Osa', 'victoria island': 'Eti-Osa', 'vi': 'Eti-Osa',
                'ikoyi': 'Eti-Osa', 'ajah': 'Eti-Osa',
                'yaba': 'Lagos Mainland', 'ebute metta': 'Lagos Mainland',
                'surulere': 'Surulere',
                'gbagada': 'Kosofe', 'ogudu': 'Kosofe', 'maryland': 'Kosofe',
                'oshodi': 'Oshodi-Isolo', 'isolo': 'Oshodi-Isolo',
                'festac': 'Amuwo-Odofin',
            }

            for area, lga in lga_mapping.items():
                if area in location_lower:
                    restaurant_data['lga'] = lga
                    break

        # Abuja/FCT areas
        elif any(area in location_lower for area in ['abuja', 'garki', 'wuse', 'gwarinpa', 'maitama', 'asokoro', 'jabi', 'utako']):
            restaurant_data['state'] = 'FCT'
            restaurant_data['city'] = 'Abuja'
            restaurant_data['lga'] = 'Abuja Municipal'

        # Other cities
        elif 'ibadan' in location_lower:
            restaurant_data['state'] = 'Oyo'
            restaurant_data['city'] = 'Ibadan'
            restaurant_data['lga'] = 'Ibadan North'

        elif 'port harcourt' in location_lower:
            restaurant_data['state'] = 'Rivers'
            restaurant_data['city'] = 'Port Harcourt'
            restaurant_data['lga'] = 'Port Harcourt'

        elif 'benin' in location_lower:
            restaurant_data['state'] = 'Edo'
            restaurant_data['city'] = 'Benin City'
            restaurant_data['lga'] = 'Oredo'

    def _matches_location(self, restaurant_data: Dict, state: str, lga: str = None) -> bool:
        """Check if restaurant matches the requested location"""
        # Must match state
        if restaurant_data.get('state') != state:
            return False

        # If LGA specified, must match
        if lga and restaurant_data.get('lga') != lga:
            return False

        return True

    def _generate_id(self, name: str) -> str:
        """Generate a unique ID from restaurant name"""
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        slug = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
        return f"{slug}_{name_hash}"
