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

    def get_vehicle_makes(self):
        """Fetch all vehicle brands (makes) from API."""
        url = f"{self.BASE_URL}/vehicle_makes"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return [
                {
                    "id": make["data"]["id"],
                    "name": make["data"]["attributes"]["name"]
                }
                for make in response.json()
            ]
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_vehicle_models(self, make_id):
        """Fetch vehicle models based on a brand (make_id)."""
        url = f"{self.BASE_URL}/vehicle_makes/{make_id}/vehicle_models"
        response = requests.get(url, headers=self.headers)

        if response.status_code == 200:
            return [
                {
                    "id": model["data"]["id"],
                    "name": model["data"]["attributes"]["name"]
                }
                for model in response.json()
            ]
        else:
            print(f"Error {response.status_code}: {response.text}")
            return None

    def get_vehicle_uuid(self, vehicle_make: str, vehicle_model: str):
        """Find the vehicle UUID based on make and model."""
        makes = self.get_vehicle_makes()
        if not makes:
            return None
        
        # Find the correct brand (make)
        make_id = next((make["id"] for make in makes if make["name"].lower() == vehicle_make.lower()), None)
        if not make_id:
            print(f"⚠️ Error: Vehicle make '{vehicle_make}' not found.")
            return None

        # Find the model within the selected make
        models = self.get_vehicle_models(make_id)
        if not models:
            return None

        model_id = next((model["id"] for model in models if model["name"].lower() == vehicle_model.lower()), None)
        if not model_id:
            print(f"⚠️ Error: Vehicle model '{vehicle_model}' not found for make '{vehicle_make}'.")
            return None

        return model_id

    def get_vehicle_emissions(self, vehicle_make: str, vehicle_model: str, distance_km: float):
        """Fetch carbon emissions for a given vehicle and distance."""
        vehicle_uuid = self.get_vehicle_uuid(vehicle_make, vehicle_model)
        if not vehicle_uuid:
            return None

        url = f"{self.BASE_URL}/estimates"
        data = {
            "type": "vehicle",
            "distance_unit": "km",
            "distance_value": distance_km,
            "vehicle_model_id": vehicle_uuid
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