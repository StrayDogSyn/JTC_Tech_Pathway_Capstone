"""
OpenWeatherMap API implementation for current weather data.
API Documentation: https://openweathermap.org/current
"""

import requests
from typing import Dict, Optional
from config import Config

class WeatherAPI:
    """Class for interacting with the OpenWeatherMap Current Weather API."""
    
    def __init__(self):
        """Initialize the WeatherAPI with configuration validation."""
        Config.validate_config()
        self.api_key = Config.OPENWEATHER_API_KEY
        self.base_url = Config.OPENWEATHER_BASE_URL
        self.default_units = Config.TEMPERATURE_UNITS
    
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
            Dict: Weather data from OpenWeatherMap API
        
        Raises:
            requests.RequestException: If API request fails
            ValueError: If city is not found
        """
        # Build location query
        location = city
        if country_code:
            location = f"{city},{country_code}"
        
        # Set units
        units = units or self.default_units
        
        # API parameters
        params = {
            'q': location,
            'appid': self.api_key,
            'units': units
        }
        
        try:
            response = requests.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            if e.response and e.response.status_code == 404:
                raise ValueError(f"City '{city}' not found")
            elif e.response and e.response.status_code == 401:
                raise ValueError("Invalid API key")
            else:
                raise requests.RequestException(f"API request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API request failed: {e}")
    
    def get_weather_by_coordinates(self, 
                                 lat: float, 
                                 lon: float,
                                 units: Optional[str] = None) -> Dict:
        """
        Get current weather data by geographic coordinates.
        
        Args:
            lat (float): Latitude
            lon (float): Longitude
            units (str, optional): Temperature units ('metric', 'imperial', 'kelvin')
        
        Returns:
            Dict: Weather data from OpenWeatherMap API
        """
        units = units or self.default_units
        
        params = {
            'lat': lat,
            'lon': lon,
            'appid': self.api_key,
            'units': units
        }
        
        try:
            response = requests.get(f"{self.base_url}/weather", params=params)
            response.raise_for_status()
            return response.json()
        
        except requests.exceptions.HTTPError as e:
            if e.response and e.response.status_code == 401:
                raise ValueError("Invalid API key")
            else:
                raise requests.RequestException(f"API request failed: {e}")
        except requests.exceptions.RequestException as e:
            raise requests.RequestException(f"API request failed: {e}")
    
    def format_weather_data(self, weather_data: Dict) -> Dict:
        """
        Format raw weather data into a more readable structure.
        
        Args:
            weather_data (Dict): Raw weather data from API
        
        Returns:
            Dict: Formatted weather information
        """
        try:
            return {
                'city': weather_data['name'],
                'country': weather_data['sys']['country'],
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
                }
            }
        except KeyError as e:
            raise ValueError(f"Unexpected API response format: missing {e}")

def main():
    """Example usage of the WeatherAPI class."""
    try:
        # Initialize the weather API
        weather = WeatherAPI()
        
        # Get weather for default city
        print(f"Getting weather for {Config.DEFAULT_CITY}...")
        weather_data = weather.get_current_weather(Config.DEFAULT_CITY)
        formatted_data = weather.format_weather_data(weather_data)
        
        # Display formatted weather information
        print(f"\n🌤️  Weather in {formatted_data['city']}, {formatted_data['country']}")
        print(f"🌡️  Temperature: {formatted_data['temperature']}°")
        print(f"🤔 Feels like: {formatted_data['feels_like']}°")
        print(f"☁️  Conditions: {formatted_data['description']}")
        print(f"💧 Humidity: {formatted_data['humidity']}%")
        print(f"🌬️  Wind: {formatted_data['wind_speed']} m/s")
        
    except ValueError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
