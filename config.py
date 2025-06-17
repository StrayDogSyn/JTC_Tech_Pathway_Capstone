"""
Configuration module for managing environment variables and API settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings."""
      # OpenWeatherMap Student Pack API configuration
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    OPENWEATHER_API_KEY_BACKUP = os.getenv('OPENWEATHER_API_KEY_BACKUP')  # Backup key for redundancy
    OPENWEATHER_BASE_URL = "https://api.openweathermap.org/data/2.5"  # Standard endpoint
    OPENWEATHER_ONECALL_URL = "https://api.openweathermap.org/data/3.0/onecall"  # One Call API 3.0
    OPENWEATHER_HISTORY_URL = "https://api.openweathermap.org/data/3.0/onecall/timemachine"  # Historical data
    OPENWEATHER_GEOCODING_URL = "https://api.openweathermap.org/geo/1.0"  # Geocoding API
    OPENWEATHER_POLLUTION_URL = "https://api.openweathermap.org/data/2.5/air_pollution"  # Air Pollution API
    OPENWEATHER_MAPS_URL = "https://tile.openweathermap.org/map"  # Weather Maps API
    OPENWEATHER_STATISTICS_URL = "https://api.openweathermap.org/data/2.5/statistics"  # Statistical API
    
    # Student Pack subscription details
    API_SUBSCRIPTION_TYPE = "Student Pack"  # Free for students
    API_SUBSCRIPTION_PLAN = "Student Educational Pack"
    API_CALLS_PER_MINUTE = 3000  # 3,000 calls/minute limit
    API_CALLS_PER_MONTH = 100000000  # 100,000,000 calls/month
    HISTORY_CALLS_PER_DAY = 50000  # 50,000 historical calls/day
      # Available features for Student Pack subscription
    API_FEATURES = {
        'current_weather': True,
        'forecast_weather': True,  # Hourly forecast 4 days, Daily forecast 16 days
        'history_api': True,  # 1 year archive, 50,000 calls/day
        'premium_endpoints': True,
        'maps_api': True,  # 15 weather layers (History, Current, Forecast)
        'alerts_api': True,  # Weather alerts
        'statistics_api': True,  # Statistical Weather Data API
        'air_pollution': True,  # Air Pollution API
        'geocoding_api': True,  # Geocoding API
        'accumulated_parameters': True,  # Accumulated Parameters
        'hourly_forecast_4days': True,  # Hourly Forecast 4 days
        'daily_forecast_16days': True,  # Daily Forecast 16 days
        'one_year_archive': True,  # 1 year historical archive
    }
      # Subscription information
    SUBSCRIPTION_INFO = {
        'plan': 'Student Educational Pack',
        'price': 'Free for students',
        'calls_per_minute': 3000,
        'calls_per_month': 100000000,
        'history_calls_per_day': 50000,
        'support': 'Community support + Documentation',
        'features': [
            'Current weather data',
            'Hourly Forecast 4 days', 
            'Daily Forecast 16 days',
            'Weather Maps - 15 layers (History, Current, Forecast)',
            'Air Pollution API',
            'Geocoding API',
            'Historical data - 1 year archive',
            'History API',
            'Statistical Weather Data API',
            'Accumulated Parameters',
            'Enhanced data accuracy',
            'Educational use license'
        ],
        'documentation': 'https://openweathermap.org/api',
        'subscription_url': 'https://openweathermap.org/price#student',
        'support_email': 'support@openweathermap.org'}
    
    # Default settings
    DEFAULT_CITY = os.getenv('DEFAULT_CITY', 'New York')
    TEMPERATURE_UNITS = os.getenv('TEMPERATURE_UNITS', 'metric')
    
    @classmethod
    def validate_config(cls):
        """Validate that required configuration is present and show subscription info."""
        if not cls.OPENWEATHER_API_KEY:
            raise ValueError(
                "OPENWEATHER_API_KEY is required. "
                "Please set it in your .env file or environment variables.\n\n"
                "🔑 OpenWeatherMap Developer API Subscription Required:\n"
                f"Plan: {cls.SUBSCRIPTION_INFO['plan']} (${cls.SUBSCRIPTION_INFO['price']})\n"
                f"Calls: {cls.SUBSCRIPTION_INFO['calls_per_minute']}/min, {cls.SUBSCRIPTION_INFO['calls_per_month']:,}/month\n"
                f"Endpoint: {cls.OPENWEATHER_BASE_URL}\n"
                f"Features: {', '.join(cls.SUBSCRIPTION_INFO['features'][:3])}...\n\n"
                f"📖 Get API key: {cls.SUBSCRIPTION_INFO['subscription_url']}\n"
                f"📧 Support: {cls.SUBSCRIPTION_INFO['support_email']}\n"
                f"📚 Docs: {cls.SUBSCRIPTION_INFO['documentation']}"
            )
          # Log subscription information (for debugging)
        primary_key_display = f"{cls.OPENWEATHER_API_KEY[:8]}..." if cls.OPENWEATHER_API_KEY else "Not set"
        backup_key_display = f"{cls.OPENWEATHER_API_KEY_BACKUP[:8]}..." if cls.OPENWEATHER_API_KEY_BACKUP else "Not set"
        
        print(f"🎓 Using {cls.API_SUBSCRIPTION_TYPE} OpenWeatherMap API")
        print(f"🔑 Primary API Key: {primary_key_display}")
        if cls.OPENWEATHER_API_KEY_BACKUP:
            print(f"🔑 Backup API Key: {backup_key_display} (configured)")
        print(f"🌐 Endpoint: {cls.OPENWEATHER_BASE_URL}")
        print(f"📊 Rate limits: {cls.API_CALLS_PER_MINUTE:,}/min, {cls.API_CALLS_PER_MONTH:,}/month")
        print(f"📚 Historical: {cls.HISTORY_CALLS_PER_DAY:,}/day, 1 year archive")
        print(f"✅ Features: Current, Forecasts (4h/16d), Maps, Air Pollution, Geocoding, History, Statistics")
        return True        
    @classmethod
    def get_api_info(cls):
        """Get API subscription information."""
        return {
            'subscription_type': cls.API_SUBSCRIPTION_TYPE,
            'subscription_plan': cls.SUBSCRIPTION_INFO['plan'],
            'pricing': cls.SUBSCRIPTION_INFO['price'],
            'rate_limits': {
                'per_minute': cls.API_CALLS_PER_MINUTE,
                'per_month': cls.API_CALLS_PER_MONTH,
                'history_per_day': cls.HISTORY_CALLS_PER_DAY
            },
            'endpoint': cls.OPENWEATHER_BASE_URL,
            'api_key': cls.OPENWEATHER_API_KEY[:8] + "..." if cls.OPENWEATHER_API_KEY else "Not set",
            'features': cls.API_FEATURES,
            'subscription_info': cls.SUBSCRIPTION_INFO,
            'documentation': cls.SUBSCRIPTION_INFO['documentation'],
            'support_email': cls.SUBSCRIPTION_INFO['support_email']
        }
    
    @classmethod
    def get_subscription_instructions(cls):
        """
        Get comprehensive subscription instructions for OpenWeatherMap Developer API.
        Based on official activation confirmation email.
        """
        return {
            'title': 'OpenWeatherMap Developer API - Subscription Instructions',
            'activation_status': 'Your account and API key are activated and ready for operating with Weather API',
            'instructions': {
                '1_endpoints': {
                    'title': '1. Endpoints',
                    'primary_endpoint': 'pro.openweathermap.org',
                    'description': 'Use the high-end servers endpoint for all API calls',
                    'example': 'pro.openweathermap.org/data/2.5/weather?q=London,uk&APPID=YOUR_API_KEY',
                    'note': 'Always use the premium endpoint for best performance and reliability'
                },
                '2_api_key': {
                    'title': '2. API Key (APPID)',
                    'requirements': [
                        'Always use your API key in each API call',
                        'You can create more API keys on your account page',
                        'Keep your API key secure and never share it publicly'
                    ],
                    'documentation': 'http://openweathermap.org/appid#use'
                },
                '3_subscription': {
                    'title': '3. Subscription',
                    'plan': 'Developer',
                    'included_products': [
                        'Current weather data',
                        '5-day weather forecast',
                        'Weather maps',
                        'Weather alerts'
                    ],
                    'not_included': [
                        'History API (not available for your subscription)'
                    ],
                    'links': {
                        'plan_details': 'https://openweathermap.org/price',
                        'manage_subscription': 'https://openweathermap.org/price#commonquestions',
                        'api_documentation': 'https://openweathermap.org/api'
                    }
                },
                '4_support': {
                    'title': '4. Support',
                    'description': 'For further technical questions and support',
                    'contact': 'support@openweathermap.org',
                    'priority': 'High priority customer support for Developer plan subscribers'
                }
            },
            'rate_limits': {
                'calls_per_minute': cls.API_CALLS_PER_MINUTE,
                'calls_per_month': cls.API_CALLS_PER_MONTH
            },            'endpoints': {
                'base': cls.OPENWEATHER_BASE_URL,
                'onecall': cls.OPENWEATHER_ONECALL_URL,
                'history': cls.OPENWEATHER_HISTORY_URL,
                'geocoding': cls.OPENWEATHER_GEOCODING_URL,
                'pollution': cls.OPENWEATHER_POLLUTION_URL,
                'maps': cls.OPENWEATHER_MAPS_URL,
                'statistics': cls.OPENWEATHER_STATISTICS_URL
            }
        }
