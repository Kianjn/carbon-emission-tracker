from .api_handler import CarbonAPIHandler

class CarbonCalculator:
    def __init__(self):
        self.api_handler = CarbonAPIHandler()

    def calculate_vehicle_emissions(self, vehicle_model, distance_km):
        """Calculate emissions based on vehicle model ID and distance."""
        return self.api_handler.get_vehicle_emissions(None, vehicle_model, distance_km)

    def calculate_energy_emissions(self, country_code, energy_value):
        """Calculate emissions based on electricity consumption."""
        return self.api_handler.get_electricity_emissions(country_code, energy_value)

    def calculate_flight_emissions(self, departure_airport, destination_airport, passengers):
        """Calculate emissions based on flight details."""
        return self.api_handler.get_flight_emissions(departure_airport, destination_airport, passengers)