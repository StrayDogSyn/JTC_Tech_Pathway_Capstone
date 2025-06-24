"""
Historical weather data utilities and processing functions.

This module provides utilities for processing, analyzing, and visualizing
historical weather data from the Open-Meteo API.
"""

import pandas as pd
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime, timedelta
from pathlib import Path

from ..models.weather_models import HistoricalWeatherDataset, HistoricalWeatherData
from ..utils.logging import get_logger
from ..utils.exceptions import ValidationError
from ..services.weather_api import WeatherAPIService


logger = get_logger()


class HistoricalWeatherProcessor:
    """Processor for historical weather data analysis and management."""
    
    def __init__(self, api_service: WeatherAPIService):
        """Initialize the historical weather processor."""
        self.api_service = api_service
        self.cache_dir = Path("data/historical_cache")
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        logger.info("HistoricalWeatherProcessor initialized")

    def fetch_and_process_historical_data(self, lat: float, lon: float, 
                                        start_date: str, end_date: str) -> Optional[HistoricalWeatherDataset]:
        """
        Fetch and process historical weather data for a location and date range.
        
        Args:
            lat: Latitude
            lon: Longitude
            start_date: Start date in YYYY-MM-DD format
            end_date: End date in YYYY-MM-DD format
            
        Returns:
            Processed historical weather dataset
        """
        try:
            logger.info(f"Fetching historical data for {lat}, {lon} from {start_date} to {end_date}")
            
            # Check cache first
            cache_key = f"{lat}_{lon}_{start_date}_{end_date}"
            cached_data = self._get_cached_data(cache_key)
            if cached_data:
                logger.info("Using cached historical data")
                return cached_data
            
            # Fetch from API
            raw_data = self.api_service.get_historical_weather(lat, lon, start_date, end_date)
            if not raw_data:
                logger.error("No historical data received from API")
                return None
            
            # Process the data
            dataset = HistoricalWeatherDataset.from_api_response(raw_data)
            
            # Cache the processed data
            self._cache_data(cache_key, dataset)
            
            logger.info(f"Successfully processed {len(dataset.daily_data)} days of historical data")
            return dataset
            
        except Exception as e:
            logger.error(f"Error fetching/processing historical data: {e}")
            return None

    def get_sample_berlin_data(self) -> Optional[HistoricalWeatherDataset]:
        """
        Get the sample Berlin historical data (2000-2009) from the provided URL.
        
        Returns:
            Historical weather dataset for Berlin 2000-2009
        """
        try:
            logger.info("Fetching sample Berlin historical data (2000-2009)")
            raw_data = self.api_service.get_historical_weather_sample()
            
            if not raw_data:
                logger.error("No sample historical data received")
                return None
            
            dataset = HistoricalWeatherDataset.from_api_response(raw_data)
            logger.info(f"Successfully loaded {len(dataset.daily_data)} days of Berlin historical data")
            return dataset
            
        except Exception as e:
            logger.error(f"Error fetching sample Berlin data: {e}")
            return None

    def analyze_temperature_trends(self, dataset: HistoricalWeatherDataset) -> Dict[str, Any]:
        """
        Analyze temperature trends in historical data.
        
        Args:
            dataset: Historical weather dataset
            
        Returns:
            Temperature trend analysis results
        """
        try:
            if not dataset.daily_data:
                return {}
            
            # Extract temperature data
            temperatures = []
            dates = []
            
            for day_data in dataset.daily_data:
                if day_data.temperature_mean is not None:
                    temperatures.append(day_data.temperature_mean)
                    dates.append(day_data.date)
            
            if not temperatures:
                return {}
            
            # Calculate statistics
            analysis = {
                'total_days': len(temperatures),
                'average_temperature': round(sum(temperatures) / len(temperatures), 2),
                'min_temperature': min(temperatures),
                'max_temperature': max(temperatures),
                'temperature_range': round(max(temperatures) - min(temperatures), 2),
                'date_range': {
                    'start': dates[0] if dates else '',
                    'end': dates[-1] if dates else ''
                }
            }
            
            # Monthly averages
            monthly_data = {}
            for i, temp in enumerate(temperatures):
                if i < len(dates):
                    try:
                        month = datetime.fromisoformat(dates[i]).strftime('%Y-%m')
                        if month not in monthly_data:
                            monthly_data[month] = []
                        monthly_data[month].append(temp)
                    except:
                        continue
            
            monthly_averages = {
                month: round(sum(temps) / len(temps), 2)
                for month, temps in monthly_data.items()
            }
            
            analysis['monthly_averages'] = monthly_averages
            
            logger.debug(f"Temperature trend analysis completed: {len(temperatures)} data points")
            return analysis
            
        except Exception as e:
            logger.error(f"Error analyzing temperature trends: {e}")
            return {}

    def get_extreme_weather_events(self, dataset: HistoricalWeatherDataset) -> Dict[str, Any]:
        """
        Identify extreme weather events in historical data.
        
        Args:
            dataset: Historical weather dataset
            
        Returns:
            Extreme weather events analysis
        """
        try:
            if not dataset.daily_data:
                return {}
            
            # Extract data for analysis
            temps_max = [d.temperature_max for d in dataset.daily_data if d.temperature_max is not None]
            temps_min = [d.temperature_min for d in dataset.daily_data if d.temperature_min is not None]
            wind_speeds = [d.wind_speed_max for d in dataset.daily_data if d.wind_speed_max is not None]
            wind_gusts = [d.wind_gusts_max for d in dataset.daily_data if d.wind_gusts_max is not None]
            
            events = {
                'temperature_extremes': {
                    'hottest_day': max(temps_max) if temps_max else None,
                    'coldest_day': min(temps_min) if temps_min else None,
                    'largest_daily_range': max([
                        (d.temperature_max or 0) - (d.temperature_min or 0) 
                        for d in dataset.daily_data 
                        if d.temperature_max is not None and d.temperature_min is not None
                    ]) if any(d.temperature_max is not None and d.temperature_min is not None for d in dataset.daily_data) else None
                },
                'wind_extremes': {
                    'highest_wind_speed': max(wind_speeds) if wind_speeds else None,
                    'highest_wind_gust': max(wind_gusts) if wind_gusts else None
                },
                'statistics': {
                    'total_analyzed_days': len(dataset.daily_data),
                    'days_with_temperature_data': len(temps_max),
                    'days_with_wind_data': len(wind_speeds)
                }
            }
            
            logger.debug("Extreme weather events analysis completed")
            return events
            
        except Exception as e:
            logger.error(f"Error analyzing extreme weather events: {e}")
            return {}

    def export_to_csv(self, dataset: HistoricalWeatherDataset, filename: Optional[str] = None) -> str:
        """
        Export historical weather dataset to CSV format.
        
        Args:
            dataset: Historical weather dataset
            filename: Optional custom filename
            
        Returns:
            Path to the exported CSV file
        """
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"historical_weather_{timestamp}.csv"
            
            export_path = Path("exports") / filename
            export_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Prepare data for CSV
            csv_data = []
            for day_data in dataset.daily_data:
                csv_data.append({
                    'date': day_data.date,
                    'temperature_mean': day_data.temperature_mean,
                    'temperature_max': day_data.temperature_max,
                    'temperature_min': day_data.temperature_min,
                    'wind_speed_max': day_data.wind_speed_max,
                    'wind_gusts_max': day_data.wind_gusts_max,
                    'sunrise': day_data.sunrise,
                    'sunset': day_data.sunset,
                    'latitude': day_data.latitude,
                    'longitude': day_data.longitude
                })
            
            # Create DataFrame and export
            df = pd.DataFrame(csv_data)
            df.to_csv(export_path, index=False)
            
            logger.info(f"Historical data exported to {export_path}")
            return str(export_path)
            
        except Exception as e:
            logger.error(f"Error exporting historical data to CSV: {e}")
            raise

    def _get_cached_data(self, cache_key: str) -> Optional[HistoricalWeatherDataset]:
        """Get cached historical data if available and valid."""
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            if not cache_file.exists():
                return None
            
            # Check if cache is still valid (24 hours)
            if datetime.now().timestamp() - cache_file.stat().st_mtime > 86400:
                cache_file.unlink()  # Remove expired cache
                return None
            
            with open(cache_file, 'r') as f:
                cached_data = json.load(f)
            
            return HistoricalWeatherDataset.from_api_response(cached_data)
            
        except Exception as e:
            logger.debug(f"Cache retrieval failed: {e}")
            return None

    def _cache_data(self, cache_key: str, dataset: HistoricalWeatherDataset) -> None:
        """Cache historical weather dataset."""
        try:
            cache_file = self.cache_dir / f"{cache_key}.json"
            
            # Convert dataset back to API response format for caching
            cache_data = {
                'latitude': dataset.location_info.get('latitude'),
                'longitude': dataset.location_info.get('longitude'),
                'timezone': dataset.location_info.get('timezone'),
                'elevation': dataset.location_info.get('elevation'),
                'daily_units': dataset.units,
                'daily': {
                    'time': [d.date for d in dataset.daily_data],
                    'temperature_2m_mean': [d.temperature_mean for d in dataset.daily_data],
                    'temperature_2m_max': [d.temperature_max for d in dataset.daily_data],
                    'temperature_2m_min': [d.temperature_min for d in dataset.daily_data],
                    'wind_speed_10m_max': [d.wind_speed_max for d in dataset.daily_data],
                    'wind_gusts_10m_max': [d.wind_gusts_max for d in dataset.daily_data],
                    'sunrise': [d.sunrise for d in dataset.daily_data],
                    'sunset': [d.sunset for d in dataset.daily_data]
                },
                'hourly': {
                    'time': [h.datetime for h in dataset.hourly_data],
                    'temperature_2m': [h.temperature for h in dataset.hourly_data],
                    'precipitation': [h.precipitation for h in dataset.hourly_data]
                }
            }
            
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)
            
            logger.debug(f"Historical data cached: {cache_key}")
            
        except Exception as e:
            logger.debug(f"Cache storage failed: {e}")
