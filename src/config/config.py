"""
Enhanced configuration management for the weather dashboard application.

This module provides a modern, type-safe configuration system with validation,
environment variable support, and proper error handling.
"""

import json
import os
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict, field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


@dataclass
class APIConfiguration:
    """API configuration settings."""
    api_key: str = field(default_factory=lambda: os.getenv("OPENWEATHER_API_KEY", ""))
    base_url: str = "https://api.openweathermap.org/data/2.5"
    forecast_url: str = "https://api.openweathermap.org/data/2.5/forecast"
    geocoding_url: str = "https://api.openweathermap.org/geo/1.0"
    air_pollution_url: str = "https://api.openweathermap.org/data/2.5/air_pollution"
    timeout: int = 10
    max_retries: int = 3
    rate_limit_per_minute: int = 60
    rate_limit_per_month: int = 1000000


@dataclass
class UIConfiguration:
    """UI configuration settings."""
    theme: str = "darkly"
    window_title: str = "🌦️ Advanced Weather Intelligence Platform"
    min_size: tuple = (1000, 700)
    default_size: tuple = (1200, 800)
    max_size: tuple = (1920, 1080)
    update_interval: int = 30000  # milliseconds
    enable_animations: bool = True
    enable_sound: bool = False
    auto_save_position: bool = True


@dataclass
class DataConfiguration:
    """Data management configuration."""
    cache_enabled: bool = True
    cache_duration: int = 300  # seconds
    auto_refresh: bool = False
    auto_refresh_interval: int = 300  # seconds
    max_history_entries: int = 1000
    export_format: str = "json"  # json, csv, xml
    data_validation: bool = True
    backup_enabled: bool = True


@dataclass
class LoggingConfiguration:
    """Logging configuration settings."""
    log_level: str = "INFO"
    log_to_file: bool = True
    log_to_console: bool = True
    max_log_size: int = 10  # MB
    log_retention_days: int = 30
    performance_logging: bool = True
    api_logging: bool = True
    ui_logging: bool = False


@dataclass
class ApplicationConfiguration:
    """Main application configuration."""
    api: APIConfiguration = field(default_factory=APIConfiguration)
    ui: UIConfiguration = field(default_factory=UIConfiguration)
    data: DataConfiguration = field(default_factory=DataConfiguration)
    logging: LoggingConfiguration = field(default_factory=LoggingConfiguration)
    
    # User preferences
    default_city: str = "Seattle, US"
    favorite_cities: list = field(default_factory=list)
    temperature_unit: str = "C"  # C or F
    wind_speed_unit: str = "km/h"  # km/h, mph, m/s
    pressure_unit: str = "hPa"  # hPa, inHg, mmHg
    
    # Advanced settings
    enable_ml_predictions: bool = False
    enable_weather_alerts: bool = True
    enable_location_services: bool = False
    privacy_mode: bool = False


