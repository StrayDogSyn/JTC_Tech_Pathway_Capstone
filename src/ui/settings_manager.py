"""
Settings management for the weather dashboard.

This module handles application settings, preferences, and state management.
"""

import json
import os
from dataclasses import dataclass, asdict
from typing import Dict, Any, Optional
from pathlib import Path

from ..utils.logging import get_logger
from ..utils.exceptions import ConfigurationError


logger = get_logger()


@dataclass
class UISettings:
    """UI-specific settings for the weather dashboard."""
    temperature_unit: str = 'C'
    wind_speed_unit: str = 'km/h'
    pressure_unit: str = 'hPa'
    auto_save_favorites: bool = True
    show_animations: bool = True
    update_interval: int = 300  # 5 minutes
    show_notifications: bool = True
    theme: str = 'darkly'
    window_size: tuple = (1700, 1100)
    
    def validate(self) -> bool:
        """Validate settings values."""
        try:
            if self.temperature_unit not in ['C', 'F']:
                return False
            if self.wind_speed_unit not in ['km/h', 'm/s', 'mph']:
                return False
            if not 30 <= self.update_interval <= 3600:  # 30s to 1h
                return False
            return True
        except Exception as e:
            logger.error(f"Error validating UI settings: {e}")
            return False


class SettingsManager:
    """Manages application settings with persistence."""
    
    def __init__(self, settings_file: Optional[str] = None):
        """Initialize settings manager."""
        self.settings_file = settings_file or self._get_default_settings_path()
        self.ui_settings = UISettings()
        self.favorites_list: list = []
        self.recent_searches: list = []
        self._load_settings()
        
        logger.info(f"SettingsManager initialized with file: {self.settings_file}")
    
    def _get_default_settings_path(self) -> str:
        """Get default settings file path."""
        # Use user's home directory for settings
        home_dir = Path.home()
        app_dir = home_dir / ".weather_dashboard"
        app_dir.mkdir(exist_ok=True)
        return str(app_dir / "settings.json")
    
    def _load_settings(self) -> None:
        """Load settings from file."""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Load UI settings
                if 'ui_settings' in data:
                    ui_data = data['ui_settings']
                    self.ui_settings = UISettings(**ui_data)
                
                # Load other data
                self.favorites_list = data.get('favorites', [])
                self.recent_searches = data.get('recent_searches', [])
                
                # Validate loaded settings
                if not self.ui_settings.validate():
                    logger.warning("Invalid settings detected, using defaults")
                    self.ui_settings = UISettings()
                
                logger.info("Settings loaded successfully")
            else:
                logger.info("No settings file found, using defaults")
                
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            self.ui_settings = UISettings()
            self.favorites_list = []
            self.recent_searches = []
    
    def save_settings(self) -> None:
        """Save current settings to file."""
        try:
            settings_data = {
                'ui_settings': asdict(self.ui_settings),
                'favorites': self.favorites_list,
                'recent_searches': self.recent_searches
            }
            
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.settings_file), exist_ok=True)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_data, f, indent=2, ensure_ascii=False)
            
            logger.info("Settings saved successfully")
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            raise ConfigurationError(f"Could not save settings: {e}")
    
    def update_ui_setting(self, key: str, value: Any) -> None:
        """Update a specific UI setting."""
        try:
            if hasattr(self.ui_settings, key):
                setattr(self.ui_settings, key, value)
                if self.ui_settings.validate():
                    if self.ui_settings.auto_save_favorites:
                        self.save_settings()
                    logger.debug(f"Updated UI setting: {key} = {value}")
                else:
                    logger.warning(f"Invalid value for setting {key}: {value}")
            else:
                logger.warning(f"Unknown UI setting: {key}")
        except Exception as e:
            logger.error(f"Error updating UI setting {key}: {e}")
    
    def add_favorite(self, city: str) -> None:
        """Add a city to favorites."""
        try:
            if city and city not in self.favorites_list:
                self.favorites_list.append(city)
                # Keep only last 20 favorites
                if len(self.favorites_list) > 20:
                    self.favorites_list = self.favorites_list[-20:]
                
                if self.ui_settings.auto_save_favorites:
                    self.save_settings()
                logger.info(f"Added to favorites: {city}")
        except Exception as e:
            logger.error(f"Error adding favorite {city}: {e}")
    
    def remove_favorite(self, city: str) -> None:
        """Remove a city from favorites."""
        try:
            if city in self.favorites_list:
                self.favorites_list.remove(city)
                if self.ui_settings.auto_save_favorites:
                    self.save_settings()
                logger.info(f"Removed from favorites: {city}")
        except Exception as e:
            logger.error(f"Error removing favorite {city}: {e}")
    
    def add_recent_search(self, city: str) -> None:
        """Add a city to recent searches."""
        try:
            if city:
                # Remove if already exists to avoid duplicates
                if city in self.recent_searches:
                    self.recent_searches.remove(city)
                
                # Add to beginning
                self.recent_searches.insert(0, city)
                
                # Keep only last 10 searches
                if len(self.recent_searches) > 10:
                    self.recent_searches = self.recent_searches[:10]
                
                if self.ui_settings.auto_save_favorites:
                    self.save_settings()
                logger.debug(f"Added to recent searches: {city}")
        except Exception as e:
            logger.error(f"Error adding recent search {city}: {e}")
    
    def get_search_suggestions(self) -> list:
        """Get search suggestions combining recent searches and favorites."""
        suggestions = []
        
        # Add recent searches first
        suggestions.extend(self.recent_searches[:5])
        
        # Add favorites
        for fav in self.favorites_list[:5]:
            if fav not in suggestions:
                suggestions.append(fav)
        
        # Add default suggestions if we don't have enough
        defaults = [
            "London, UK", "New York, NY", "Tokyo, Japan", "Paris, France",
            "Sydney, Australia", "Berlin, Germany", "Moscow, Russia",
            "Dubai, UAE", "Singapore", "Mumbai, India"
        ]
        
        for default in defaults:
            if len(suggestions) >= 10:
                break
            if default not in suggestions:
                suggestions.append(default)
        
        return suggestions
