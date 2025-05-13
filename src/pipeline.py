import logging
import os
from datetime import datetime
from src.extract import extract_weather_data
from src.transform import transform_weather_data
from src.load import load_data_to_db

# Setup logging
os.makedirs('logs', exist_ok=True)
logging.basicConfig(
    filename=f'logs/pipeline_{datetime.now().strftime("%Y%m%d")}.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('pipeline')

def run_pipeline(cities=None):
    """
    Run the complete ETL pipeline
    """
    if cities is None:
        cities = ["London", "New York", "Tokyo", "Sydney", "Rio de Janeiro", 
                 "Moscow", "Dubai", "Paris", "Berlin", "Mumbai"]
    
    try:
        logger.info("Starting data pipeline")
        
        # Extract
        logger.info("Starting extraction phase")
        raw_data = extract_weather_data(cities)
        logger.info(f"Extraction complete - {len(raw_data)} records extracted")
        
        # Transform
        logger.info("Starting transformation phase")
        transformed_data = transform_weather_data(raw_data)
        logger.info(f"Transformation complete - {len(transformed_data)} records transformed")
        
        # Load
        logger.info("Starting loading phase")
        success = load_data_to_db(transformed_data)
        if success:
            logger.info("Data pipeline completed successfully")
        else:
            logger.error("Error in loading phase")
            
        return success
    
    except Exception as e:
        logger.error(f"Error in pipeline: {str(e)}")
        return False

if __name__ == "__main__":
    run_pipeline()