"""
Core business logic for the weather dashboard application.

This module contains the main application logic, coordinating between
different services and managing the application state.
"""

import threading
from typing import Optional, Dict, Any, Callable
from datetime import datetime

from src.utils.logging import get_logger, get_api_logger, performance_timer, log_weather_data_update
from src.utils.logging import log_function_call

try:
    # Try relative imports first (when run as module)
    from ..models.weather_models import WeatherData, ForecastData, LocationData, AirQualityData
    from ..services.weather_api import WeatherAPIService
    from ..config.config import config_manager
except ImportError:
    # Fall back to absolute imports (when run directly or from verification)
    from src.models.weather_models import WeatherData, ForecastData, LocationData, AirQualityData
    from src.services.weather_api import WeatherAPIService
    from src.config.config import config_manager

# Initialize loggers
logger = get_logger()
api_logger = get_api_logger()


class WeatherDashboardCore:
    """Core business logic for the weather dashboard."""
    
    def __init__(self):
        """Initialize the weather dashboard core."""
        logger.info("Initializing Weather Dashboard Core")
        
        self.api_service = WeatherAPIService(config_manager.config)
        self.current_weather: Optional[WeatherData] = None
        self.forecast_data: Optional[ForecastData] = None
        self.air_quality_data: Optional[AirQualityData] = None
        self.current_location: Optional[LocationData] = None
        
        # Callbacks for UI updates
        self._status_callback: Optional[Callable[[str], None]] = None
        self._data_update_callback: Optional[Callable[[], None]] = None
        
        logger.info("Weather Dashboard Core initialized successfully")
        
    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for status updates."""
        self._status_callback = callback
    
    def set_data_update_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for data updates."""
        self._data_update_callback = callback
    
    def _update_status(self, message: str) -> None:
        """Update status through callback."""
        if self._status_callback:
            self._status_callback(message)
    
    def _notify_data_update(self) -> None:
        """Notify UI of data updates through callback."""
        if self._data_update_callback:
            self._data_update_callback()
    
    def load_weather_data(self, city: str) -> None:
        """Load weather data for the specified city asynchronously."""
        if not city.strip():
            self._update_status("❌ Please enter a city name")
            return
          # Save city to settings
        config_manager.save_settings(city=city)
        
        def task():
            try:
                self._update_status("🔄 Loading weather data...")
                
                # Geocode city
                locations = self.api_service.geocode_location(city, limit=1)
                if not locations:
                    self._update_status("❌ Location not found")
                    return
                
                location = locations[0]
                self.current_location = LocationData.from_api_response(location)
                
                # Fetch all weather data
                lat, lon = self.current_location.lat, self.current_location.lon
                  # Get current weather
                weather_response = self.api_service.get_current_weather(lat, lon)
                if weather_response:
                    self.current_weather = WeatherData.from_api_response(weather_response)
                
                # Get forecast data
                forecast_response = self.api_service.get_extended_forecast(lat, lon)
                if forecast_response and 'list' in forecast_response:
                    self.forecast_data = ForecastData.from_api_response(forecast_response['list'])
                
                # Get air quality data
                air_quality_response = self.api_service.get_air_pollution(lat, lon)
                if air_quality_response:
                    self.air_quality_data = AirQualityData.from_api_response(air_quality_response)
                
                # Notify UI of successful data update
                self._notify_data_update()
                self._update_status(f"✅ Weather loaded for {self.current_location.display_name}")
                
            except Exception as e:
                self._update_status(f"❌ Error loading weather data: {str(e)}")
        
        # Run in background thread
        threading.Thread(target=task, daemon=True).start()
    
    def get_location_display_name(self) -> str:
        """Get the display name for the current location."""
        if not self.current_location:
            return "Unknown Location"
        return self.current_location.display_name
    
    def has_weather_data(self) -> bool:
        """Check if weather data is available."""
        return self.current_weather is not None
    
    def has_forecast_data(self) -> bool:
        """Check if forecast data is available."""
        return self.forecast_data is not None and bool(self.forecast_data.hourly)
    
    def has_air_quality_data(self) -> bool:
        """Check if air quality data is available."""
        return self.air_quality_data is not None
    
    def get_weather_summary(self) -> Dict[str, Any]:
        """Get a summary of current weather data."""
        if not self.current_weather:
            return {}
        
        return {
            "temperature": self.current_weather.temperature,
            "feels_like": self.current_weather.feels_like,
            "description": self.current_weather.description,
            "humidity": self.current_weather.humidity,
            "pressure": self.current_weather.pressure,            "wind_speed": self.current_weather.wind_speed,
            "cloudiness": self.current_weather.cloudiness,
            "location": self.get_location_display_name(),
            "timestamp": self.current_weather.timestamp
        }
    
    def get_api_info(self) -> Dict[str, Any]:
        """Get API subscription information."""
        return {
            "subscription": self.api_service.get_subscription_info(),
            "api_key_configured": bool(config_manager.api_key),
            "api_key_preview": f"{config_manager.api_key[:10]}..." if config_manager.api_key else "Not configured"
        }
