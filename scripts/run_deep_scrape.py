"""
Run deep scraping of Chowdeck restaurants
This will take several minutes to complete
"""
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.clients.deep_scraper import DeepChowdeckScraper


def main():
    print("=" * 60)
    print("DEEP CHOWDECK SCRAPER")
    print("=" * 60)
    print("\nThis will scrape restaurants from 20+ areas across Lagos & Abuja")
    print("Estimated time: 5-10 minutes\n")

    # Ask for confirmation
    response = input("Continue? (yes/no): ").strip().lower()
    if response != 'yes':
        print("Scraping cancelled.")
        return

    # Initialize scraper
    scraper = DeepChowdeckScraper(headless=True)

    print("\nStarting deep scrape...")
    print("-" * 60)

    # Scrape all restaurants
    # For testing, you can limit with max_areas parameter
    restaurants = scraper.scrape_all_restaurants()

    # Save to JSON file
    output_file = 'comprehensive_restaurants.json'
    with open(output_file, 'w') as f:
        json.dump(restaurants, f, indent=2)

    print(f"\n✓ Saved {len(restaurants)} restaurants to {output_file}")

    # Print summary by state
    print("\n" + "=" * 60)
    print("SUMMARY BY STATE")
    print("=" * 60)

    states = {}
    for restaurant in restaurants:
        state = restaurant.get('state', 'Unknown')
        if state not in states:
            states[state] = []
        states[state].append(restaurant)

    for state, rests in sorted(states.items()):
        print(f"\n{state}: {len(rests)} restaurants")

        # Group by LGA
        lgas = {}
        for r in rests:
            lga = r.get('lga', 'Unknown')
            if lga not in lgas:
                lgas[lga] = 0
            lgas[lga] += 1

        for lga, count in sorted(lgas.items()):
            print(f"  - {lga}: {count}")

    print("\n" + "=" * 60)
    print("DONE!")
    print("=" * 60)


if __name__ == '__main__':
    main()
