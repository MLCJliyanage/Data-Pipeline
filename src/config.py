"""
Configuration settings for the data pipeline
"""

# Cities to collect data for
CITIES = [
    "London", "New York", "Tokyo", "Sydney", "Rio de Janeiro", 
    "Moscow", "Dubai", "Paris", "Berlin", "Mumbai"
]

# API configuration
API_CONFIG = {
    "base_url": "http://api.openweathermap.org/data/2.5/weather",
    "units": "metric"
}

# Database configuration
DB_CONFIG = {
    "host": "localhost",  # Override with environment variables
    "port": "5432",
    "dbname": "weather_data",
    "table": "weather_data"
}

# Pipeline settings
PIPELINE_CONFIG = {
    "schedule_interval": "1h",  # Run every hour
    "retry_attempts": 3,
    "retry_delay": 300  # 5 minutes
}

# Logging configuration
LOG_CONFIG = {
    "level": "INFO",
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "retention_days": 7
}