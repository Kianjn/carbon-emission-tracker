from src.api_handler import CarbonAPIHandler

class CarbonCalculator:
    def __init__(self):
        self.api_handler = CarbonAPIHandler()

    def calculate_travel_emissions(self, vehicle_make, vehicle_model, distance_km):
        """Calculate emissions based on vehicle make, model, and distance."""
        emission = self.api_handler.get_vehicle_emissions(vehicle_make, vehicle_model, distance_km)
        return emission

    def calculate_energy_emissions(self, country_code, energy_value):
        """Calculate emissions based on electricity consumption."""
        emission = self.api_handler.get_electricity_emissions(country_code, energy_value)
        return emission

    def calculate_flight_emissions(self, departure_airport, destination_airport, passengers):
        """Calculate emissions based on flight details."""
        emission = self.api_handler.get_flight_emissions(departure_airport, destination_airport, passengers)
        return emission