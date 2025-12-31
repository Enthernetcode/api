"""
Comprehensive Lagos restaurant scraper
Scrapes all Lagos areas systematically using requests + BeautifulSoup
"""
import requests
import json
import time
import re
from bs4 import BeautifulSoup
from typing import List, Dict

# All Lagos areas to scrape
LAGOS_AREAS = [
    # Ikeja LGA
    {'slug': 'ikeja', 'lga': 'Ikeja', 'city': 'Ikeja'},
    {'slug': 'allen-avenue', 'lga': 'Ikeja', 'city': 'Allen Avenue'},
    {'slug': 'ogba', 'lga': 'Ikeja', 'city': 'Ogba'},
    {'slug': 'alausa', 'lga': 'Ikeja', 'city': 'Alausa'},
    {'slug': 'computer-village', 'lga': 'Ikeja', 'city': 'Computer Village'},
    {'slug': 'ikeja-gra', 'lga': 'Ikeja', 'city': 'Ikeja GRA'},

    # Eti-Osa LGA
    {'slug': 'lekki', 'lga': 'Eti-Osa', 'city': 'Lekki'},
    {'slug': 'victoria-island', 'lga': 'Eti-Osa', 'city': 'Victoria Island'},
    {'slug': 'ikoyi', 'lga': 'Eti-Osa', 'city': 'Ikoyi'},
    {'slug': 'ajah', 'lga': 'Eti-Osa', 'city': 'Ajah'},
    {'slug': 'lekki-phase-1', 'lga': 'Eti-Osa', 'city': 'Lekki Phase 1'},
    {'slug': 'lekki-phase-2', 'lga': 'Eti-Osa', 'city': 'Lekki Phase 2'},
    {'slug': 'agungi', 'lga': 'Eti-Osa', 'city': 'Agungi'},
    {'slug': 'oniru', 'lga': 'Eti-Osa', 'city': 'Oniru'},

    # Lagos Mainland LGA
    {'slug': 'yaba', 'lga': 'Lagos Mainland', 'city': 'Yaba'},
    {'slug': 'ebute-metta', 'lga': 'Lagos Mainland', 'city': 'Ebute Metta'},
    {'slug': 'sabo', 'lga': 'Lagos Mainland', 'city': 'Sabo'},

    # Surulere LGA
    {'slug': 'surulere', 'lga': 'Surulere', 'city': 'Surulere'},
    {'slug': 'adeniran-ogunsanya', 'lga': 'Surulere', 'city': 'Adeniran Ogunsanya'},

    # Kosofe LGA
    {'slug': 'gbagada', 'lga': 'Kosofe', 'city': 'Gbagada'},
    {'slug': 'ogudu', 'lga': 'Kosofe', 'city': 'Ogudu'},
    {'slug': 'maryland', 'lga': 'Kosofe', 'city': 'Maryland'},
    {'slug': 'ketu', 'lga': 'Kosofe', 'city': 'Ketu'},

    # Oshodi-Isolo LGA
    {'slug': 'oshodi', 'lga': 'Oshodi-Isolo', 'city': 'Oshodi'},
    {'slug': 'isolo', 'lga': 'Oshodi-Isolo', 'city': 'Isolo'},
    {'slug': 'mafoluku', 'lga': 'Oshodi-Isolo', 'city': 'Mafoluku'},

    # Amuwo-Odofin LGA
    {'slug': 'festac', 'lga': 'Amuwo-Odofin', 'city': 'Festac'},
    {'slug': 'amuwo-odofin', 'lga': 'Amuwo-Odofin', 'city': 'Amuwo Odofin'},

    # Alimosho LGA
    {'slug': 'egbeda', 'lga': 'Alimosho', 'city': 'Egbeda'},
    {'slug': 'ikotun', 'lga': 'Alimosho', 'city': 'Ikotun'},
    {'slug': 'idimu', 'lga': 'Alimosho', 'city': 'Idimu'},
    {'slug': 'ipaja', 'lga': 'Alimosho', 'city': 'Ipaja'},

    # Apapa LGA
    {'slug': 'apapa', 'lga': 'Apapa', 'city': 'Apapa'},

    # Somolu LGA
    {'slug': 'somolu', 'lga': 'Somolu', 'city': 'Somolu'},
    {'slug': 'palmgrove', 'lga': 'Somolu', 'city': 'Palmgrove'},
]


