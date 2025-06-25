"""
Weather Controller for the Weather Dashboard application.

This controller handles all weather-related operations and coordinates between
the weather services and the UI components. It implements the controller part
of the MVC pattern, ensuring separation of concerns.
"""

from typing import Optional, Callable, Dict, Any, List
from datetime import datetime
import threading

from ..models.weather_models import WeatherData, ForecastData, LocationData, AirQualityData
from ..services.weather_api import WeatherAPIService
from ..utils.logging import get_logger, log_weather_data_update
from ..utils.exceptions import WeatherAPIError, ValidationError
from ..config.config import config_manager


logger = get_logger()


class WeatherController:
    """
    Controller for weather operations following MVC pattern.
    
    Responsibilities:
    - Coordinate weather data retrieval and processing
    - Manage weather-related business logic
    - Provide interface between weather services and views
    - Handle weather data validation and transformation
    """
    
    def __init__(self, api_service: Optional[WeatherAPIService] = None):
        """Initialize the weather controller."""
        logger.info("Initializing Weather Controller")
        
        # Services
        self.api_service = api_service or WeatherAPIService(config_manager.config)
        
        # Model state
        self.current_weather: Optional[WeatherData] = None
        self.forecast_data: Optional[ForecastData] = None
        self.air_quality_data: Optional[AirQualityData] = None
        self.current_location: Optional[LocationData] = None
        
        # View callbacks (observers)
        self._weather_update_callbacks: List[Callable[[WeatherData], None]] = []
        self._forecast_update_callbacks: List[Callable[[ForecastData], None]] = []
        self._air_quality_update_callbacks: List[Callable[[AirQualityData], None]] = []
        self._error_callbacks: List[Callable[[str], None]] = []
        self._status_callbacks: List[Callable[[str], None]] = []
        
        logger.info("Weather Controller initialized successfully")
    
    # Observer pattern methods for view updates
    def add_weather_update_observer(self, callback: Callable[[WeatherData], None]) -> None:
        """Add observer for weather data updates."""
        self._weather_update_callbacks.append(callback)
    
    def add_forecast_update_observer(self, callback: Callable[[ForecastData], None]) -> None:
        """Add observer for forecast data updates."""
        self._forecast_update_callbacks.append(callback)
    
    def add_air_quality_update_observer(self, callback: Callable[[AirQualityData], None]) -> None:
        """Add observer for air quality data updates."""
        self._air_quality_update_callbacks.append(callback)
    
    def add_error_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for error notifications."""
        self._error_callbacks.append(callback)
    
    def add_status_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for status updates."""
        self._status_callbacks.append(callback)
    
    # Private notification methods
    def _notify_weather_update(self, weather_data: WeatherData) -> None:
        """Notify all observers of weather data update."""
        for callback in self._weather_update_callbacks:
            try:
                callback(weather_data)
            except Exception as e:
                logger.error(f"Error in weather update callback: {e}")
    
    def _notify_forecast_update(self, forecast_data: ForecastData) -> None:
        """Notify all observers of forecast data update."""
        for callback in self._forecast_update_callbacks:
            try:
                callback(forecast_data)
            except Exception as e:
                logger.error(f"Error in forecast update callback: {e}")
    
    def _notify_air_quality_update(self, air_quality_data: AirQualityData) -> None:
        """Notify all observers of air quality data update."""
        for callback in self._air_quality_update_callbacks:
            try:
                callback(air_quality_data)
            except Exception as e:
                logger.error(f"Error in air quality update callback: {e}")
    
    def _notify_error(self, error_message: str) -> None:
        """Notify all observers of errors."""
        for callback in self._error_callbacks:
            try:
                callback(error_message)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")
    
    def _notify_status(self, status_message: str) -> None:
        """Notify all observers of status updates."""
        for callback in self._status_callbacks:
            try:
                callback(status_message)
            except Exception as e:
                logger.error(f"Error in status callback: {e}")
    
    # Public interface methods
    def load_weather_for_city(self, city_name: str) -> bool:
        """
        Load weather data for a given city.
        
        Args:
            city_name: Name of the city to get weather for
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._notify_status(f"Loading weather data for {city_name}...")
            logger.info(f"Loading weather data for city: {city_name}")
            
            # Get location data first
            location_data = self._get_location_data(city_name)
            if not location_data:
                self._notify_error(f"Could not find location: {city_name}")
                return False
            
            self.current_location = location_data
            
            # Load all weather data
            self._load_all_weather_data(location_data.lat, location_data.lon)
            
            # Save the city as current
            config_manager.save_settings(city=city_name)
            
            self._notify_status(f"Weather data loaded successfully for {city_name}")
            return True
            
        except Exception as e:
            error_msg = f"Failed to load weather data for {city_name}: {str(e)}"
            logger.error(error_msg)
            self._notify_error(error_msg)
            return False
    
    def load_weather_for_coordinates(self, lat: float, lon: float) -> bool:
        """
        Load weather data for given coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self._notify_status(f"Loading weather data for coordinates {lat}, {lon}...")
            logger.info(f"Loading weather data for coordinates: {lat}, {lon}")
            
            self._load_all_weather_data(lat, lon)
            
            self._notify_status("Weather data loaded successfully")
            return True
            
        except Exception as e:
            error_msg = f"Failed to load weather data for coordinates: {str(e)}"
            logger.error(error_msg)
            self._notify_error(error_msg)
            return False
    
    def refresh_weather_data(self) -> bool:
        """Refresh current weather data."""
        if not self.current_location:
            self._notify_error("No location set for refresh")
            return False
        
        return self.load_weather_for_coordinates(
            self.current_location.lat, 
            self.current_location.lon
        )
    
    # Private helper methods
    def _get_location_data(self, city_name: str) -> Optional[LocationData]:
        """Get location data from city name or handle GPS requests."""
        try:
            # Handle GPS/Current Location requests
            if city_name in ["Current Location (GPS)", "Current Location"]:
                self._notify_status("Detecting your location...")
                return self._get_current_location_data()
            
            location_response = self.api_service.geocode_location(city_name, limit=1)
            if location_response:
                return LocationData.from_api_response(location_response[0])
            return None
        except Exception as e:
            logger.error(f"Failed to get location data: {e}")
            return None
    
    def _get_current_location_data(self) -> Optional[LocationData]:
        """Get current location using available methods."""
        try:
            logger.info("Attempting to get current location...")
            
            # Try IP-based location detection as fallback
            location_data = self._try_ip_based_location()
            if location_data:
                self._notify_status(f"Location detected: {location_data.display_name}")
                logger.info(f"Successfully detected location: {location_data.display_name}")
                return location_data
            
            # If IP-based detection fails, inform user with helpful message
            error_msg = "Location detection failed. Please enter a city name manually."
            self._notify_error(error_msg)
            logger.warning("All location detection methods failed - user should enter city manually")
            return None
            
        except Exception as e:
            logger.error(f"Failed to get current location: {e}")
            self._notify_error("Location detection error. Please enter a city name manually.")
            return None
    
    def _try_ip_based_location(self) -> Optional[LocationData]:
        """Try to get approximate location using IP-based geolocation."""
        try:
            import requests
            # Using a free IP geolocation service as fallback
            # Note: This is a basic implementation for demonstration
            logger.info("Attempting IP-based location detection...")
            
            response = requests.get('http://ip-api.com/json/', timeout=5)
            if response.status_code == 200:
                data = response.json()
                if data.get('status') == 'success':
                    city = data.get('city', 'Unknown')
                    lat = data.get('lat')
                    lon = data.get('lon')
                    country = data.get('country', 'Unknown')
                    
                    if lat is not None and lon is not None:
                        logger.info(f"IP-based location found: {city}, {country} ({lat}, {lon})")
                        
                        # Create a LocationData object
                        from ..models.weather_models import LocationData
                        location_data = LocationData(
                            name=city,
                            country=country,
                            lat=float(lat),
                            lon=float(lon)
                        )
                        return location_data
                        
        except Exception as e:
            logger.warning(f"IP-based location detection failed: {e}")
        
        return None
    
    def _load_all_weather_data(self, lat: float, lon: float) -> None:
        """Load all weather data for given coordinates."""
        # Load weather data sequentially for now
        self._load_current_weather(lat, lon)
        self._load_forecast_data(lat, lon)
        self._load_air_quality_data(lat, lon)
    
    def _load_current_weather(self, lat: float, lon: float) -> None:
        """Load current weather data."""
        try:
            weather_response = self.api_service.get_current_weather(lat, lon)
            if weather_response:
                weather_data = WeatherData.from_api_response(weather_response)
                if weather_data.validate():
                    self.current_weather = weather_data
                    self._notify_weather_update(weather_data)
                    log_weather_data_update(weather_data.city, True)
                else:
                    logger.warning("Weather data validation failed")
        except Exception as e:
            logger.error(f"Failed to load current weather: {e}")
    
    def _load_forecast_data(self, lat: float, lon: float) -> None:
        """Load forecast data."""
        try:
            forecast_response = self.api_service.get_extended_forecast(lat, lon)
            if forecast_response:
                forecast_data = ForecastData.from_api_response(forecast_response['list'])
                self.forecast_data = forecast_data
                self._notify_forecast_update(forecast_data)
        except Exception as e:
            logger.error(f"Failed to load forecast data: {e}")
    
    def _load_air_quality_data(self, lat: float, lon: float) -> None:
        """Load air quality data."""
        try:
            air_quality_response = self.api_service.get_air_pollution(lat, lon)
            if air_quality_response:
                air_quality_data = AirQualityData.from_api_response(air_quality_response)
                self.air_quality_data = air_quality_data
                self._notify_air_quality_update(air_quality_data)
        except Exception as e:
            logger.error(f"Failed to load air quality data: {e}")
    
    # Data access methods
    def get_current_weather(self) -> Optional[WeatherData]:
        """Get current weather data."""
        return self.current_weather
    
    def get_forecast_data(self) -> Optional[ForecastData]:
        """Get forecast data."""
        return self.forecast_data
    
    def get_air_quality_data(self) -> Optional[AirQualityData]:
        """Get air quality data."""
        return self.air_quality_data
    
    def get_current_location(self) -> Optional[LocationData]:
        """Get current location data."""
        return self.current_location
    
    # Utility methods
    def is_data_loaded(self) -> bool:
        """Check if any weather data is loaded."""
        return any([
            self.current_weather is not None,
            self.forecast_data is not None,
            self.air_quality_data is not None
        ])
    
    def clear_data(self) -> None:
        """Clear all weather data."""
        self.current_weather = None
        self.forecast_data = None
        self.air_quality_data = None
        self.current_location = None
        logger.info("Weather data cleared")
