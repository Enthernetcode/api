"""
Enhanced Chowdeck scraper using Selenium for dynamic content
Scrapes restaurants from multiple locations across Nigeria
"""
import os
import re
import time
import hashlib
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class ChowdeckDynamicScraper:
    """Scraper for Chowdeck using Selenium to handle dynamic JavaScript content"""

    # Major locations to scrape across Nigeria
    LOCATIONS = [
        # Lagos locations
        {'name': 'Ikeja', 'state': 'Lagos', 'lga': 'Ikeja'},
        {'name': 'Lekki', 'state': 'Lagos', 'lga': 'Eti-Osa'},
        {'name': 'Victoria Island', 'state': 'Lagos', 'lga': 'Eti-Osa'},
        {'name': 'Yaba', 'state': 'Lagos', 'lga': 'Lagos Mainland'},
        {'name': 'Surulere', 'state': 'Lagos', 'lga': 'Surulere'},
        {'name': 'Ikoyi', 'state': 'Lagos', 'lga': 'Eti-Osa'},
        {'name': 'Gbagada', 'state': 'Lagos', 'lga': 'Kosofe'},
        {'name': 'Ogudu', 'state': 'Lagos', 'lga': 'Kosofe'},

        # Abuja locations
        {'name': 'Wuse', 'state': 'FCT', 'lga': 'Abuja Municipal'},
        {'name': 'Garki', 'state': 'FCT', 'lga': 'Abuja Municipal'},
        {'name': 'Gwarinpa', 'state': 'FCT', 'lga': 'Abuja Municipal'},
        {'name': 'Maitama', 'state': 'FCT', 'lga': 'Abuja Municipal'},

        # Other cities
        {'name': 'Ibadan', 'state': 'Oyo', 'lga': 'Ibadan North'},
        {'name': 'Port Harcourt', 'state': 'Rivers', 'lga': 'Port Harcourt'},
        {'name': 'Benin City', 'state': 'Edo', 'lga': 'Oredo'},
    ]

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.restaurants_cache = []

    def _init_driver(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)

    def _close_driver(self):
        """Close Selenium WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def fetch_restaurants_for_location(self, location: Dict) -> List[Dict]:
        """
        Fetch restaurants for a specific location
        """
        restaurants = []
        location_name = location['name'].lower().replace(' ', '-')
        url = f"https://chowdeck.com/store/{location_name}"

        try:
            if not self.driver:
                self._init_driver()

            self.driver.get(url)

            # Wait for content to load
            time.sleep(5)  # Allow JavaScript to execute

            # Try multiple selectors for restaurant cards
            selectors = [
                "//div[contains(@class, 'restaurant')]",
                "//div[contains(@class, 'vendor')]",
                "//div[contains(@class, 'store')]",
                "//a[contains(@href, '/store/') and contains(@href, '/restaurants/')]",
            ]

            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        for element in elements:
                            restaurant = self._parse_restaurant_element(
                                element,
                                location
                            )
                            if restaurant:
                                restaurants.append(restaurant)
                        break
                except Exception:
                    continue

        except Exception as e:
            print(f"Error fetching restaurants for {location['name']}: {str(e)}")

        return restaurants

    def _parse_restaurant_element(self, element, location: Dict) -> Dict:
        """Parse restaurant data from HTML element"""
        try:
            # Try to extract restaurant name
            name = None
            try:
                name = element.find_element(By.TAG_NAME, 'h2').text
            except:
                try:
                    name = element.find_element(By.TAG_NAME, 'h3').text
                except:
                    try:
                        name = element.text.split('\n')[0]
                    except:
                        return None

            if not name or len(name) < 2:
                return None

            # Generate unique ID
            restaurant_id = self._generate_id(name, location['name'])

            # Build restaurant data
            restaurant = {
                'id': restaurant_id,
                'name': name,
                'city': location['name'],
                'state': location['state'],
                'lga': location['lga'],
                'location': f"{location['name']}, {location['state']}",
                'url': '',
                'rating': None,
                'cuisine': 'Nigerian',
                'delivery_areas': [location['name']],
                'specialties': [],
                'opening_hours': None
            }

            # Try to extract URL
            try:
                restaurant['url'] = element.get_attribute('href')
            except:
                pass

            # Try to extract rating
            try:
                rating_text = element.text
                rating_match = re.search(r'(\d+\.\d+)', rating_text)
                if rating_match:
                    restaurant['rating'] = float(rating_match.group(1))
            except:
                pass

            return restaurant

        except Exception as e:
            return None

    def fetch_all_restaurants(self) -> List[Dict]:
        """
        Fetch restaurants from all configured locations
        """
        all_restaurants = []
        seen_ids = set()

        try:
            self._init_driver()

            for location in self.LOCATIONS:
                print(f"Scraping restaurants in {location['name']}, {location['state']}...")

                restaurants = self.fetch_restaurants_for_location(location)

                # Deduplicate based on ID
                for restaurant in restaurants:
                    if restaurant['id'] not in seen_ids:
                        all_restaurants.append(restaurant)
                        seen_ids.add(restaurant['id'])

                # Small delay between requests
                time.sleep(2)

        except Exception as e:
            print(f"Error in fetch_all_restaurants: {str(e)}")

        finally:
            self._close_driver()

        self.restaurants_cache = all_restaurants
        return all_restaurants

    def _generate_id(self, name: str, location: str) -> str:
        """Generate a unique ID from restaurant name and location"""
        combined = f"{name}_{location}"
        name_hash = hashlib.md5(combined.encode()).hexdigest()[:8]
        slug = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
        return f"{slug}_{name_hash}"
