"""
Script to find all available Chowdeck blog posts and restaurant listings
"""
import requests
from bs4 import BeautifulSoup
import json
import re

def find_blog_posts_with_restaurants():
    """Find all blog posts that list restaurants"""
    blog_urls = []

    # Check blog homepage
    try:
        response = requests.get('https://chowdeck.com/blog', timeout=30)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all blog post links
        links = soup.find_all('a', href=re.compile(r'/blog/'))

        for link in links:
            href = link.get('href')
            if href and 'restaurant' in href.lower() or 'food' in href.lower() or 'where-to' in href.lower():
                full_url = f"https://chowdeck.com{href}" if href.startswith('/') else href
                blog_urls.append(full_url)

        print(f"Found {len(blog_urls)} potential restaurant blog posts")
        for url in set(blog_urls):
            print(f"  - {url}")

    except Exception as e:
        print(f"Error fetching blog: {str(e)}")

    return list(set(blog_urls))


def check_sitemap():
    """Check sitemap for restaurant pages"""
    try:
        response = requests.get('https://chowdeck.com/sitemap.xml', timeout=30)
        if response.status_code == 200:
            print("\n=== Sitemap URLs ===")
            soup = BeautifulSoup(response.content, 'xml')
            locs = soup.find_all('loc')

            restaurant_urls = []
            for loc in locs:
                url = loc.text
                if 'store' in url or 'restaurant' in url:
                    restaurant_urls.append(url)

            print(f"Found {len(restaurant_urls)} store/restaurant URLs in sitemap")
            for url in restaurant_urls[:20]:  # Show first 20
                print(f"  - {url}")

            return restaurant_urls

    except Exception as e:
        print(f"Error checking sitemap: {str(e)}")

    return []


def check_store_api():
    """Try to find API endpoints by checking common patterns"""
    print("\n=== Checking for API endpoints ===")

    # Common API patterns
    endpoints = [
        'https://api.chowdeck.com/v1/vendors',
        'https://api.chowdeck.com/v1/restaurants',
        'https://api.chowdeck.com/v1/stores',
        'https://api.chowdeck.com/vendors',
        'https://api.chowdeck.com/restaurants',
        'https://chowdeck.com/api/vendors',
        'https://chowdeck.com/api/restaurants',
        'https://chowdeck.com/api/stores',
    ]

    for endpoint in endpoints:
        try:
            response = requests.get(endpoint, timeout=10)
            if response.status_code == 200:
                print(f"✓ Found working endpoint: {endpoint}")
                print(f"  Response: {response.text[:200]}...")
            elif response.status_code != 404:
                print(f"~ {endpoint} returned {response.status_code}")
        except:
            pass


if __name__ == '__main__':
    print("=" * 60)
    print("CHOWDECK RESTAURANT DISCOVERY")
    print("=" * 60)

    # Find blog posts
    blog_posts = find_blog_posts_with_restaurants()

    # Check sitemap
    sitemap_urls = check_sitemap()

    # Check API endpoints
    check_store_api()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Blog posts found: {len(blog_posts)}")
    print(f"Sitemap URLs found: {len(sitemap_urls)}")
