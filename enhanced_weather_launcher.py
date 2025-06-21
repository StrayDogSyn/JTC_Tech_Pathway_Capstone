#!/usr/bin/env python3
"""
Enhanced Weather Dashboard Application

This launcher provides an enhanced weather dashboard with modern UX/UI features
built on top of the existing weather application architecture.
"""

import sys
import os
import logging
import threading
import time
from typing import Optional

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(__file__))

try:
    # Try to import enhanced components
    from src.ui.dashboard_ui import WeatherDashboardUI
    from src.ui.weather_displays import EnhancedWeatherDisplays
    ENHANCED_UI_AVAILABLE = True
except ImportError:
    ENHANCED_UI_AVAILABLE = False

try:
    # Try to import existing weather components
    import complete_weather_dashboard
    EXISTING_APP_AVAILABLE = True
except ImportError:
    EXISTING_APP_AVAILABLE = False


class EnhancedWeatherLauncher:
    """Enhanced weather application launcher with modern UX features."""
    
    def __init__(self):
        """Initialize the enhanced weather launcher."""
        self.setup_logging()
        self.logger.info("🚀 Enhanced Weather Dashboard starting...")
    
    def setup_logging(self):
        """Setup application logging."""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('enhanced_weather.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def launch_enhanced_ui(self):
        """Launch the enhanced UI if available."""
        try:
            self.logger.info("🎨 Launching Enhanced Weather Dashboard UI...")
            
            # Create enhanced dashboard
            dashboard = WeatherDashboardUI(
                title="🌦️ Enhanced Weather Intelligence Platform",
                theme="darkly", 
                size=(1500, 950)
            )
            
            # Setup some demo callbacks for now
            dashboard.set_search_callback(self._demo_search_callback)
            dashboard.set_theme_change_callback(self._demo_theme_callback)
            
            # Show startup notification
            self._show_startup_notification(dashboard)
            
            # Run the dashboard            dashboard.run()
            
        except Exception as e:
            self.logger.error(f"❌ Enhanced UI failed: {e}")
            raise
    
    def _demo_search_callback(self, city: str):
        """Demo search callback."""
        self.logger.info(f"🔍 Demo search for: {city}")
        # TODO: Integrate with actual weather API
    
    def _demo_theme_callback(self, theme: str):
        """Demo theme change callback."""
        self.logger.info(f"🎨 Theme changed to: {theme}")
    
    def _show_startup_notification(self, dashboard):
        """Show startup notification after delay."""
        def show_notification():
            time.sleep(1.5)  # Wait for UI to load
            try:
                if hasattr(dashboard, 'show_notification'):
                    dashboard.show_notification(
                        "🚀 Enhanced Weather Dashboard loaded successfully!",
                        "success",
                        4000
                    )
                dashboard.update_status("✅ Enhanced Weather Dashboard ready!")
            except Exception as e:
                self.logger.warning(f"Notification failed: {e}")
        
        threading.Thread(target=show_notification, daemon=True).start()
    
    def launch_existing_app(self):
        """Launch the existing weather application."""
        try:
            self.logger.info("🔄 Launching existing weather application...")
            complete_weather_dashboard.main()
        except Exception as e:
            self.logger.error(f"❌ Existing app failed: {e}")
            raise
    
    def launch_fallback(self):
        """Launch fallback weather app."""
        try:
            self.logger.info("🔄 Launching fallback weather application...")
            
            # Try other weather apps in the directory
            fallback_apps = [
                'cobra_weather_app.py',
                'launcher.py'
            ]
            
            for app in fallback_apps:
                if os.path.exists(app):
                    self.logger.info(f"🚀 Running {app}...")
                    os.system(f'python "{app}"')
                    return
            
            # If no apps found, show a simple message
            print("🌦️ Weather Dashboard")
            print("=" * 40)
            print("Welcome to the Weather Intelligence Platform!")
            print("Enhanced UI components are not fully available.")
            print("Please ensure all dependencies are installed.")
            print("\nTo get started:")
            print("1. Install required packages: pip install -r requirements.txt")
            print("2. Check that all source files are present")
            print("3. Run: python advanced_weather_launcher.py")
            
        except Exception as e:
            self.logger.error(f"❌ Fallback failed: {e}")
            print(f"Error: {e}")
    
    def run(self):
        """Run the appropriate weather application."""
        try:
            if ENHANCED_UI_AVAILABLE:
                self.logger.info("✅ Enhanced UI components available")
                self.launch_enhanced_ui()
            elif EXISTING_APP_AVAILABLE:
                self.logger.info("⚠️ Enhanced UI not available, using existing app")
                self.launch_existing_app()
            else:
                self.logger.warning("⚠️ No weather apps available, using fallback")
                self.launch_fallback()
                
        except KeyboardInterrupt:
            self.logger.info("👋 Application interrupted by user")
        except Exception as e:
            self.logger.error(f"❌ Application error: {e}")
            print(f"\n❌ Error: {e}")
            print("\nTrying fallback options...")
            self.launch_fallback()


def main():
    """Main application entry point."""
    print("🌦️ Enhanced Weather Dashboard Launcher")
    print("=" * 50)
    print("Initializing advanced weather intelligence platform...")
    print()
    
    launcher = EnhancedWeatherLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
