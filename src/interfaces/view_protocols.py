"""
View protocols for the Weather Dashboard application.

These protocols define the contracts for view components in the MVC architecture,
ensuring proper separation between presentation and business logic.
"""

from typing import Protocol, Callable, Dict, Any, Optional
from ..models.weather_models import WeatherData, ForecastData, AirQualityData


class NotificationProtocol(Protocol):
    """Protocol for notification handling."""
    
    def show_error(self, title: str, message: str) -> None:
        """Show error message to user."""
        ...
    
    def show_info(self, title: str, message: str) -> None:
        """Show info message to user."""
        ...
    
    def show_warning(self, title: str, message: str) -> None:
        """Show warning message to user."""
        ...


class WeatherViewProtocol(Protocol):
    """Protocol defining the weather view interface."""
    
    def update_weather_display(self, weather_data: WeatherData) -> None:
        """Update the current weather display."""
        ...
    
    def update_forecast_display(self, forecast_data: ForecastData) -> None:
        """Update the forecast display."""
        ...
    
    def update_air_quality_display(self, air_quality_data: AirQualityData) -> None:
        """Update the air quality display."""
        ...
    
    def show_loading_state(self, message: str) -> None:
        """Show loading state with message."""
        ...
    
    def hide_loading_state(self) -> None:
        """Hide loading state."""
        ...
    
    def set_search_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for search requests."""
        ...
    
    def set_refresh_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for refresh requests."""
        ...


class MainViewProtocol(Protocol):
    """Protocol defining the main view interface."""
    
    def initialize_ui(self) -> None:
        """Initialize the user interface."""
        ...
    
    def show(self) -> None:
        """Show the main view."""
        ...
    
    def hide(self) -> None:
        """Hide the main view."""
        ...
    
    def destroy(self) -> None:
        """Destroy the main view."""
        ...
    
    def set_title(self, title: str) -> None:
        """Set the window title."""
        ...
    
    def set_theme(self, theme: str) -> None:
        """Set the UI theme."""
        ...
    
    def show_status(self, message: str) -> None:
        """Show status message."""
        ...
    
    def get_weather_view(self) -> Optional[WeatherViewProtocol]:
        """Get the weather view component."""
        ...
    
    def set_theme_change_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for theme changes."""
        ...
    
    def set_settings_change_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Set callback for settings changes."""
        ...
