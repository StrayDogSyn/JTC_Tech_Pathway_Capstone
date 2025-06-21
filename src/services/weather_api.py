"""
Weather API service for handling all external weather data requests.

This module provides a clean interface for interacting with the OpenWeatherMap API
and handles all HTTP requests, response parsing, and error handling.
"""

import requests
import os
from typing import Dict, List, Optional, Any
from functools import lru_cache


class WeatherAPIError(Exception):
    """Custom exception for weather API related errors."""
    pass


class WeatherAPIService:
    """Enhanced Weather API client with all Student Pack features."""
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the weather API service."""
        self.api_key = api_key or os.getenv("OPENWEATHER_API_KEY", "")
        if not self.api_key:
            print("⚠️ Warning: No API key configured. Some features may not work.")
        
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0"
        self.air_pollution_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        self.timeout = 10

    def _make_request(self, url: str, params: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Make HTTP request with error handling."""
        if not self.api_key:
            print("❌ No API key available for request")
            return None
            
        params["appid"] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=self.timeout)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None

    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get current weather data for coordinates."""
        params = {"lat": lat, "lon": lon, "units": "metric"}
        return self._make_request(f"{self.base_url}/weather", params)

    def get_extended_forecast(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get 5-day forecast data with caching."""
        params = {"lat": lat, "lon": lon, "units": "metric"}
        return self._make_request(self.forecast_url, params)

    def get_air_pollution(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get air quality data for given coordinates."""
        params = {"lat": lat, "lon": lon}
        return self._make_request(self.air_pollution_url, params)

    def geocode_location(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Search for cities by name."""
        url = f"{self.geocoding_url}/direct"
        params = {"q": query, "limit": limit}
        
        result = self._make_request(url, params)
        return result if isinstance(result, list) else []

    def get_subscription_info(self) -> Dict[str, Any]:
        """Get API subscription information."""
        return {
            'plan': 'Free/Student Pack',
            'features': [
                'Current weather data',
                '5-day/3-hour forecasts',
                'Air pollution monitoring',
                'Advanced geocoding'
            ]
        }
