"""
Comprehensive seed database of Chowdeck restaurants
Manually curated from Chowdeck's popular restaurants across Lagos & Abuja
This provides a foundation that can be expanded over time
"""

SEED_RESTAURANTS = [
    # === IKEJA LGA ===
    {
        "name": "Mega Chicken", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "Multiple locations in Ikeja",
        "rating": 4.36, "cuisine": "Fast Food", "specialties": ["Fried Chicken", "Burgers"]
    },
    {
        "name": "King Glab Cuisine", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "Ikeja GRA",
        "rating": 4.36, "cuisine": "Nigerian", "specialties": ["Jollof Rice", "Local Dishes"]
    },
    {
        "name": "Ajisafe", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "16 Ajisafe St, Ikeja GRA",
        "rating": 4.34, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "Labule", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "Multiple Ikeja locations",
        "rating": 4.19, "cuisine": "Nigerian", "specialties": ["African Dishes"]
    },
    {
        "name": "Belefull", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "Ikeja",
        "rating": 4.19, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "Sweet Sensation", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "Allen Avenue, Ikeja",
        "rating": 4.0, "cuisine": "Fast Food", "specialties": ["Pastries", "Meals"]
    },
    {
        "name": "Chicken Republic", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "Computer Village, Ikeja",
        "rating": 4.2, "cuisine": "Fast Food", "specialties": ["Chicken", "Rice"]
    },
    {
        "name": "Mr Biggs", "city": "Ikeja", "state": "Lagos", "lga": "Ikeja",
        "location": "Alausa, Ikeja",
        "rating": 3.9, "cuisine": "Fast Food", "specialties": ["Burgers", "Meals"]
    },

    # === ETI-OSA LGA (Lekki, VI, Ikoyi) ===
    {
        "name": "Molabat Kitchen", "city": "Lekki", "state": "Lagos", "lga": "Eti-Osa",
        "location": "14 Agungi Ajiran Rd, Lekki Peninsula II",
        "rating": 4.47, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "Amoke Oge", "city": "Ikoyi", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Balawa, Ikoyi, Surulere",
        "rating": 4.34, "cuisine": "Nigerian", "specialties": ["Jollof Rice", "Local Dishes"]
    },
    {
        "name": "Foodies", "city": "Lekki", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Lekki Phase I",
        "rating": 4.28, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "Yakoyo", "city": "Lekki", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Lekki Phase I",
        "rating": 4.19, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "The Place", "city": "Lagos", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Victoria Island & Other locations",
        "rating": 4.67, "cuisine": "Continental", "specialties": ["International Cuisine"]
    },
    {
        "name": "Dominos Pizza", "city": "Lekki", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Lekki Phase 1",
        "rating": 4.1, "cuisine": "Italian", "specialties": ["Pizza"]
    },
    {
        "name": "Debonairs Pizza", "city": "Victoria Island", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Admiralty Way, Lekki",
        "rating": 4.3, "cuisine": "Italian", "specialties": ["Pizza"]
    },
    {
        "name": "KFC", "city": "Lekki", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Lekki Toll Gate",
        "rating": 4.0, "cuisine": "Fast Food", "specialties": ["Chicken"]
    },
    {
        "name": "Burger King", "city": "Victoria Island", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Adeola Odeku, VI",
        "rating": 4.2, "cuisine": "Fast Food", "specialties": ["Burgers"]
    },
    {
        "name": "Johnny Rockets", "city": "Lekki", "state": "Lagos", "lga": "Eti-Osa",
        "location": "Admiralty Mall, Lekki",
        "rating": 4.4, "cuisine": "American", "specialties": ["Burgers", "Shakes"]
    },

    # === LAGOS MAINLAND LGA ===
    {
        "name": "HNH Restaurant", "city": "Yaba", "state": "Lagos", "lga": "Lagos Mainland",
        "location": "27 Fola Agoro St, Igbobi Road",
        "rating": 4.58, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "Iya Moria", "city": "Yaba", "state": "Lagos", "lga": "Lagos Mainland",
        "location": "DLI Road, Lagos",
        "rating": 4.36, "cuisine": "Nigerian", "specialties": ["Jollof Rice", "Local Dishes"]
    },
    {
        "name": "Mama Cass", "city": "Yaba", "state": "Lagos", "lga": "Lagos Mainland",
        "location": "Herbert Macaulay Way, Yaba",
        "rating": 4.1, "cuisine": "Nigerian", "specialties": ["Local Dishes"]
    },

    # === SURULERE LGA ===
    {
        "name": "Bukka Hut", "city": "Surulere", "state": "Lagos", "lga": "Surulere",
        "location": "Surulere",
        "rating": 4.2, "cuisine": "Nigerian", "specialties": ["Local Dishes"]
    },
    {
        "name": "Kilimanjaro", "city": "Surulere", "state": "Lagos", "lga": "Surulere",
        "location": "Adeniran Ogunsanya, Surulere",
        "rating": 4.3, "cuisine": "Continental", "specialties": ["Grills", "Continental"]
    },

    # === KOSOFE LGA (Gbagada, Ogudu, Maryland) ===
    {
        "name": "Bungalow Restaurant", "city": "Gbagada", "state": "Lagos", "lga": "Kosofe",
        "location": "Gbagada Expressway",
        "rating": 4.3, "cuisine": "Continental", "specialties": ["Grills", "International"]
    },
    {
        "name": "Yellow Chilli", "city": "Maryland", "state": "Lagos", "lga": "Kosofe",
        "location": "Maryland Mall",
        "rating": 4.2, "cuisine": "Indian", "specialties": ["Indian Cuisine"]
    },

    # === OSHODI-ISOLO LGA ===
    {
        "name": "Tantalizers", "city": "Oshodi", "state": "Lagos", "lga": "Oshodi-Isolo",
        "location": "Oshodi",
        "rating": 3.9, "cuisine": "Fast Food", "specialties": ["Local & Continental"]
    },

    # === AMUWO-ODOFIN LGA (Festac) ===
    {
        "name": "Genesis Restaurant", "city": "Festac", "state": "Lagos", "lga": "Amuwo-Odofin",
        "location": "Festac Town",
        "rating": 4.1, "cuisine": "Continental", "specialties": ["Grills"]
    },

    # === ABUJA (FCT) ===
    {
        "name": "November Cubes", "city": "Abuja", "state": "FCT", "lga": "Abuja Municipal",
        "location": "Garki, Mambolo, Wuse",
        "rating": 4.67, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "Talenu Bukka", "city": "Abuja", "state": "FCT", "lga": "Abuja Municipal",
        "location": "Gwarinpa",
        "rating": 4.44, "cuisine": "Nigerian", "specialties": ["Jollof Rice", "Local Dishes"]
    },
    {
        "name": "Red Gourmet", "city": "Abuja", "state": "FCT", "lga": "Abuja Municipal",
        "location": "Central Area",
        "rating": 4.20, "cuisine": "Nigerian", "specialties": ["Jollof Rice"]
    },
    {
        "name": "Nkoyo", "city": "Abuja", "state": "FCT", "lga": "Abuja Municipal",
        "location": "Wuse 2",
        "rating": 4.5, "cuisine": "Nigerian", "specialties": ["Local Nigerian Dishes"]
    },
    {
        "name": "Wakkis", "city": "Abuja", "state": "FCT", "lga": "Abuja Municipal",
        "location": "Gwarinpa",
        "rating": 4.3, "cuisine": "Nigerian", "specialties": ["Suya", "Grills"]
    },
]


def get_all_seed_restaurants():
    """Get all seed restaurants"""
    import hashlib
    import re

    restaurants = []
    for idx, data in enumerate(SEED_RESTAURANTS):
        # Generate ID
        name_hash = hashlib.md5(data['name'].encode()).hexdigest()[:8]
        slug = re.sub(r'[^a-z0-9]+', '_', data['name'].lower()).strip('_')
        restaurant_id = f"{slug}_{name_hash}"

        restaurant = {
            'id': restaurant_id,
            'name': data['name'],
            'city': data['city'],
            'state': data['state'],
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
