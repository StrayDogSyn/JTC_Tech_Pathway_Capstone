#!/usr/bin/env python3
"""
Advanced Weather Dashboard Application

This is the main entry point for the advanced weather dashboard with modern UX/UI features.
"""

import sys
import os
import logging
from typing import Optional
import threading
import time

# Add src directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    from src.ui.dashboard_ui import WeatherDashboardUI
    from src.ui.enhanced_dashboard import EnhancedWeatherDashboard
    from src.ui.weather_displays import EnhancedWeatherDisplays
    from src.core.weather_core import WeatherCore
    from src.config.app_config import AppConfig
    UI_MODULES_AVAILABLE = True
except ImportError as e:
    print(f"Error importing UI modules: {e}")
    print("Falling back to legacy weather app...")
    UI_MODULES_AVAILABLE = False


class AdvancedWeatherApp:
    """Advanced weather application with modern UX/UI features."""
    
    def __init__(self):
        """Initialize the advanced weather application."""
        self.config = AppConfig()
        self.weather_core: Optional[WeatherCore] = None
        self.ui: Optional[WeatherDashboardUI] = None
        self.enhanced_ui: Optional[EnhancedWeatherDashboard] = None
        
        # Setup logging
        self._setup_logging()
        
        # Initialize components
        self._initialize_components()
    
    def _setup_logging(self):
        """Setup application logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('weather_app.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
        self.logger.info("🚀 Advanced Weather Dashboard starting up...")
    
    def _initialize_components(self):
        """Initialize application components."""
        try:
            # Initialize weather core
            self.weather_core = WeatherCore()
            
            # Initialize UI based on availability of enhanced components
            self._initialize_ui()
            
            # Setup callbacks between core and UI
            self._setup_callbacks()
            
            self.logger.info("✅ Application components initialized successfully")
            
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize components: {e}")
            raise
    
    def _initialize_ui(self):
        """Initialize the user interface."""
        try:
            # Try to use enhanced dashboard first
            try:
                self.enhanced_ui = EnhancedWeatherDashboard(
                    title="🌦️ Advanced Weather Intelligence Platform",
                    theme="darkly",
                    size=(1600, 1000)
                )
                self.ui = self.enhanced_ui
                self.logger.info("🎨 Using Enhanced Weather Dashboard UI")
                
            except Exception as e:
                self.logger.warning(f"Enhanced UI not available: {e}")
                
                # Fallback to standard dashboard
                self.ui = WeatherDashboardUI(
                    title="🌦️ Weather Dominator Pro",
                    theme="darkly",
                    size=(1400, 900)
                )
                self.logger.info("🎨 Using Standard Weather Dashboard UI")
                
        except Exception as e:
            self.logger.error(f"❌ Failed to initialize UI: {e}")
            raise
    
    def _setup_callbacks(self):
        """Setup callbacks between UI and business logic."""
        if not self.ui or not self.weather_core:
            return
        
        # Set UI callbacks
        self.ui.set_search_callback(self._on_search)
        self.ui.set_theme_change_callback(self._on_theme_change)
        
        if hasattr(self.ui, 'set_auto_refresh_callback'):
            self.ui.set_auto_refresh_callback(self._on_auto_refresh)
        
        # Set weather core callbacks
        self.weather_core.set_weather_callback(self._on_weather_update)
        self.weather_core.set_forecast_callback(self._on_forecast_update)
        self.weather_core.set_air_quality_callback(self._on_air_quality_update)
        self.weather_core.set_status_callback(self._on_status_update)
        self.weather_core.set_error_callback(self._on_error)
        
        self.logger.info("🔗 Callbacks configured successfully")
    
    def _on_search(self, city: str):
        """Handle search request from UI."""
        self.logger.info(f"🔍 Searching for weather data: {city}")
        
        # Show loading state
        if hasattr(self.ui, 'set_loading'):
            self.ui.set_loading(True)
        
        # Update status
        self.ui.update_status(f"🔍 Searching weather data for {city}...")
        
        # Perform search in background
        threading.Thread(
            target=self._perform_search,
            args=(city,),
            daemon=True
        ).start()
    
    def _perform_search(self, city: str):
        """Perform weather search in background thread."""
        try:
            self.weather_core.get_weather_data(city)
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            self._on_error("Search Error", str(e))
        finally:
            # Hide loading state
            if hasattr(self.ui, 'set_loading'):
                self.ui.set_loading(False)
    
    def _on_theme_change(self, theme: str):
        """Handle theme change from UI."""
        self.logger.info(f"🎨 Changing theme to: {theme}")
        
        try:
            # Update theme in config
            self.config.set_theme(theme)
            
            # Show notification
            if hasattr(self.ui, 'show_notification'):
                self.ui.show_notification(f"Theme changed to {theme}", "success")
            
            self.ui.update_status(f"🎨 Theme changed to {theme}")
            
        except Exception as e:
            self.logger.error(f"Theme change failed: {e}")
            self._on_error("Theme Error", str(e))
    
    def _on_auto_refresh(self, enabled: bool):
        """Handle auto-refresh toggle from UI."""
        self.logger.info(f"🔄 Auto-refresh {'enabled' if enabled else 'disabled'}")
        
        if enabled:
            self.weather_core.start_auto_refresh()
            if hasattr(self.ui, 'show_notification'):
                self.ui.show_notification("Auto-refresh enabled (5 minutes)", "info")
        else:
            self.weather_core.stop_auto_refresh()
            if hasattr(self.ui, 'show_notification'):
                self.ui.show_notification("Auto-refresh disabled", "info")
    
    def _on_weather_update(self, weather_data):
        """Handle weather data update from core."""
        self.logger.info(f"🌤️ Weather data updated for {weather_data.city}")
        
        # Update current weather display
        if hasattr(self.ui, 'weather_frame') and self.ui.weather_frame:
            if hasattr(EnhancedWeatherDisplays, 'create_modern_weather_card'):
                # Clear existing content
                for widget in self.ui.weather_frame.winfo_children():
                    widget.destroy()
                
                # Create modern weather card
                weather_card = EnhancedWeatherDisplays.create_modern_weather_card(
                    self.ui.weather_frame, weather_data
                )
                weather_card.pack(fill="both", expand=True)
            else:
                # Fallback to basic display
                from src.ui.weather_displays import WeatherDisplays
                WeatherDisplays.update_current_weather(self.ui.weather_frame, weather_data)
        
        # Update status
        self.ui.update_status(f"🌤️ Weather updated for {weather_data.city}, {weather_data.country}")
        
        # Show success notification
        if hasattr(self.ui, 'show_notification'):
            self.ui.show_notification(
                f"Weather data loaded for {weather_data.city}",
                "success",
                3000
            )
    
    def _on_forecast_update(self, forecast_data):
        """Handle forecast data update from core."""
        self.logger.info("📊 Forecast data updated")
        
        # Update forecast display
        if hasattr(self.ui, 'forecast_frame') and self.ui.forecast_frame:
            if hasattr(EnhancedWeatherDisplays, 'create_enhanced_forecast_display'):
                # Clear existing content
                for widget in self.ui.forecast_frame.winfo_children():
                    widget.destroy()
                
                # Create enhanced forecast display
                forecast_card = EnhancedWeatherDisplays.create_enhanced_forecast_display(
                    self.ui.forecast_frame, forecast_data
                )
                forecast_card.pack(fill="both", expand=True)
            else:
                # Fallback to basic display
                from src.ui.weather_displays import WeatherDisplays
                WeatherDisplays.update_forecast(self.ui.forecast_frame, forecast_data)
    
    def _on_air_quality_update(self, air_quality_data):
        """Handle air quality data update from core."""
        self.logger.info("🌬️ Air quality data updated")
        
        # Update air quality display
        if hasattr(self.ui, 'air_quality_frame') and self.ui.air_quality_frame:
            if hasattr(EnhancedWeatherDisplays, 'create_enhanced_air_quality_display'):
                # Clear existing content
                for widget in self.ui.air_quality_frame.winfo_children():
                    widget.destroy()
                
                # Create enhanced air quality display
                air_quality_card = EnhancedWeatherDisplays.create_enhanced_air_quality_display(
                    self.ui.air_quality_frame, air_quality_data
                )
                air_quality_card.pack(fill="both", expand=True)
            else:
                # Fallback to basic display
                from src.ui.weather_displays import WeatherDisplays
                WeatherDisplays.update_air_quality(self.ui.air_quality_frame, air_quality_data)
    
    def _on_status_update(self, message: str):
        """Handle status update from core."""
        self.ui.update_status(message)
    
    def _on_error(self, title: str, message: str):
        """Handle error from core."""
        self.logger.error(f"{title}: {message}")
        self.ui.show_error(title, message)
        
        # Hide loading state on error
        if hasattr(self.ui, 'set_loading'):
            self.ui.set_loading(False)
    
    def show_startup_notification(self):
        """Show startup notification."""
        if hasattr(self.ui, 'show_notification'):
            self.ui.show_notification(
                "🚀 Advanced Weather Dashboard loaded successfully!",
                "success",
                4000
            )
    
    def run(self):
        """Run the application."""
        try:
            self.logger.info("🚀 Starting Advanced Weather Dashboard...")
            
            # Show startup notification after a short delay
            threading.Timer(1.0, self.show_startup_notification).start()
            
            # Start the UI main loop
            self.ui.run()
            
        except KeyboardInterrupt:
            self.logger.info("👋 Application interrupted by user")
        except Exception as e:
            self.logger.error(f"❌ Application error: {e}")
            raise
        finally:
            self._cleanup()
    
    def _cleanup(self):
        """Cleanup application resources."""
        self.logger.info("🧹 Cleaning up application resources...")
        
        try:
            if self.weather_core:
                self.weather_core.cleanup()
            
            if self.ui:
                self.ui.destroy()
                
        except Exception as e:
            self.logger.error(f"Error during cleanup: {e}")


def main():
    """Main application entry point."""
    try:
        if not UI_MODULES_AVAILABLE:
            # Fallback to simple weather app
            print("🔄 Falling back to legacy weather application...")
            try:
                import cobra_weather_app
                cobra_weather_app.main()
            except ImportError:
                print("❌ No weather application available. Please check your installation.")
                sys.exit(1)
            return
        
        # Create and run advanced weather app
        app = AdvancedWeatherApp()
        app.run()
        
    except Exception as e:
        print(f"❌ Failed to start application: {e}")
        logging.error(f"Application startup failed: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
