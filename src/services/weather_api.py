"""
Weather API service for handling all external weather data requests.

This module provides a clean interface for interacting with the OpenWeatherMap API
and handles all HTTP requests, response parsing, and error handling.
"""

import requests
import os
from typing import Dict, List, Optional, Any
from functools import lru_cache
from datetime import datetime, timedelta

from ..interfaces import WeatherAPIProtocol
from ..utils.logging import get_logger
from ..utils.exceptions import WeatherAPIError, ConfigurationError
from ..config.config import ApplicationConfiguration


logger = get_logger()


class WeatherAPIService:
    """Enhanced Weather API client with all Student Pack features."""
    
    def __init__(self, config: Optional[ApplicationConfiguration] = None):
        """Initialize the weather API service."""
        self.config = config or ApplicationConfiguration()
        self.api_key = self.config.api.api_key
        
        if not self.api_key:
            logger.warning("No API key configured. Some features may not work.")
            raise ConfigurationError("OpenWeather API key is required")
        
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0"
        self.air_pollution_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        self.historical_url = self.config.api.historical_url
        self.timeout = self.config.api.timeout
        
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
                'Advanced geocoding',
                'Historical weather data (Open-Meteo)'
            ]
        }

    def _make_historical_request(self, url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make HTTP request to Open-Meteo API (no API key required)."""
        logger.debug(f"Making historical API request to {url}")
        
        response = None
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            
            data = response.json()
            logger.debug(f"Historical API request successful: {response.status_code}")
            return data
            
        except requests.exceptions.Timeout:
            logger.error(f"Historical API request timeout after {self.timeout}s")
            raise WeatherAPIError("Historical data request timed out")
            
        except requests.exceptions.HTTPError as e:
            if response and response.status_code == 400:
                logger.error("Invalid parameters for historical data request")
                raise WeatherAPIError("Invalid historical data parameters")
            elif response and response.status_code == 404:
                logger.error("Historical data not found for specified location/date")
                raise WeatherAPIError("Historical data not available")
            else:
                logger.error(f"Historical API HTTP error: {e}")
                raise WeatherAPIError(f"Historical API error: {e}")
                
        except requests.exceptions.RequestException as e:
            logger.error(f"Historical API request failed: {e}")
            raise WeatherAPIError(f"Historical data network error: {e}")
            
        except ValueError as e:
            logger.error(f"Invalid JSON response from historical API: {e}")
            raise WeatherAPIError("Invalid historical data response format")

    def get_historical_weather(self, lat: float, lon: float, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """
        Get historical weather data from Open-Meteo API.
        
        Args:
            lat: Latitude
            lon: Longitude  
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Historical weather data dictionary
        """
        logger.info(f"Fetching historical weather data for coordinates: {lat}, {lon} from {start_date} to {end_date}")
        
        params = {
            "latitude": lat,
            "longitude": lon,
            "start_date": start_date,
            "end_date": end_date,
            "daily": "temperature_2m_mean,temperature_2m_max,temperature_2m_min,wind_speed_10m_max,wind_gusts_10m_max,sunrise,sunset",
            "hourly": "temperature_2m,precipitation"
        }
        
        return self._make_historical_request(self.historical_url, params)

    def get_historical_weather_sample(self, lat: float = 52.52, lon: float = 13.41) -> Optional[Dict[str, Any]]:
        """
        Get sample historical weather data (Berlin, 2000-2009) for demonstration.
        
        Args:
            lat: Latitude (default: Berlin)
            lon: Longitude (default: Berlin)
            
        Returns:
            Sample historical weather data
        """
        logger.info(f"Fetching sample historical weather data for coordinates: {lat}, {lon}")
        
        return self.get_historical_weather(
            lat=lat,
            lon=lon,
            start_date="2000-01-01",
            end_date="2009-12-31"
        )
