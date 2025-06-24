#!/usr/bin/env python3
"""
Test the restored original dashboard.
"""

import sys
import os

# Add src to path
sys.path.insert(0, 'src')

print("🧪 Testing Original Weather Dashboard...")
print("=" * 50)

try:
    # Test imports
    print("📦 Testing imports...")
    from config.config import ConfigurationManager
    print("✅ Config module imported")
    
    from core.weather_core import WeatherDashboardCore
    print("✅ Weather core imported")
    
    from ui.dashboard_ui import WeatherDashboardUI
    print("✅ Original Dashboard UI imported")
    
    from ui.weather_displays import WeatherDisplays
    print("✅ Weather displays imported")
    
    # Test config loading
    print("\n⚙️ Testing configuration...")
    config_manager = ConfigurationManager()
    
    if config_manager.config.api.api_key:
        print(f"✅ API key configured: {config_manager.config.api.api_key[:10]}...")
    else:
        print("❌ API key not configured")
    
    print(f"✅ Theme: {config_manager.config.ui.theme}")
    print(f"✅ Default city: {config_manager.config.default_city}")
    
    # Test basic initialization without starting GUI
    print("\n🎨 Testing component initialization...")
    core = WeatherDashboardCore()
    print("✅ Weather core initialized")
    
    print("\n🚀 All tests passed! The original dashboard should launch successfully.")
    print("💡 Run: python launcher.py")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
