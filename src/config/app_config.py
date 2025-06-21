"""
Configuration management for the weather dashboard application.

This module handles loading and saving application settings, environment variables,
and configuration constants.
"""

import json
import os
from typing import Dict, Any, Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration constants
DEFAULT_CITY = "Seattle, US"
DEFAULT_THEME = "darkly"
SETTINGS_FILE = "settings.json"

# API Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")

# Application settings
APP_CONFIG = {
    "title": "🌦️ Complete Weather Dashboard",
    "min_size": (1000, 700),
    "default_size": (1200, 800),
    "update_interval": 30000,  # 30 seconds
}

# API Rate limits and features (Student Pack)
STUDENT_PACK_INFO = {
    'plan': 'Free Tier with Student Pack Benefits',
    'pricing': 'Free Educational License',
    'rate_limits': {
        'calls_per_minute': 60,
        'calls_per_month': 1000000,
        'historical_per_day': 'Unlimited (Student Pack)'
    },
    'features': [
        'Current weather data',
        '5-day/3-hour forecasts',
        'Air pollution monitoring',
        'Interactive weather maps (12 layers)',
        'Advanced geocoding',
        'Machine learning predictions',
        'Extended rate limits for learning',
        'Full historical data archive',
        'Advanced analytics capabilities',
        'Statistical weather data access'
    ]
}


class ConfigManager:
    """Manages application configuration and settings."""
    
    def __init__(self, settings_file: str = SETTINGS_FILE):
        """Initialize the configuration manager."""
        self.settings_file = settings_file
        self._settings = self.load_settings()
    
    def load_settings(self) -> Dict[str, Any]:
        """Load application settings from file."""
        try:
            with open(self.settings_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {"city": DEFAULT_CITY, "theme": DEFAULT_THEME}
    
    def save_settings(self, city: Optional[str] = None, theme: Optional[str] = None) -> None:
        """Save application settings to file."""
        if city is not None:
            self._settings["city"] = city
        if theme is not None:
            self._settings["theme"] = theme
        
        try:
            with open(self.settings_file, "w", encoding="utf-8") as f:
                json.dump(self._settings, f, indent=2)
        except Exception as e:
            print(f"Error saving settings: {e}")
    
    @property
    def current_city(self) -> str:
        """Get the current city setting."""
        return self._settings.get("city", DEFAULT_CITY)
    
    @property
    def current_theme(self) -> str:
        """Get the current theme setting."""
        return self._settings.get("theme", DEFAULT_THEME)
    
    @property
    def api_key(self) -> str:
        """Get the API key from environment."""
        return API_KEY
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get a specific setting value."""
        return self._settings.get(key, default)
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set a specific setting value."""
        self._settings[key] = value
        self.save_settings()


# Global configuration instance
config = ConfigManager()
