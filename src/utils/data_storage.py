"""
File-based data storage utilities for weather data.

This module handles CSV storage, weather history tracking, and data persistence.
"""

import csv
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pathlib import Path

from ..models.weather_models import WeatherData
from ..utils.logging import get_logger

logger = get_logger()


class WeatherDataStorage:
    """Handles file-based storage of weather data."""
    
    def __init__(self, data_dir: str = "data"):
        """Initialize storage with data directory."""
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # File paths
        self.history_file = self.data_dir / "weather_history.csv"
        self.favorites_file = self.data_dir / "favorite_cities.json"
        self.journal_file = self.data_dir / "weather_journal.txt"
        self.settings_file = self.data_dir / "user_settings.json"
        self.predictions_file = self.data_dir / "predictions.json"
        
        # Initialize files if they don't exist
        self._initialize_files()
        
    def _initialize_files(self):
        """Initialize CSV and JSON files with headers if they don't exist."""
        # Initialize weather history CSV
        if not self.history_file.exists():
            with open(self.history_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    'date', 'city', 'country', 'temperature', 'feels_like',
                    'humidity', 'pressure', 'wind_speed', 'wind_direction',
                    'visibility', 'description', 'cloudiness'
                ])
        
        # Initialize other files
        for file_path, default_content in [
            (self.favorites_file, []),
            (self.settings_file, {}),
            (self.predictions_file, [])
        ]:
            if not file_path.exists():
                with open(file_path, 'w', encoding='utf-8') as f:
                    json.dump(default_content, f)
        
        if not self.journal_file.exists():
            self.journal_file.write_text("", encoding='utf-8')
    
    def save_weather_data(self, weather_data: WeatherData) -> bool:
        """Save weather data to CSV file."""
        try:
            with open(self.history_file, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    weather_data.city,
                    weather_data.country,
                    weather_data.temperature,
                    weather_data.feels_like,
                    weather_data.humidity,
                    weather_data.pressure,
                    weather_data.wind_speed,
                    weather_data.wind_direction,
                    weather_data.visibility,
                    weather_data.description,
                    weather_data.cloudiness
                ])
            logger.info(f"Weather data saved for {weather_data.city}")
            return True
        except Exception as e:
            logger.error(f"Failed to save weather data: {e}")
            return False
    
    def get_weather_history(self, days: int = 7) -> List[Dict[str, Any]]:
        """Get weather history for the last N days."""
        try:
            if not self.history_file.exists():
                return []
            
            history = []
            cutoff_date = datetime.now() - timedelta(days=days)
            
            with open(self.history_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        row_date = datetime.strptime(row['date'], '%Y-%m-%d %H:%M:%S')
                        if row_date >= cutoff_date:
                            # Convert numeric fields
                            row['temperature'] = float(row['temperature'])
                            row['feels_like'] = float(row['feels_like'])
                            row['humidity'] = int(row['humidity'])
                            row['pressure'] = int(row['pressure'])
                            row['wind_speed'] = float(row['wind_speed'])
                            row['wind_direction'] = int(row['wind_direction'])
                            row['visibility'] = int(row['visibility'])
                            row['cloudiness'] = int(row['cloudiness'])
                            history.append(row)
                    except (ValueError, KeyError) as e:
                        logger.warning(f"Skipping invalid row: {e}")
                        continue
            
            return sorted(history, key=lambda x: x['date'], reverse=True)
        except Exception as e:
            logger.error(f"Failed to read weather history: {e}")
            return []
    
    def calculate_weekly_averages(self) -> Dict[str, float]:
        """Calculate weekly averages from weather history."""
        history = self.get_weather_history(7)
        if not history:
            return {}
        
        totals = {
            'temperature': 0,
            'feels_like': 0,
            'humidity': 0,
            'pressure': 0,
            'wind_speed': 0
        }
        
        for record in history:
            for key in totals:
                totals[key] += record[key]
        
        count = len(history)
        averages = {key: round(total / count, 1) for key, total in totals.items()}
        
        return averages
    
    def get_temperature_stats(self) -> Dict[str, Any]:
        """Get temperature statistics (min/max, weather type counts)."""
        history = self.get_weather_history(30)  # Last 30 days
        if not history:
            return {}
        
        temperatures = [record['temperature'] for record in history]
        weather_types = [record['description'] for record in history]
        
        # Count weather types
        weather_counts = {}
        for weather in weather_types:
            weather_counts[weather] = weather_counts.get(weather, 0) + 1
        
        return {
            'min_temp': min(temperatures),
            'max_temp': max(temperatures),
            'avg_temp': round(sum(temperatures) / len(temperatures), 1),
            'weather_counts': weather_counts,
            'total_records': len(history)
        }
    
    def save_favorite_cities(self, cities: List[str]) -> bool:
        """Save favorite cities to JSON file."""
        try:
            with open(self.favorites_file, 'w', encoding='utf-8') as f:
                json.dump(cities, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save favorite cities: {e}")
            return False
    
    def load_favorite_cities(self) -> List[str]:
        """Load favorite cities from JSON file."""
        try:
            if self.favorites_file.exists():
                with open(self.favorites_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Failed to load favorite cities: {e}")
            return []
    
    def get_favorite_cities(self) -> List[str]:
        """Get list of favorite cities."""
        return self.load_favorite_cities()
    
    def add_favorite_city(self, city: str) -> bool:
        """Add a city to favorites."""
        favorites = self.load_favorite_cities()
        if city not in favorites:
            favorites.append(city)
            return self.save_favorite_cities(favorites)
        return True
    
    def remove_favorite_city(self, city: str) -> bool:
        """Remove a city from favorites."""
        favorites = self.load_favorite_cities()
        if city in favorites:
            favorites.remove(city)
            return self.save_favorite_cities(favorites)
        return True
    
    def save_journal_entry(self, date: str, mood: str, text: str) -> bool:
        """Save journal entry with date, mood, and text."""
        try:
            # Read existing entries
            existing_entries = []
            if self.journal_file.exists():
                with open(self.journal_file, 'r', encoding='utf-8') as f:
                    existing_entries = [line.strip() for line in f.readlines() if line.strip()]
            
            # Remove existing entry for this date
            existing_entries = [entry for entry in existing_entries 
                              if not entry.startswith(f"{date}|")]
            
            # Add new entry
            new_entry = f"{date}|{mood}|{text}"
            existing_entries.append(new_entry)
            
            # Write back to file
            with open(self.journal_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(existing_entries))
            
            logger.info(f"Journal entry saved for {date}")
            return True
        except Exception as e:
            logger.error(f"Error saving journal entry: {e}")
            return False
    
    def load_journal_entries(self, days: int = 7) -> List[str]:
        """Load recent journal entries."""
        try:
            if not self.journal_file.exists():
                return []
            
            content = self.journal_file.read_text(encoding='utf-8')
            entries = content.split('-'*50)
            
            # Filter by date if needed
            recent_entries = []
            cutoff_date = datetime.now() - timedelta(days=days)
            
            for entry in entries:
                if entry.strip():
                    # Try to extract date from entry
                    try:
                        lines = entry.strip().split('\n')
                        if lines and lines[0].startswith('['):
                            date_str = lines[0].split(']')[0][1:]
                            entry_date = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
                            if entry_date >= cutoff_date:
                                recent_entries.append(entry.strip())
                    except:
                        recent_entries.append(entry.strip())
            
            return recent_entries[-10:]  # Last 10 entries
        except Exception as e:
            logger.error(f"Failed to load journal entries: {e}")
            return []
    
    def get_journal_entry(self, date: str) -> Optional[Dict[str, Any]]:
        """Get journal entry for a specific date."""
        try:
            if self.journal_file.exists():
                with open(self.journal_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Parse journal entries (simple format: date|mood|text)
                    for line in content.split('\n'):
                        if line.strip() and '|' in line:
                            parts = line.split('|', 2)
                            if len(parts) >= 3 and parts[0] == date:
                                return {
                                    'date': parts[0],
                                    'mood': parts[1],
                                    'text': parts[2]
                                }
        except Exception as e:
            logger.error(f"Error reading journal entry: {e}")
        return None
    
    def save_alert_settings(self, settings: Dict[str, Any]) -> bool:
        """Save weather alert settings."""
        try:
            existing_settings = self.load_user_settings()
            existing_settings['alerts'] = settings
            return self.save_user_settings(existing_settings)
        except Exception as e:
            logger.error(f"Error saving alert settings: {e}")
            return False
    
    def get_alert_settings(self) -> Dict[str, Any]:
        """Get weather alert settings."""
        settings = self.load_user_settings()
        return settings.get('alerts', {
            'high_temp_threshold': 30.0,
            'low_temp_threshold': 0.0,
            'rain_alerts': True,
            'storm_alerts': True,
            'wind_alerts': False
        })

    def save_user_settings(self, settings: Dict[str, Any]) -> bool:
        """Save user settings to JSON file."""
        try:
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save user settings: {e}")
            return False
    
    def load_user_settings(self) -> Dict[str, Any]:
        """Load user settings from JSON file."""
        try:
            if self.settings_file.exists():
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return {}
        except Exception as e:
            logger.error(f"Failed to load user settings: {e}")
            return {}
    
    def save_prediction(self, prediction: Dict[str, Any]) -> bool:
        """Save weather prediction for accuracy tracking."""
        try:
            predictions = []
            if self.predictions_file.exists():
                with open(self.predictions_file, 'r', encoding='utf-8') as f:
                    predictions = json.load(f)
            
            prediction['timestamp'] = datetime.now().isoformat()
            predictions.append(prediction)
            
            # Keep only last 100 predictions
            predictions = predictions[-100:]
            
            with open(self.predictions_file, 'w', encoding='utf-8') as f:
                json.dump(predictions, f, indent=2)
            return True
        except Exception as e:
            logger.error(f"Failed to save prediction: {e}")
            return False
    
    def load_predictions(self) -> List[Dict[str, Any]]:
        """Load prediction history."""
        try:
            if self.predictions_file.exists():
                with open(self.predictions_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Failed to load predictions: {e}")
            return []
    
    def save_alert_settings(self, settings: Dict[str, Any]) -> bool:
        """Save weather alert settings."""
        try:
            existing_settings = self.load_user_settings()
            existing_settings['alerts'] = settings
            return self.save_user_settings(existing_settings)
        except Exception as e:
            logger.error(f"Error saving alert settings: {e}")
            return False
    
    def get_alert_settings(self) -> Dict[str, Any]:
        """Get weather alert settings."""
        settings = self.load_user_settings()
        return settings.get('alerts', {
            'high_temp_threshold': 30.0,
            'low_temp_threshold': 0.0,
            'rain_alerts': True,
            'storm_alerts': True,
            'wind_alerts': False
        })


# Global storage instance
storage = WeatherDataStorage()
