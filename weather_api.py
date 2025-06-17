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
        self.base_url = Config.OPENWEATHER_BASE_URL  # Premium endpoint
        self.fallback_url = Config.OPENWEATHER_FREE_URL  # Free endpoint fallback
        self.default_units = Config.TEMPERATURE_UNITS
        self.subscription_info = Config.get_api_info()
        
    def _make_api_request(self, endpoint, params):
        """Make API request with premium endpoint and fallback capability."""
        # Try premium endpoint first
        try:
            url = f"{self.base_url}/{endpoint}"
            print(f"🔄 Trying premium endpoint: {url}")
            response = requests.get(url, params=params)
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.HTTPError as e:
            # If premium endpoint fails, try fallback to free endpoint
            if e.response and e.response.status_code in [401, 403]:
                print(f"⚠️ Premium endpoint failed, trying free endpoint...")
                try:
                    fallback_url = f"{self.fallback_url}/{endpoint}"
                    response = requests.get(fallback_url, params=params)
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.HTTPError as fallback_error:
                    # Handle errors from fallback endpoint
                    if fallback_error.response and fallback_error.response.status_code == 401:
                        raise ValueError(
                            "❌ API Authentication Failed\n\n"
                            "Developer API Subscription Details:\n"
                            f"• API Key: {self.api_key[:8]}...\n"
                            f"• Premium Endpoint: {self.base_url}\n"
                            f"• Free Endpoint: {self.fallback_url}\n\n"
                            "Troubleshooting:\n"
                            "1. Verify your API key is activated\n"
                            "2. Check subscription status at https://openweathermap.org/price\n"
                            "3. New API keys take up to 2 hours to activate\n"
                            "4. Contact support@openweathermap.org for assistance\n\n"
                            "API Documentation: https://openweathermap.org/api"
                        )
                    elif fallback_error.response and fallback_error.response.status_code == 404:
                        raise ValueError("City not found")
                    else:
                        raise requests.RequestException(f"API request failed: {fallback_error}")
            else:
                # Re-raise original error if not auth-related
                raise e
    
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
                raise ValueError(
                    "Invalid API key. Possible causes:\n"
                    "1. New API keys take up to 2 hours to activate\n"
                    "2. Check your API key at https://home.openweathermap.org/api_keys\n"
                    "3. Ensure your API key is correctly set in the .env file\n"
                    f"Current API key (first 8 chars): {self.api_key[:8] if self.api_key else 'None'}..."
                )
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
        print(f"❌ Configuration/API Error:\n{e}")
    except requests.RequestException as e:
        print(f"❌ Network/API Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")

if __name__ == "__main__":
    main()
