import requests
import pandas as pd
from datetime import datetime, timedelta

def fetch_weather_data(city_name, latitude, longitude, start_date, end_date):
    """
    Fetch historical weather data using Open-Meteo API (free, no API key needed)
    
    Parameters:
    - city_name: Name of the city (for reference)
    - latitude: Latitude of the location
    - longitude: Longitude of the location
    - start_date: Start date in format 'YYYY-MM-DD'
    - end_date: End date in format 'YYYY-MM-DD'
    """
    
    print(f"Fetching weather data for {city_name}...")
    print(f"Period: {start_date} to {end_date}")
    
    # Open-Meteo API endpoint
    url = f'https://archive-api.open-meteo.com/v1/archive'
    
    params = {
        'latitude': latitude,
        'longitude': longitude,
        'start_date': start_date,
        'end_date': end_date,
        'daily': [
            'temperature_2m_max',
            'temperature_2m_min',
            'temperature_2m_mean',
            'precipitation_sum',
            'windspeed_10m_max',
            'windspeed_10m_mean',
            'relative_humidity_2m_mean',
            'pressure_msl_mean'
        ],
        'timezone': 'auto'
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Create DataFrame
        df = pd.DataFrame({
            'date': data['daily']['time'],
            'temperature': data['daily']['temperature_2m_mean'],
            'temp_max': data['daily']['temperature_2m_max'],
            'temp_min': data['daily']['temperature_2m_min'],
            'precipitation': data['daily']['precipitation_sum'],
            'wind_speed': data['daily']['windspeed_10m_mean'],
            'wind_speed_max': data['daily']['windspeed_10m_max'],
            'humidity': data['daily']['relative_humidity_2m_mean'],
            'pressure': data['daily']['pressure_msl_mean']
        })
        
        # Save to CSV
        filename = f'weather_data_{city_name.lower().replace(" ", "_")}_{start_date}_to_{end_date}.csv'
        df.to_csv(filename, index=False)
        
        print(f"\n✅ Success! Data saved to: {filename}")
        print(f"📊 Total records: {len(df)}")
        print(f"\nFirst few rows:")
        print(df.head())
        
        return df
        
    except Exception as e:
        print(f"❌ Error fetching data: {str(e)}")
        return None


def get_coordinates(city_name):
    """Get coordinates for major cities (you can expand this dictionary)"""
    cities = {
        'mumbai': (19.0760, 72.8777),
        'delhi': (28.6139, 77.2090),
        'bangalore': (12.9716, 77.5946),
        'kolkata': (22.5726, 88.3639),
        'chennai': (13.0827, 80.2707),
        'hyderabad': (17.3850, 78.4867),
        'pune': (18.5204, 73.8567),
        'ahmedabad': (23.0225, 72.5714),
        'new york': (40.7128, -74.0060),
        'london': (51.5074, -0.1278),
        'tokyo': (35.6762, 139.6503),
        'paris': (48.8566, 2.3522),
        'sydney': (-33.8688, 151.2093),
        'dubai': (25.2048, 55.2708),
        'singapore': (1.3521, 103.8198),
        'los angeles': (34.0522, -118.2437),
        'san francisco': (37.7749, -122.4194),
        'chicago': (41.8781, -87.6298),
        'boston': (42.3601, -71.0589),
        'seattle': (47.6062, -122.3321)
    }
    
    city_lower = city_name.lower()
    if city_lower in cities:
        return cities[city_lower]
    else:
        print(f"City '{city_name}' not found in database.")
        print("Please provide latitude and longitude manually.")
        return None


# Example usage
if __name__ == "__main__":
    print("=" * 60)
    print("🌤️  WEATHER DATA FETCHER")
    print("=" * 60)
    print()
    
    # Option 1: Use predefined cities
    city = input("Enter city name (e.g., Mumbai, Delhi, New York): ").strip()
    
    coords = get_coordinates(city)
    
    if coords:
        lat, lon = coords
    else:
        # Option 2: Manual coordinates
        lat = float(input("Enter latitude: "))
        lon = float(input("Enter longitude: "))
    
    # Date range
    print("\nEnter date range (YYYY-MM-DD format):")
    start = input("Start date (e.g., 2024-01-01): ").strip()
    end = input("End date (e.g., 2024-12-31): ").strip()
    
    # Fetch data
    df = fetch_weather_data(city, lat, lon, start, end)
    
    if df is not None:
        print("\n" + "=" * 60)
        print("Summary Statistics:")
        print("=" * 60)
        print(df.describe())
        
        print("\n💡 You can now use this CSV file in your Streamlit app!")
        print("   Just upload it in the sidebar.")


# Quick preset functions for common use cases
def fetch_last_year(city_name):
    """Fetch last year's data for a city"""
    coords = get_coordinates(city_name)
    if coords:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
        return fetch_weather_data(city_name, coords[0], coords[1], start_date, end_date)
    return None


def fetch_last_month(city_name):
    """Fetch last month's data for a city"""
    coords = get_coordinates(city_name)
    if coords:
        end_date = datetime.now().strftime('%Y-%m-%d')
        start_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        return fetch_weather_data(city_name, coords[0], coords[1], start_date, end_date)
    return None


# Uncomment to use quick presets:
# df = fetch_last_year('Mumbai')
# df = fetch_last_month('Delhi')