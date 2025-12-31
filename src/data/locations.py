"""
Nigeria States and LGAs with Chowdeck availability
"""

LOCATIONS = {
    "Lagos": {
        "state_code": "LAG",
        "lgas": {
            "Ikeja": ["Ikeja GRA", "Allen Avenue", "Alausa", "Ogba"],
            "Eti-Osa": ["Lekki", "Victoria Island", "Ikoyi", "Ajah", "Chevron"],
            "Lagos Mainland": ["Yaba", "Ebute Metta", "Sabo"],
            "Surulere": ["Surulere", "Shitta", "Adeniran Ogunsanya"],
            "Kosofe": ["Gbagada", "Ogudu", "Maryland", "Ketu"],
            "Oshodi-Isolo": ["Oshodi", "Isolo", "Ejigbo"],
            "Mushin": ["Mushin", "Idi-Oro"],
            "Shomolu": ["Shomolu", "Bariga"],
            "Amuwo-Odofin": ["Festac", "Amuwo Odofin"],
            "Alimosho": ["Egbeda", "Ikotun", "Iyana Ipaja"],
        }
    },
    "FCT": {
        "state_code": "FCT",
        "lgas": {
            "Abuja Municipal": [
                "Wuse", "Garki", "Maitama", "Asokoro", "Central Area",
                "Gwarinpa", "Jabi", "Utako", "Kubwa", "Kado", "Wuye"
            ],
            "Gwagwalada": ["Gwagwalada"],
            "Kuje": ["Kuje"],
            "Abaji": ["Abaji"],
        }
    },
    "Oyo": {
        "state_code": "OYO",
        "lgas": {
            "Ibadan North": ["Bodija", "Agodi", "Mokola"],
            "Ibadan South-West": ["Ring Road", "Oke-Ado"],
            "Ibadan North-East": ["Iwo Road", "Sango"],
            "Ibadan South-East": ["Mapo", "Beere"],
        }
    },
    "Rivers": {
        "state_code": "RIV",
        "lgas": {
            "Port Harcourt": ["GRA", "Trans Amadi", "Rumuola", "D-Line"],
            "Obio-Akpor": ["Rumuokoro", "Choba", "Eliozu"],
        }
    },
    "Edo": {
        "state_code": "EDO",
        "lgas": {
            "Oredo": ["Ring Road", "Ugbowo", "Uselu"],
            "Egor": ["Uselu", "Ugbor"],
        }
    },
    "Delta": {
        "state_code": "DEL",
        "lgas": {
            "Oshimili South": ["Asaba", "Cable Point"],
        }
    },
    "Ogun": {
        "state_code": "OGU",
        "lgas": {
            "Abeokuta South": ["Oke-Ilewo", "Isale Igbein"],
        }
    },
    "Kaduna": {
        "state_code": "KAD",
        "lgas": {
            "Kaduna North": ["Kaduna North"],
            "Kaduna South": ["Kaduna South"],
        }
    },
    "Enugu": {
        "state_code": "ENU",
        "lgas": {
            "Enugu North": ["GRA", "Independence Layout"],
        }
    },
}


def get_all_states():
    """Get all available states"""
    return list(LOCATIONS.keys())


def get_lgas_for_state(state):
    """Get all LGAs for a given state"""
    if state in LOCATIONS:
        return list(LOCATIONS[state]["lgas"].keys())
    return []


def get_areas_for_lga(state, lga):
    """Get all areas within an LGA"""
    if state in LOCATIONS and lga in LOCATIONS[state]["lgas"]:
        return LOCATIONS[state]["lgas"][lga]
    return []


def get_chowdeck_url_for_area(area):
    """Generate Chowdeck store URL for a specific area"""
    # Normalize area name for URL
    area_slug = area.lower().replace(" ", "-")
    return f"https://chowdeck.com/store/{area_slug}"
