import os
import requests
import numpy as np
import pandas as pd
from datetime import datetime
import h5py
from io import BytesIO
from ftplib import FTP

# Define constants
LATITUDE = 40.7128
LONGITUDE = -74.0060
YEAR = 2023
FTP_SERVER = 'arthurhou.pps.eosdis.nasa.gov'
FTP_DIR = f'/gpm/IMERG/2023/'

# Function to fetch solar data
def fetch_solar_data(latitude, longitude, api_key, year=2020):
    file_name = f"solar_data_with_temperature_adjusted_irradiance_{year}.csv"
    if os.path.exists(file_name):
        data = pd.read_csv(file_name)
        return data
    else:
        url = "https://developer.nrel.gov/api/solar/nsrdb_psm3_download.csv"
        params = {
            'api_key': api_key,
            'wkt': f"POINT({longitude} {latitude})",
            'attributes': 'ghi,air_temperature',
            'names': year,
            'leap_day': 'false',
            'interval': '60',  # Data at 60-minute intervals
            'utc': 'false',  # Local time
            'email': 'your_email@example.com',  # Your email for NREL API usage
        }
        response = requests.get(url, params=params)
        if response.status_code == 200:
            data = pd.read_csv(BytesIO(response.content), skiprows=2)
            data.to_csv(file_name, index=False)
            return data
        else:
            raise Exception(f"Error fetching solar data: {response.status_code} - {response.text}")

# Function to fetch precipitation data from FTP server
def fetch_precipitation_data(year, month, day):
    """
    Download the precipitation data from the NASA FTP server.
    Args:
        year (int): Year of the data to fetch.
        month (int): Month of the data to fetch.
        day (int): Day of the data to fetch.
    """
    # Establish FTP connection
    ftp = FTP(FTP_SERVER)
    ftp.login()

    # Construct file name (adjust this based on file naming convention in the directory)
    filename = f"3B-HHR-L.MS.MRG.3IMERG.{year}{month:02d}{day:02d}-S000000-E235959.0000.V06B.HDF5"

    # Download file
    local_filepath = f"{filename}"
    with open(local_filepath, 'wb') as f:
        ftp.retrbinary(f"RETR {FTP_DIR}{filename}", f.write)
    
    ftp.quit()
    return local_filepath

# Function to process GPM precipitation data (HDF5)
def process_gpm_precipitation_data(file_path):
    """
    Process the downloaded GPM HDF5 precipitation data.
    """
    with h5py.File(file_path, 'r') as f:
        # List available datasets
        print(f.keys())  # This will print the structure of the HDF5 file
        
        # Extract precipitation data (adjust path as per the actual HDF5 structure)
        precip_data = f['precipitationCal'][:]  # Modify if needed
        
        # Create DataFrame from extracted data
        precip_df = pd.DataFrame(precip_data, columns=["Precipitation"])
        
        # Example: Extract timestamp if available
        precip_df['Timestamp'] = pd.to_datetime(f['time'][:], unit='s')  # Adjust as needed
        precip_df.set_index('Timestamp', inplace=True)

        return precip_df

# Function to calculate solar zenith angle
def calculate_solar_zenith_angle(data, latitude):
    """
    Calculate the solar zenith angle using the simplified method.
    """
    # Solar Declination Calculation (simplified)
    solar_declination = 23.45 * np.sin(np.radians(360 * (284 + data.index.dayofyear) / 365))
    hour_angle = (data.index.hour - 12) * 15  # Approximate Hour Angle
    solar_zenith_angle = np.degrees(np.arccos(np.cos(np.radians(latitude)) *
                                              np.cos(np.radians(solar_declination)) *
                                              np.cos(np.radians(hour_angle)) +
                                              np.sin(np.radians(latitude)) *
                                              np.sin(np.radians(solar_declination))))
    return solar_zenith_angle

# Main Script
if __name__ == "__main__":
    """
    Main script execution point. This script checks if a file exists, and if not, it fetches solar data, processes it, 
    calculates the solar zenith angle, fetches precipitation data, merges the data, and saves it to a CSV file.
    """
    try:
        # Check if the file exists
        file_path = "solar_data_with_temperature_adjusted_irradiance.csv"
        if not os.path.exists(file_path):
            # Fetch solar data
            solar_data = fetch_solar_data(LATITUDE, LONGITUDE, 'YOUR_API_KEY', YEAR)

            # Process solar data to prepare the DataFrame
            solar_data['Year'] = pd.to_numeric(solar_data['Year'], errors='coerce')
            solar_data['Month'] = pd.to_numeric(solar_data['Month'], errors='coerce')
            solar_data['Day'] = pd.to_numeric(solar_data['Day'], errors='coerce')
            solar_data['Hour'] = pd.to_numeric(solar_data['Hour'], errors='coerce')

            solar_data['time'] = pd.to_datetime(solar_data['Year'].astype(str) + '-' + 
                                                 solar_data['Month'].astype(str) + '-' + 
                                                 solar_data['Day'].astype(str) + ' ' + 
                                                 solar_data['Hour'].astype(str) + ':00', errors='coerce')

            solar_data.set_index('time', inplace=True)

            # Ensure GHI and Temperature are numeric
            solar_data['GHI'] = pd.to_numeric(solar_data['GHI'], errors='coerce')
            solar_data['Temperature'] = pd.to_numeric(solar_data['Temperature'], errors='coerce')

            # Calculate solar zenith angle
            solar_data['Solar Zenith Angle'] = calculate_solar_zenith_angle(solar_data, LATITUDE)

            # Fetch precipitation data for a specific day
            precip_file_path = fetch_precipitation_data(YEAR, 1, 1)  # Example: Fetch for January 1, 2023
            precip_data = process_gpm_precipitation_data(precip_file_path)

            # Merge precipitation data with solar data
            solar_data = solar_data.join(precip_data['Precipitation'], how='left')

            # Save to CSV
            solar_data.to_csv(file_path)
            print(f"Data saved to {file_path}")
        else:
            print(f"File {file_path} already exists. No new data generated.")

    except Exception as e:
        print(f"Error: {e}")
