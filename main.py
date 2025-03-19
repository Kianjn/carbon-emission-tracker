from src.calculator import CarbonCalculator

def main():
    calculator = CarbonCalculator()

    print("\n🚗 Travel Carbon Footprint Calculator:")

    # Fetch and display available vehicle makes
    available_makes = calculator.api_handler.get_vehicle_makes()
    if available_makes:
        print("\n✅ Available vehicle makes:")
        for make in available_makes:
            print(f" - {make['name']}")
    else:
        print("⚠️ Unable to fetch vehicle makes. Check your API connection.")
        return  # Exit if we cannot fetch makes

    # Ask the user to choose a make
    vehicle_make = input("\nEnter vehicle make (e.g., Toyota, Ford, BMW): ").strip()

    # Fetch and display available models for the selected make
    make_id = next((make["id"] for make in available_makes if make["name"].lower() == vehicle_make.lower()), None)
    if make_id:
        available_models = calculator.api_handler.get_vehicle_models(make_id)
        if available_models:
            print("\n✅ Available vehicle models:")
            for model in available_models:
                print(f" - {model['name']}")
        else:
            print("⚠️ No models found for this make.")
            return  # Exit if no models are found
    else:
        print(f"⚠️ Error: Vehicle make '{vehicle_make}' not found.")
        return  # Exit if the make is invalid

    # Ask the user to choose a model
    vehicle_model = input("\nEnter vehicle model: ").strip()
    distance_km = float(input("Enter distance traveled (in km): "))

    # Calculate emissions
    travel_emissions = calculator.calculate_travel_emissions(vehicle_make, vehicle_model, distance_km)
    print(f"Estimated travel emissions: {travel_emissions} kg CO2")

if __name__ == "__main__":
    main()