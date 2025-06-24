#!/usr/bin/env python3
"""
Simple test launcher to verify the glassmorphic weather app works.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

try:
    print("🚀 Testing Glassmorphic Weather Dashboard...")
    print("📦 Importing modules...")
    
    from src.main import WeatherDashboardApp
    print("✅ Main application imported successfully")
    
    print("🎨 Initializing glassmorphic UI...")
    app = WeatherDashboardApp()
    print("✅ Application initialized successfully")
    
    print("🌦️ Starting weather dashboard...")
    app.run()
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)
except Exception as e:
    print(f"❌ Application error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
