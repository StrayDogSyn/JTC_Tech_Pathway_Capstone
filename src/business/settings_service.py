"""
Settings Service for the Weather Dashboard application.

This service handles all settings and configuration management, providing
a centralized way to manage application preferences while maintaining
separation of concerns.
"""

from typing import Dict, Any, Optional, List, Callable
import json
from pathlib import Path
from datetime import datetime

from ..config.config import config_manager
from ..utils.logging import get_logger


logger = get_logger()


class SettingsService:
    """
    Service for managing application settings and preferences.
    
    This service provides a high-level interface for settings management,
    including validation, change notifications, and persistence.
    """
    
    def __init__(self):
        """Initialize the settings service."""
        logger.info("Initializing Settings Service")
        
        # Settings change observers
        self._change_observers: List[Callable[[str, Any, Any], None]] = []
        
        # Settings validation rules
        self._validation_rules: Dict[str, Callable[[Any], bool]] = {
            'theme': self._validate_theme,
            'city': self._validate_city,
            'auto_refresh_interval': self._validate_refresh_interval,
            'temperature_unit': self._validate_temperature_unit,
            'wind_speed_unit': self._validate_wind_speed_unit,
            'pressure_unit': self._validate_pressure_unit
        }
        
        # Default settings
        self._default_settings = {
            'theme': 'darkly',
            'city': '',
            'auto_refresh_interval': 300,  # 5 minutes
            'temperature_unit': 'celsius',
            'wind_speed_unit': 'ms',
            'pressure_unit': 'hPa',
            'show_notifications': True,
            'play_sounds': False,
            'auto_save_position': True,
            'remember_last_city': True,
            'show_air_quality': True,
            'show_extended_forecast': True
        }
        
        logger.info("Settings Service initialized")
    
    def add_change_observer(self, observer: Callable[[str, Any, Any], None]) -> None:
        """
        Add an observer for settings changes.
        
        Args:
            observer: Function that will be called when settings change
                     Signature: (setting_name, old_value, new_value) -> None
        """
        self._change_observers.append(observer)
        logger.debug("Settings change observer added")
    
    def remove_change_observer(self, observer: Callable[[str, Any, Any], None]) -> None:
        """
        Remove a settings change observer.
        
        Args:
            observer: Observer function to remove
        """
        if observer in self._change_observers:
            self._change_observers.remove(observer)
            logger.debug("Settings change observer removed")
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Get a setting value.
        
        Args:
            key: Setting key
            default: Default value if setting not found
            
        Returns:
            Setting value or default
        """
        try:
            # Try to get from config manager properties first
            if hasattr(config_manager, key):
                value = getattr(config_manager, key)
                if value is not None:
                    return value
            
            # Fall back to default settings
            if key in self._default_settings:
                return self._default_settings[key]
            
            return default
            
        except Exception as e:
            logger.error(f"Error getting setting {key}: {e}")
            return default
    
    def set_setting(self, key: str, value: Any, validate: bool = True) -> bool:
        """
        Set a setting value.
        
        Args:
            key: Setting key
            value: Setting value
            validate: Whether to validate the value
            
        Returns:
            True if setting was successfully set
        """
        try:
            # Get old value for change notification
            old_value = self.get_setting(key)
            
            # Validate if requested
            if validate and not self._validate_setting(key, value):
                logger.warning(f"Setting validation failed for {key}: {value}")
                return False
            
            # Set the setting using config manager save_settings
            config_manager.save_settings(**{key: value})
            
            # Notify observers
            self._notify_change_observers(key, old_value, value)
            
            logger.info(f"Setting updated: {key} = {value}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting {key}: {e}")
            return False
    
    def update_settings(self, settings: Dict[str, Any], validate: bool = True) -> Dict[str, bool]:
        """
        Update multiple settings at once.
        
        Args:
            settings: Dictionary of setting key-value pairs
            validate: Whether to validate the values
            
        Returns:
            Dictionary indicating success/failure for each setting
        """
        results = {}
        
        for key, value in settings.items():
            results[key] = self.set_setting(key, value, validate)
        
        logger.info(f"Updated {len(settings)} settings")
        return results
    
    def reset_setting(self, key: str) -> bool:
        """
        Reset a setting to its default value.
        
        Args:
            key: Setting key to reset
            
        Returns:
            True if setting was successfully reset
        """
        if key in self._default_settings:
            return self.set_setting(key, self._default_settings[key], validate=False)
        else:
            logger.warning(f"No default value for setting: {key}")
            return False
    
    def reset_all_settings(self) -> bool:
        """
        Reset all settings to their default values.
        
        Returns:
            True if all settings were successfully reset
        """
        try:
            results = self.update_settings(self._default_settings, validate=False)
            success = all(results.values())
            
            if success:
                logger.info("All settings reset to defaults")
            else:
                logger.warning("Some settings failed to reset")
            
            return success
            
        except Exception as e:
            logger.error(f"Error resetting all settings: {e}")
            return False
    
    def get_all_settings(self) -> Dict[str, Any]:
        """
        Get all current settings.
        
        Returns:
            Dictionary of all current settings
        """
        try:
            settings = {}
            
            # Get all default setting keys
            for key in self._default_settings.keys():
                settings[key] = self.get_setting(key)
            
            return settings
            
        except Exception as e:
            logger.error(f"Error getting all settings: {e}")
            return {}
    
    def export_settings(self, file_path_str: Optional[str] = None) -> bool:
        """
        Export settings to a file.
        
        Args:
            file_path_str: Path to export file (optional)
            
        Returns:
            True if export was successful
        """
        try:
            if not file_path_str:
                # Use default export location
                export_dir = Path.cwd() / "exports"
                export_dir.mkdir(parents=True, exist_ok=True)
                file_path_str = str(export_dir / f"settings_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
            
            settings = self.get_all_settings()
            
            # Add metadata
            export_data = {
                'metadata': {
                    'export_date': datetime.now().isoformat(),
                    'version': '1.0',
                    'application': 'Weather Dashboard'
                },
                'settings': settings
            }
            
            with open(file_path_str, 'w', encoding='utf-8') as f:
                json.dump(export_data, f, indent=2, ensure_ascii=False)
            
            logger.info(f"Settings exported to: {file_path_str}")
            return True
            
        except Exception as e:
            logger.error(f"Error exporting settings: {e}")
            return False
    
    def import_settings(self, file_path: str, merge: bool = True) -> bool:
        """
        Import settings from a file.
        
        Args:
            file_path: Path to import file
            merge: Whether to merge with existing settings (True) or replace all (False)
            
        Returns:
            True if import was successful
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                import_data = json.load(f)
            
            if 'settings' not in import_data:
                logger.error("Invalid settings file format")
                return False
            
            imported_settings = import_data['settings']
            
            if not merge:
                # Reset to defaults first
                self.reset_all_settings()
            
            # Apply imported settings
            results = self.update_settings(imported_settings)
            success_count = sum(1 for success in results.values() if success)
            
            logger.info(f"Imported {success_count}/{len(imported_settings)} settings from: {file_path}")
            return success_count > 0
            
        except Exception as e:
            logger.error(f"Error importing settings: {e}")
            return False
    
    def get_setting_info(self, key: str) -> Dict[str, Any]:
        """
        Get information about a setting.
        
        Args:
            key: Setting key
            
        Returns:
            Dictionary with setting information
        """
        info = {
            'key': key,
            'current_value': self.get_setting(key),
            'default_value': self._default_settings.get(key),
            'has_validation': key in self._validation_rules,
            'type': type(self.get_setting(key)).__name__ if self.get_setting(key) is not None else 'unknown'
        }
        
        return info
    
    # Private validation methods
    def _validate_setting(self, key: str, value: Any) -> bool:
        """Validate a setting value."""
        if key in self._validation_rules:
            return self._validation_rules[key](value)
        return True  # No validation rule means always valid
    
    def _validate_theme(self, theme: str) -> bool:
        """Validate theme setting."""
        valid_themes = [
            "darkly", "flatly", "litera", "minty", "lumen",
            "sandstone", "yeti", "pulse", "united", "morph",
            "journal", "solar", "superhero", "cyborg"
        ]
        return isinstance(theme, str) and theme in valid_themes
    
    def _validate_city(self, city: str) -> bool:
        """Validate city setting."""
        return isinstance(city, str) and len(city.strip()) <= 100
    
    def _validate_refresh_interval(self, interval: int) -> bool:
        """Validate auto refresh interval."""
        return isinstance(interval, int) and 60 <= interval <= 3600  # 1 minute to 1 hour
    
    def _validate_temperature_unit(self, unit: str) -> bool:
        """Validate temperature unit."""
        return isinstance(unit, str) and unit in ['celsius', 'fahrenheit', 'kelvin']
    
    def _validate_wind_speed_unit(self, unit: str) -> bool:
        """Validate wind speed unit."""
        return isinstance(unit, str) and unit in ['ms', 'kmh', 'mph', 'knots']
    
    def _validate_pressure_unit(self, unit: str) -> bool:
        """Validate pressure unit."""
        return isinstance(unit, str) and unit in ['hPa', 'inHg', 'mmHg', 'atm']
    
    def _notify_change_observers(self, key: str, old_value: Any, new_value: Any) -> None:
        """Notify all change observers."""
        for observer in self._change_observers:
            try:
                observer(key, old_value, new_value)
            except Exception as e:
                logger.error(f"Error in settings change observer: {e}")
    
    # Property accessors for common settings
    @property
    def current_theme(self) -> str:
        """Get current theme."""
        return self.get_setting('theme', 'darkly')
    
    @property
    def current_city(self) -> str:
        """Get current city."""
        return self.get_setting('city', '')
    
    @property
    def auto_refresh_interval(self) -> int:
        """Get auto refresh interval."""
        return self.get_setting('auto_refresh_interval', 300)
    
    @property
    def temperature_unit(self) -> str:
        """Get temperature unit."""
        return self.get_setting('temperature_unit', 'celsius')
