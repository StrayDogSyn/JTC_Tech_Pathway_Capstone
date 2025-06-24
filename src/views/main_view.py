"""
Main View for the Weather Dashboard application.

This view coordinates the overall UI and provides the main interface between
the application controller and the user interface. It implements the main
view component of the MVC pattern.
"""

from typing import Optional, Callable, Dict, Any
from abc import ABC, abstractmethod

from .weather_view import WeatherView, TkinterWeatherView
from ..utils.logging import get_logger


logger = get_logger()


class MainView(ABC):
    """
    Abstract base class for the main application view.
    
    This class coordinates all sub-views and provides the main interface
    for the application controller.
    """
    
    def __init__(self):
        """Initialize the main view."""
        logger.info("Initializing Main View")
        
        # Sub-views
        self.weather_view: Optional[WeatherView] = None
        
        # Application-level callbacks
        self._theme_change_callback: Optional[Callable[[str], None]] = None
        self._settings_change_callback: Optional[Callable[[Dict[str, Any]], None]] = None
        
        logger.info("Main View initialized")
    
    # Abstract methods
    @abstractmethod
    def initialize_ui(self) -> None:
        """Initialize the user interface."""
        pass
    
    @abstractmethod
    def show(self) -> None:
        """Show the main view."""
        pass
    
    @abstractmethod
    def hide(self) -> None:
        """Hide the main view."""
        pass
    
    @abstractmethod
    def destroy(self) -> None:
        """Destroy the main view."""
        pass
    
    @abstractmethod
    def set_title(self, title: str) -> None:
        """Set the window title."""
        pass
    
    @abstractmethod
    def set_theme(self, theme: str) -> None:
        """Set the UI theme."""
        pass
    
    @abstractmethod
    def show_status(self, message: str) -> None:
        """Show status message."""
        pass
    
    @abstractmethod
    def show_error_message(self, title: str, message: str) -> None:
        """Show error message."""
        pass
    
    @abstractmethod
    def show_info_message(self, title: str, message: str) -> None:
        """Show info message."""
        pass
    
    # Callback management
    def set_theme_change_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for theme changes."""
        self._theme_change_callback = callback
    
    def set_settings_change_callback(self, callback: Callable[[Dict[str, Any]], None]) -> None:
        """Set callback for settings changes."""
        self._settings_change_callback = callback
    
    # Protected methods
    def _on_theme_change_requested(self, theme: str) -> None:
        """Handle theme change request."""
        if self._theme_change_callback:
            logger.info(f"Theme change requested: {theme}")
            self._theme_change_callback(theme)
    
    def _on_settings_change_requested(self, settings: Dict[str, Any]) -> None:
        """Handle settings change request."""
        if self._settings_change_callback:
            logger.info(f"Settings change requested: {settings}")
            self._settings_change_callback(settings)
    
    # Public interface
    def handle_status_update(self, message: str) -> None:
        """Handle status update from controller."""
        self.show_status(message)
    
    def handle_error(self, message: str) -> None:
        """Handle error from controller."""
        self.show_error_message("Error", message)
    
    def handle_theme_change(self, theme: str) -> None:
        """Handle theme change from controller."""
        try:
            self.set_theme(theme)
            logger.info(f"Theme changed to: {theme}")
        except Exception as e:
            logger.error(f"Error changing theme: {e}")
            self.show_error_message("Theme Error", f"Failed to change theme: {str(e)}")
    
    # Sub-view access
    def get_weather_view(self) -> Optional[WeatherView]:
        """Get the weather view."""
        return self.weather_view


class TkinterMainView(MainView):
    """
    Concrete implementation of MainView using Tkinter.
    
    This class wraps the existing Tkinter UI and provides the interface
    expected by the MVC architecture.
    """
    
    def __init__(self, ui_component):
        """Initialize with existing UI component."""
        super().__init__()
        self.ui = ui_component
        
        # Create weather view wrapper
        self.weather_view = TkinterWeatherView(ui_component)
        
        logger.info("Tkinter Main View initialized")
    
    def initialize_ui(self) -> None:
        """Initialize the user interface."""
        try:
            # The UI component should already be initialized
            # This method can be used for additional setup
            logger.info("UI initialized")
        except Exception as e:
            logger.error(f"Error initializing UI: {e}")
            raise
    
    def show(self) -> None:
        """Show the main view."""
        try:
            if hasattr(self.ui, 'root'):
                self.ui.root.deiconify()
            logger.info("Main view shown")
        except Exception as e:
            logger.error(f"Error showing main view: {e}")
    
    def hide(self) -> None:
        """Hide the main view."""
        try:
            if hasattr(self.ui, 'root'):
                self.ui.root.withdraw()
            logger.info("Main view hidden")
        except Exception as e:
            logger.error(f"Error hiding main view: {e}")
    
    def destroy(self) -> None:
        """Destroy the main view."""
        try:
            if hasattr(self.ui, 'root'):
                self.ui.root.destroy()
            logger.info("Main view destroyed")
        except Exception as e:
            logger.error(f"Error destroying main view: {e}")
    
    def set_title(self, title: str) -> None:
        """Set the window title."""
        try:
            if hasattr(self.ui, 'root'):
                self.ui.root.title(title)
            logger.info(f"Title set to: {title}")
        except Exception as e:
            logger.error(f"Error setting title: {e}")
    
    def set_theme(self, theme: str) -> None:
        """Set the UI theme."""
        try:
            if hasattr(self.ui, 'root') and hasattr(self.ui.root, 'style'):
                self.ui.root.style.theme_use(theme)
            logger.info(f"Theme set to: {theme}")
        except Exception as e:
            logger.error(f"Error setting theme: {e}")
            # Don't raise here as theme change might not be critical
    
    def show_status(self, message: str) -> None:
        """Show status message."""
        try:
            if hasattr(self.ui, 'update_status'):
                self.ui.update_status(message)
        except Exception as e:
            logger.error(f"Error showing status: {e}")
    
    def show_error_message(self, title: str, message: str) -> None:
        """Show error message."""
        try:
            if hasattr(self.ui, 'show_error'):
                self.ui.show_error(title, message)
            else:
                # Fallback to basic message box
                import tkinter.messagebox as messagebox
                messagebox.showerror(title, message)
        except Exception as e:
            logger.error(f"Error showing error message: {e}")
    
    def show_info_message(self, title: str, message: str) -> None:
        """Show info message."""
        try:
            if hasattr(self.ui, 'show_info'):
                self.ui.show_info(title, message)
            else:
                # Fallback to basic message box
                import tkinter.messagebox as messagebox
                messagebox.showinfo(title, message)
        except Exception as e:
            logger.error(f"Error showing info message: {e}")
    
    # Setup methods for connecting to existing UI
    def setup_callbacks(self) -> None:
        """Setup callbacks to connect view to controllers."""
        try:
            # Connect search callback
            if hasattr(self.ui, 'set_search_callback') and self.weather_view:
                self.ui.set_search_callback(self.weather_view._on_search_requested)
            
            # Connect theme change callback
            if hasattr(self.ui, 'set_theme_change_callback'):
                self.ui.set_theme_change_callback(self._on_theme_change_requested)
            
            logger.info("View callbacks setup completed")
        except Exception as e:
            logger.error(f"Error setting up callbacks: {e}")
    
    def set_weather_callbacks(self, search_callback: Callable[[str], None], 
                            refresh_callback: Callable[[], None]) -> None:
        """Set weather-related callbacks."""
        if self.weather_view:
            self.weather_view.set_search_callback(search_callback)
            self.weather_view.set_refresh_callback(refresh_callback)
