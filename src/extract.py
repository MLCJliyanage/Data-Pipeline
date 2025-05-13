import requests
import json
import os
import logging
from datetime import datetime
from dotenv import load_dotenv

# Setup logging
logging.basicConfig(
    filename='logs/extract.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('extract')

# Load environment variables
load_dotenv()
API_KEY = os.getenv('WEATHER_API_KEY')

def extract_weather_data(cities):
    """
    Extract weather data for a list of cities
    """
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    
    all_data = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for city in cities:
        try:
            params = {
                'q': city,
                'appid': API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise exception for HTTP errors
            
            data = response.json()
            data['extraction_timestamp'] = datetime.now().isoformat()
            all_data.append(data)
            
            logger.info(f"Successfully extracted data for {city}")
            
        except Exception as e:
            logger.error(f"Error extracting data for {city}: {str(e)}")
    
    # Save raw data to file
    os.makedirs('data/raw', exist_ok=True)
    with open(f'data/raw/weather_data_{timestamp}.json', 'w') as f:
        json.dump(all_data, f)
    
    logger.info(f"Extracted data for {len(all_data)} cities")
    return all_data

if __name__ == "__main__":
    cities = ["London", "New York", "Tokyo", "Sydney", "Rio de Janeiro"]
    extract_weather_data(cities)