# Groundwater status data with coordinates for map markers
# Source: CGWB 2022 Assessment

MAP_DATA = [
    {"state": "Punjab",         "lat": 31.1471, "lng": 75.3412, "stage": 165.3, "category": "Over-Exploited",  "recharge": 21.58, "extraction": 35.78},
    {"state": "Haryana",        "lat": 29.0588, "lng": 76.0856, "stage": 135.6, "category": "Over-Exploited",  "recharge": 14.23, "extraction": 13.56},
    {"state": "Rajasthan",      "lat": 27.0238, "lng": 74.2179, "stage": 140.2, "category": "Over-Exploited",  "recharge": 20.79, "extraction": 25.43},
    {"state": "Delhi",          "lat": 28.7041, "lng": 77.1025, "stage": 122.4, "category": "Over-Exploited",  "recharge": 0.32,  "extraction": 0.39},
    {"state": "Uttar Pradesh",  "lat": 26.8467, "lng": 80.9462, "stage": 74.3,  "category": "Safe",            "recharge": 76.03, "extraction": 68.91},
    {"state": "Gujarat",        "lat": 22.2587, "lng": 71.1924, "stage": 67.8,  "category": "Semi-Critical",   "recharge": 21.08, "extraction": 14.89},
    {"state": "Maharashtra",    "lat": 19.7515, "lng": 75.7139, "stage": 43.1,  "category": "Safe",            "recharge": 34.07, "extraction": 18.24},
    {"state": "Madhya Pradesh", "lat": 22.9734, "lng": 78.6569, "stage": 38.7,  "category": "Safe",            "recharge": 30.45, "extraction": 16.32},
    {"state": "Tamil Nadu",     "lat": 11.1271, "lng": 78.6569, "stage": 55.2,  "category": "Semi-Critical",   "recharge": 22.42, "extraction": 8.96},
    {"state": "Karnataka",      "lat": 15.3173, "lng": 75.7139, "stage": 48.9,  "category": "Safe",            "recharge": 16.03, "extraction": 9.87},
    {"state": "Andhra Pradesh", "lat": 15.9129, "lng": 79.7400, "stage": 42.3,  "category": "Safe",            "recharge": 22.35, "extraction": 10.23},
    {"state": "Bihar",          "lat": 25.0961, "lng": 85.3131, "stage": 36.2,  "category": "Safe",            "recharge": 29.17, "extraction": 12.45},
    {"state": "West Bengal",    "lat": 22.9868, "lng": 87.8550, "stage": 41.8,  "category": "Safe",            "recharge": 27.45, "extraction": 11.23},
    {"state": "Odisha",         "lat": 20.9517, "lng": 85.0985, "stage": 28.4,  "category": "Safe",            "recharge": 18.92, "extraction": 6.45},
    {"state": "Chhattisgarh",   "lat": 21.2787, "lng": 81.8661, "stage": 22.1,  "category": "Safe",            "recharge": 12.34, "extraction": 5.67},
]

CATEGORY_COLORS = {
    "Safe": "#16a34a",
    "Semi-Critical": "#ca8a04",
    "Critical": "#ea580c",
    "Over-Exploited": "#dc2626",
}

def get_map_data():
    return {
        "markers": MAP_DATA,
        "colors": CATEGORY_COLORS
    }