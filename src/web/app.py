from flask import Flask, render_template, request, jsonify
from ..calculator import CarbonCalculator
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

app = Flask(__name__)
calculator = CarbonCalculator()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vehicle-makes', methods=['GET'])
def get_vehicle_makes():
    makes = calculator.api_handler.get_vehicle_makes()
    return jsonify(makes)

@app.route('/api/vehicle-models/<make_id>', methods=['GET'])
def get_vehicle_models(make_id):
    models = calculator.api_handler.get_vehicle_models(make_id)
    return jsonify(models)

@app.route('/api/calculate/travel', methods=['POST'])
def calculate_travel():
    try:
        data = request.json
        vehicle_make = data.get('make')
        vehicle_model = data.get('model')
        distance_km = float(data.get('distance'))
        
        if not all([vehicle_make, vehicle_model, distance_km]):
            return jsonify({'error': 'Missing required fields'}), 400

        emissions = calculator.calculate_travel_emissions(vehicle_make, vehicle_model, distance_km)
        if emissions is None:
            return jsonify({'error': 'Failed to calculate emissions'}), 500
            
        return jsonify({'emissions': emissions})
    except Exception as e:
        print(f"Error calculating travel emissions: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/api/calculate/flight', methods=['POST'])
def calculate_flight():
    data = request.json
    departure = data.get('departure')
    destination = data.get('destination')
    passengers = int(data.get('passengers'))
    
    emissions = calculator.calculate_flight_emissions(departure, destination, passengers)
    return jsonify({'emissions': emissions})

@app.route('/api/calculate/electricity', methods=['POST'])
def calculate_electricity():
    data = request.json
    country_code = data.get('country')
    consumption = float(data.get('consumption'))
    
    emissions = calculator.calculate_energy_emissions(country_code, consumption)
    return jsonify({'emissions': emissions})

if __name__ == '__main__':
    app.run(debug=True) 