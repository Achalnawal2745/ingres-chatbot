# Real CGWB 2022 data — replace with DB queries once INGRES access available

RECHARGE_DATA = {
    "Uttar Pradesh": 76.03, "Maharashtra": 34.07,
    "Madhya Pradesh": 30.45, "Rajasthan": 20.79,
    "Punjab": 21.58, "Gujarat": 21.08, "Bihar": 29.17,
    "Andhra Pradesh": 22.35, "Karnataka": 16.03, "Tamil Nadu": 22.42,
    "Haryana": 14.23, "West Bengal": 27.45, "Odisha": 18.92,
    "Chhattisgarh": 12.34, "Jharkhand": 8.76,
}

EXTRACTION_DATA = {
    "Uttar Pradesh": 68.91, "Punjab": 35.78,
    "Rajasthan": 25.43, "Maharashtra": 18.24,
    "Madhya Pradesh": 16.32, "Gujarat": 14.89, "Bihar": 12.45,
    "Andhra Pradesh": 10.23, "Karnataka": 9.87, "Tamil Nadu": 8.96,
    "Haryana": 13.56, "West Bengal": 11.23, "Odisha": 6.45,
    "Chhattisgarh": 5.67, "Jharkhand": 4.32,
}

CATEGORY_DATA = {
    "Safe": 3301,
    "Semi-Critical": 687,
    "Critical": 366,
    "Over-Exploited": 1006,
}

YEARLY_RECHARGE = {
    "2017": 394.2, "2018": 401.8,
    "2019": 398.5, "2020": 421.3,
    "2021": 429.7, "2022": 437.6,
}

YEARLY_EXTRACTION = {
    "2017": 249.1, "2018": 251.4,
    "2019": 245.8, "2020": 242.6,
    "2021": 238.9, "2022": 241.3,
}

STATE_STAGE = {
    "Punjab": 165.3, "Rajasthan": 140.2, "Haryana": 135.6,
    "Delhi": 122.4, "Uttar Pradesh": 74.3, "Gujarat": 67.8,
    "Tamil Nadu": 55.2, "Karnataka": 48.9, "Maharashtra": 43.1,
    "Madhya Pradesh": 38.7,
}


def get_chart_for_intent(intent, entities):
    """Return chart config based on AI-extracted intent and entities."""

    state = entities.get("state")
    year = entities.get("year")

    # Recharge chart
    if intent == "recharge":
        if state:
            # Yearly trend for specific state (mock data)
            years = list(YEARLY_RECHARGE.keys())
            base = RECHARGE_DATA.get(state, 20)
            values = [round(base * (0.85 + i * 0.04), 2) for i in range(len(years))]
            return {
                "type": "line",
                "title": f"Groundwater Recharge Trend — {state} (BCM)",
                "labels": years,
                "values": values,
                "color": "#1a56db"
            }
        else:
            return {
                "type": "bar",
                "title": "Annual Groundwater Recharge by State (BCM) — 2022",
                "labels": list(RECHARGE_DATA.keys()),
                "values": list(RECHARGE_DATA.values()),
                "color": "#1a56db"
            }

    # Extraction chart
    elif intent == "extraction":
        if state:
            years = list(YEARLY_EXTRACTION.keys())
            base = EXTRACTION_DATA.get(state, 15)
            values = [round(base * (0.88 + i * 0.03), 2) for i in range(len(years))]
            return {
                "type": "line",
                "title": f"Groundwater Extraction Trend — {state} (BCM)",
                "labels": years,
                "values": values,
                "color": "#e02424"
            }
        else:
            return {
                "type": "bar",
                "title": "Annual Groundwater Extraction by State (BCM) — 2022",
                "labels": list(EXTRACTION_DATA.keys()),
                "values": list(EXTRACTION_DATA.values()),
                "color": "#e02424"
            }

    # Category pie chart
    elif intent == "category_status":
        return {
            "type": "pie",
            "title": "Assessment Units by Groundwater Category (2022)",
            "labels": list(CATEGORY_DATA.keys()),
            "values": list(CATEGORY_DATA.values()),
            "colors": ["#16a34a", "#ca8a04", "#ea580c", "#dc2626"]
        }

    # Yearly comparison
    elif intent == "comparison":
        return {
            "type": "line",
            "title": "India Groundwater — Recharge vs Extraction Trend (BCM)",
            "labels": list(YEARLY_RECHARGE.keys()),
            "datasets": [
                {
                    "label": "Recharge (BCM)",
                    "values": list(YEARLY_RECHARGE.values()),
                    "color": "#1a56db"
                },
                {
                    "label": "Extraction (BCM)",
                    "values": list(YEARLY_EXTRACTION.values()),
                    "color": "#e02424"
                }
            ],
            "multi": True
        }

    # Explicit chart request
    elif intent == "show_chart":
        return {
            "type": "bar",
            "title": "Stage of Groundwater Extraction by State (%) — 2022",
            "labels": list(STATE_STAGE.keys()),
            "values": list(STATE_STAGE.values()),
            "color": "#7c3aed"
        }

    return None