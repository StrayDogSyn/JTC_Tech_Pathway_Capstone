"""
Main weather dashboard application.

This is the main entry point that coordinates between UI and business logic,
maintaining clean separation of concerns.
"""

import sys
import os
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.weather_core import WeatherDashboardCore
from src.config.config import config_manager, APP_CONFIG, setup_environment
from src.ui.glassmorphic_dashboard import GlassmorphicWeatherDashboard
from src.ui.glassmorphic_weather_displays import WeatherDisplays
from src.utils.logging import get_logger, get_ui_logger

# Initialize loggers
logger = get_logger()
ui_logger = get_ui_logger()


class WeatherDashboardApp:
    """Main weather dashboard application coordinator."""
    
    def __init__(self):
        """Initialize the weather dashboard application."""
        logger.info("Initializing Weather Dashboard Application")
        
        # Set up environment
        setup_environment()
        
        # Initialize business logic
        self.core = WeatherDashboardCore()
          # Initialize UI with glassmorphic design
        self.ui = GlassmorphicWeatherDashboard(
            title=APP_CONFIG["title"],
            theme=config_manager.current_theme,
            size=APP_CONFIG["default_size"]
        )
        # Set up callbacks between UI and business logic
        self._setup_callbacks()
        
        # Load initial data
        self._load_initial_data()
        
        logger.info("Weather Dashboard Application initialized successfully")
    
    def _setup_callbacks(self) -> None:
        """Set up callbacks between UI and business logic."""
        # UI callbacks to business logic
        self.ui.set_search_callback(self._on_search)
        self.ui.set_theme_change_callback(self._on_theme_change)
        
        # Business logic callbacks to UI
        self.core.set_status_callback(self.ui.update_status)
        self.core.set_data_update_callback(self._update_displays)
    
    def _load_initial_data(self) -> None:
        """Load initial weather data for the default city."""
        logger.info("Loading initial application data")
        
        # Set initial UI state
        self.ui.set_city_text(config_manager.current_city)
        self.ui.set_theme(config_manager.current_theme)
        
        # Load data for the saved city if available
        if config_manager.current_city and config_manager.current_city.strip():
            self.core.load_weather_data(config_manager.current_city)
    
    def _on_search(self, city: str) -> None:
        """Handle search request from UI."""
        if city:
            ui_logger.log_user_action("search", {"city": city})
            self.core.load_weather_data(city)    
    
    def _on_theme_change(self, theme: str) -> None:
        """Handle theme change request from UI."""
        if theme:
            ui_logger.log_user_action("theme_change", {"theme": theme})
            config_manager.save_settings(theme=theme)
            self.ui.show_info("Theme Changed", 
                             f"Theme changed to {theme}. Restart the app to see full effect.")
    
    def _update_displays(self) -> None:
        """Update all display areas with current data from business logic."""
        # Update current weather
        if self.ui.weather_frame:
            WeatherDisplays.update_current_weather(
                self.ui.weather_frame, 
                self.core.current_weather
            )
        
        # Update air quality
        if self.ui.air_quality_frame:
            WeatherDisplays.update_air_quality(
                self.ui.air_quality_frame, 
                self.core.air_quality_data
            )
        
        # Update forecast
        if self.ui.forecast_frame:
            WeatherDisplays.update_forecast(
                self.ui.forecast_frame, 
                self.core.forecast_data
            )
        
        # Update predictions (basic for now, can be enhanced with ML)
        if self.ui.predictions_frame:
            WeatherDisplays.update_predictions(
                self.ui.predictions_frame, 
                self.core.forecast_data
            )
    
    def run(self) -> None:
        """Start the application."""
        try:
            self.ui.run()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
            self.ui.show_error("Application Error", f"An error occurred: {e}")


def main():
    """Main entry point."""
    try:
        app = WeatherDashboardApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        # Try to show error dialog if possible
        try:
            from tkinter import messagebox
            messagebox.showerror("Startup Error", f"Failed to start application: {e}")
        except:
            pass


if __name__ == "__main__":
    main()
