"""
Weather View for the Weather Dashboard application.

This view handles the display of weather-related information and provides
a clean interface between the weather UI components and the controllers.
It implements the view part of the MVC pattern.
"""

from typing import Protocol, Optional, Callable, Dict, Any
from abc import ABC, abstractmethod
import tkinter as tk

from ..models.weather_models import WeatherData, ForecastData, AirQualityData
from ..utils.logging import get_logger


logger = get_logger()


class WeatherViewProtocol(Protocol):
    """Protocol defining the interface for weather views."""
    
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
        """Show loading state."""
        ...
    
    def hide_loading_state(self) -> None:
        """Hide loading state."""
        ...
    
    def show_error(self, title: str, message: str) -> None:
        """Show error message."""
        ...
    
    def show_info(self, title: str, message: str) -> None:
        """Show info message."""
        ...


class WeatherView(ABC):
    """
    Abstract base class for weather views.
    
    This class defines the interface and common functionality for weather views,
    ensuring proper separation of concerns and adherence to MVC patterns.
    """
    
    def __init__(self):
        """Initialize the weather view."""
        logger.info("Initializing Weather View")
        
        # UI state
        self._is_loading = False
        self._current_weather_data: Optional[WeatherData] = None
        self._current_forecast_data: Optional[ForecastData] = None
        self._current_air_quality_data: Optional[AirQualityData] = None
        
        # Callbacks to controllers
        self._search_callback: Optional[Callable[[str], None]] = None
        self._refresh_callback: Optional[Callable[[], None]] = None
        
        logger.info("Weather View initialized")
    
    # Abstract methods to be implemented by concrete views
    @abstractmethod
    def update_weather_display(self, weather_data: WeatherData) -> None:
        """Update the current weather display."""
        pass
    
    @abstractmethod
    def update_forecast_display(self, forecast_data: ForecastData) -> None:
        """Update the forecast display."""
        pass
    
    @abstractmethod
    def update_air_quality_display(self, air_quality_data: AirQualityData) -> None:
        """Update the air quality display."""
        pass
    
    @abstractmethod
    def show_loading_state(self, message: str) -> None:
        """Show loading state."""
        pass
    
    @abstractmethod
    def hide_loading_state(self) -> None:
        """Hide loading state."""
        pass
    
    @abstractmethod
    def show_error(self, title: str, message: str) -> None:
        """Show error message."""
        pass
    
    @abstractmethod
    def show_info(self, title: str, message: str) -> None:
        """Show info message."""
        pass
    
    # Callback management
    def set_search_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for search requests."""
        self._search_callback = callback
    
    def set_refresh_callback(self, callback: Callable[[], None]) -> None:
        """Set callback for refresh requests."""
        self._refresh_callback = callback
    
    # Protected methods for concrete implementations
    def _on_search_requested(self, city: str) -> None:
        """Handle search request from UI."""
        if self._search_callback and city.strip():
            logger.info(f"Search requested for city: {city}")
            self._search_callback(city.strip())
    
    def _on_refresh_requested(self) -> None:
        """Handle refresh request from UI."""
        if self._refresh_callback:
            logger.info("Refresh requested")
            self._refresh_callback()
    
    # Public interface methods
    def handle_weather_update(self, weather_data: WeatherData) -> None:
        """Handle weather data update from controller."""
        try:
            logger.info(f"Updating weather display for {weather_data.city}")
            self._current_weather_data = weather_data
            self.update_weather_display(weather_data)
            self.hide_loading_state()
        except Exception as e:
            logger.error(f"Error updating weather display: {e}")
            self.show_error("Display Error", f"Failed to update weather display: {str(e)}")
    
    def handle_forecast_update(self, forecast_data: ForecastData) -> None:
        """Handle forecast data update from controller."""
        try:
            logger.info("Updating forecast display")
            self._current_forecast_data = forecast_data
            self.update_forecast_display(forecast_data)
        except Exception as e:
            logger.error(f"Error updating forecast display: {e}")
            self.show_error("Display Error", f"Failed to update forecast display: {str(e)}")
    
    def handle_air_quality_update(self, air_quality_data: AirQualityData) -> None:
        """Handle air quality data update from controller."""
        try:
            logger.info("Updating air quality display")
            self._current_air_quality_data = air_quality_data
            self.update_air_quality_display(air_quality_data)
        except Exception as e:
            logger.error(f"Error updating air quality display: {e}")
            self.show_error("Display Error", f"Failed to update air quality display: {str(e)}")
    
    def handle_status_update(self, message: str) -> None:
        """Handle status update from controller."""
        if "loading" in message.lower() or "fetching" in message.lower():
            self.show_loading_state(message)
        else:
            self.hide_loading_state()
    
    def handle_error(self, error_message: str) -> None:
        """Handle error from controller."""
        logger.warning(f"Displaying error to user: {error_message}")
        self.hide_loading_state()
        self.show_error("Error", error_message)
    
    # Property accessors
    @property
    def is_loading(self) -> bool:
        """Check if view is in loading state."""
        return self._is_loading
    
    @property
    def current_weather_data(self) -> Optional[WeatherData]:
        """Get current weather data."""
        return self._current_weather_data
    
    @property
    def current_forecast_data(self) -> Optional[ForecastData]:
        """Get current forecast data."""
        return self._current_forecast_data
    
    @property
    def current_air_quality_data(self) -> Optional[AirQualityData]:
        """Get current air quality data."""
        return self._current_air_quality_data


class TkinterWeatherView(WeatherView):
    """
    Concrete implementation of WeatherView using Tkinter.
    
    This class wraps the existing UI components and provides the interface
    expected by the MVC architecture.
    """
    
    def __init__(self, ui_component):
        """Initialize with existing UI component."""
        super().__init__()
        self.ui = ui_component
        logger.info("Tkinter Weather View initialized")
    
    def update_weather_display(self, weather_data: WeatherData) -> None:
        """Update the current weather display."""
        try:
            # Convert to dict format expected by existing UI
            weather_dict = {
                'temperature': weather_data.temperature,
                'feels_like': weather_data.feels_like,
                'humidity': weather_data.humidity,
                'pressure': weather_data.pressure,
                'wind_speed': weather_data.wind_speed,
                'wind_direction': weather_data.wind_direction,
                'visibility': weather_data.visibility,
                'description': weather_data.description,
                'icon': weather_data.icon,
                'city': weather_data.city,
                'country': weather_data.country,
                'timestamp': weather_data.timestamp,
                'cloudiness': weather_data.cloudiness
            }
            self.ui.update_weather_display(weather_dict)
        except Exception as e:
            logger.error(f"Error updating weather display: {e}")
            raise
    
    def update_forecast_display(self, forecast_data: ForecastData) -> None:
        """Update the forecast display."""
        try:
            # Convert to dict format expected by existing UI
            forecast_dict = {
                'hourly': forecast_data.hourly,
                'daily': forecast_data.daily
            }
            self.ui.update_forecast_display(forecast_dict)
        except Exception as e:
            logger.error(f"Error updating forecast display: {e}")
            raise
    
    def update_air_quality_display(self, air_quality_data: AirQualityData) -> None:
        """Update the air quality display."""
        try:
            # Convert to dict format expected by existing UI
            air_quality_dict = {
                'aqi': air_quality_data.aqi,
                'co': air_quality_data.co,
                'no': air_quality_data.no,
                'no2': air_quality_data.no2,
                'o3': air_quality_data.o3,
                'so2': air_quality_data.so2,
                'pm2_5': air_quality_data.pm2_5,
                'pm10': air_quality_data.pm10,
                'nh3': air_quality_data.nh3
            }
            self.ui.update_air_quality_display(air_quality_dict)
        except Exception as e:
            logger.error(f"Error updating air quality display: {e}")
            raise
    
    def show_loading_state(self, message: str) -> None:
        """Show loading state."""
        self._is_loading = True
        if hasattr(self.ui, 'update_status'):
            self.ui.update_status(message)
    
    def hide_loading_state(self) -> None:
        """Hide loading state."""
        self._is_loading = False
        if hasattr(self.ui, 'update_status'):
            self.ui.update_status("Ready")
    
    def show_error(self, title: str, message: str) -> None:
        """Show error message."""
        if hasattr(self.ui, 'show_error'):
            self.ui.show_error(title, message)
        else:
            # Fallback to basic message box
            import tkinter.messagebox as messagebox
            messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str) -> None:
        """Show info message."""
        if hasattr(self.ui, 'show_info'):
            self.ui.show_info(title, message)
        else:
            # Fallback to basic message box
            import tkinter.messagebox as messagebox
            messagebox.showinfo(title, message)
