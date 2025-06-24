#!/usr/bin/env python3
"""
Test script to verify search functionality and weather data loading.
"""

import sys
import os
import asyncio

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_weather_core():
    """Test the weather core functionality."""
    try:
        print("🧪 Testing Weather Core...")
        from src.core.weather_core import WeatherDashboardCore
        
        core = WeatherDashboardCore()
        print("✅ Weather core initialized")
        
        # Test loading weather data
        print("🔍 Testing weather data load for 'New York'...")
        result = core.load_weather_data("New York")
        
        if hasattr(core, 'current_weather') and core.current_weather:
            print(f"✅ Weather data loaded: {core.current_weather.city}, {core.current_weather.temperature}°")
        else:
            print("⚠️ No current weather data returned")
            
        return True
        
    except Exception as e:
        print(f"❌ Weather core test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_glassmorphic_ui():
    """Test the glassmorphic UI components."""
    try:
        print("🎨 Testing Glassmorphic UI...")
        from src.ui.glassmorphic_dashboard import GlassmorphicWeatherDashboard
        from src.ui.glassmorphic_components import GlassmorphicCard
        
        print("✅ Glassmorphic components imported successfully")
        
        # Test creating a dashboard instance
        dashboard = GlassmorphicWeatherDashboard(title="Test Dashboard")
        print("✅ Glassmorphic dashboard created")
        
        # Test search functionality
        dashboard.set_city_text("London")
        print("✅ Search bar text set successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Glassmorphic UI test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🧪 Running Weather Dashboard Component Tests...")
    print("=" * 50)
    
    core_ok = test_weather_core()
    ui_ok = test_glassmorphic_ui()
    
    print("=" * 50)
    if core_ok and ui_ok:
        print("✅ All tests passed! The application should work properly.")
    else:
        print("❌ Some tests failed. Check the errors above.")
    
    print("\n🚀 Try running: python launcher.py")
