import requests
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
CARBON_API_KEY = os.getenv("CARBON_API_KEY")

class CarbonAPIHandler:
    BASE_URL = "https://www.carboninterface.com/api/v1"

    def __init__(self):
        if not CARBON_API_KEY:
            raise ValueError("API key is missing! Please add it to the .env file.")
        
        self.headers = {
            "Authorization": f"Bearer {CARBON_API_KEY}",
            "Content-Type": "application/json"
        }
        # Cache for vehicle makes and models
        self._vehicle_makes = None
        self._vehicle_models_cache = {}

    def get_vehicle_makes(self):
        """Fetch all vehicle brands (makes) from API."""
        if self._vehicle_makes is not None:
            return self._vehicle_makes

        url = f"{self.BASE_URL}/vehicle_makes"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                makes = [
                    {
                        "id": make["data"]["id"],
                        "name": make["data"]["attributes"]["name"]
                    }
                    for make in data
                ]
                self._vehicle_makes = makes
                return makes
            else:
                print(f"⚠️ Unexpected API response format for vehicle makes: {data}")
                return []
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return []

    def get_vehicle_models(self, make_id):
        """Fetch vehicle models based on a brand (make_id)."""
        if make_id in self._vehicle_models_cache:
            return self._vehicle_models_cache[make_id]

        url = f"{self.BASE_URL}/vehicle_makes/{make_id}/vehicle_models"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                models = [
                    {
                        "id": model["data"]["id"],
                        "name": model["data"]["attributes"]["name"]
                    }
                    for model in data
                ]
                self._vehicle_models_cache[make_id] = models
                return models
            else:
                print(f"⚠️ Unexpected API response format for vehicle models: {data}")
                return []
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return []

    def get_vehicle_emissions(self, vehicle_make: str, vehicle_model: str, distance_km: float):
        """Fetch carbon emissions for a given vehicle and distance."""
        try:
            # Calculate emissions directly using the provided model ID
            url = f"{self.BASE_URL}/estimates"
            data = {
                "type": "vehicle",
                "distance_unit": "km",
                "distance_value": distance_km,
                "vehicle_model_id": vehicle_model  # This is now the model ID directly
            }
            response = requests.post(url, json=data, headers=self.headers)

            if response.status_code == 201:
                result = response.json()
                if "data" in result and "attributes" in result["data"]:
                    emissions_kg = result["data"]["attributes"].get("carbon_kg", None)
                    if emissions_kg is not None:
                        print(f"✅ Calculated emissions: {emissions_kg} kg CO2")
                        return emissions_kg
                    else:
                        print("⚠️ No emissions data found in API response")
                        return None
                else:
                    print("⚠️ Unexpected API response format")
                    return None
            else:
                print(f"❌ API Error {response.status_code}: {response.text}")
                return None
        except Exception as e:
            print(f"❌ Error calculating vehicle emissions: {str(e)}")
            return None

    def get_flight_emissions(self, departure_airport: str, destination_airport: str, passengers: int = 1, cabin_class: str = "economy"):
        """Fetch carbon emissions for a flight between two airports."""
        url = f"{self.BASE_URL}/estimates"
        data = {
            "type": "flight",
            "passengers": passengers,
            "legs": [
                {"departure_airport": departure_airport, "destination_airport": destination_airport, "cabin_class": cabin_class}
            ],
            "distance_unit": "km"
        }
        response = requests.post(url, json=data, headers=self.headers)

        if response.status_code == 201:
            result = response.json()
            if "data" in result and "attributes" in result["data"]:
                emissions_kg = result["data"]["attributes"].get("carbon_kg", None)
                return emissions_kg
            else:
                print("⚠️ Unexpected API response format. Missing 'data' or 'attributes'.")
                return None
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None

    def get_electricity_emissions(self, country: str, electricity_value_kwh: float):
        """Fetch electricity emissions for a given consumption in kWh and country."""
        url = f"{self.BASE_URL}/estimates"
        data = {
            "type": "electricity",
            "electricity_unit": "kwh",
            "electricity_value": electricity_value_kwh,
            "country": country
        }
        response = requests.post(url, json=data, headers=self.headers)

        print(f"🔍 API Response: {response.status_code} - {response.text}")

        if response.status_code == 201:
            result = response.json()
            if "data" in result and "attributes" in result["data"]:
                emissions_kg = result["data"]["attributes"].get("carbon_kg", None)
                print(f"✅ Extracted Emissions: {emissions_kg} kg CO2")
                return emissions_kg
            else:
                print("⚠️ Unexpected API response format. Missing 'data' or 'attributes'.")
                return None
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
            return None