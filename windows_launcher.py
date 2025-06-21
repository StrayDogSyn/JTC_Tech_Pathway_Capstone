"""
Enhanced Weather Dashboard Launcher - Windows Compatible Version
===============================================================

A robust launcher for the enhanced weather dashboard with Windows Unicode compatibility.
This launcher provides graceful fallbacks and comprehensive error handling.
"""

import sys
import os
import logging
import traceback
from pathlib import Path
import importlib.util

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

class WindowsCompatibleLauncher:
    """Windows-compatible launcher for the enhanced weather dashboard."""
    
    def __init__(self):
        """Initialize the launcher with Windows-compatible logging."""
        self.setup_logging()
        self.logger.info("Enhanced Weather Dashboard starting...")
        
    def setup_logging(self):
        """Set up Windows-compatible logging without Unicode characters."""
        log_format = '%(asctime)s - %(levelname)s - %(message)s'
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('weather_dashboard.log', encoding='utf-8')
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def check_enhanced_ui_available(self) -> bool:
        """Check if enhanced UI components are available."""
        try:
            from src.ui.modern_components import ModernCard
            from src.ui.enhanced_dashboard import EnhancedWeatherDashboardUI
            from src.ui.dashboard_ui import WeatherDashboardUI
            return True
        except ImportError as e:
            self.logger.warning(f"Enhanced UI components not available: {e}")
            return False
    
    def launch_enhanced_ui(self):
        """Launch the enhanced weather dashboard UI."""
        try:
            self.logger.info("Launching Enhanced Weather Dashboard UI...")
            
            # Import the enhanced dashboard
            from src.ui.dashboard_ui import WeatherDashboardUI
            
            # Create and run the dashboard
            dashboard = WeatherDashboardUI(
                title="Enhanced Weather Intelligence Platform",
                theme="darkly",
                size=(1500, 950)
            )
            
            # Set up callbacks
            dashboard.set_search_callback(self.handle_search)
            dashboard.set_theme_change_callback(self.handle_theme_change)
            
            self.logger.info("Enhanced UI launched successfully")
            
            # Run the main loop
            dashboard.run()
            
        except Exception as e:
            self.logger.error(f"Enhanced UI failed: {e}")
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            raise
    
    def launch_alternative_ui(self):
        """Launch alternative UI from enhanced_dashboard.py."""
        try:
            self.logger.info("Launching alternative enhanced UI...")
            
            from src.ui.enhanced_dashboard import EnhancedWeatherDashboardUI
            
            dashboard = EnhancedWeatherDashboardUI(
                title="Enhanced Weather Dashboard",
                theme="darkly",
                size=(1400, 900)
            )
            
            # Set up callbacks
            dashboard.set_search_callback(self.handle_search)
            dashboard.set_theme_change_callback(self.handle_theme_change)
            
            self.logger.info("Alternative UI launched successfully")
            
            # Run the main loop
            dashboard.run()
            
        except Exception as e:
            self.logger.error(f"Alternative UI failed: {e}")
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            raise
    
    def launch_fallback(self):
        """Launch fallback weather application."""
        try:
            self.logger.info("Launching fallback weather application...")
            
            # Try various fallback options
            fallback_apps = [
                "complete_weather_dashboard.py",
                "cobra_weather_app.py", 
                "launcher.py"
            ]
            
            for app in fallback_apps:
                if os.path.exists(app):
                    self.logger.info(f"Running {app}...")
                    os.system(f'python "{app}"')
                    return
            
            self.logger.error("No fallback applications found")
            
        except Exception as e:
            self.logger.error(f"Fallback launch failed: {e}")
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
    
    def handle_search(self, query: str):
        """Handle search queries."""
        self.logger.info(f"Search query: {query}")
        # Add search logic here
    
    def handle_theme_change(self, theme: str):
        """Handle theme changes."""
        self.logger.info(f"Theme changed to: {theme}")
        # Add theme change logic here
    
    def run(self):
        """Run the launcher with fallback options."""
        try:
            print("Enhanced Weather Dashboard Launcher")
            print("=" * 50)
            print("Initializing advanced weather intelligence platform...")
            
            if self.check_enhanced_ui_available():
                self.logger.info("Enhanced UI components available")
                try:
                    self.launch_enhanced_ui()
                except Exception as e:
                    self.logger.warning(f"Enhanced UI failed, trying alternative: {e}")
                    try:
                        self.launch_alternative_ui()
                    except Exception as e2:
                        self.logger.warning(f"Alternative UI failed: {e2}")
                        self.launch_fallback()
            else:
                self.logger.warning("Enhanced UI not available, launching fallback")
                self.launch_fallback()
                
        except Exception as e:
            self.logger.error(f"Application error: {e}")
            self.logger.debug(f"Traceback: {traceback.format_exc()}")
            print(f"Error: {e}")
            print("Trying fallback options...")
            self.launch_fallback()


def main():
    """Main entry point."""
    launcher = WindowsCompatibleLauncher()
    launcher.run()


if __name__ == "__main__":
    main()
