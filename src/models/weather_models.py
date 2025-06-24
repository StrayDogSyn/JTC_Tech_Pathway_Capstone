"""
Weather data models and structures.

This module contains all data classes and models used throughout the weather application.
"""

from dataclasses import dataclass
from typing import Dict, List, Optional, Any
from datetime import datetime

from ..utils.logging import get_logger
from ..utils.exceptions import ValidationError


logger = get_logger()


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
        """Create WeatherData instance from API response with validation."""
        try:
            logger.debug("Creating WeatherData from API response")
            if not data or 'main' not in data or 'weather' not in data:
                raise ValueError("Invalid weather data structure")
            
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
        except (KeyError, IndexError, TypeError) as e:
            logger.error(f"Failed to parse weather data: {e}")
            raise ValueError(f"Invalid weather data format: {e}")
    
    def validate(self) -> bool:
        """Validate weather data values."""
        try:
            # Temperature range check (-100 to 60 Celsius)
            if not -100 <= self.temperature <= 60:
                logger.warning(f"Temperature out of range: {self.temperature}")
                return False
            
            # Humidity range check (0-100%)
            if not 0 <= self.humidity <= 100:
                logger.warning(f"Humidity out of range: {self.humidity}")
                return False
            
            # Wind speed check (0-200 m/s)
            if not 0 <= self.wind_speed <= 200:
                logger.warning(f"Wind speed out of range: {self.wind_speed}")
                return False
            
            return True
        except Exception as e:
            logger.error(f"Error validating weather data: {e}")
            return False


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


@dataclass
class HistoricalWeatherData:
    """Data class for historical weather information from Open-Meteo API."""
    date: str
    temperature_mean: Optional[float]
    temperature_max: Optional[float]
    temperature_min: Optional[float]
    wind_speed_max: Optional[float]
    wind_gusts_max: Optional[float]
    sunrise: Optional[str]
    sunset: Optional[str]
    latitude: float
    longitude: float
    timezone: str

    @classmethod
    def from_api_response(cls, data: Dict[str, Any], index: int) -> 'HistoricalWeatherData':
        """Create HistoricalWeatherData instance from Open-Meteo API response."""
        try:
            daily = data.get('daily', {})
            return cls(
                date=daily.get('time', [])[index] if daily.get('time') else '',
                temperature_mean=daily.get('temperature_2m_mean', [])[index] if daily.get('temperature_2m_mean') else None,
                temperature_max=daily.get('temperature_2m_max', [])[index] if daily.get('temperature_2m_max') else None,
                temperature_min=daily.get('temperature_2m_min', [])[index] if daily.get('temperature_2m_min') else None,
                wind_speed_max=daily.get('wind_speed_10m_max', [])[index] if daily.get('wind_speed_10m_max') else None,
                wind_gusts_max=daily.get('wind_gusts_10m_max', [])[index] if daily.get('wind_gusts_10m_max') else None,
                sunrise=daily.get('sunrise', [])[index] if daily.get('sunrise') else None,
                sunset=daily.get('sunset', [])[index] if daily.get('sunset') else None,
                latitude=data.get('latitude', 0.0),
                longitude=data.get('longitude', 0.0),
                timezone=data.get('timezone', 'UTC')
            )
        except (IndexError, KeyError, TypeError) as e:
            logger.error(f"Error parsing historical weather data at index {index}: {e}")
            raise ValidationError(f"Invalid historical weather data: {e}")


@dataclass
class HourlyHistoricalData:
    """Data class for hourly historical weather information."""
    datetime: str
    temperature: Optional[float]
    precipitation: Optional[float]

    @classmethod
    def from_api_response(cls, data: Dict[str, Any], index: int) -> 'HourlyHistoricalData':
        """Create HourlyHistoricalData instance from Open-Meteo API response."""
        try:
            hourly = data.get('hourly', {})
            return cls(
                datetime=hourly.get('time', [])[index] if hourly.get('time') else '',
                temperature=hourly.get('temperature_2m', [])[index] if hourly.get('temperature_2m') else None,
                precipitation=hourly.get('precipitation', [])[index] if hourly.get('precipitation') else None
            )
        except (IndexError, KeyError, TypeError) as e:
            logger.error(f"Error parsing hourly historical data at index {index}: {e}")
            raise ValidationError(f"Invalid hourly historical data: {e}")


@dataclass
class HistoricalWeatherDataset:
    """Container for complete historical weather dataset."""
    daily_data: List[HistoricalWeatherData]
    hourly_data: List[HourlyHistoricalData]
    location_info: Dict[str, Any]
    date_range: Dict[str, str]
    units: Dict[str, str]

    @classmethod
    def from_api_response(cls, data: Dict[str, Any]) -> 'HistoricalWeatherDataset':
        """Create complete historical dataset from Open-Meteo API response."""
        try:
            logger.debug("Creating HistoricalWeatherDataset from API response")
            
            # Parse daily data
            daily_data = []
            daily = data.get('daily', {})
            if daily.get('time'):
                for i in range(len(daily['time'])):
                    daily_data.append(HistoricalWeatherData.from_api_response(data, i))
            
            # Parse hourly data
            hourly_data = []
            hourly = data.get('hourly', {})
            if hourly.get('time'):
                for i in range(len(hourly['time'])):
                    hourly_data.append(HourlyHistoricalData.from_api_response(data, i))
            
            # Extract metadata
            location_info = {
                'latitude': data.get('latitude'),
                'longitude': data.get('longitude'),
                'timezone': data.get('timezone'),
                'elevation': data.get('elevation')
            }
            
            date_range = {
                'start': daily.get('time', [''])[0] if daily.get('time') else '',
                'end': daily.get('time', [''])[-1] if daily.get('time') else ''
            }
            
            units = data.get('daily_units', {})
            
            return cls(
                daily_data=daily_data,
                hourly_data=hourly_data,
                location_info=location_info,
                date_range=date_range,
                units=units
            )
        except Exception as e:
            logger.error(f"Error creating historical weather dataset: {e}")
            raise ValidationError(f"Invalid historical weather dataset: {e}")
