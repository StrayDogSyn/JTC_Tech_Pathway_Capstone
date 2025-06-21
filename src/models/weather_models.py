"""
Weather data models and structures.

This module contains all data classes and models used throughout the weather application.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime


@dataclass
class WeatherData:
    """Data class for current weather information."""
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    visibility: int
    description: str
    icon: str
    city: str
    country: str
    timestamp: int
    cloudiness: int

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'WeatherData':
        """Create WeatherData instance from API response."""
        return cls(
            temperature=data['main']['temp'],
            feels_like=data['main']['feels_like'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            wind_speed=data.get('wind', {}).get('speed', 0),
            wind_direction=data.get('wind', {}).get('deg', 0),
            visibility=data.get('visibility', 0),
            description=data['weather'][0]['description'].title(),
            icon=data['weather'][0]['icon'],
            city=data['name'],
            country=data['sys']['country'],
            timestamp=data['dt'],
            cloudiness=data.get('clouds', {}).get('all', 0)
        )


@dataclass
class ForecastData:
    """Data class for forecast information."""
    hourly: List[Dict]
    daily: List[Dict]

    @classmethod
    def from_api_response(cls, forecast_list: List[Dict]) -> 'ForecastData':
        """Create ForecastData instance from API response."""
        return cls(
            hourly=forecast_list[:40],  # 5 days * 8 periods per day = 40 periods
            daily=cls._convert_to_daily_forecast(forecast_list)
        )
    
    @staticmethod
    def _convert_to_daily_forecast(forecast_list: List[Dict]) -> List[Dict]:
        """Convert 3-hour forecast data to daily forecast."""
        daily_data = []
        current_date = None
        daily_temps = []
        daily_entry = None
        
        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).date()
            
            if current_date != date:
                if daily_entry and daily_temps:
                    daily_entry['temp'] = {
                        'min': min(daily_temps),
                        'max': max(daily_temps)
                    }
                    daily_data.append(daily_entry)
                
                current_date = date
                daily_temps = []
                daily_entry = {
                    'dt': item['dt'],
                    'weather': item['weather'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'wind_speed': item.get('wind', {}).get('speed', 0),
                    'clouds': item.get('clouds', {}).get('all', 0)
                }
            
            daily_temps.append(item['main']['temp'])
        
        if daily_entry and daily_temps:
            daily_entry['temp'] = {
                'min': min(daily_temps),
                'max': max(daily_temps)
            }
            daily_data.append(daily_entry)
        
        return daily_data[:5]


@dataclass
class LocationData:
    """Data class for location information."""
    name: str
    lat: float
    lon: float
    country: str
    state: Optional[str] = None
    
    @property
    def display_name(self) -> str:
        """Get formatted display name for the location."""
        if self.state:
            return f"{self.name}, {self.state}, {self.country}"
        return f"{self.name}, {self.country}"

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'LocationData':
        """Create LocationData instance from geocoding API response."""
        return cls(
            name=data['name'],
            lat=data['lat'],
            lon=data['lon'],
            country=data['country'],
            state=data.get('state')
        )


@dataclass
class AirQualityData:
    """Data class for air quality information."""
    aqi: int
    co: float
    no: float
    no2: float
    o3: float
    so2: float
    pm2_5: float
    pm10: float
    nh3: float

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'AirQualityData':
        """Create AirQualityData instance from API response."""
        components = data['list'][0]['components']
        return cls(
            aqi=data['list'][0]['main']['aqi'],
            co=components['co'],
            no=components['no'],
            no2=components['no2'],
            o3=components['o3'],
            so2=components['so2'],
            pm2_5=components['pm2_5'],
            pm10=components['pm10'],
            nh3=components['nh3']
        )


@dataclass
class WeatherAlert:
    """Data class for weather alerts."""
    sender_name: str
    event: str
    start: int
    end: int
    description: str
    tags: List[str]

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'WeatherAlert':
        """Create WeatherAlert instance from API response."""
        return cls(
            sender_name=data['sender_name'],
            event=data['event'],
            start=data['start'],
            end=data['end'],
            description=data['description'],
            tags=data.get('tags', [])
        )
