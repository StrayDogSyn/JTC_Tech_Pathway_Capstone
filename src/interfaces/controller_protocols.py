"""
Controller protocols for the Weather Dashboard application.

These protocols define the contracts for controller components in the MVC architecture,
ensuring proper separation of concerns and loose coupling.
"""

from typing import Protocol, Callable, Optional, Dict, Any
from ..models.weather_models import WeatherData, ForecastData, AirQualityData, LocationData


class WeatherControllerProtocol(Protocol):
    """Protocol defining the weather controller interface."""
    
    def load_weather_for_city(self, city_name: str) -> bool:
        """Load weather data for a given city."""
        ...
    
    def load_weather_for_coordinates(self, lat: float, lon: float) -> bool:
        """Load weather data for given coordinates."""
        ...
    
    def refresh_weather_data(self) -> bool:
        """Refresh current weather data."""
        ...
    
    def get_current_weather(self) -> Optional[WeatherData]:
        """Get current weather data."""
        ...
    
    def get_forecast_data(self) -> Optional[ForecastData]:
        """Get forecast data."""
        ...
    
    def get_air_quality_data(self) -> Optional[AirQualityData]:
        """Get air quality data."""
        ...
    
    def get_current_location(self) -> Optional[LocationData]:
        """Get current location data."""
        ...
    
    def is_data_loaded(self) -> bool:
        """Check if any weather data is loaded."""
        ...
    
    def clear_data(self) -> None:
        """Clear all weather data."""
        ...
    
    # Observer pattern methods
    def add_weather_update_observer(self, callback: Callable[[WeatherData], None]) -> None:
        """Add observer for weather data updates."""
        ...
    
    def add_forecast_update_observer(self, callback: Callable[[ForecastData], None]) -> None:
        """Add observer for forecast data updates."""
        ...
    
    def add_air_quality_update_observer(self, callback: Callable[[AirQualityData], None]) -> None:
        """Add observer for air quality data updates."""
        ...
    
    def add_error_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for error notifications."""
        ...
    
    def add_status_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for status updates."""
        ...


class ApplicationControllerProtocol(Protocol):
    """Protocol defining the application controller interface."""
    
    def start(self) -> bool:
        """Start the application."""
        ...
    
    def stop(self) -> None:
        """Stop the application."""
        ...
    
    def restart(self) -> bool:
        """Restart the application."""
        ...
    
    def change_theme(self, theme: str) -> bool:
        """Change application theme."""
        ...
    
    def update_settings(self, **settings) -> bool:
        """Update application settings."""
        ...
    
    def search_weather(self, city_name: str) -> bool:
        """Search for weather data for a city."""
        ...
    
    def refresh_weather(self) -> bool:
        """Refresh current weather data."""
        ...
    
    @property
    def is_running(self) -> bool:
        """Check if application is running."""
        ...
    
    @property
    def current_city(self) -> Optional[str]:
        """Get current city name."""
        ...
    
    @property
    def current_theme(self) -> str:
        """Get current theme."""
        ...
    
    @property
    def weather_controller(self) -> WeatherControllerProtocol:
        """Get weather controller instance."""
        ...
    
    # Observer pattern methods
    def add_status_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for application status updates."""
        ...
    
    def add_error_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for application errors."""
        ...
    
    def add_theme_change_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for theme changes."""
        ...
