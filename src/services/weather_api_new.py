"""
Weather API service for handling all external weather data requests.

This module provides a clean interface for interacting with the OpenWeatherMap API
and handles all HTTP requests, response parsing, and error handling.
"""

import requests
import os
from typing import Dict, List, Optional, Any
from functools import lru_cache

from ..interfaces import WeatherAPIProtocol
from ..utils.logging import get_logger
from ..utils.exceptions import WeatherAPIError, ConfigurationError
from ..config.config import WeatherConfig


logger = get_logger()


class WeatherAPIService:
    """Enhanced Weather API client with all Student Pack features."""
    
    def __init__(self, config: Optional[WeatherConfig] = None):
        """Initialize the weather API service."""
        self.config = config or WeatherConfig()
        self.api_key = self.config.api_key
        
        if not self.api_key:
            logger.warning("No API key configured. Some features may not work.")
            raise ConfigurationError("OpenWeather API key is required")
        
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0"
        self.air_pollution_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        self.timeout = self.config.api_timeout
        
        logger.info("WeatherAPIService initialized successfully")

    def _make_request(self, url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make HTTP request with enhanced error handling and logging."""
        if not self.api_key:
            logger.error("No API key available for request")
            raise WeatherAPIError("No API key configured")
            
        params["appid"] = self.api_key
        logger.debug(f"Making API request to {url}")
        
        response = None
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"API request successful: {response.status_code}")
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"API request timeout after {self.timeout}s")
            raise WeatherAPIError("Request timed out")
            
        except requests.exceptions.HTTPError as e:
            if response and response.status_code == 401:
                logger.error("Invalid API key")
                raise WeatherAPIError("Invalid API key")
            elif response and response.status_code == 404:
                logger.error("Location not found")
                raise WeatherAPIError("Location not found")
            else:
                logger.error(f"HTTP error: {e}")
                raise WeatherAPIError(f"HTTP error: {e}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise WeatherAPIError(f"Network error: {e}")
            
        except ValueError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise WeatherAPIError("Invalid response format")

    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get current weather data for coordinates."""
        logger.info(f"Fetching current weather for coordinates: {lat}, {lon}")
        params = {"lat": lat, "lon": lon, "units": "metric"}
        return self._make_request(f"{self.base_url}/weather", params)

    def get_extended_forecast(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get 5-day forecast data with caching."""
        logger.info(f"Fetching extended forecast for coordinates: {lat}, {lon}")
        params = {"lat": lat, "lon": lon, "units": "metric"}
        return self._make_request(self.forecast_url, params)

    def get_air_pollution(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get air quality data for given coordinates."""
        logger.info(f"Fetching air pollution data for coordinates: {lat}, {lon}")
        params = {"lat": lat, "lon": lon}
        return self._make_request(self.air_pollution_url, params)

    def geocode_location(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for cities by name."""
        logger.info(f"Geocoding location: {query}")
        url = f"{self.geocoding_url}/direct"
        params = {"q": query, "limit": limit}
        
        try:
            result = self._make_request(url, params)
            return result if isinstance(result, list) else []
        except WeatherAPIError:
            logger.warning(f"Geocoding failed for query: {query}")
            return []

    def get_subscription_info(self) -> Dict[str, Any]:
        """Get API subscription information."""
        logger.debug("Getting subscription information")
        return {
            'plan': 'Free/Student Pack',
            'features': [
                'Current weather data',
                '5-day/3-hour forecasts',
                'Air pollution monitoring',
                'Advanced geocoding'
            ]
        }
