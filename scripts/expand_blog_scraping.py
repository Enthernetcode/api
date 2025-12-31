"""
Expand blog scraping to find ALL blog posts with restaurant lists
Then extract every restaurant from those posts
"""
import requests
from bs4 import BeautifulSoup
import re
import hashlib
import json
from typing import List, Dict

# Known food category blog posts
BLOG_POSTS = {
    'jollof': 'https://chowdeck.com/blog/get-it-here-jollof-rice-on-chowdeck',
    'pizza': 'https://chowdeck.com/blog/get-it-here-pizza-on-chowdeck',
    'chinese': 'https://chowdeck.com/blog/get-it-here-chinese-food-on-chowdeck',
    'shawarma': 'https://chowdeck.com/blog/get-it-here-shawarma-on-chowdeck',
    'suya': 'https://chowdeck.com/blog/get-it-here-suya-on-chowdeck',
    'burgers': 'https://chowdeck.com/blog/get-it-here-burgers-on-chowdeck',
    'chicken': 'https://chowdeck.com/blog/get-it-here-fried-chicken-on-chowdeck',
    'rice': 'https://chowdeck.com/blog/get-it-here-rice-on-chowdeck',
    'breakfast': 'https://chowdeck.com/blog/get-it-here-breakfast-on-chowdeck',
    'lunch': 'https://chowdeck.com/blog/get-it-here-lunch-on-chowdeck',
    'dinner': 'https://chowdeck.com/blog/get-it-here-dinner-on-chowdeck',
    'amala': 'https://chowdeck.com/blog/get-it-here-amala-on-chowdeck',
    'pounded-yam': 'https://chowdeck.com/blog/get-it-here-pounded-yam-on-chowdeck',
    'semo': 'https://chowdeck.com/blog/get-it-here-semo-on-chowdeck',
    'pasta': 'https://chowdeck.com/blog/get-it-here-pasta-on-chowdeck',
    'seafood': 'https://chowdeck.com/blog/get-it-here-seafood-on-chowdeck',
    'ice-cream': 'https://chowdeck.com/blog/get-it-here-ice-cream-on-chowdeck',
    'smoothies': 'https://chowdeck.com/blog/get-it-here-smoothies-on-chowdeck',
    'salad': 'https://chowdeck.com/blog/get-it-here-salad-on-chowdeck',
    'soup': 'https://chowdeck.com/blog/get-it-here-soup-on-chowdeck',
}

# LGA mapping for Lagos
LAGOS_LGA_MAP = {
    'ikeja': 'Ikeja', 'allen': 'Ikeja', 'ogba': 'Ikeja', 'alausa': 'Ikeja',
    'computer village': 'Ikeja', 'ikeja gra': 'Ikeja',
    'lekki': 'Eti-Osa', 'victoria island': 'Eti-Osa', 'vi': 'Eti-Osa',
    'ikoyi': 'Eti-Osa', 'ajah': 'Eti-Osa', 'lekki phase 1': 'Eti-Osa',
    'lekki phase 2': 'Eti-Osa', 'agungi': 'Eti-Osa', 'oniru': 'Eti-Osa',
    'yaba': 'Lagos Mainland', 'ebute metta': 'Lagos Mainland', 'sabo': 'Lagos Mainland',
    'surulere': 'Surulere', 'adeniran': 'Surulere',
    'gbagada': 'Kosofe', 'ogudu': 'Kosofe', 'maryland': 'Kosofe', 'ketu': 'Kosofe',
    'oshodi': 'Oshodi-Isolo', 'isolo': 'Oshodi-Isolo', 'mafoluku': 'Oshodi-Isolo',
    'festac': 'Amuwo-Odofin', 'amuwo': 'Amuwo-Odofin',
    'egbeda': 'Alimosho', 'ikotun': 'Alimosho', 'idimu': 'Alimosho', 'ipaja': 'Alimosho',
    'apapa': 'Apapa',
    'somolu': 'Somolu', 'palmgrove': 'Somolu',
}


