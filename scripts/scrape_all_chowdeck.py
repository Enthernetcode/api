"""
Comprehensive Chowdeck scraper using multiple sources
Aggregates restaurants from blog posts and other available sources
"""
import requests
from bs4 import BeautifulSoup
import json

# Known blog posts with restaurant listings
BLOG_POSTS = [
    'https://chowdeck.com/blog/get-it-here-jollof-rice-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-amala-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-fried-rice-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-shawarma-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-suya-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-pounded-yam-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-pizza-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-chicken-republic-on-chowdeck',
   'https://chowdeck.com/blog/get-it-here-chinese-food-on-chowdeck',
    'https://chowdeck.com/blog/get-it-here-ice-cream-on-chowdeck',
]


def scrape_blog_post(url):
    """Scrape restaurants from a single blog post"""
    restaurants = []

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all h2 headings containing restaurant names
        restaurant_headings = soup.find_all('h2')

        for heading in restaurant_headings:
            try:
                link = heading.find('a')
                if not link:
                    continue

                name = link.get_text(strip=True)
                if not name or name.lower() in ['chowdeck', 'get it here']:
                    continue

                restaurant_data = {
                    'name': name,
                    'url': link.get('href', ''),
                    'source': url
                }

                # Get the next siblings to extract details
                current = heading.find_next_sibling()

                while current and current.name != 'h2' and current.name != 'hr':
                    if current.name == 'p':
                        text = current.get_text(strip=True)

                        # Extract location
                        if 'Where:' in text:
                            location_text = text.replace('Where:', '').strip()
                            restaurant_data['location'] = location_text

                        # Extract rating
                        import re
                        rating_match = re.search(r'(\d+\.\d+)\s*out of\s*5', text)
                        if rating_match:
                            restaurant_data['rating'] = float(rating_match.group(1))

                    current = current.find_next_sibling()

                if restaurant_data.get('location'):
                    restaurants.append(restaurant_data)

            except:
                continue

    except Exception as e:
        print(f"Error scraping {url}: {str(e)}")

    return restaurants


def main():
    """Scrape all available sources"""
    all_restaurants = {}  # Use dict to deduplicate by name

    print("Scraping Chowdeck blog posts for restaurants...")
    print("=" * 60)

    for blog_url in BLOG_POSTS:
        print(f"\nScraping: {blog_url}")
        restaurants = scrape_blog_post(blog_url)

        if restaurants:
            print(f"  Found {len(restaurants)} restaurants")
            for rest in restaurants:
                # Use name as key to avoid duplicates
                if rest['name'] not in all_restaurants:
                    all_restaurants[rest['name']] = rest
                else:
                    # Merge data
                    existing = all_restaurants[rest['name']]
                    existing['url'] = existing.get('url') or rest.get('url')
                    existing['rating'] = existing.get('rating') or rest.get('rating')
        else:
            print(f"  No restaurants found")

    print("\n" + "=" * 60)
    print(f"TOTAL UNIQUE RESTAURANTS: {len(all_restaurants)}")
    print("=" * 60)

    # Save to JSON
    output = list(all_restaurants.values())
    with open('all_chowdeck_restaurants.json', 'w') as f:
        json.dump(output, f, indent=2)

    print(f"\nSaved {len(output)} restaurants to all_chowdeck_restaurants.json")

    # Print summary
    print("\nRestaurant List:")
    for name in sorted(all_restaurants.keys()):
        print(f"  - {name}")


if __name__ == '__main__':
    main()
