"""
Enhanced OpenWeatherMap API implementation with Student Pack features.
Includes: Current, Forecast, Historical, Air Pollution, Geocoding, Maps, and Statistics APIs.
API Documentation: https://openweathermap.org/api
Student Pack: Free for educational use with extended limits.
"""

import requests
from typing import Dict, List, Optional, Tuple
from datetime import datetime, timedelta
import time
from config import Config

class EnhancedWeatherAPI:
    """
    Comprehensive Weather API class with Student Pack features.
    
    Features:
    - Current weather data
    - Hourly forecast (4 days)
    - Daily forecast (16 days)
    - Historical data (1 year archive)
    - Air pollution data
    - Geocoding
    - Weather maps
    - Statistical weather data
    - Accumulated parameters
    """
    
    def __init__(self):
        """Initialize the Enhanced WeatherAPI with Student Pack configuration."""
        Config.validate_config()
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
        self.onecall_url = Config.OPENWEATHER_ONECALL_URL
        self.history_url = Config.OPENWEATHER_HISTORY_URL
        self.geocoding_url = Config.OPENWEATHER_GEOCODING_URL
        self.pollution_url = Config.OPENWEATHER_POLLUTION_URL
        self.maps_url = Config.OPENWEATHER_MAPS_URL
        self.statistics_url = Config.OPENWEATHER_STATISTICS_URL
        self.default_units = Config.TEMPERATURE_UNITS
        self.subscription_info = Config.get_api_info()
        
    def _make_api_request(self, url: str, params: Dict) -> Dict:
        """Make API request with error handling and rate limiting."""
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            if e.response and e.response.status_code == 401:
                api_key_display = f"{self.api_key[:8]}..." if self.api_key else "Not set"
                raise ValueError(
                    "❌ API Authentication Failed\n\n"
                    "Student Pack API Subscription Details:\n"
                    f"• API Key: {api_key_display}\n"
                    f"• Plan: {self.subscription_info['subscription_plan']}\n"
                    f"• Rate Limits: {self.subscription_info['rate_limits']['per_minute']:,}/min, "
                    f"{self.subscription_info['rate_limits']['per_month']:,}/month\n"
                    f"• Historical: {self.subscription_info['rate_limits']['history_per_day']:,}/day\n\n"
                    "Troubleshooting:\n"
                    "1. Verify your API key is activated for Student Pack\n"
                    "2. Check subscription status at https://openweathermap.org/price#student\n"
                    "3. New API keys take up to 2 hours to activate\n"
                    "4. Contact support@openweathermap.org for student verification\n\n"
                    "API Documentation: https://openweathermap.org/api"
                )
            elif e.response and e.response.status_code == 404:
                raise ValueError("Location not found")
            elif e.response and e.response.status_code == 429:
                raise ValueError("Rate limit exceeded. Please wait before making more requests.")
            else:
                raise requests.RequestException(f"API request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API request failed: {e}")

    # CURRENT WEATHER API
    def get_current_weather(self, 
                          city: str, 
                          country_code: Optional[str] = None,
                          units: Optional[str] = None) -> Dict:
        """
        Get current weather data for a specific city.
        
        Args:
            city (str): City name
            country_code (str, optional): ISO 3166 country code (e.g., 'US', 'GB')
            units (str, optional): Temperature units ('metric', 'imperial', 'kelvin')
        
        Returns:
            Dict: Current weather data from OpenWeatherMap API
        """
        location = city
        if country_code:
            location = f"{city},{country_code}"
        
        units = units or self.default_units
        params = {
            'q': location,
            'appid': self.api_key,
            'units': units
        }
        
        url = f"{self.base_url}/weather"
        return self._make_api_request(url, params)

    def get_current_weather_by_coordinates(self, 
                                         lat: float, 
                                         lon: float,
                                         units: Optional[str] = None) -> Dict:
        """Get current weather data by geographic coordinates."""
        units = units or self.default_units
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units
        }
        
        url = f"{self.base_url}/weather"
        return self._make_api_request(url, params)

    # FORECAST APIs
    def get_hourly_forecast_4days(self, 
                                  lat: float, 
                                  lon: float,
                                  units: Optional[str] = None) -> Dict:
        """
        Get hourly weather forecast for 4 days.
        Student Pack Feature: Hourly forecast up to 4 days.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            units (str, optional): Temperature units
        
        Returns:
            Dict: Hourly forecast data for 4 days
        """
        units = units or self.default_units
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units,
            'exclude': 'minutely,alerts'  # Focus on hourly data
        }
        
        url = self.onecall_url
        return self._make_api_request(url, params)

    def get_daily_forecast_16days(self, 
                                  lat: float, 
                                  lon: float,
                                  units: Optional[str] = None) -> Dict:
        """
        Get daily weather forecast for 16 days.
        Student Pack Feature: Extended daily forecast up to 16 days.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            units (str, optional): Temperature units
        
        Returns:
            Dict: Daily forecast data for 16 days
        """
        units = units or self.default_units
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units,
            'exclude': 'minutely,hourly,alerts'  # Focus on daily data
        }
        
        # Note: For 16-day forecast, you might need to use a different endpoint
        # The standard One Call API provides 8 days. For 16 days, use the Climate forecast API
        url = f"{self.base_url}/forecast/daily"
        params.update({'cnt': 16})  # Request 16 days
        
        return self._make_api_request(url, params)

    # HISTORICAL DATA API
    def get_historical_weather(self, 
                             lat: float, 
                             lon: float,
                             date: datetime,
                             units: Optional[str] = None) -> Dict:
        """
        Get historical weather data for a specific date.
        Student Pack Feature: 1 year archive, 50,000 calls/day.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            date (datetime): Date for historical data (up to 1 year ago)
            units (str, optional): Temperature units
        
        Returns:
            Dict: Historical weather data
        """
        units = units or self.default_units
        
        # Convert date to Unix timestamp
        timestamp = int(date.timestamp())
        
        params = {
            'lat': lat,
            'lon': lon,
            'dt': timestamp,
            'appid': self.api_key,
            'units': units
        }
        
        url = self.history_url
        return self._make_api_request(url, params)

    def get_historical_weather_range(self, 
                                   lat: float, 
                                   lon: float,
                                   start_date: datetime,
                                   end_date: datetime,
                                   units: Optional[str] = None) -> List[Dict]:
        """
        Get historical weather data for a date range.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            start_date (datetime): Start date
            end_date (datetime): End date
            units (str, optional): Temperature units
        
        Returns:
            List[Dict]: List of historical weather data
        """
        historical_data = []
        current_date = start_date
        
        while current_date <= end_date:
            try:
                data = self.get_historical_weather(lat, lon, current_date, units)
                historical_data.append(data)
                current_date += timedelta(days=1)
                time.sleep(0.1)  # Small delay to respect rate limits
            except Exception as e:
                print(f"Error fetching data for {current_date}: {e}")
                current_date += timedelta(days=1)
        
        return historical_data

    # AIR POLLUTION API
    def get_air_pollution_current(self, lat: float, lon: float) -> Dict:
        """
        Get current air pollution data.
        Student Pack Feature: Air Pollution API.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
        
        Returns:
            Dict: Current air pollution data
        """
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        url = f"{self.pollution_url}/current"
        return self._make_api_request(url, params)

    def get_air_pollution_forecast(self, lat: float, lon: float) -> Dict:
        """Get air pollution forecast for 5 days."""
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key
        }
        
        url = f"{self.pollution_url}/forecast"
        return self._make_api_request(url, params)

    def get_air_pollution_history(self, 
                                lat: float, 
                                lon: float,
                                start: datetime,
                                end: datetime) -> Dict:
        """Get historical air pollution data."""
        params = {
            'lat': lat,
            'lon': lon,
            'start': int(start.timestamp()),
            'end': int(end.timestamp()),
            'appid': self.api_key
        }
        
        url = f"{self.pollution_url}/history"
        return self._make_api_request(url, params)

    # GEOCODING API
    def geocode_city(self, city: str, limit: int = 5) -> List[Dict]:
        """
        Get coordinates for a city name.
        Student Pack Feature: Geocoding API.
        
        Args:
            city (str): City name
            limit (int): Maximum number of results (default: 5)
        
        Returns:
            List[Dict]: List of location data with coordinates
        """
        params = {
            'q': city,
            'limit': limit,
            'appid': self.api_key
        }        
        url = f"{self.geocoding_url}/direct"
        result = self._make_api_request(url, params)
        return result if isinstance(result, list) else [result]

    def reverse_geocode(self, lat: float, lon: float, limit: int = 5) -> List[Dict]:
        """Get location names from coordinates (reverse geocoding)."""
        params = {
            'lat': lat,
            'lon': lon,
            'limit': limit,
            'appid': self.api_key
        }        
        url = f"{self.geocoding_url}/reverse"
        result = self._make_api_request(url, params)
        return result if isinstance(result, list) else [result]

    # WEATHER MAPS API
    def get_weather_map_url(self, 
                          layer: str, 
                          z: int, 
                          x: int, 
                          y: int) -> str:
        """
        Get weather map tile URL.
        Student Pack Feature: 15 weather layers (History, Current, Forecast).
        
        Available layers:
        - temp_new: Temperature
        - precipitation_new: Precipitation
        - pressure_new: Pressure
        - wind_new: Wind
        - clouds_new: Clouds
        - etc.
        
        Args:
            layer (str): Map layer type
            z (int): Zoom level (0-18)
            x (int): Tile X coordinate
            y (int): Tile Y coordinate
        
        Returns:
            str: Map tile URL
        """
        return f"{self.maps_url}/{layer}/{z}/{x}/{y}.png?appid={self.api_key}"

    def get_available_map_layers(self) -> List[str]:
        """Get list of available weather map layers."""
        return [
            'temp_new',      # Temperature
            'precipitation_new',  # Precipitation
            'pressure_new',  # Sea level pressure
            'wind_new',      # Wind speed
            'clouds_new',    # Clouds
            'radar',         # Precipitation radar
            'satellite',     # Satellite imagery
            'temp',          # Temperature (legacy)
            'precipitation', # Precipitation (legacy)
            'pressure',      # Pressure (legacy)
            'wind',          # Wind (legacy)
            'clouds',        # Clouds (legacy)
        ]

    # STATISTICAL WEATHER DATA API
    def get_statistical_weather(self, 
                              lat: float, 
                              lon: float,
                              start: datetime,
                              end: datetime) -> Dict:
        """
        Get statistical weather data.
        Student Pack Feature: Statistical Weather Data API.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            start (datetime): Start date
            end (datetime): End date
        
        Returns:
            Dict: Statistical weather data
        """
        params = {
            'lat': lat,
            'lon': lon,
            'start': int(start.timestamp()),
            'end': int(end.timestamp()),
            'appid': self.api_key
        }
        
        url = self.statistics_url
        return self._make_api_request(url, params)

    # ACCUMULATED PARAMETERS
    def get_accumulated_temperature(self, 
                                  lat: float, 
                                  lon: float,
                                  threshold: float,
                                  start: datetime,
                                  end: datetime) -> Dict:
        """
        Get accumulated temperature data.
        Student Pack Feature: Accumulated Parameters.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            threshold (float): Temperature threshold
            start (datetime): Start date
            end (datetime): End date
        
        Returns:
            Dict: Accumulated temperature data
        """
        params = {
            'lat': lat,
            'lon': lon,
            'threshold': threshold,
            'start': int(start.timestamp()),
            'end': int(end.timestamp()),
            'appid': self.api_key
        }
        
        url = f"{self.base_url}/accumulation/temperature"
        return self._make_api_request(url, params)

    def get_accumulated_precipitation(self, 
                                    lat: float, 
                                    lon: float,
                                    threshold: float,
                                    start: datetime,
                                    end: datetime) -> Dict:
        """Get accumulated precipitation data."""
        params = {
            'lat': lat,
            'lon': lon,
            'threshold': threshold,
            'start': int(start.timestamp()),
            'end': int(end.timestamp()),
            'appid': self.api_key
        }
        
        url = f"{self.base_url}/accumulation/precipitation"
        return self._make_api_request(url, params)

    # UTILITY METHODS
    def format_weather_data(self, weather_data: Dict) -> Dict:
        """Format raw weather data into a more readable structure."""
        try:
            return {
                'city': weather_data.get('name', 'Unknown'),
                'country': weather_data.get('sys', {}).get('country', 'Unknown'),
                'temperature': weather_data['main']['temp'],
                'feels_like': weather_data['main']['feels_like'],
                'humidity': weather_data['main']['humidity'],
                'pressure': weather_data['main']['pressure'],
                'description': weather_data['weather'][0]['description'].title(),
                'main': weather_data['weather'][0]['main'],
                'wind_speed': weather_data.get('wind', {}).get('speed', 'N/A'),
                'wind_direction': weather_data.get('wind', {}).get('deg', 'N/A'),
                'visibility': weather_data.get('visibility', 'N/A'),
                'coordinates': {
                    'lat': weather_data['coord']['lat'],
                    'lon': weather_data['coord']['lon']
                },
                'timestamp': weather_data.get('dt', int(time.time())),
                'sunrise': weather_data.get('sys', {}).get('sunrise'),
                'sunset': weather_data.get('sys', {}).get('sunset')
            }
        except KeyError as e:
            raise ValueError(f"Unexpected API response format: missing {e}")

    def format_forecast_data(self, forecast_data: Dict) -> Dict:
        """Format forecast data for easy use."""
        try:
            formatted = {
                'location': {
                    'lat': forecast_data.get('lat'),
                    'lon': forecast_data.get('lon'),
                    'timezone': forecast_data.get('timezone'),
                    'timezone_offset': forecast_data.get('timezone_offset')
                },
                'current': None,
                'hourly': [],
                'daily': []
            }
            
            # Format current weather if available
            if 'current' in forecast_data:
                current = forecast_data['current']
                formatted['current'] = {
                    'timestamp': current.get('dt'),
                    'temperature': current.get('temp'),
                    'feels_like': current.get('feels_like'),
                    'humidity': current.get('humidity'),
                    'pressure': current.get('pressure'),
                    'wind_speed': current.get('wind_speed'),
                    'wind_deg': current.get('wind_deg'),
                    'weather': current.get('weather', [{}])[0],
                    'visibility': current.get('visibility'),
                    'uv_index': current.get('uvi')
                }
            
            # Format hourly forecast
            if 'hourly' in forecast_data:
                for hour in forecast_data['hourly']:
                    formatted['hourly'].append({
                        'timestamp': hour.get('dt'),
                        'temperature': hour.get('temp'),
                        'feels_like': hour.get('feels_like'),
                        'humidity': hour.get('humidity'),
                        'pressure': hour.get('pressure'),
                        'wind_speed': hour.get('wind_speed'),
                        'weather': hour.get('weather', [{}])[0],
                        'pop': hour.get('pop', 0)  # Probability of precipitation
                    })
            
            # Format daily forecast
            if 'daily' in forecast_data:
                for day in forecast_data['daily']:
                    formatted['daily'].append({
                        'timestamp': day.get('dt'),
                        'temperature': day.get('temp', {}),
                        'feels_like': day.get('feels_like', {}),
                        'humidity': day.get('humidity'),
                        'pressure': day.get('pressure'),
                        'wind_speed': day.get('wind_speed'),
                        'weather': day.get('weather', [{}])[0],
                        'pop': day.get('pop', 0),
                        'rain': day.get('rain', {}),
                        'snow': day.get('snow', {}),
                        'uv_index': day.get('uvi')
                    })
            
            return formatted
            
        except Exception as e:
            raise ValueError(f"Error formatting forecast data: {e}")

    def get_api_usage_info(self) -> Dict:
        """Get comprehensive API usage and limits information."""
        return {
            'subscription': self.subscription_info,
            'endpoints': {
                'current_weather': f"{self.base_url}/weather",
                'forecast_onecall': self.onecall_url,
                'historical': self.history_url,
                'geocoding': self.geocoding_url,
                'air_pollution': self.pollution_url,
                'weather_maps': self.maps_url,
                'statistics': self.statistics_url
            },
            'rate_limits': {
                'current_forecast': f"{Config.API_CALLS_PER_MINUTE:,} calls/minute",
                'monthly_total': f"{Config.API_CALLS_PER_MONTH:,} calls/month",
                'historical_daily': f"{Config.HISTORY_CALLS_PER_DAY:,} calls/day"
            },
            'features_available': list(Config.API_FEATURES.keys()),
            'student_pack_benefits': [
                "Free for educational use",
                "Extended rate limits",
                "Full historical data access",
                "All weather map layers",
                "Air pollution data",
                "Advanced forecasting"
            ]
        }

