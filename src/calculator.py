from src.api_handler import CarbonAPIHandler

class CarbonCalculator:
    def __init__(self):
        self.api_handler = CarbonAPIHandler()

    def calculate_travel_emissions(self, vehicle_make, vehicle_model, distance_km):
        """Calculate emissions based on vehicle make, model, and distance."""
        emission = self.api_handler.get_vehicle_emissions(vehicle_make, vehicle_model, distance_km)
        print(f"🔍 Travel Emission Calculation: {emission}")  # Debugging line
        return emission

    def calculate_energy_emissions(self, country_code, energy_kwh):
        emission = self.api_handler.get_electricity_emissions(country_code, energy_kwh)
        print(f"🔍 Energy Emission Calculation: {emission}")  # Debugging line
        return emission