from src.calculator import CarbonCalculator

def main():
    calculator = CarbonCalculator()

    print("\n🌍 Carbon Footprint Calculator:")
    print("Choose carbon tracking type:")
    print("1. Vehicle Travel")
    print("2. Flight")
    
    choice = input("Enter 1 or 2: ").strip()
    
    if choice == "1":
        # Vehicle emissions tracking (no display of available makes)
        vehicle_make = input("\nEnter vehicle make (e.g., Toyota, Ford, BMW): ").strip()
        available_makes = calculator.api_handler.get_vehicle_makes()
        make_id = next((make["id"] for make in available_makes if make["name"].lower() == vehicle_make.lower()), None)

        if make_id:
            available_models = calculator.api_handler.get_vehicle_models(make_id)
            if available_models:
                # No listing of available models, just directly asking for model input
                vehicle_model = input("\nEnter vehicle model: ").strip()
                distance_km = float(input("Enter distance traveled (in km): "))

                travel_emissions = calculator.calculate_travel_emissions(vehicle_make, vehicle_model, distance_km)
                print(f"Estimated travel emissions: {travel_emissions} kg CO2")
            else:
                print("⚠️ No models found for this make.")
                return  # Exit if no models are found
        else:
            print(f"⚠️ Error: Vehicle make '{vehicle_make}' not found.")
            return  # Exit if the make is invalid

    elif choice == "2":
        # Flight emissions tracking
        departure_airport = input("\nEnter departure airport IATA code (e.g., SFO, JFK): ").strip().upper()
        destination_airport = input("Enter destination airport IATA code (e.g., LHR, DXB): ").strip().upper()
        passengers = int(input("Enter number of passengers: "))
        
        flight_emissions = calculator.calculate_flight_emissions(departure_airport, destination_airport, passengers)
        print(f"Estimated flight emissions: {flight_emissions} kg CO2")

    else:
        print("⚠️ Invalid choice. Please enter 1 or 2.")

if __name__ == "__main__":
    main()