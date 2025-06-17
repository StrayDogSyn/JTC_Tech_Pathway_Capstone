"""
Configuration module for managing environment variables and API settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings."""
    
    # OpenWeatherMap API configuration
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"
    
    # Default settings
    DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'New York')
    TEMPERATURE_UNITS = os.getenv('TEMPERATURE_UNITS', 'metric')
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present."""
        if not cls.OPENWEATHER_API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
        return True
