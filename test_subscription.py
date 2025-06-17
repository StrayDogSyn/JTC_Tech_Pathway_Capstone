#!/usr/bin/env python3
"""
Test script to verify OpenWeatherMap Developer API subscription integration.
Run this to test the subscription information and API configuration.
"""

from config import Config
from weather_api import WeatherAPI
import json

def test_subscription_info():
    """Test the subscription information functionality."""
    print("🧪 Testing OpenWeatherMap Developer API Subscription Integration\n")
    
    try:
        # Test 1: Config validation
        print("1️⃣ Testing configuration validation...")
        Config.validate_config()
        print("✅ Configuration validation passed\n")
        
        # Test 2: API info retrieval
        print("2️⃣ Testing API information retrieval...")
        api_info = Config.get_api_info()
        print(f"✅ API Info Retrieved:")
        print(f"   • Plan: {api_info['subscription_plan']}")
        print(f"   • Pricing: {api_info['pricing']}")
        print(f"   • Rate Limits: {api_info['rate_limits']['per_minute']}/min, {api_info['rate_limits']['per_month']:,}/month")
        print(f"   • Endpoint: {api_info['endpoint']}")
        print(f"   • API Key: {api_info['api_key']}")
        print()
        
        # Test 3: Subscription instructions
        print("3️⃣ Testing subscription instructions...")
        instructions = Config.get_subscription_instructions()
        print(f"✅ Subscription Instructions Retrieved:")
        print(f"   • Title: {instructions['title']}")
        print(f"   • Status: {instructions['activation_status']}")
        print(f"   • Endpoints: Premium ({instructions['endpoints']['premium']}) + Fallback ({instructions['endpoints']['fallback']})")
        print()
        
        # Test 4: API initialization
        print("4️⃣ Testing WeatherAPI initialization...")
        weather_api = WeatherAPI()
        print(f"✅ WeatherAPI initialized successfully")
        print(f"   • Using endpoint: {weather_api.base_url}")
        print(f"   • Fallback endpoint: {weather_api.fallback_url}")
        print()
        
        print("🎉 All tests passed! OpenWeatherMap Developer API subscription is properly configured.\n")
        
        # Display subscription summary
        print("📋 SUBSCRIPTION SUMMARY")
        print("=" * 50)
        print(f"Plan: {instructions['instructions']['3_subscription']['plan']}")
        print(f"Features: {', '.join(instructions['instructions']['3_subscription']['included_products'])}")
        print(f"Rate Limits: {instructions['rate_limits']['calls_per_minute']}/min, {instructions['rate_limits']['calls_per_month']:,}/month")
        print(f"Support: {instructions['instructions']['4_support']['contact']}")
        print(f"Documentation: {instructions['instructions']['3_subscription']['links']['api_documentation']}")
        print("=" * 50)
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
        
    return True

if __name__ == "__main__":
    test_subscription_info()
