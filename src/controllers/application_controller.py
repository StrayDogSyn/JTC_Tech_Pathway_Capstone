"""
Application Controller for the Weather Dashboard application.

This controller manages the overall application flow and coordinates between
different components. It implements the main controller in the MVC pattern,
handling application-level concerns like configuration, settings, and
coordination between different subsystems.
"""

from typing import Optional, Callable, Dict, Any
import threading
import time

from .weather_controller import WeatherController
from ..config.config import config_manager, ApplicationConfiguration
from ..utils.logging import get_logger, get_ui_logger
from ..utils.exceptions import ConfigurationError


logger = get_logger()
ui_logger = get_ui_logger()


class ApplicationController:
    """
    Main application controller following MVC pattern.
    
    Responsibilities:
    - Coordinate between different controllers
    - Manage application lifecycle
    - Handle configuration changes
    - Provide application-level services
    - Coordinate UI and business logic
    """
    
    def __init__(self, config: Optional[ApplicationConfiguration] = None):
        """Initialize the application controller."""
        logger.info("Initializing Application Controller")
        
        # Configuration
        self.config = config or config_manager.config
        
        # Sub-controllers
        self.weather_controller = WeatherController()
        
        # Application state
        self._is_running = False
        self._background_tasks = []
        
        # View callbacks
        self._status_callbacks: list[Callable[[str], None]] = []
        self._error_callbacks: list[Callable[[str], None]] = []
        self._theme_change_callbacks: list[Callable[[str], None]] = []
        
        logger.info("Application Controller initialized successfully")
    
    # Observer pattern for application-level events
    def add_status_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for application status updates."""
        self._status_callbacks.append(callback)
    
    def add_error_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for application errors."""
        self._error_callbacks.append(callback)
    
    def add_theme_change_observer(self, callback: Callable[[str], None]) -> None:
        """Add observer for theme changes."""
        self._theme_change_callbacks.append(callback)
    
    # Private notification methods
    def _notify_status(self, message: str) -> None:
        """Notify all observers of status updates."""
        for callback in self._status_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in status callback: {e}")
    
    def _notify_error(self, message: str) -> None:
        """Notify all observers of errors."""
        for callback in self._error_callbacks:
            try:
                callback(message)
            except Exception as e:
                logger.error(f"Error in error callback: {e}")
    
    def _notify_theme_change(self, theme: str) -> None:
        """Notify all observers of theme changes."""
        for callback in self._theme_change_callbacks:
            try:
                callback(theme)
            except Exception as e:
                logger.error(f"Error in theme change callback: {e}")
    
    # Application lifecycle methods
    def start(self) -> bool:
        """Start the application."""
        try:
            logger.info("Starting Weather Dashboard Application")
            self._notify_status("Starting application...")
            
            # Validate configuration
            if not self._validate_configuration():
                return False
            
            # Initialize components
            self._initialize_components()
            
            # Load initial data
            self._load_initial_data()
            
            # Start background tasks
            self._start_background_tasks()
            
            self._is_running = True
            self._notify_status("Application started successfully")
            logger.info("Weather Dashboard Application started successfully")
            return True
            
        except Exception as e:
            error_msg = f"Failed to start application: {str(e)}"
            logger.error(error_msg)
            self._notify_error(error_msg)
            return False
    
    def stop(self) -> None:
        """Stop the application."""
        try:
            logger.info("Stopping Weather Dashboard Application")
            self._notify_status("Stopping application...")
            
            # Stop background tasks
            self._stop_background_tasks()
            
            # Save current state
            self._save_application_state()
            
            self._is_running = False
            self._notify_status("Application stopped")
            logger.info("Weather Dashboard Application stopped")
            
        except Exception as e:
            logger.error(f"Error stopping application: {e}")
    
    def restart(self) -> bool:
        """Restart the application."""
        logger.info("Restarting Weather Dashboard Application")
        self.stop()
        time.sleep(1)  # Brief pause
        return self.start()
    
    # Configuration management
    def change_theme(self, theme: str) -> bool:
        """Change application theme."""
        try:
            logger.info(f"Changing theme to: {theme}")
            ui_logger.log_user_action("theme_change", {"theme": theme})
            
            # Validate theme
            if not self._validate_theme(theme):
                self._notify_error(f"Invalid theme: {theme}")
                return False
            
            # Save configuration
            config_manager.save_settings(theme=theme)
            
            # Notify observers
            self._notify_theme_change(theme)
            self._notify_status(f"Theme changed to {theme}")
            
            return True
            
        except Exception as e:
            error_msg = f"Failed to change theme: {str(e)}"
            logger.error(error_msg)
            self._notify_error(error_msg)
            return False
    
    def update_settings(self, **settings) -> bool:
        """Update application settings."""
        try:
            logger.info(f"Updating settings: {settings}")
            
            # Validate settings
            if not self._validate_settings(settings):
                return False
            
            # Apply settings
            config_manager.save_settings(**settings)
            
            self._notify_status("Settings updated successfully")
            return True
            
        except Exception as e:
            error_msg = f"Failed to update settings: {str(e)}"
            logger.error(error_msg)
            self._notify_error(error_msg)
            return False
    
    # Weather operations delegation
    def search_weather(self, city_name: str) -> bool:
        """Search for weather data for a city."""
        try:
            ui_logger.log_user_action("search", {"city": city_name})
            return self.weather_controller.load_weather_for_city(city_name)
        except Exception as e:
            error_msg = f"Failed to search weather for {city_name}: {str(e)}"
            logger.error(error_msg)
            self._notify_error(error_msg)
            return False
    
    def refresh_weather(self) -> bool:
        """Refresh current weather data."""
        try:
            ui_logger.log_user_action("refresh", {})
            return self.weather_controller.refresh_weather_data()
        except Exception as e:
            error_msg = f"Failed to refresh weather data: {str(e)}"
            logger.error(error_msg)
            self._notify_error(error_msg)
            return False
    
    def get_current_location_data(self) -> Optional[Dict[str, Any]]:
        """Get current location and weather data for import functionality."""
        try:
            location = self.weather_controller.get_current_location()
            weather = self.weather_controller.current_weather
            
            if not location:
                return None
            
            # Create combined data structure
            data = {
                'lat': location.lat,
                'lon': location.lon,
                'location': location.display_name,
                'city': location.name,
                'country': location.country,
                'state': location.state
            }
            
            # Add weather data if available
            if weather:
                data['weather'] = {
                    'city': weather.city,
                    'country': weather.country,
                    'temperature': weather.temperature,
                    'feels_like': weather.feels_like,
                    'humidity': weather.humidity,
                    'pressure': weather.pressure,
                    'wind_speed': weather.wind_speed,
                    'wind_direction': weather.wind_direction,
                    'visibility': weather.visibility,
                    'description': weather.description,
                    'icon': weather.icon,
                    'timestamp': weather.timestamp,
                    'cloudiness': weather.cloudiness
                }
            
            return data
            
        except Exception as e:
            logger.error(f"Error getting current location data: {e}")
            return None
    
    # Private helper methods
    def _validate_configuration(self) -> bool:
        """Validate application configuration."""
        try:
            if not self.config.api.api_key:
                self._notify_error("API key is required")
                return False
            
            logger.info("Configuration validation passed")
            return True
            
        except Exception as e:
            logger.error(f"Configuration validation failed: {e}")
            self._notify_error("Configuration validation failed")
            return False
    
    def _validate_theme(self, theme: str) -> bool:
        """Validate theme name."""
        valid_themes = [
            "darkly", "flatly", "litera", "minty", "lumen",
            "sandstone", "yeti", "pulse", "united", "morph",
            "journal", "solar", "superhero", "cyborg"
        ]
        return theme in valid_themes
    
    def _validate_settings(self, settings: Dict[str, Any]) -> bool:
        """Validate settings dictionary."""
        # Add validation logic for specific settings
        return True
    
    def _initialize_components(self) -> None:
        """Initialize application components."""
        logger.info("Initializing application components")
        
        # Setup weather controller observers
        self.weather_controller.add_status_observer(self._notify_status)
        self.weather_controller.add_error_observer(self._notify_error)
        
        logger.info("Application components initialized")
    
    def _load_initial_data(self) -> None:
        """Load initial application data."""
        logger.info("Loading initial application data")
        
        # Load weather data for saved city if available
        current_city = config_manager.current_city
        if current_city and current_city.strip():
            self.weather_controller.load_weather_for_city(current_city)
        
        logger.info("Initial application data loaded")
    
    def _start_background_tasks(self) -> None:
        """Start background tasks."""
        logger.info("Starting background tasks")
        
        # Start auto-refresh task (using default 5 minute interval)
        refresh_task = threading.Thread(
            target=self._auto_refresh_task,
            daemon=True
        )
        refresh_task.start()
        self._background_tasks.append(refresh_task)
        
        logger.info("Background tasks started")
    
    def _stop_background_tasks(self) -> None:
        """Stop background tasks."""
        logger.info("Stopping background tasks")
        
        # Background tasks are daemon threads, they'll stop when main thread stops
        self._background_tasks.clear()
        
        logger.info("Background tasks stopped")
    
    def _auto_refresh_task(self) -> None:
        """Background task for auto-refreshing weather data."""
        refresh_interval = 300  # 5 minutes
        
        while self._is_running:
            try:
                time.sleep(refresh_interval)
                if self._is_running and self.weather_controller.is_data_loaded():
                    logger.debug("Auto-refreshing weather data")
                    self.weather_controller.refresh_weather_data()
            except Exception as e:
                logger.error(f"Error in auto-refresh task: {e}")
    
    def _save_application_state(self) -> None:
        """Save current application state."""
        try:
            logger.info("Saving application state")
            
            # Save current city if available
            if self.weather_controller.current_location:
                config_manager.save_settings(
                    city=self.weather_controller.current_weather.city if self.weather_controller.current_weather else None
                )
            
            logger.info("Application state saved")
            
        except Exception as e:
            logger.error(f"Failed to save application state: {e}")
    
    # Property accessors
    @property
    def is_running(self) -> bool:
        """Check if application is running."""
        return self._is_running
    
    @property
    def current_city(self) -> Optional[str]:
        """Get current city name."""
        if self.weather_controller.current_weather:
            return self.weather_controller.current_weather.city
        return config_manager.current_city
    
    @property
    def current_theme(self) -> str:
        """Get current theme."""
        return config_manager.current_theme