class ComprehensiveLagosScraper:
    """Scrape restaurants from all Lagos areas"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive',
        })
        self.restaurants = {}  # Deduplicate by name+area

    def scrape_all_areas(self, max_areas=None) -> List[Dict]:
        """Scrape all Lagos areas"""
        areas_to_scrape = LAGOS_AREAS[:max_areas] if max_areas else LAGOS_AREAS

        print(f"Scraping {len(areas_to_scrape)} Lagos areas...")
        print("=" * 60)

        for idx, area in enumerate(areas_to_scrape, 1):
            print(f"\n[{idx}/{len(areas_to_scrape)}] {area['city']} ({area['lga']})")

            try:
                restaurants = self.scrape_area(area)

                # Add to database
                for restaurant in restaurants:
                    key = f"{restaurant['name']}_{area['lga']}"
                    if key not in self.restaurants:
                        self.restaurants[key] = restaurant

                print(f"  Found {len(restaurants)} restaurants (Total unique: {len(self.restaurants)})")

                # Polite delay
                time.sleep(1)

            except Exception as e:
                print(f"  Error: {str(e)}")
                continue

        print(f"\n{'=' * 60}")
        print(f"TOTAL: {len(self.restaurants)} unique restaurants")
        print(f"{'=' * 60}")

        return list(self.restaurants.values())

    def scrape_area(self, area: Dict) -> List[Dict]:
        """Scrape restaurants from a specific area"""
        restaurants = []

        # Try to fetch the area page
        url = f"https://chowdeck.com/store/{area['slug']}"

        try:
            response = self.session.get(url, timeout=15)

            if response.status_code != 200:
                return restaurants

            # Parse HTML
            soup = BeautifulSoup(response.text, 'html.parser')

            # Look for restaurant names in various elements
            # Method 1: Look for image alt tags with restaurant names
            images = soup.find_all('img', alt=True)
            for img in images:
                alt_text = img.get('alt', '').strip()
                # Skip common non-restaurant images
                if alt_text and len(alt_text) > 2 and alt_text not in [
                    'Chowdeck Logo', 'logo', 'Chowdeck', 'Restaurants',
                    'Shops', 'Pharmacy', 'African Meals', 'Healthy', 'Drinks',
                    'Chow combo', 'Local Markets'
                ]:
                    # This might be a restaurant name
                    restaurant = self._create_restaurant(alt_text, area)
                    restaurants.append(restaurant)

            # Method 2: Look for links that might be restaurant pages
            links = soup.find_all('a', href=True)
            for link in links:
                href = link.get('href', '')
                if '/restaurants/' in href:
                    # Extract restaurant name from URL or link text
                    text = link.get_text(strip=True)
                    if text and len(text) > 2 and text not in ['Restaurants', 'View Menu']:
                        restaurant = self._create_restaurant(text, area, href)
                        restaurants.append(restaurant)

            # Method 3: Look for specific class patterns that might contain restaurant info
            # (This would need to be adjusted based on actual HTML structure)

        except Exception as e:
            print(f"    Error fetching {url}: {str(e)}")

        return restaurants

    def _create_restaurant(self, name: str, area: Dict, url: str = '') -> Dict:
        """Create restaurant dict"""
        import hashlib

        # Clean name
        name = name.strip()

        # Generate ID
        name_hash = hashlib.md5(f"{name}_{area['city']}".encode()).hexdigest()[:8]
        slug = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
        restaurant_id = f"{slug}_{name_hash}"

        return {
            'id': restaurant_id,
            'name': name,
            'city': area['city'],
            'state': 'Lagos',
            'lga': area['lga'],
            'location': f"{area['city']}, Lagos",
            'url': url if url else f"https://chowdeck.com/store?q={name.replace(' ', '+')}",
            'rating': None,
            'cuisine': 'Nigerian',
            'specialties': [],
            'delivery_areas': [area['city']],
            'opening_hours': None,
        }


def main():
    scraper = ComprehensiveLagosScraper()

    # Test with first 5 areas
    print("TESTING WITH 5 AREAS")
    print("=" * 60)
    restaurants = scraper.scrape_all_areas(max_areas=5)

    print(f"\nFirst 10 restaurants:")
    for i, r in enumerate(restaurants[:10], 1):
        print(f"{i}. {r['name']} - {r['city']} ({r['lga']})")

    # Save results
    with open('lagos_restaurants_sample.json', 'w') as f:
        json.dump(restaurants, f, indent=2)

    print(f"\nSaved to lagos_restaurants_sample.json")


if __name__ == '__main__':
    main()
