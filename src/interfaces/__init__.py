"""
Core interfaces and protocols for the weather dashboard application.

This module defines the contracts and interfaces used throughout the application
to ensure proper separation of concerns and dependency injection.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Protocol, Union
from src.models.weather_models import WeatherData, ForecastData, AirQualityData, LocationData


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


class ConfigurationProtocol(Protocol):
    """Protocol defining the configuration management interface."""

    @property
    def api_key(self) -> str:
        """Get the API key."""
        ...

    @property
    def current_city(self) -> str:
        """Get the current city."""
        ...

    @property
    def current_theme(self) -> str:
        """Get the current theme."""
        ...

    def save_settings(self, **kwargs: Any) -> None:
        """Save application settings."""
        ...

    def load_settings(self) -> Dict[str, Any]:
        """Load application settings."""
        ...


class UIProtocol(Protocol):
    """Protocol defining the user interface contract."""

    def update_status(self, message: str) -> None:
        """Update the status bar message."""
        ...

    def show_error(self, title: str, message: str) -> None:
        """Show an error dialog."""
        ...

    def show_info(self, title: str, message: str) -> None:
        """Show an information dialog."""
        ...

    def set_loading(self, loading: bool) -> None:
        """Set the loading state."""
        ...

    def run(self) -> None:
        """Start the UI main loop."""
        ...


class WeatherCoreProtocol(Protocol):
    """Protocol defining the weather core business logic interface."""

    def load_weather_data(self, city: str) -> None:
        """Load weather data for a city."""
        ...

    def has_weather_data(self) -> bool:
        """Check if weather data is available."""
        ...

    def has_forecast_data(self) -> bool:
        """Check if forecast data is available."""
        ...

    def has_air_quality_data(self) -> bool:
        """Check if air quality data is available."""
        ...

    def get_weather_summary(self) -> Dict[str, Any]:
        """Get a summary of current weather data."""
        ...

    def set_status_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for status updates."""
        ...

    def set_data_update_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for data updates."""
        ...


class LoggerProtocol(Protocol):
    """Protocol defining the logging interface."""

    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message."""
        ...

    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message."""
        ...

    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message."""
        ...

    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message."""
        ...

    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message."""
        ...


class DataValidatorProtocol(Protocol):
    """Protocol defining data validation interface."""

    def validate_weather_data(self, data: Dict[str, Any]) -> bool:
        """Validate weather data structure."""
        ...

    def validate_api_response(self, response: Dict[str, Any]) -> bool:
        """Validate API response structure."""
        ...

    def sanitize_user_input(self, input_data: str) -> str:
        """Sanitize user input data."""
        ...


# Abstract base classes for concrete implementations

class BaseWeatherService(ABC):
    """Base class for weather services."""

    @abstractmethod
    def fetch_weather_data(self, location: Union[str, tuple]) -> Optional[WeatherData]:
        """Fetch weather data for a location."""
        pass

    @abstractmethod
    def fetch_forecast_data(self, location: Union[str, tuple]) -> Optional[ForecastData]:
        """Fetch forecast data for a location."""
        pass


class BaseUIComponent(ABC):
    """Base class for UI components."""

    @abstractmethod
    def setup_ui(self) -> None:
        """Set up the UI component."""
        pass

    @abstractmethod
    def update_display(self, data: Dict[str, Any]) -> None:
        """Update the display with new data."""
        pass

    @abstractmethod
    def clear_display(self) -> None:
        """Clear the display."""
        pass


class BaseDataProcessor(ABC):
    """Base class for data processors."""

    @abstractmethod
    def process_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process raw data into application format."""
        pass

    @abstractmethod
    def validate_data(self, data: Dict[str, Any]) -> bool:
        """Validate processed data."""
        pass


# Event system interfaces

class EventPublisher(ABC):
    """Base class for event publishers."""

    def __init__(self) -> None:
        self._subscribers: Dict[str, List[Callable]] = {}

    def subscribe(self, event_type: str, callback: Callable) -> None:
        """Subscribe to an event type."""
        if event_type not in self._subscribers:
            self._subscribers[event_type] = []
        self._subscribers[event_type].append(callback)

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        """Unsubscribe from an event type."""
        if event_type in self._subscribers:
            self._subscribers[event_type].remove(callback)

    def publish(self, event_type: str, data: Any = None) -> None:
        """Publish an event to all subscribers."""
        if event_type in self._subscribers:
            for callback in self._subscribers[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    # Log error but don't break other subscribers
                    print(f"Error in event callback: {e}")


# Dependency injection container interface

class DIContainer(ABC):
    """Dependency injection container interface."""

    @abstractmethod
    def register(self, interface: type, implementation: type, singleton: bool = False) -> None:
        """Register an implementation for an interface."""
        pass

    @abstractmethod
    def get(self, interface: type) -> Any:
        """Get an implementation for an interface."""
        pass

    @abstractmethod
    def has(self, interface: type) -> bool:
        """Check if an interface is registered."""
        pass
