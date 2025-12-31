"""
Chowdeck web scraper client
"""
import os
import re
import hashlib
import requests
from bs4 import BeautifulSoup
from typing import List, Dict


class ChowdeckClient:
    """Client for fetching restaurant data from Chowdeck"""

    # Lagos LGA mapping
    LAGOS_LGA_MAP = {
        'ikeja': 'Ikeja',
        'lekki': 'Eti-Osa',
        'victoria island': 'Eti-Osa',
        'vi': 'Eti-Osa',
        'ikoyi': 'Eti-Osa',
        'yaba': 'Lagos Mainland',
        'surulere': 'Surulere',
        'gbagada': 'Kosofe',
        'ogudu': 'Kosofe',
        'oshodi': 'Oshodi-Isolo',
        'mushin': 'Mushin',
        'shomolu': 'Shomolu',
        'maryland': 'Kosofe',
        'ojota': 'Kosofe',
        'festac': 'Amuwo-Odofin',
        'ajah': 'Eti-Osa',
        'badagry': 'Badagry',
        'epe': 'Epe',
    }

    # Abuja areas (all in FCT)
    ABUJA_AREAS = [
        'wuse', 'garki', 'gwarinpa', 'maitama', 'asokoro', 'jabi',
        'utako', 'kubwa', 'nyanya', 'karu', 'lugbe', 'gwagwalada'
    ]

    def __init__(self):
        self.base_url = os.getenv(
            'CHOWDECK_URL',
            'https://chowdeck.com/blog/get-it-here-jollof-rice-on-chowdeck'
        )
        self.timeout = 30
        self.use_dynamic_scraper = os.getenv('USE_DYNAMIC_SCRAPER', 'False').lower() == 'true'

    def fetch_restaurants(self) -> List[Dict]:
        """
        Fetch restaurant data from Chowdeck website
        Returns list of restaurant dictionaries
        """
        # Use dynamic scraper if enabled
        if self.use_dynamic_scraper:
            try:
                from src.clients.chowdeck_dynamic import ChowdeckDynamicScraper
                scraper = ChowdeckDynamicScraper(headless=True)
                return scraper.fetch_all_restaurants()
            except Exception as e:
                print(f"Dynamic scraper failed: {str(e)}, falling back to static scraper")

        # Use static blog scraper
        try:
            response = requests.get(self.base_url, timeout=self.timeout)
            response.raise_for_status()

            # Parse HTML content
            soup = BeautifulSoup(response.content, 'html.parser')

            # Extract restaurant data
            restaurants = self._parse_restaurants(soup)

            return restaurants

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch data from Chowdeck: {str(e)}")

    def _parse_restaurants(self, soup: BeautifulSoup) -> List[Dict]:
        """
        Parse restaurant data from Chowdeck blog post HTML
        Extracts restaurant name, location, rating, and delivery areas
        """
        restaurants = []

        # Find all h2 headings containing restaurant names
        restaurant_headings = soup.find_all('h2')

        for heading in restaurant_headings:
            try:
                # Extract restaurant name from h2 > a
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
                    'cuisine': 'Nigerian',  # Default based on jollof rice context
                    'specialties': ['Jollof Rice']
                }

                # Get the next siblings to extract details
                current = heading.find_next_sibling()

                while current and current.name != 'h2' and current.name != 'hr':
                    if current.name == 'p':
                        text = current.get_text(strip=True)

                        # Extract rating
                        rating_match = re.search(r'(\d+\.\d+)\s*out of\s*5', text)
                        if rating_match:
                            restaurant_data['rating'] = float(rating_match.group(1))

                        # Extract location (Where:)
                        if 'Where:' in text or text.startswith('Where'):
                            location_text = text.replace('Where:', '').strip()
                            restaurant_data['location'] = location_text

                            # Extract city, state, and LGA from location
                            location_lower = location_text.lower()

                            # Check for Lagos areas
                            if any(area in location_lower for area in ['lagos', 'ikeja', 'lekki', 'yaba', 'surulere', 'ikoyi', 'victoria island']):
                                restaurant_data['city'] = 'Lagos'
                                restaurant_data['state'] = 'Lagos'

                                # Extract LGA for Lagos
                                for area, lga in self.LAGOS_LGA_MAP.items():
                                    if area in location_lower:
                                        restaurant_data['lga'] = lga
                                        break

                            # Check for Abuja/FCT areas
                            elif any(area in location_lower for area in self.ABUJA_AREAS):
                                restaurant_data['city'] = 'Abuja'
                                restaurant_data['state'] = 'FCT'
                                restaurant_data['lga'] = 'Abuja Municipal'

                            # Check for other cities
                            elif 'ibadan' in location_lower:
                                restaurant_data['city'] = 'Ibadan'
                                restaurant_data['state'] = 'Oyo'
                                restaurant_data['lga'] = 'Ibadan North'

                            elif 'port harcourt' in location_lower:
                                restaurant_data['city'] = 'Port Harcourt'
                                restaurant_data['state'] = 'Rivers'
                                restaurant_data['lga'] = 'Port Harcourt'

                            elif 'benin' in location_lower:
                                restaurant_data['city'] = 'Benin City'
                                restaurant_data['state'] = 'Edo'
                                restaurant_data['lga'] = 'Oredo'

                        # Extract delivery areas (Delivering To:)
                        if 'Delivering To:' in text or 'Delivering to:' in text:
                            delivery_text = re.sub(
                                r'Delivering [Tt]o:\s*',
                                '',
                                text
                            ).strip()
                            # Split by comma and clean up
                            areas = [
                                area.strip()
                                for area in delivery_text.split(',')
                                if area.strip()
                            ]
                            restaurant_data['delivery_areas'] = areas

                        # Extract opening hours
                        if 'Opening Hours:' in text or 'Hours:' in text:
                            hours_text = re.sub(
                                r'Opening Hours:\s*|Hours:\s*',
                                '',
                                text
                            ).strip()
                            restaurant_data['opening_hours'] = hours_text

                    current = current.find_next_sibling()

                # Only add if we have minimum required data
                if restaurant_data['name'] and restaurant_data['location']:
                    restaurants.append(restaurant_data)

            except Exception as e:
                # Skip problematic entries but continue processing
                continue

        return restaurants

    def _generate_id(self, name: str) -> str:
        """Generate a unique ID from restaurant name"""
        # Create a hash of the name for consistent IDs
        name_hash = hashlib.md5(name.encode()).hexdigest()[:8]
        # Create a slug-like ID
        slug = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
        return f"{slug}_{name_hash}"

    def fetch_restaurant_details(self, restaurant_url: str) -> Dict:
        """
        Fetch detailed information for a specific restaurant
        """
        try:
            response = requests.get(restaurant_url, timeout=self.timeout)
            response.raise_for_status()

            soup = BeautifulSoup(response.content, 'html.parser')

            # Parse restaurant details
            # This would be customized based on the actual page structure
            details = {
                'url': restaurant_url,
                'menu': [],
                'contact': {},
                'hours': {}
            }

            return details

        except requests.RequestException as e:
            raise Exception(f"Failed to fetch restaurant details: {str(e)}")
