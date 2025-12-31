"""
Deep Selenium-based scraper for Chowdeck
Browses actual store pages and extracts all restaurant cards
"""
import time
import re
import hashlib
from typing import List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class DeepChowdeckScraper:
    """Deep scraper that browses Chowdeck store pages for comprehensive restaurant data"""

    # Lagos areas to scrape
    LAGOS_AREAS = [
        # Ikeja LGA
        {'name': 'Ikeja', 'lga': 'Ikeja', 'state': 'Lagos'},
        {'name': 'Allen-Avenue', 'lga': 'Ikeja', 'state': 'Lagos'},
        {'name': 'Ogba', 'lga': 'Ikeja', 'state': 'Lagos'},
        {'name': 'Alausa', 'lga': 'Ikeja', 'state': 'Lagos'},

        # Eti-Osa LGA
        {'name': 'Lekki', 'lga': 'Eti-Osa', 'state': 'Lagos'},
        {'name': 'Victoria-Island', 'lga': 'Eti-Osa', 'state': 'Lagos'},
        {'name': 'Ikoyi', 'lga': 'Eti-Osa', 'state': 'Lagos'},
        {'name': 'Ajah', 'lga': 'Eti-Osa', 'state': 'Lagos'},
        {'name': 'Lekki-Phase-1', 'lga': 'Eti-Osa', 'state': 'Lagos'},

        # Lagos Mainland LGA
        {'name': 'Yaba', 'lga': 'Lagos Mainland', 'state': 'Lagos'},
        {'name': 'Ebute-Metta', 'lga': 'Lagos Mainland', 'state': 'Lagos'},

        # Surulere LGA
        {'name': 'Surulere', 'lga': 'Surulere', 'state': 'Lagos'},

        # Kosofe LGA
        {'name': 'Gbagada', 'lga': 'Kosofe', 'state': 'Lagos'},
        {'name': 'Ogudu', 'lga': 'Kosofe', 'state': 'Lagos'},
        {'name': 'Maryland', 'lga': 'Kosofe', 'state': 'Lagos'},
        {'name': 'Ketu', 'lga': 'Kosofe', 'state': 'Lagos'},

        # Oshodi-Isolo LGA
        {'name': 'Oshodi', 'lga': 'Oshodi-Isolo', 'state': 'Lagos'},
        {'name': 'Isolo', 'lga': 'Oshodi-Isolo', 'state': 'Lagos'},

        # Amuwo-Odofin LGA
        {'name': 'Festac', 'lga': 'Amuwo-Odofin', 'state': 'Lagos'},

        # Alimosho LGA
        {'name': 'Egbeda', 'lga': 'Alimosho', 'state': 'Lagos'},
        {'name': 'Ikotun', 'lga': 'Alimosho', 'state': 'Lagos'},
    ]

    # Abuja areas
    ABUJA_AREAS = [
        {'name': 'Wuse', 'lga': 'Abuja Municipal', 'state': 'FCT'},
        {'name': 'Garki', 'lga': 'Abuja Municipal', 'state': 'FCT'},
        {'name': 'Gwarinpa', 'lga': 'Abuja Municipal', 'state': 'FCT'},
        {'name': 'Maitama', 'lga': 'Abuja Municipal', 'state': 'FCT'},
        {'name': 'Jabi', 'lga': 'Abuja Municipal', 'state': 'FCT'},
        {'name': 'Utako', 'lga': 'Abuja Municipal', 'state': 'FCT'},
    ]

    def __init__(self, headless=True):
        self.headless = headless
        self.driver = None
        self.restaurants_db = {}  # Store unique restaurants by ID

    def _init_driver(self):
        """Initialize Selenium WebDriver"""
        chrome_options = Options()

        if self.headless:
            chrome_options.add_argument('--headless=new')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--disable-gpu')
        chrome_options.add_argument('--window-size=1920,1080')
        chrome_options.add_argument('--disable-blink-features=AutomationControlled')
        chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.implicitly_wait(10)

    def _close_driver(self):
        """Close WebDriver"""
        if self.driver:
            self.driver.quit()
            self.driver = None

    def scrape_all_restaurants(self, areas=None, max_areas=None) -> List[Dict]:
        """
        Scrape restaurants from multiple areas

        Args:
            areas: List of area configs to scrape (default: all Lagos + Abuja)
            max_areas: Maximum number of areas to scrape (for testing)
        """
        if areas is None:
            areas = self.LAGOS_AREAS + self.ABUJA_AREAS

        if max_areas:
            areas = areas[:max_areas]

        try:
            self._init_driver()

            for idx, area_config in enumerate(areas):
                print(f"\n[{idx+1}/{len(areas)}] Scraping {area_config['name']}, {area_config['state']}...")

                try:
                    restaurants = self._scrape_area(area_config)
                    print(f"  Found {len(restaurants)} restaurants")

                    # Add to database (deduplicating by ID)
                    for restaurant in restaurants:
                        if restaurant['id'] not in self.restaurants_db:
                            self.restaurants_db[restaurant['id']] = restaurant

                    # Small delay between areas
                    time.sleep(2)

                except Exception as e:
                    print(f"  Error scraping {area_config['name']}: {str(e)}")
                    continue

        finally:
            self._close_driver()

        print(f"\n{'='*60}")
        print(f"TOTAL UNIQUE RESTAURANTS: {len(self.restaurants_db)}")
        print(f"{'='*60}")

        return list(self.restaurants_db.values())

    def _scrape_area(self, area_config: Dict) -> List[Dict]:
        """Scrape restaurants from a specific area"""
        restaurants = []
        area_slug = area_config['name'].lower()
        url = f"https://chowdeck.com/store/{area_slug}"

        try:
            self.driver.get(url)

            # Wait for page to load
            time.sleep(3)

            # Try to find restaurant containers with various selectors
            selectors = [
                "//div[contains(@class, 'vendor')]",
                "//div[contains(@class, 'restaurant')]",
                "//div[contains(@class, 'store')]",
                "//a[contains(@href, '/restaurants/')]",
                "//div[contains(@class, 'card')]",
                "//*[contains(@class, 'item')]",
            ]

            elements_found = []
            for selector in selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements and len(elements) > 3:  # Likely found restaurant cards
                        elements_found = elements
                        print(f"    Using selector: {selector[:50]}... ({len(elements)} elements)")
                        break
                except:
                    continue

            # If no elements found, try scrolling to load more
            if not elements_found:
                self._scroll_page()
                time.sleep(2)

                # Try again after scrolling
                for selector in selectors:
                    try:
                        elements = self.driver.find_elements(By.XPATH, selector)
                        if elements and len(elements) > 3:
                            elements_found = elements
                            break
                    except:
                        continue

            # Parse restaurant cards
            for element in elements_found:
                restaurant = self._parse_restaurant_card(element, area_config)
                if restaurant:
                    restaurants.append(restaurant)

        except Exception as e:
            print(f"    Error loading page: {str(e)}")

        return restaurants

    def _scroll_page(self):
        """Scroll page to load lazy-loaded content"""
        try:
            # Scroll to bottom
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            # Scroll back up
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")
            time.sleep(0.5)
        except:
            pass

    def _parse_restaurant_card(self, element, area_config: Dict) -> Dict:
        """Parse restaurant data from a card element"""
        try:
            # Try to extract name
            name = None
            for tag in ['h1', 'h2', 'h3', 'h4', 'h5']:
                try:
                    name_elem = element.find_element(By.TAG_NAME, tag)
                    name = name_elem.text.strip()
                    if name and len(name) > 2:
                        break
                except:
                    continue

            if not name:
                # Try getting text from element
                text = element.text.strip()
                if text:
                    lines = text.split('\n')
                    if lines:
                        name = lines[0].strip()

            if not name or len(name) < 2:
                return None

            # Skip if it's a generic element
            if name.lower() in ['restaurants', 'stores', 'vendors', 'categories', 'filter']:
                return None

            # Generate ID
            restaurant_id = self._generate_id(name, area_config['name'])

            # Build restaurant data
            restaurant = {
                'id': restaurant_id,
                'name': name,
                'city': area_config['name'].replace('-', ' ').title(),
                'state': area_config['state'],
                'lga': area_config['lga'],
                'location': f"{area_config['name'].replace('-', ' ').title()}, {area_config['state']}",
                'url': '',
                'rating': None,
                'cuisine': 'Nigerian',
                'delivery_areas': [area_config['name'].replace('-', ' ').title()],
                'specialties': [],
                'opening_hours': None,
            }

            # Try to extract URL
            try:
                link = element.find_element(By.TAG_NAME, 'a')
                href = link.get_attribute('href')
                if href:
                    restaurant['url'] = href
            except:
                pass

            # Try to extract rating
            try:
                text = element.text
                rating_match = re.search(r'(\d+\.?\d*)\s*(?:★|stars?|rating)', text, re.IGNORECASE)
                if rating_match:
                    restaurant['rating'] = float(rating_match.group(1))
            except:
                pass

            return restaurant

        except Exception as e:
            return None

    def _generate_id(self, name: str, area: str) -> str:
        """Generate unique restaurant ID"""
        combined = f"{name}_{area}"
        name_hash = hashlib.md5(combined.encode()).hexdigest()[:8]
        slug = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
        return f"{slug}_{name_hash}"