class ConfigurationManager:
    """Professional configuration management system."""
    
    def __init__(self, config_file: str = "settings.json"):
        """Initialize the configuration manager."""
        self.config_file = Path(config_file)
        self.config = ApplicationConfiguration()
        self._load_configuration()
        self._validate_configuration()
    
    def _load_configuration(self) -> None:
        """Load configuration from file and environment variables."""
        try:
            # Load from environment variables first
            self._load_from_environment()
            
            # Load from file if it exists
            if self.config_file.exists():
                self._load_from_file()
            else:
                print(f"Configuration file {self.config_file} not found, using defaults")
                self.save_configuration()  # Create default config file
            
        except Exception as e:
            print(f"Error loading configuration: {e}")
            print("Using default configuration")
    
    def _load_from_environment(self) -> None:
        """Load configuration from environment variables."""
        # Override settings from environment if provided
        theme = os.getenv("WEATHER_THEME")
        if theme:
            self.config.ui.theme = theme
        
        default_city = os.getenv("WEATHER_DEFAULT_CITY")
        if default_city:
            self.config.default_city = default_city
        
        log_level = os.getenv("WEATHER_LOG_LEVEL")
        if log_level:
            self.config.logging.log_level = log_level.upper()
    
    def _load_from_file(self) -> None:
        """Load configuration from JSON file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update configuration with loaded data
            self._update_config_from_dict(data)
            print(f"Configuration loaded from {self.config_file}")
            
        except (json.JSONDecodeError, FileNotFoundError) as e:
            print(f"Error loading configuration file: {e}")
            raise
    
    def _update_config_from_dict(self, data: Dict[str, Any]) -> None:
        """Update configuration from dictionary data."""
        if "api" in data:
            for key, value in data["api"].items():
                if hasattr(self.config.api, key):
                    setattr(self.config.api, key, value)
        
        if "ui" in data:
            for key, value in data["ui"].items():
                if hasattr(self.config.ui, key):
                    setattr(self.config.ui, key, value)
        
        if "data" in data:
            for key, value in data["data"].items():
                if hasattr(self.config.data, key):
                    setattr(self.config.data, key, value)
        
        if "logging" in data:
            for key, value in data["logging"].items():
                if hasattr(self.config.logging, key):
                    setattr(self.config.logging, key, value)
        
        # Direct properties
        for key in ["default_city", "favorite_cities", "temperature_unit", 
                   "wind_speed_unit", "pressure_unit", "enable_ml_predictions",
                   "enable_weather_alerts", "enable_location_services", "privacy_mode"]:
            if key in data:
                setattr(self.config, key, data[key])
    
    def _validate_configuration(self) -> None:
        """Validate configuration values."""
        errors = []
        
        # Validate API configuration
        if not self.config.api.api_key:
            errors.append("API key is not configured")
        
        if self.config.api.timeout < 1 or self.config.api.timeout > 60:
            errors.append("API timeout must be between 1 and 60 seconds")
        
        # Validate UI configuration
        valid_themes = ["darkly", "flatly", "litera", "minty", "lumen", "sandstone", "superhero", "vapor"]
        if self.config.ui.theme not in valid_themes:
            print(f"Invalid theme '{self.config.ui.theme}', using default")
            self.config.ui.theme = "darkly"
        
        # Validate units
        if self.config.temperature_unit not in ["C", "F"]:
            errors.append("Temperature unit must be 'C' or 'F'")
        
        if self.config.wind_speed_unit not in ["km/h", "mph", "m/s"]:
            errors.append("Wind speed unit must be 'km/h', 'mph', or 'm/s'")
        
        if self.config.pressure_unit not in ["hPa", "inHg", "mmHg"]:
            errors.append("Pressure unit must be 'hPa', 'inHg', or 'mmHg'")
        
        # Validate logging configuration
        valid_log_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if self.config.logging.log_level not in valid_log_levels:
            print(f"Invalid log level '{self.config.logging.log_level}', using INFO")
            self.config.logging.log_level = "INFO"
        
        if errors:
            print(f"Configuration validation errors: {'; '.join(errors)}")
    
    def save_configuration(self) -> None:
        """Save current configuration to file."""
        try:
            # Convert to dictionary
            config_dict = {
                "api": asdict(self.config.api),
                "ui": asdict(self.config.ui),
                "data": asdict(self.config.data),
                "logging": asdict(self.config.logging),
                "default_city": self.config.default_city,
                "favorite_cities": self.config.favorite_cities,
                "temperature_unit": self.config.temperature_unit,
                "wind_speed_unit": self.config.wind_speed_unit,
                "pressure_unit": self.config.pressure_unit,
                "enable_ml_predictions": self.config.enable_ml_predictions,
                "enable_weather_alerts": self.config.enable_weather_alerts,
                "enable_location_services": self.config.enable_location_services,
                "privacy_mode": self.config.privacy_mode
            }
            
            # Don't save sensitive information to file
            config_dict["api"]["api_key"] = ""
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config_dict, f, indent=2, ensure_ascii=False)
            
            print(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            print(f"Error saving configuration: {e}")
    
    def update_setting(self, category: str, key: str, value: Any) -> bool:
        """Update a specific setting."""
        try:
            if category == "api" and hasattr(self.config.api, key):
                setattr(self.config.api, key, value)
            elif category == "ui" and hasattr(self.config.ui, key):
                setattr(self.config.ui, key, value)
            elif category == "data" and hasattr(self.config.data, key):
                setattr(self.config.data, key, value)
            elif category == "logging" and hasattr(self.config.logging, key):
                setattr(self.config.logging, key, value)
            elif hasattr(self.config, key):
                setattr(self.config, key, value)
            else:
                print(f"Invalid setting: {category}.{key}")
                return False
            
            self._validate_configuration()
            self.save_configuration()
            print(f"Setting updated: {category}.{key} = {value}")
            return True
            
        except Exception as e:
            print(f"Error updating setting {category}.{key}: {e}")
            return False
    
    # Convenience properties for backward compatibility
    @property
    def api_key(self) -> str:
        """Get the API key."""
        return self.config.api.api_key
    
    @property
    def current_city(self) -> str:
        """Get the current default city."""
        return self.config.default_city
    
    @property
    def current_theme(self) -> str:
        """Get the current theme."""
        return self.config.ui.theme
    
    def save_settings(self, **kwargs: Any) -> None:
        """Save settings (backward compatibility method)."""
        if "city" in kwargs:
            self.config.default_city = kwargs["city"]
        if "theme" in kwargs:
            self.config.ui.theme = kwargs["theme"]
        if "api_key" in kwargs:
            self.config.api.api_key = kwargs["api_key"]
        
        self.save_configuration()


# Global configuration instance
config_manager = ConfigurationManager()

# Backward compatibility aliases
config = config_manager
APP_CONFIG = {
    "title": config_manager.config.ui.window_title,
    "min_size": config_manager.config.ui.min_size,
    "default_size": config_manager.config.ui.default_size,
    "update_interval": config_manager.config.ui.update_interval,
}

# API information for UI display
API_INFO = {
    'subscription_type': 'OpenWeatherMap Student Pack',
    'rate_limits': {
        'per_minute': config_manager.config.api.rate_limit_per_minute,
        'per_month': config_manager.config.api.rate_limit_per_month
    },
    'features': [
        'Current weather data for any location',
        '5-day weather forecasts',
        'Air quality monitoring',
        'Interactive weather maps (12 layers)',
        'Advanced geocoding',
        'Machine learning predictions',
        'Extended rate limits for learning',
        'Full historical data archive',
        'Advanced analytics capabilities',
        'Statistical weather data access'
    ]
}


# Configuration validation functions
def validate_api_key(api_key: str) -> bool:
    """Validate API key format."""
    return bool(api_key and len(api_key) >= 32 and api_key.replace('-', '').replace('_', '').isalnum())


def validate_coordinates(lat: float, lon: float) -> bool:
    """Validate latitude and longitude coordinates."""
    return -90 <= lat <= 90 and -180 <= lon <= 180


def validate_city_name(city: str) -> bool:
    """Validate city name format."""
    return bool(city and len(city.strip()) >= 2 and not city.isdigit())


# Environment setup helper
def setup_environment() -> None:
    """Set up the application environment."""
    # Create necessary directories
    directories = ["logs", "cache", "exports", "backups"]
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
    
    print("Application environment initialized")


if __name__ == "__main__":
    # Test configuration system
    print("Configuration Test:")
    print(f"API Key configured: {bool(config_manager.api_key)}")
    print(f"Current theme: {config_manager.current_theme}")
    print(f"Default city: {config_manager.current_city}")
    print(f"Log level: {config_manager.config.logging.log_level}")
