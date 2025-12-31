"""
Investigate Chowdeck's actual API endpoints by analyzing network requests
"""
import requests
import json


def test_api_endpoints():
    """Test various API endpoint patterns"""

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'application/json',
        'Origin': 'https://chowdeck.com',
        'Referer': 'https://chowdeck.com/store/ikeja',
    }

    # Common API patterns to test
    endpoints = [
        # GraphQL
        'https://chowdeck.com/api/graphql',
        'https://api.chowdeck.com/graphql',

        # REST endpoints
        'https://api.chowdeck.com/v1/vendors',
        'https://api.chowdeck.com/v1/stores',
        'https://api.chowdeck.com/v1/restaurants',
        'https://api.chowdeck.com/vendors',
        'https://api.chowdeck.com/stores',

        # Internal API patterns
        'https://chowdeck.com/_next/data/*/store/ikeja.json',
        'https://chowdeck.com/api/stores',
        'https://chowdeck.com/api/vendors',

        # Location-based
        'https://api.chowdeck.com/locations/ikeja/vendors',
        'https://api.chowdeck.com/locations/ikeja/stores',
    ]

    print("Testing Chowdeck API endpoints...")
    print("=" * 60)

    found_endpoints = []

    for endpoint in endpoints:
        try:
            print(f"\nTesting: {endpoint}")
            response = requests.get(endpoint, headers=headers, timeout=10)

            print(f"  Status: {response.status_code}")

            if response.status_code == 200:
                print(f"  ✓ SUCCESS!")
                print(f"  Content-Type: {response.headers.get('content-type')}")
                print(f"  Response length: {len(response.text)}")

                # Try to parse as JSON
                try:
                    data = response.json()
                    print(f"  JSON keys: {list(data.keys())[:5]}")
                    found_endpoints.append({
                        'url': endpoint,
                        'status': response.status_code,
                        'sample': str(data)[:200]
                    })
                except:
                    print(f"  First 200 chars: {response.text[:200]}")

            elif response.status_code in [301, 302, 307, 308]:
                print(f"  Redirect to: {response.headers.get('location')}")

        except requests.exceptions.Timeout:
            print(f"  Timeout")
        except requests.exceptions.ConnectionError:
            print(f"  Connection error")
        except Exception as e:
            print(f"  Error: {str(e)[:100]}")

    print("\n" + "=" * 60)
    print(f"Found {len(found_endpoints)} working endpoints")
    print("=" * 60)

    for ep in found_endpoints:
        print(f"\n{ep['url']}")
        print(f"  Sample: {ep['sample']}")


if __name__ == '__main__':
    test_api_endpoints()
