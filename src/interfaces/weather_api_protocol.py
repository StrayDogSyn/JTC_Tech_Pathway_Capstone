"""
Weather API Protocol for the Weather Dashboard application.

This protocol defines the contract for weather API services, ensuring
proper abstraction and testability.
"""

from typing import Protocol, Dict, List, Optional, Any


class WeatherAPIProtocol(Protocol):
    """Protocol defining the weather API service interface."""

    def get_current_weather(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get current weather data for given coordinates."""
        ...

    def get_extended_forecast(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get extended forecast data for given coordinates."""
        ...

    def get_air_pollution(self, lat: float, lon: float) -> Optional[Dict[str, Any]]:
        """Get air pollution data for given coordinates."""
        ...

    def geocode_location(self, location: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Geocode a location string to coordinates."""
        ...

    def get_historical_weather(self, lat: float, lon: float, start_date: str, end_date: str) -> Optional[Dict[str, Any]]:
        """Get historical weather data for given coordinates and date range."""
        ...

    def get_subscription_info(self) -> Dict[str, Any]:
        """Get API subscription information."""
        ...
