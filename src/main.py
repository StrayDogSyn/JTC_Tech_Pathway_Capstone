"""
Refactored main weather dashboard application implementing MVC architecture.

This is the main entry point that coordinates between the new MVC components,
maintaining clean separation of concerns and proper architectural patterns.
"""

import sys
import os
from typing import Optional
from dataclasses import asdict

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

# Import new MVC components
from src.controllers.application_controller import ApplicationController
from src.views.main_view import TkinterMainView
from src.business.weather_service import WeatherService
from src.business.notification_service import NotificationService
from src.business.settings_service import SettingsService

# Import existing components
from src.config.config import config_manager, APP_CONFIG, setup_environment
from src.ui.dashboard_ui import WeatherDashboardUI
from src.utils.logging import get_logger, get_ui_logger

# Initialize loggers
logger = get_logger()
ui_logger = get_ui_logger()


class WeatherDashboardApp:
    """
    Refactored weather dashboard application using MVC architecture.
    
    This class now serves as a facade that coordinates the new MVC components
    while maintaining backward compatibility with the existing UI components.
    """
    
    def __init__(self):
        """Initialize the weather dashboard application with MVC architecture."""
        logger.info("Initializing Weather Dashboard Application with MVC Architecture")
        
        # Set up environment
        setup_environment()
        
        # Initialize business services
        self.weather_service = WeatherService()
        self.notification_service = NotificationService()
        self.settings_service = SettingsService()
        
        # Initialize application controller
        self.app_controller = ApplicationController()
        
        # Initialize UI component (legacy)
        self.ui = WeatherDashboardUI(
            title=APP_CONFIG["title"],
            theme=config_manager.current_theme,
            size=APP_CONFIG["default_size"]
        )
        
        # Initialize view abstraction
        self.main_view = TkinterMainView(self.ui)
        
        # Set up MVC connections
        self._setup_mvc_architecture()
        
        # Load initial data
        self._load_initial_data()
        
        logger.info("Weather Dashboard Application with MVC Architecture initialized successfully")
    
    def _setup_mvc_architecture(self) -> None:
        """Set up the MVC architecture connections."""
        logger.info("Setting up MVC architecture connections")
        
        # Connect View to Controller (user actions)
        self._connect_view_to_controller()
        
        # Connect Controller to View (data updates and notifications)
        self._connect_controller_to_view()
        
        # Setup business service connections
        self._setup_business_services()
        
        logger.info("MVC architecture connections established")
    
    def _connect_view_to_controller(self) -> None:
        """Connect view events to controller methods."""
        weather_view = self.main_view.get_weather_view()
        
        if weather_view:
            # Weather search
            def search_handler(city: str) -> None:
                success = self.app_controller.search_weather(city)
                if success:
                    self.notification_service.notify_success(
                        "Search Complete", 
                        f"Weather data loaded for {city}"
                    )
                else:
                    self.notification_service.notify_error(
                        "Search Failed", 
                        f"Could not load weather data for {city}"
                    )
            
            weather_view.set_search_callback(search_handler)
            
            # Weather refresh
            def refresh_handler() -> None:
                success = self.app_controller.refresh_weather()
                if success:
                    self.notification_service.notify_info(
                        "Data Refreshed", 
                        "Weather data has been updated"
                    )
                else:
                    self.notification_service.notify_warning(
                        "Refresh Failed", 
                        "Could not refresh weather data"
                    )
            
            weather_view.set_refresh_callback(refresh_handler)
        
        # Theme changes
        def theme_handler(theme: str) -> None:
            success = self.app_controller.change_theme(theme)
            if success:
                self.notification_service.notify_success(
                    "Theme Changed", 
                    f"Theme changed to {theme}"
                )
        
        self.main_view.set_theme_change_callback(theme_handler)
    
    def _connect_controller_to_view(self) -> None:
        """Connect controller events to view updates."""
        weather_view = self.main_view.get_weather_view()
        
        if weather_view:
            # Weather data updates
            self.app_controller.weather_controller.add_weather_update_observer(
                weather_view.handle_weather_update
            )
            
            self.app_controller.weather_controller.add_forecast_update_observer(
                weather_view.handle_forecast_update
            )
            
            self.app_controller.weather_controller.add_air_quality_update_observer(
                weather_view.handle_air_quality_update
            )
            
            # Status and error updates
            self.app_controller.weather_controller.add_status_observer(
                weather_view.handle_status_update
            )
            
            self.app_controller.weather_controller.add_error_observer(
                weather_view.handle_error
            )
        
        # Application-level updates
        self.app_controller.add_status_observer(
            self.main_view.handle_status_update
        )
        
        self.app_controller.add_error_observer(
            self.main_view.handle_error
        )
        
        self.app_controller.add_theme_change_observer(
            self.main_view.handle_theme_change
        )
    
    def _setup_business_services(self) -> None:
        """Setup connections to business services."""
        # Connect notification service to UI
        def notification_handler(notification) -> None:
            if hasattr(self.ui, 'show_notification'):
                self.ui.show_notification(
                    notification.title, 
                    notification.message, 
                    notification.level.value
                )
        
        self.notification_service.add_notification_handler(notification_handler)
        
        # Connect settings service to configuration changes
        def settings_change_handler(key: str, old_value, new_value) -> None:
            logger.info(f"Setting changed: {key} = {new_value}")
            ui_logger.log_user_action("setting_change", {
                "key": key, 
                "old_value": str(old_value), 
                "new_value": str(new_value)
            })
        
        self.settings_service.add_change_observer(settings_change_handler)
    
    def _load_initial_data(self) -> None:
        """Load initial weather data for the default city."""
        logger.info("Loading initial application data")
        
        # Set initial UI state
        self.ui.set_city_text(config_manager.current_city)
        self.ui.set_theme(config_manager.current_theme)
        
        # Load data for the saved city if available
        if config_manager.current_city and config_manager.current_city.strip():
            self.app_controller.search_weather(config_manager.current_city)
    
    # Legacy callback methods for backward compatibility
    def _on_search(self, city: str) -> None:
        """Handle search request from UI (legacy compatibility)."""
        if city:
            ui_logger.log_user_action("search", {"city": city})
            success = self.app_controller.search_weather(city)
            if not success:
                self.ui.show_error("Search Error", f"Could not find weather data for {city}")
    
    def _on_theme_change(self, theme: str) -> None:
        """Handle theme change request from UI (legacy compatibility)."""
        if theme:
            ui_logger.log_user_action("theme_change", {"theme": theme})
            success = self.app_controller.change_theme(theme)
            if success:
                self.ui.show_info("Theme Changed", 
                                 f"Theme changed to {theme}. Restart the app to see full effect.")
    
    def _update_displays(self) -> None:
        """Update all display areas with current data (legacy compatibility)."""
        weather_controller = self.app_controller.weather_controller
        
        # Update current weather
        current_weather = weather_controller.get_current_weather()
        if current_weather:
            self.ui.update_weather_display(asdict(current_weather))
        
        # Update air quality
        air_quality = weather_controller.get_air_quality_data()
        if air_quality:
            self.ui.update_air_quality_display(asdict(air_quality))
        
        # Update forecast
        forecast = weather_controller.get_forecast_data()
        if forecast:
            self.ui.update_forecast_display(asdict(forecast))
    
    def run(self) -> None:
        """Run the weather dashboard application."""
        try:
            logger.info("Starting Weather Dashboard Application")
            
            # Start the application controller
            if not self.app_controller.start():
                logger.error("Failed to start application controller")
                return
            
            # Set up legacy callbacks for backward compatibility
            self.ui.set_search_callback(self._on_search)
            self.ui.set_theme_change_callback(self._on_theme_change)
            
            # Start the UI
            self.ui.run()
            
        except KeyboardInterrupt:
            logger.info("Application interrupted by user")
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise
        finally:
            self._cleanup()
    
    def _cleanup(self) -> None:
        """Cleanup application resources."""
        try:
            logger.info("Cleaning up application resources")
            
            # Stop services
            self.notification_service.stop()
            self.app_controller.stop()
            
            logger.info("Application cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


def main():
    """Main entry point."""
    try:
        app = WeatherDashboardApp()
        app.run()
    except Exception as e:
        logger.critical(f"Critical application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
