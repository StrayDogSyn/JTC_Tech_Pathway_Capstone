"""
Weather Business Service for the Weather Dashboard application.

This service encapsulates weather-related business logic, providing a clean
interface for weather operations while maintaining separation of concerns.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta

from ..models.weather_models import WeatherData, ForecastData, LocationData, AirQualityData
from ..services.weather_api import WeatherAPIService
from ..utils.logging import get_logger
from ..utils.exceptions import WeatherAPIError, ValidationError
from ..config.config import config_manager


logger = get_logger()


class WeatherService:
    """
    Business service for weather operations.
    
    This service encapsulates all weather-related business logic,
    including data validation, caching, and business rules.
    """
    
    def __init__(self, api_service: Optional[WeatherAPIService] = None):
        """Initialize the weather service."""
        logger.info("Initializing Weather Service")
        
        self.api_service = api_service or WeatherAPIService(config_manager.config)
        self._cache: Dict[str, Any] = {}
        self._cache_ttl = timedelta(minutes=10)  # 10 minute cache TTL
        
        logger.info("Weather Service initialized")
    
    def get_weather_for_city(self, city_name: str) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive weather data for a city.
        
        Args:
            city_name: Name of the city
            
        Returns:
            Dictionary containing weather, forecast, and air quality data
        """
        try:
            logger.info(f"Getting weather data for city: {city_name}")
            
            # Check cache first
            cache_key = f"weather_{city_name.lower()}"
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                logger.debug(f"Returning cached data for {city_name}")
                return cached_data
            
            # Get location data
            location_data = self._get_location_for_city(city_name)
            if not location_data:
                logger.warning(f"Could not find location for city: {city_name}")
                return None
            
            # Get weather data
            weather_data = self._get_current_weather(location_data.lat, location_data.lon)
            forecast_data = self._get_forecast_data(location_data.lat, location_data.lon)
            air_quality_data = self._get_air_quality_data(location_data.lat, location_data.lon)
            
            # Combine all data
            result = {
                'location': location_data,
                'current_weather': weather_data,
                'forecast': forecast_data,
                'air_quality': air_quality_data,
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache the result
            self._store_in_cache(cache_key, result)
            
            logger.info(f"Successfully retrieved weather data for {city_name}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting weather for city {city_name}: {e}")
            return None
    
    def get_weather_for_coordinates(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """
        Get comprehensive weather data for coordinates.
        
        Args:
            lat: Latitude
            lon: Longitude
            
        Returns:
            Dictionary containing weather, forecast, and air quality data
        """
        try:
            logger.info(f"Getting weather data for coordinates: {lat}, {lon}")
            
            # Check cache first
            cache_key = f"weather_{lat}_{lon}"
            cached_data = self._get_from_cache(cache_key)
            if cached_data:
                logger.debug(f"Returning cached data for coordinates {lat}, {lon}")
                return cached_data
            
            # Get weather data
            weather_data = self._get_current_weather(lat, lon)
            forecast_data = self._get_forecast_data(lat, lon)
            air_quality_data = self._get_air_quality_data(lat, lon)
            
            # Combine all data
            result = {
                'current_weather': weather_data,
                'forecast': forecast_data,
                'air_quality': air_quality_data,
                'coordinates': {'lat': lat, 'lon': lon},
                'timestamp': datetime.now().isoformat()
            }
            
            # Cache the result
            self._store_in_cache(cache_key, result)
            
            logger.info(f"Successfully retrieved weather data for coordinates {lat}, {lon}")
            return result
            
        except Exception as e:
            logger.error(f"Error getting weather for coordinates {lat}, {lon}: {e}")
            return None
    
    def search_cities(self, query: str, limit: int = 5) -> List[LocationData]:
        """
        Search for cities by name.
        
        Args:
            query: Search query
            limit: Maximum number of results
            
        Returns:
            List of LocationData objects
        """
        try:
            logger.info(f"Searching for cities: {query}")
            
            # Use API service to search
            results = self.api_service.geocode_location(query, limit)
            
            # Convert to LocationData objects
            locations = []
            for result in results:
                try:
                    location = LocationData.from_api_response(result)
                    locations.append(location)
                except Exception as e:
                    logger.warning(f"Error parsing location data: {e}")
                    continue
            
            logger.info(f"Found {len(locations)} cities for query: {query}")
            return locations
            
        except Exception as e:
            logger.error(f"Error searching cities for query {query}: {e}")
            return []
    
    def validate_weather_data(self, weather_data: WeatherData) -> bool:
        """
        Validate weather data using business rules.
        
        Args:
            weather_data: Weather data to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            # Use model validation
            if not weather_data.validate():
                return False
            
            # Additional business validation rules
            if weather_data.temperature < -100 or weather_data.temperature > 60:
                logger.warning(f"Temperature out of expected range: {weather_data.temperature}")
                return False
            
            if weather_data.humidity < 0 or weather_data.humidity > 100:
                logger.warning(f"Humidity out of range: {weather_data.humidity}")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"Error validating weather data: {e}")
            return False
    
    def clear_cache(self) -> None:
        """Clear the weather data cache."""
        self._cache.clear()
        logger.info("Weather cache cleared")
    
    # Private helper methods
    def _get_location_for_city(self, city_name: str) -> Optional[LocationData]:
        """Get location data for a city name."""
        try:
            results = self.api_service.geocode_location(city_name, limit=1)
            if results:
                return LocationData.from_api_response(results[0])
            return None
        except Exception as e:
            logger.error(f"Error getting location for city {city_name}: {e}")
            return None
    
    def _get_current_weather(self, lat: float, lon: float) -> Optional[WeatherData]:
        """Get current weather data for coordinates."""
        try:
            response = self.api_service.get_current_weather(lat, lon)
            if response:
                weather_data = WeatherData.from_api_response(response)
                if self.validate_weather_data(weather_data):
                    return weather_data
                else:
                    logger.warning("Weather data validation failed")
            return None
        except Exception as e:
            logger.error(f"Error getting current weather: {e}")
            return None
    
    def _get_forecast_data(self, lat: float, lon: float) -> Optional[ForecastData]:
        """Get forecast data for coordinates."""
        try:
            response = self.api_service.get_extended_forecast(lat, lon)
            if response:
                return ForecastData.from_api_response(response['list'])
            return None
        except Exception as e:
            logger.error(f"Error getting forecast data: {e}")
            return None
    
    def _get_air_quality_data(self, lat: float, lon: float) -> Optional[AirQualityData]:
        """Get air quality data for coordinates."""
        try:
            response = self.api_service.get_air_pollution(lat, lon)
            if response:
                return AirQualityData.from_api_response(response)
            return None
        except Exception as e:
            logger.error(f"Error getting air quality data: {e}")
            return None
    
    def _get_from_cache(self, key: str) -> Optional[Any]:
        """Get data from cache if not expired."""
        if key in self._cache:
            data, timestamp = self._cache[key]
            if datetime.now() - timestamp < self._cache_ttl:
                return data
            else:
                # Remove expired data
                del self._cache[key]
        return None
    
    def _store_in_cache(self, key: str, data: Any) -> None:
        """Store data in cache with timestamp."""
        self._cache[key] = (data, datetime.now())
