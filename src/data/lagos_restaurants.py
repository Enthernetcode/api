"""
Comprehensive Lagos restaurant database
Manually curated from popular restaurants across all Lagos LGAs
Focus: Maximum coverage of restaurants available on Chowdeck in Lagos
"""

LAGOS_RESTAURANTS = [
    # === IKEJA LGA ===
    # Fast Food Chains
    {"name": "Mega Chicken", "lga": "Ikeja", "city": "Ikeja", "rating": 4.36, "cuisine": "Fast Food",
     "specialties": ["Fried Chicken", "Burgers"], "location": "Multiple locations in Ikeja"},

    {"name": "Chicken Republic", "lga": "Ikeja", "city": "Ikeja", "rating": 4.2, "cuisine": "Fast Food",
     "specialties": ["Chicken", "Rice"], "location": "Computer Village, Ikeja"},

    {"name": "Sweet Sensation", "lga": "Ikeja", "city": "Allen Avenue", "rating": 4.0, "cuisine": "Fast Food",
     "specialties": ["Pastries", "Meals"], "location": "Allen Avenue, Ikeja"},

    {"name": "Mr Biggs", "lga": "Ikeja", "city": "Alausa", "rating": 3.9, "cuisine": "Fast Food",
     "specialties": ["Burgers", "Meals"], "location": "Alausa, Ikeja"},

    {"name": "Tantalizers", "lga": "Ikeja", "city": "Ikeja", "rating": 3.9, "cuisine": "Fast Food",
     "specialties": ["Local & Continental"], "location": "Ikeja"},

    # Nigerian Restaurants
    {"name": "King Glab Cuisine", "lga": "Ikeja", "city": "Ikeja GRA", "rating": 4.36, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice", "Local Dishes"], "location": "Ikeja GRA"},

    {"name": "Ajisafe", "lga": "Ikeja", "city": "Ikeja", "rating": 4.34, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "16 Ajisafe St, Ikeja GRA"},

    {"name": "Labule", "lga": "Ikeja", "city": "Ikeja", "rating": 4.19, "cuisine": "Nigerian",
     "specialties": ["African Dishes"], "location": "Multiple Ikeja locations"},

    {"name": "Belefull", "lga": "Ikeja", "city": "Ikeja", "rating": 4.19, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "Ikeja"},

    {"name": "Mama Put", "lga": "Ikeja", "city": "Ogba", "rating": 4.1, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Ogba, Ikeja"},

    {"name": "Yellow Chilli", "lga": "Ikeja", "city": "Ikeja", "rating": 4.2, "cuisine": "Indian",
     "specialties": ["Indian Cuisine"], "location": "Ikeja City Mall"},

    # === ETI-OSA LGA ===
    # Lekki
    {"name": "Molabat Kitchen", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.47, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "14 Agungi Ajiran Rd, Lekki"},

    {"name": "Foodies", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.28, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "Lekki Phase I"},

    {"name": "Yakoyo", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.19, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "Lekki Phase I"},

    {"name": "Dominos Pizza", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.1, "cuisine": "Italian",
     "specialties": ["Pizza"], "location": "Lekki Phase 1"},

    {"name": "Debonairs Pizza", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.3, "cuisine": "Italian",
     "specialties": ["Pizza"], "location": "Admiralty Way, Lekki"},

    {"name": "KFC", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.0, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Lekki Toll Gate"},

    {"name": "Johnny Rockets", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.4, "cuisine": "American",
     "specialties": ["Burgers", "Shakes"], "location": "Admiralty Mall, Lekki"},

    {"name": "Spice Route", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.3, "cuisine": "Indian",
     "specialties": ["Indian Cuisine"], "location": "Lekki Phase 1"},

    {"name": "Bottles", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.2, "cuisine": "Continental",
     "specialties": ["Grills", "Seafood"], "location": "Lekki"},

    # Victoria Island / Ikoyi
    {"name": "Amoke Oge", "lga": "Eti-Osa", "city": "Ikoyi", "rating": 4.34, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice", "Local Dishes"], "location": "Balawa, Ikoyi"},

    {"name": "The Place", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.67, "cuisine": "Continental",
     "specialties": ["International Cuisine"], "location": "Victoria Island"},

    {"name": "Burger King", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.2, "cuisine": "Fast Food",
     "specialties": ["Burgers"], "location": "Adeola Odeku, VI"},

    {"name": "Hard Rock Cafe", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.5, "cuisine": "American",
     "specialties": ["Burgers", "Grills"], "location": "Victoria Island"},

    {"name": "Nok by Alara", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.6, "cuisine": "Contemporary Nigerian",
     "specialties": ["Modern Nigerian"], "location": "Victoria Island"},

    {"name": "Cactus", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.3, "cuisine": "Mexican",
     "specialties": ["Tacos", "Mexican Food"], "location": "VI"},

    {"name": "Shiro", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.4, "cuisine": "Asian",
     "specialties": ["Asian Fusion"], "location": "Victoria Island"},

    # Ajah
    {"name": "Chicken Republic Ajah", "lga": "Eti-Osa", "city": "Ajah", "rating": 4.1, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Ajah"},

    {"name": "Sweet Sensation Ajah", "lga": "Eti-Osa", "city": "Ajah", "rating": 3.9, "cuisine": "Fast Food",
     "specialties": ["Pastries"], "location": "Ajah"},

    # === LAGOS MAINLAND LGA ===
    {"name": "HNH Restaurant", "lga": "Lagos Mainland", "city": "Yaba", "rating": 4.58, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "27 Fola Agoro St, Igbobi Road"},

    {"name": "Iya Moria", "lga": "Lagos Mainland", "city": "Yaba", "rating": 4.36, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice", "Local Dishes"], "location": "DLI Road, Lagos"},

    {"name": "Mama Cass", "lga": "Lagos Mainland", "city": "Yaba", "rating": 4.1, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Herbert Macaulay Way, Yaba"},

    {"name": "Chicken Republic Yaba", "lga": "Lagos Mainland", "city": "Yaba", "rating": 4.1, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Yaba"},

    {"name": "De Marquee", "lga": "Lagos Mainland", "city": "Yaba", "rating": 4.2, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Yaba"},

    # === SURULERE LGA ===
    {"name": "Bukka Hut", "lga": "Surulere", "city": "Surulere", "rating": 4.2, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Surulere"},

    {"name": "Kilimanjaro", "lga": "Surulere", "city": "Surulere", "rating": 4.3, "cuisine": "Continental",
     "specialties": ["Grills", "Continental"], "location": "Adeniran Ogunsanya, Surulere"},

    {"name": "Chicken Republic Surulere", "lga": "Surulere", "city": "Surulere", "rating": 4.0, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Surulere"},

    {"name": "Mama Dee", "lga": "Surulere", "city": "Surulere", "rating": 4.1, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "Surulere"},

    {"name": "Ofada Boy", "lga": "Surulere", "city": "Surulere", "rating": 4.2, "cuisine": "Nigerian",
     "specialties": ["Ofada Rice"], "location": "Surulere"},

    # === KOSOFE LGA ===
    {"name": "Bungalow Restaurant", "lga": "Kosofe", "city": "Gbagada", "rating": 4.3, "cuisine": "Continental",
     "specialties": ["Grills", "International"], "location": "Gbagada Expressway"},

    {"name": "Yellow Chilli Maryland", "lga": "Kosofe", "city": "Maryland", "rating": 4.2, "cuisine": "Indian",
     "specialties": ["Indian Cuisine"], "location": "Maryland Mall"},

    {"name": "Chicken Republic Maryland", "lga": "Kosofe", "city": "Maryland", "rating": 4.1, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Maryland"},

    {"name": "Mama Ebo", "lga": "Kosofe", "city": "Gbagada", "rating": 4.0, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Gbagada"},

    {"name": "Obalende Suya", "lga": "Kosofe", "city": "Ogudu", "rating": 4.2, "cuisine": "Nigerian",
     "specialties": ["Suya"], "location": "Ogudu"},

    # === OSHODI-ISOLO LGA ===
    {"name": "Tantalizers Oshodi", "lga": "Oshodi-Isolo", "city": "Oshodi", "rating": 3.9, "cuisine": "Fast Food",
     "specialties": ["Local & Continental"], "location": "Oshodi"},

    {"name": "Chicken Republic Isolo", "lga": "Oshodi-Isolo", "city": "Isolo", "rating": 4.0, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Isolo"},

    {"name": "Mama Cass Isolo", "lga": "Oshodi-Isolo", "city": "Isolo", "rating": 4.0, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Isolo"},

    # === AMUWO-ODOFIN LGA ===
    {"name": "Genesis Restaurant", "lga": "Amuwo-Odofin", "city": "Festac", "rating": 4.1, "cuisine": "Continental",
     "specialties": ["Grills"], "location": "Festac Town"},

    {"name": "Chicken Republic Festac", "lga": "Amuwo-Odofin", "city": "Festac", "rating": 4.0, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Festac"},

    {"name": "Mama Put Festac", "lga": "Amuwo-Odofin", "city": "Festac", "rating": 4.1, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Festac"},

    # === ALIMOSHO LGA ===
    {"name": "Chicken Republic Egbeda", "lga": "Alimosho", "city": "Egbeda", "rating": 4.0, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Egbeda"},

    {"name": "Mama Cass Ikotun", "lga": "Alimosho", "city": "Ikotun", "rating": 3.9, "cuisine": "Nigerian",
     "specialties": ["Local Dishes"], "location": "Ikotun"},

    {"name": "De Angelo", "lga": "Alimosho", "city": "Egbeda", "rating": 4.1, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "Egbeda"},

    # === APAPA LGA ===
    {"name": "Chicken Republic Apapa", "lga": "Apapa", "city": "Apapa", "rating": 3.9, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Apapa"},

    {"name": "The Wharf", "lga": "Apapa", "city": "Apapa", "rating": 4.0, "cuisine": "Seafood",
     "specialties": ["Seafood"], "location": "Apapa"},

    # === SOMOLU LGA ===
    {"name": "Chicken Republic Somolu", "lga": "Somolu", "city": "Somolu", "rating": 3.9, "cuisine": "Fast Food",
     "specialties": ["Chicken"], "location": "Somolu"},

    {"name": "Mama Dee Palmgrove", "lga": "Somolu", "city": "Palmgrove", "rating": 4.0, "cuisine": "Nigerian",
     "specialties": ["Jollof Rice"], "location": "Palmgrove"},

    # === Additional Popular Chains (Multiple Locations) ===
    {"name": "Coldstone Creamery", "lga": "Eti-Osa", "city": "Lekki", "rating": 4.3, "cuisine": "Dessert",
     "specialties": ["Ice Cream"], "location": "Multiple locations"},

    {"name": "Shoprite Food Court", "lga": "Ikeja", "city": "Ikeja", "rating": 4.0, "cuisine": "Various",
     "specialties": ["Multiple Cuisines"], "location": "Shoprite Ikeja"},

    {"name": "Spur", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.2, "cuisine": "Steakhouse",
     "specialties": ["Steaks", "Burgers"], "location": "VI"},

    {"name": "Ocean Basket", "lga": "Eti-Osa", "city": "Victoria Island", "rating": 4.3, "cuisine": "Seafood",
     "specialties": ["Seafood"], "location": "Victoria Island"},
]


def get_all_lagos_restaurants():
    """Get all Lagos restaurants with generated IDs"""
    import hashlib
    import re

    restaurants = []

    for idx, data in enumerate(LAGOS_RESTAURANTS):
        # Generate ID
        name_hash = hashlib.md5(data['name'].encode()).hexdigest()[:8]
        slug = re.sub(r'[^a-z0-9]+', '_', data['name'].lower()).strip('_')
        restaurant_id = f"{slug}_{name_hash}"

        restaurant = {
            'id': restaurant_id,
            'name': data['name'],
            'city': data['city'],
            'state': 'Lagos',
            'lga': data['lga'],
            'location': data['location'],
            'rating': data.get('rating'),
            'cuisine': data.get('cuisine', 'Nigerian'),
            'specialties': data.get('specialties', []),
            'delivery_areas': [data['city']],
            'opening_hours': None,
            'url': f"https://chowdeck.com/store?q={data['name'].replace(' ', '+').lower()}",
        }

        restaurants.append(restaurant)

    return restaurants