def main():
    """Example usage of the Enhanced Weather API with Student Pack features."""
    try:
        # Initialize the enhanced weather API
        weather = EnhancedWeatherAPI()
        print("🎓 Student Pack Weather API initialized!")
        
        # Display API info
        api_info = weather.get_api_usage_info()
        print(f"\n📋 Subscription: {api_info['subscription']['subscription_plan']}")
        print(f"💳 Pricing: {api_info['subscription']['pricing']}")
        print(f"⚡ Rate Limits: {api_info['rate_limits']['current_forecast']}")
        
        # Get coordinates for a city using geocoding
        print(f"\n🔍 Geocoding: {Config.DEFAULT_CITY}")
        locations = weather.geocode_city(Config.DEFAULT_CITY)
        if locations:
            location = locations[0]
            lat, lon = location['lat'], location['lon']
            print(f"📍 Found: {location['name']}, {location.get('country')} ({lat}, {lon})")
            
            # Get current weather
            print(f"\n🌤️ Current Weather:")
            current = weather.get_current_weather_by_coordinates(lat, lon)
            formatted = weather.format_weather_data(current)
            print(f"🌡️ Temperature: {formatted['temperature']}°C")
            print(f"☁️ Conditions: {formatted['description']}")
            
            # Get hourly forecast (4 days)
            print(f"\n📊 Hourly Forecast (4 days):")
            forecast = weather.get_hourly_forecast_4days(lat, lon)
            forecast_formatted = weather.format_forecast_data(forecast)
            print(f"📈 {len(forecast_formatted['hourly'])} hourly forecasts available")
            
            # Get air pollution
            print(f"\n🏭 Air Pollution:")
            pollution = weather.get_air_pollution_current(lat, lon)
            aqi = pollution['list'][0]['main']['aqi']
            print(f"🌬️ Air Quality Index: {aqi}/5")
            
            # Get historical weather (7 days ago)
            print(f"\n📚 Historical Weather (7 days ago):")
            week_ago = datetime.now() - timedelta(days=7)
            historical = weather.get_historical_weather(lat, lon, week_ago)
            if 'data' in historical:
                hist_temp = historical['data'][0]['temp']
                print(f"🕰️ Temperature 7 days ago: {hist_temp}°C")
        
    except ValueError as e:
        print(f"❌ Configuration/API Error:\n{e}")
    except requests.RequestException as e:
        print(f"❌ Network/API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
