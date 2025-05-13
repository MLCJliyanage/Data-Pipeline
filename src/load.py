import pandas as pd
import os
import logging
from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, Boolean, MetaData, Table
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
from datetime import datetime

# Setup logging
logging.basicConfig(
    filename='logs/load.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('load')

# Load environment variables
load_dotenv()
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'weather_data')

# Database connection
def get_engine():
    """Create database engine connection"""
    connection_string = f"postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    # Alternatively for SQLite:
    # connection_string = "sqlite:///data/weather_data.db"
    return create_engine(connection_string)

# Define database schema
Base = declarative_base()

class WeatherData(Base):
    __tablename__ = 'weather_data'
    
    id = Column(Integer, primary_key=True)
    city_id = Column(Integer)
    city_name = Column(String)
    country = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    temperature = Column(Float)
    feels_like = Column(Float)
    humidity = Column(Integer)
    pressure = Column(Integer)
    wind_speed = Column(Float)
    wind_direction = Column(Float)
    cloudiness = Column(Integer)
    weather_main = Column(String)
    weather_description = Column(String)
    weather_icon = Column(String)
    sunrise = Column(DateTime)
    sunset = Column(DateTime)
    timezone = Column(Integer)
    extraction_timestamp = Column(DateTime)
    local_time = Column(DateTime)
    is_day = Column(Boolean)

def load_data_to_db(df):
    """
    Load transformed data into the database
    """
    try:
        engine = get_engine()
        
        # Create table if it doesn't exist
        Base.metadata.create_all(engine)
        
        # Convert datetime columns to proper format
        datetime_cols = ['extraction_timestamp', 'sunrise', 'sunset', 'local_time']
        for col in datetime_cols:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col])
        
        # Load data to database
        df.to_sql('weather_data', engine, if_exists='append', index=False)
        
        logger.info(f"Successfully loaded {len(df)} records to database")
        return True
        
    except Exception as e:
        logger.error(f"Error loading data to database: {str(e)}")
        return False

if __name__ == "__main__":
    # For testing, load the latest processed file
    processed_files = sorted(os.listdir('data/processed'))
    if processed_files:
        latest_file = processed_files[-1]
        df = pd.read_csv(f'data/processed/{latest_file}')
        load_data_to_db(df)