"""
Refactored main application entry point implementing proper MVC architecture.

This module coordinates the application components using the MVC pattern,
ensuring proper separation of concerns, loose coupling, and high cohesion.
"""

import sys
import os
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.controllers.application_controller import ApplicationController
from src.views.main_view import TkinterMainView
from src.ui.dashboard_ui import WeatherDashboardUI
from src.config.config import config_manager, APP_CONFIG
from src.utils.logging import get_logger


logger = get_logger()


class WeatherDashboardMVCApp:
    """
    Main application class implementing MVC architecture.
    
    This class coordinates the Model-View-Controller components and ensures
    proper separation of concerns throughout the application.
    
    Architecture:
    - Controller: ApplicationController (business logic coordination)
    - View: MainView (UI abstraction) -> TkinterMainView (concrete implementation)
    - Model: WeatherData, ForecastData, etc. (data models)
    """
    
    def __init__(self):
        """Initialize the MVC application."""
        logger.info("Initializing Weather Dashboard MVC Application")
        
        # Initialize the controller (business logic layer)
        self.application_controller = ApplicationController()
        
        # Initialize the UI component (existing implementation)
        self.ui_component = WeatherDashboardUI(
            title=APP_CONFIG["title"],
            theme=config_manager.current_theme,
            size=APP_CONFIG["default_size"]
        )
        
        # Initialize the view (UI abstraction layer)
        self.main_view = TkinterMainView(self.ui_component)
        
        # Setup the MVC connections
        self._setup_mvc_connections()
        
        logger.info("Weather Dashboard MVC Application initialized successfully")
    
    def _setup_mvc_connections(self) -> None:
        """
        Setup connections between Model, View, and Controller components.
        
        This method implements the observer pattern to ensure loose coupling
        between components while maintaining proper communication channels.
        """
        logger.info("Setting up MVC connections")
        
        # Setup View -> Controller connections (user actions)
        self._setup_view_to_controller_connections()
        
        # Setup Controller -> View connections (data updates and notifications)
        self._setup_controller_to_view_connections()
        
        # Setup View callbacks for UI events
        self.main_view.setup_callbacks()
        
        logger.info("MVC connections established")
    
    def _setup_view_to_controller_connections(self) -> None:
        """Setup connections from View to Controller (user actions)."""
        weather_view = self.main_view.get_weather_view()
        
        if weather_view:
            # Connect search functionality with wrapper
            def search_wrapper(city: str) -> None:
                self.application_controller.search_weather(city)
            
            weather_view.set_search_callback(search_wrapper)
            
            # Connect refresh functionality with wrapper
            def refresh_wrapper() -> None:
                self.application_controller.refresh_weather()
            
            weather_view.set_refresh_callback(refresh_wrapper)
        
        # Connect theme change functionality with wrapper
        def theme_change_wrapper(theme: str) -> None:
            self.application_controller.change_theme(theme)
        
        self.main_view.set_theme_change_callback(theme_change_wrapper)
        
        # Connect settings change functionality with wrapper
        def settings_change_wrapper(settings: dict) -> None:
            self.application_controller.update_settings(**settings)
        
        self.main_view.set_settings_change_callback(settings_change_wrapper)
    
    def _setup_controller_to_view_connections(self) -> None:
        """Setup connections from Controller to View (data updates)."""
        weather_view = self.main_view.get_weather_view()
        
        # Application-level observers
        self.application_controller.add_status_observer(
            self.main_view.handle_status_update
        )
        
        self.application_controller.add_error_observer(
            self.main_view.handle_error
        )
        
        self.application_controller.add_theme_change_observer(
            self.main_view.handle_theme_change
        )
        
        if weather_view:
            # Weather controller observers
            weather_controller = self.application_controller.weather_controller
            
            weather_controller.add_weather_update_observer(
                weather_view.handle_weather_update
            )
            
            weather_controller.add_forecast_update_observer(
                weather_view.handle_forecast_update
            )
            
            weather_controller.add_air_quality_update_observer(
                weather_view.handle_air_quality_update
            )
            
            weather_controller.add_status_observer(
                weather_view.handle_status_update
            )
            
            weather_controller.add_error_observer(
                weather_view.handle_error
            )
    
    def run(self) -> None:
        """
        Run the application.
        
        This method starts the application controller and runs the UI main loop.
        The controller handles all business logic while the view handles presentation.
        """
        try:
            logger.info("Starting Weather Dashboard MVC Application")
            
            # Start the application controller
            if not self.application_controller.start():
                logger.error("Failed to start application controller")
                return
            
            # Initialize and show the main view
            self.main_view.initialize_ui()
            self.main_view.show()
            
            # Run the UI main loop
            if hasattr(self.ui_component, 'run'):
                self.ui_component.run()
            else:
                # Fallback to root mainloop
                self.ui_component.root.mainloop()
                
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
            
            # Stop the application controller
            self.application_controller.stop()
            
            # Destroy the view
            self.main_view.destroy()
            
            logger.info("Application cleanup completed")
            
        except Exception as e:
            logger.error(f"Error during cleanup: {e}")


def main() -> None:
    """Main entry point for the Weather Dashboard application."""
    try:
        # Create and run the MVC application
        app = WeatherDashboardMVCApp()
        app.run()
        
    except Exception as e:
        logger.critical(f"Critical application error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
