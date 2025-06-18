#!/usr/bin/env python3
"""
Test script for the unified weather dashboard application.
This script validates that all components are working properly.
"""

import sys
import os
from datetime import datetime

def test_imports():
    """Test that all required modules can be imported."""
    print("🔍 Testing imports...")
    
    try:
        import tkinter as tk
        print("✅ tkinter imported successfully")
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        return False
    
    try:
        import requests
        print("✅ requests imported successfully")
    except ImportError as e:
        print(f"❌ requests import failed: {e}")
        return False
    
    try:
        from dotenv import load_dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ python-dotenv import failed: {e}")
        return False
    
    return True

def test_unified_app():
    """Test the unified weather dashboard application."""
    print("\n🔍 Testing unified weather dashboard...")
    
    try:
        # Import the main components
        from unified_weather_dashboard import WeatherAPI, WeatherData, ForecastData
        print("✅ Main classes imported successfully")
        
        # Test API initialization
        api = WeatherAPI()
        print("✅ WeatherAPI initialized successfully")
          # Test data classes
        sample_weather = WeatherData(
            temperature=25.0,
            feels_like=27.0,
            humidity=60,
            pressure=1013,
            wind_speed=5.0,
            wind_direction=180,
            visibility=10000,
            description="Clear Sky",
            icon="01d",
            city="Test City",
            country="TC",
            timestamp=int(datetime.now().timestamp()),
            cloudiness=20
        )
        print("✅ WeatherData class works correctly")
        
        sample_forecast = ForecastData(
            hourly=[],
            daily=[]
        )
        print("✅ ForecastData class works correctly")
        
        return True
        
    except Exception as e:
        print(f"❌ Unified app test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_environment():
    """Test environment configuration."""
    print("\n🔍 Testing environment configuration...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENWEATHER_API_KEY', '')
        if api_key:
            print(f"✅ API key found: {api_key[:10]}...")
        else:
            print("⚠️ API key not found in environment variables")
            print("   Make sure to set OPENWEATHER_API_KEY in .env file")
        
        return True
        
    except Exception as e:
        print(f"❌ Environment test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("🎓 OpenWeatherMap Student Pack - Unified App Tests")
    print("=" * 60)
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test environment
    if not test_environment():
        all_passed = False
    
    # Test unified app
    if not test_unified_app():
        all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! The unified application is ready to use.")
        print("💡 Run 'python unified_weather_dashboard.py' to start the application.")
    else:
        print("❌ Some tests failed. Please check the issues above.")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
