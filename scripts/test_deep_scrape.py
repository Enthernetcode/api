"""
Test deep scraper with just 3 areas
"""
import json
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.clients.deep_scraper import DeepChowdeckScraper


def main():
    print("Testing Deep Scraper with 3 areas...")
    print("=" * 60)

    scraper = DeepChowdeckScraper(headless=True)

    # Test with just 3 areas
    test_areas = [
        {'name': 'Ikeja', 'lga': 'Ikeja', 'state': 'Lagos'},
        {'name': 'Lekki', 'lga': 'Eti-Osa', 'state': 'Lagos'},
        {'name': 'Victoria-Island', 'lga': 'Eti-Osa', 'state': 'Lagos'},
    ]

    restaurants = scraper.scrape_all_restaurants(areas=test_areas)

    print(f"\n{'='*60}")
    print(f"Test Results: {len(restaurants)} unique restaurants found")
    print(f"{'='*60}\n")

    # Show first 10 restaurants
    for i, rest in enumerate(restaurants[:10], 1):
        print(f"{i}. {rest['name']} - {rest['city']}, {rest['lga']}")

    # Save to test file
    with open('test_restaurants.json', 'w') as f:
        json.dump(restaurants, f, indent=2)

    print(f"\nSaved to test_restaurants.json")


if __name__ == '__main__':
    main()
