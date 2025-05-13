import pandas as pd
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='logs/transform.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('transform')

def transform_weather_data(data):
    """
    Transform raw weather data into a structured format
    """
    transformed_data = []
    
    for item in data:
        try:
            transformed_item = {
                'city_id': item['id'],
                'city_name': item['name'],
                'country': item['sys']['country'],
                'latitude': item['coord']['lat'],
                'longitude': item['coord']['lon'],
                'temperature': item['main']['temp'],
                'feels_like': item['main']['feels_like'],
                'humidity': item['main']['humidity'],
                'pressure': item['main']['pressure'],
                'wind_speed': item['wind']['speed'],
                'wind_direction': item['wind'].get('deg', None),
                'cloudiness': item['clouds']['all'],
                'weather_main': item['weather'][0]['main'],
                'weather_description': item['weather'][0]['description'],
                'weather_icon': item['weather'][0]['icon'],
                'sunrise': datetime.fromtimestamp(item['sys']['sunrise']).isoformat(),
                'sunset': datetime.fromtimestamp(item['sys']['sunset']).isoformat(),
                'timezone': item['timezone'],
                'extraction_timestamp': item['extraction_timestamp']
            }
            transformed_data.append(transformed_item)
            logger.info(f"Successfully transformed data for {item['name']}")
            
        except KeyError as e:
            logger.error(f"Missing key in data: {str(e)}")
        except Exception as e:
            logger.error(f"Error transforming data: {str(e)}")
    
    # Convert to DataFrame
    df = pd.DataFrame(transformed_data)
    
    # Add some derived features
    df['local_time'] = pd.to_datetime(df['extraction_timestamp']) + pd.to_timedelta(df['timezone'], unit='s')
    df['is_day'] = ((pd.to_datetime(df['local_time']).dt.time > pd.to_datetime(df['sunrise']).dt.time) & 
                    (pd.to_datetime(df['local_time']).dt.time < pd.to_datetime(df['sunset']).dt.time))
    
    # Save transformed data
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    os.makedirs('data/processed', exist_ok=True)
    csv_path = f'data/processed/weather_data_{timestamp}.csv'
    df.to_csv(csv_path, index=False)
    
    logger.info(f"Transformed data saved to {csv_path}")
    return df

if __name__ == "__main__":
    # For testing purposes, load the latest raw data file
    import json
    raw_files = sorted(os.listdir('data/raw'))
    if raw_files:
        latest_file = raw_files[-1]
        with open(f'data/raw/{latest_file}', 'r') as f:
            data = json.load(f)
        transform_weather_data(data)