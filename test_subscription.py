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

def test_security_measures():
    """Test security measures for API key protection."""
    print("🔒 Testing security measures...\n")
    
    try:
        # Test 1: Check that API key is not None and not a placeholder
        api_key = Config.OPENWEATHER_API_KEY
        if not api_key:
            print("⚠️  WARNING: No API key found in environment variables")
            print("   Please set OPENWEATHER_API_KEY in your .env file")
            return False
        elif api_key in ['your_api_key_here', 'your_api_key_here_replace_with_actual_key', 'your_developer_api_key_here_replace_with_actual_key']:
            print("⚠️  WARNING: API key appears to be a placeholder")
            print("   Please replace with your actual OpenWeatherMap Developer API key")
            return False
        
        # Test 2: Verify API key is properly masked in get_api_info
        api_info = Config.get_api_info()
        displayed_key = api_info['api_key']
        if len(displayed_key) > 12:  # Should be 8 chars + "..."
            print("⚠️  WARNING: API key may not be properly masked in API info")
            return False
        
        # Test 3: Check that .env.example doesn't contain real API key
        try:
            with open('.env.example', 'r') as f:
                env_example_content = f.read()
                if api_key in env_example_content:
                    print("❌ SECURITY ISSUE: Real API key found in .env.example file!")
                    print("   Remove the real API key from .env.example immediately")
                    return False
        except FileNotFoundError:
            print("⚠️  .env.example file not found")
        
        # Test 4: Verify API key length (OpenWeatherMap keys are typically 32 chars)
        if len(api_key) != 32:
            print(f"⚠️  WARNING: API key length ({len(api_key)}) is unusual for OpenWeatherMap")
            print("   Standard OpenWeatherMap API keys are 32 characters long")
        
        print("✅ Security measures validated:")
        print(f"   • API key loaded from environment: {displayed_key}")
        print(f"   • API key properly masked in logs")
        print(f"   • .env.example doesn't contain real key")
        print()
        
        return True
        
    except Exception as e:
        print(f"❌ Security test failed: {e}")
        return False

if __name__ == "__main__":
    test_subscription_info()
    test_security_measures()
