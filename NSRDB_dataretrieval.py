import os  # To access environment variables
import requests
import numpy as np
import pandas as pd
from io import StringIO
import dotenv

# Function to fetch solar and temperature data from NSRDB
def fetch_solar_data(latitude, longitude, api_key, year=2023):
    """
    Fetch GHI, DNI, DHI, and temperature data from NSRDB API for a given location.
    """
    url = "https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv"
    params = {
        'api_key': api_key,
        'wkt': f"POINT({longitude} {latitude})",
        'attributes': 'ghi,dni,dhi,air_temperature',  # Include temperature data
        'names': year,
        'leap_day': 'false',
        'interval': '60',
        'utc': 'false',
        'email': 'giulia.tala@mail.polimi.it',   
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = pd.read_csv(StringIO(response.text), skiprows=2)
        return data
    else:
        raise Exception(f"Error fetching data: {response.status_code} - {response.text}")

# Function to calculate optimal tilt angle
def calculate_optimal_tilt(latitude):
    """
    Calculate the optimal tilt angle for maximum yearly production.
    """
    return abs(latitude) * 0.76 + 3.1  # Empirical formula for optimal tilt

# Function to calculate irradiance on a tilted plane considering temperature
def calculate_tilted_irradiance(data, tilt_angle, latitude):
    """
    Calculate the irradiance on a tilted plane using a simple transposition model.
    Includes temperature for potential adjustments.
    """
    ghi = data['GHI']  # Global Horizontal Irradiance
    dhi = data['DHI']  # Diffuse Horizontal Irradiance
    dni = data['DNI']  # Direct Normal Irradiance
    temperature = data['Temperature']  # Ambient temperature (Celsius) - updated to match the correct column name
    
    # Solar zenith angle approximation (simplified)
    solar_declination = 23.45 * np.sin(np.radians(360 * (284 + data.index.dayofyear) / 365))
    hour_angle = (data.index.hour - 12) * 15
    solar_zenith_angle = np.degrees(np.arccos(np.cos(np.radians(latitude)) *
                                              np.cos(np.radians(solar_declination)) *
                                              np.cos(np.radians(hour_angle)) +
                                              np.sin(np.radians(latitude)) *
                                              np.sin(np.radians(solar_declination))))
    
    # Angle of incidence on tilted plane
    tilt_radians = np.radians(tilt_angle)
    solar_zenith_radians = np.radians(solar_zenith_angle)
    cos_incidence_angle = np.cos(solar_zenith_radians) * np.cos(tilt_radians) + \
                          np.sin(solar_zenith_radians) * np.sin(tilt_radians)
    cos_incidence_angle = np.clip(cos_incidence_angle, 0, 1)  # Ensure non-negative

    # Calculate tilted irradiance
    beam_tilted = dni * cos_incidence_angle
    diffuse_tilted = dhi * (1 + np.cos(tilt_radians)) / 2
    ground_reflected = ghi * 0.2 * (1 - np.cos(tilt_radians)) / 2
    total_tilted = beam_tilted + diffuse_tilted + ground_reflected

    # Temperature Adjustment (simple example):
    # As temperature increases, PV efficiency tends to decrease. This is an empirical relationship.
    # A simple temperature coefficient of -0.0045 per degree Celsius can be used.
    temperature_coefficient = -0.0045
    temperature_effect = 1 + temperature * temperature_coefficient

    # Apply temperature adjustment (if temperature is provided)
    adjusted_tilted_irradiance = total_tilted * temperature_effect

    return adjusted_tilted_irradiance

# Main script
if __name__ == "__main__":
    # Load environment variables from the .env file
    dotenv.load_dotenv()

    # Fetch the API key from environment variable
    API_KEY = os.getenv('API_KEY')  # Fetch the API key from the environment variable
    
    if not API_KEY:
        raise Exception("API Key is missing. Please set the 'API_KEY' environment variable.")
    
    latitude = 40.7128  # Example: New York City
    longitude = -74.0060
    year = 2019

    # Fetch solar data (including temperature)
    try:
        solar_data = fetch_solar_data(latitude, longitude, API_KEY, year)
        print(solar_data.columns)  # Print columns to confirm correct data

        # Ensure numeric conversion for time columns
        solar_data['Year'] = pd.to_numeric(solar_data['Year'], errors='coerce')
        solar_data['Month'] = pd.to_numeric(solar_data['Month'], errors='coerce')
        solar_data['Day'] = pd.to_numeric(solar_data['Day'], errors='coerce')
        solar_data['Hour'] = pd.to_numeric(solar_data['Hour'], errors='coerce')

        solar_data['time'] = pd.to_datetime(solar_data['Year'].astype(str) + '-' + 
                                             solar_data['Month'].astype(str) + '-' + 
                                             solar_data['Day'].astype(str) + ' ' + 
                                             solar_data['Hour'].astype(str) + ':00', errors='coerce')
        
        solar_data.set_index('time', inplace=True)

        # Ensure GHI, DHI, DNI, and temperature are numeric
        solar_data['GHI'] = pd.to_numeric(solar_data['GHI'], errors='coerce')
        solar_data['DHI'] = pd.to_numeric(solar_data['DHI'], errors='coerce')
        solar_data['DNI'] = pd.to_numeric(solar_data['DNI'], errors='coerce')
        solar_data['Temperature'] = pd.to_numeric(solar_data['Temperature'], errors='coerce')  # Use correct column name

        # Calculate optimal tilt angle
        optimal_tilt = calculate_optimal_tilt(latitude)

        # Calculate tilted plane irradiance with temperature effect
        tilted_irradiance = calculate_tilted_irradiance(solar_data, optimal_tilt, latitude)
        solar_data['Tilted Irradiance (Adjusted)'] = tilted_irradiance

        # Save to CSV
        solar_data.to_csv("solar_data_with_temperature_adjusted_irradiance.csv")
        print(f"Data saved to solar_data_with_temperature_adjusted_irradiance.csv")
    except Exception as e:
        print(f"Error: {e}")
