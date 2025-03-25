# Carbon Emission Tracker

## Overview
The **Carbon Emission Tracker** is a Python-based application that allows users to estimate and track their personal carbon footprint. This project integrates third-party APIs to fetch emissions factors, store historical data, and provide actionable recommendations to reduce environmental impact.

## Features
- **User Input:** Users enter data related to travel, energy usage, and consumption habits.
- **Carbon Footprint Calculation:** Uses APIs to fetch emission factors and compute estimated emissions.
- **Visualization:** Generates charts and reports on emission trends.
- **Recommendations:** Provides tailored advice on how users can reduce their carbon footprint.

## API Integration
To showcase API-handling skills, the project integrates:
- **Carbon Intensity API** (e.g., [Carbon Interface API](https://www.carboninterface.com/) or [Electricity Maps API](https://www.electricitymaps.com/)) for emissions calculations.

## Project Structure
```
carbon-emission-tracker/
├── src/                  # Source code
│   ├── api_handler.py    # Handles API calls
│   ├── calculator.py     # Calculates carbon footprint
│   ├── visualizer.py     # Creates graphs/charts
│   ├── recommender.py    # Provides reduction suggestions
├── requirements.txt      # Lists dependencies
├── .gitignore            # Ignores unnecessary files like __pycache__ and .env
├── README.md             # Project overview, setup guide, API usage details
├── config.py             # Stores API keys, loads them from .env file
├── main.py               # Entry point for CLI-based interaction, later extendable to GUI/Web
```

## Installation & Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Kianjn/carbon-emission-tracker.git
   ```
2. Navigate to the project folder:
   ```bash
   cd carbon-emission-tracker
   ```
3. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Set up API keys:
   - Create a `.env` file in the root directory.
   - Add API keys like this:
     ```
     CARBON_API_KEY=your_api_key_here
     GOOGLE_MAPS_API_KEY=your_api_key_here
     ```

## Usage
Run the application:
```bash
python main.py
```
Follow the prompts to enter your data and get real-time feedback on your carbon emissions.
