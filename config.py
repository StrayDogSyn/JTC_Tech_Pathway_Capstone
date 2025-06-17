"""
Configuration module for managing environment variables and API settings.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for API keys and settings."""
    
    # OpenWeatherMap Developer API configuration (Premium)
    OPENWEATHER_API_KEY = os.getenv('OPENWEATHER_API_KEY')
    OPENWEATHER_API_KEY_BACKUP = os.getenv('OPENWEATHER_API_KEY_BACKUP')  # Backup key for redundancy
    OPENWEATHER_BASE_URL = "https://pro.openweathermap.org/data/2.5"  # Premium endpoint
    OPENWEATHER_FREE_URL = "https://api.openweathermap.org/data/2.5"  # Free endpoint fallback
      # OpenWeatherMap Developer API subscription details
    API_SUBSCRIPTION_TYPE = "Developer"  # Developer subscription plan
    API_SUBSCRIPTION_PLAN = "Developer"
    API_CALLS_PER_MINUTE = 60  # 60 calls/minute limit
    API_CALLS_PER_MONTH = 1000000  # 1,000,000 calls/month
    
    # Available features for Developer subscription
    API_FEATURES = {
        'current_weather': True,
        'forecast_weather': True,  # 5-day weather forecast
        'history_api': False,  # Not available for Developer subscription
        'premium_endpoints': True,
        'maps_api': True,  # Weather maps
        'alerts_api': True,  # Weather alerts
        'statistics_api': False,  # Not available for Developer subscription
        'solar_radiation': False,  # Not available for Developer subscription
        'road_risk': False,  # Not available for Developer subscription
    }
    
    # Subscription information
    SUBSCRIPTION_INFO = {
        'plan': 'Developer',
        'price': '$40/month',
        'calls_per_minute': 60,
        'calls_per_month': 1000000,
        'support': 'Email support',
        'features': [
            'Current weather data',
            '5-day weather forecast', 
            'Weather maps',
            'Weather alerts',
            'Premium API endpoints (pro.openweathermap.org)',
            'Enhanced data accuracy',
            'Priority support'
        ],
        'documentation': 'https://openweathermap.org/api',
        'subscription_url': 'https://openweathermap.org/price',
        'support_email': 'support@openweathermap.org'    }
    
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
        
        print(f"🔑 Using {cls.API_SUBSCRIPTION_TYPE} OpenWeatherMap API")
        print(f"🔑 Primary API Key: {primary_key_display}")
        if cls.OPENWEATHER_API_KEY_BACKUP:
            print(f"🔑 Backup API Key: {backup_key_display} (configured)")
        print(f"🌐 Endpoint: {cls.OPENWEATHER_BASE_URL}")
        print(f"📊 Rate limits: {cls.API_CALLS_PER_MINUTE}/min, {cls.API_CALLS_PER_MONTH:,}/month")
        print(f"✅ Features: Current Weather, 5-Day Forecast, Weather Maps, Alerts")
        if not cls.API_FEATURES['history_api']:
            print("❌ History API: Not available for Developer subscription")
        if not cls.API_FEATURES['statistics_api']:
            print("❌ Statistics API: Not available for Developer subscription")        
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
                'per_month': cls.API_CALLS_PER_MONTH
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
            },
            'endpoints': {
                'premium': cls.OPENWEATHER_BASE_URL,
                'fallback': cls.OPENWEATHER_FREE_URL
            }
        }