class ExpandedBlogScraper:
    """Scrape all restaurant data from Chowdeck blog posts"""

    def __init__(self):
        self.timeout = 30
        self.restaurants = {}  # Deduplicate by ID

    def scrape_all_posts(self) -> List[Dict]:
        """Scrape all blog posts"""
        print("Scraping all blog posts for Lagos restaurants...")
        print("=" * 60)

        for category, url in BLOG_POSTS.items():
            print(f"\nCategory: {category}")
            print(f"  URL: {url}")

            try:
                response = requests.get(url, timeout=self.timeout)

                # Check if post exists
                if response.status_code == 404:
                    print(f"  ✗ Post not found (404)")
                    continue

                if response.status_code != 200:
                    print(f"  ✗ Error: Status {response.status_code}")
                    continue

                # Parse
                restaurants = self._scrape_post(response.text, category)

                # Filter for Lagos only
                lagos_restaurants = [r for r in restaurants if r.get('state') == 'Lagos']

                # Add to database
                for restaurant in lagos_restaurants:
                    if restaurant['id'] not in self.restaurants:
                        self.restaurants[restaurant['id']] = restaurant

                print(f"  ✓ Found {len(lagos_restaurants)} Lagos restaurants (Total: {len(self.restaurants)})")

            except Exception as e:
                print(f"  ✗ Error: {str(e)}")
                continue

        print(f"\n{'=' * 60}")
        print(f"TOTAL LAGOS RESTAURANTS: {len(self.restaurants)}")
        print(f"{'=' * 60}")

        return list(self.restaurants.values())

    def _scrape_post(self, html_content: str, category: str) -> List[Dict]:
        """Scrape a single blog post"""
        restaurants = []
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find all restaurant headings (h2 with links)
        restaurant_headings = soup.find_all('h2')

        for heading in restaurant_headings:
            try:
                link = heading.find('a')
                if not link:
                    continue

                name = link.get_text(strip=True)

                # Skip generic headings
                if not name or name.lower() in ['chowdeck', 'get it here', 'conclusion']:
                    continue

                # Initialize restaurant
                restaurant = {
                    'id': None,
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
                    'specialties': [category.replace('-', ' ').title()]
                }

                # Parse details from siblings
                current = heading.find_next_sibling()

                while current and current.name != 'h2' and current.name != 'hr':
                    if current.name == 'p':
                        text = current.get_text(strip=True)

                        # Rating
                        rating_match = re.search(r'(\d+\.\d+)\s*out of\s*5', text)
                        if rating_match:
                            restaurant['rating'] = float(rating_match.group(1))

                        # Location
                        if 'Where:' in text or text.startswith('Where'):
                            location_text = text.replace('Where:', '').strip()
                            restaurant['location'] = location_text
                            self._parse_location(restaurant, location_text)

                        # Delivery areas
                        if 'Delivering To:' in text or 'Delivering to:' in text:
                            delivery_text = re.sub(r'Delivering [Tt]o:\s*', '', text).strip()
                            areas = [area.strip() for area in delivery_text.split(',') if area.strip()]
                            restaurant['delivery_areas'] = areas

                        # Opening hours
                        if 'Opening Hours:' in text or 'Hours:' in text:
                            hours_text = re.sub(r'Opening Hours:\s*|Hours:\s*', '', text).strip()
                            restaurant['opening_hours'] = hours_text

                    current = current.find_next_sibling()

                # Generate ID
                if restaurant['state']:
                    restaurant['id'] = self._generate_id(name, restaurant.get('city', ''))
                    restaurants.append(restaurant)

            except Exception:
                continue

        return restaurants

    def _parse_location(self, restaurant: Dict, location_text: str):
        """Parse location and extract state, LGA, city"""
        location_lower = location_text.lower()

        # Check if it's Lagos
        is_lagos = any(area in location_lower for area in [
            'lagos', 'ikeja', 'lekki', 'yaba', 'surulere', 'ikoyi',
            'victoria island', 'vi', 'gbagada', 'maryland', 'festac'
        ])

        if is_lagos:
            restaurant['state'] = 'Lagos'
            restaurant['city'] = 'Lagos'

            # Match to LGA
            for area, lga in LAGOS_LGA_MAP.items():
                if area in location_lower:
                    restaurant['lga'] = lga
                    break

            # If no LGA matched, default to first keyword found
            if not restaurant['lga']:
                restaurant['lga'] = 'Lagos Mainland'

    def _generate_id(self, name: str, city: str) -> str:
        """Generate unique ID"""
        combined = f"{name}_{city}"
        name_hash = hashlib.md5(combined.encode()).hexdigest()[:8]
        slug = re.sub(r'[^a-z0-9]+', '_', name.lower()).strip('_')
        return f"{slug}_{name_hash}"


def main():
    scraper = ExpandedBlogScraper()
    restaurants = scraper.scrape_all_posts()

    # Group by LGA
    lgas = {}
    for r in restaurants:
        lga = r.get('lga', 'Unknown')
        if lga not in lgas:
            lgas[lga] = []
        lgas[lga].append(r)

    print("\n\nRestaurants by LGA:")
    for lga in sorted(lgas.keys()):
        print(f"\n{lga}: {len(lgas[lga])} restaurants")
        for r in lgas[lga][:5]:  # Show first 5
            print(f"  - {r['name']}")

    # Save to file
    with open('lagos_blog_restaurants.json', 'w') as f:
        json.dump(restaurants, f, indent=2)

    print(f"\nSaved {len(restaurants)} restaurants to lagos_blog_restaurants.json")


if __name__ == '__main__':
    main()
