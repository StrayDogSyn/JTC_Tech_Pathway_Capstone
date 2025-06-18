"""
Test script for the Complete Weather Dashboard
Verifies that all components can be imported and initialized properly.
Tests the main dashboard, COBRA styling system, and machine learning functionality.
"""

import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("🧪 Testing imports...")
    
    try:
        import tkinter as tk
        print("✅ tkinter imported successfully")
    except ImportError as e:
        print(f"❌ tkinter import failed: {e}")
        return False
    
    try:
        import ttkbootstrap as ttk
        print("✅ ttkbootstrap imported successfully")
    except ImportError as e:
        print(f"❌ ttkbootstrap import failed: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ matplotlib imported successfully")
    except ImportError as e:
        print(f"❌ matplotlib import failed: {e}")
        return False
    
    try:
        import sklearn
        print("✅ scikit-learn imported successfully")
    except ImportError as e:
        print(f"❌ scikit-learn import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas imported successfully")
    except ImportError as e:
        print(f"❌ pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ numpy imported successfully")
    except ImportError as e:
        print(f"❌ numpy import failed: {e}")
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
    
    try:
        from PIL import Image
        print("✅ Pillow imported successfully")
    except ImportError as e:
        print(f"❌ Pillow import failed: {e}")
        return False
    
    return True

def test_api_key():
    """Test API key configuration."""
    print("\n🔑 Testing API key configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENWEATHER_API_KEY', '')
    
    if not api_key:
        print("⚠️ No API key found in environment variables")
        print("   Create a .env file with: OPENWEATHER_API_KEY=your_key_here")
        return False
    elif len(api_key) < 10:
        print("⚠️ API key appears to be too short")
        return False
    else:
        print(f"✅ API key found: {api_key[:10]}...")
        return True

def test_complete_dashboard_import():
    """Test importing the complete dashboard module."""
    print("\n📱 Testing complete dashboard import...")
    
    try:
        # Import the main application components
        sys.path.insert(0, os.path.dirname(__file__))
        
        from complete_weather_dashboard import (
            WeatherAPI, 
            WeatherPredictor, 
            CompleteWeatherDashboard,
            load_settings,
            save_settings
        )
        print("✅ Complete dashboard components imported successfully")
        
        # Test settings functions
        settings = load_settings()
        print(f"✅ Settings loaded: {settings}")
        
        # Test API class initialization
        api = WeatherAPI()
        print("✅ WeatherAPI initialized successfully")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during testing: {e}")
        return False

def test_cobra_styling_import():
    """Test importing the COBRA styling components."""
    print("\n🐍 Testing COBRA styling import...")
    
    try:
        from cobra_style import COBRA_COLORS, apply_cobra_theme, CobraChartAnimator
        print("✅ COBRA styling components imported successfully")
        return True
    except ImportError as e:
        print(f"❌ COBRA styling import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Error during COBRA styling testing: {e}")
        return False

def test_ml_functionality():
    """Test machine learning functionality."""
    print("\n🧠 Testing ML functionality...")
    
    try:
        from sklearn.linear_model import LinearRegression
        import pandas as pd
        import numpy as np
        
        # Create sample data
        sample_data = [
            {"dt": 1640995200, "main": {"temp": 20.5}},
            {"dt": 1640998800, "main": {"temp": 21.0}},
            {"dt": 1641002400, "main": {"temp": 21.5}},
            {"dt": 1641006000, "main": {"temp": 22.0}},
            {"dt": 1641009600, "main": {"temp": 22.5}},
        ]
        
        from complete_weather_dashboard import WeatherPredictor
        predictor = WeatherPredictor(sample_data)
        predictions = predictor.train_and_predict(hours_ahead=3)
        
        print(f"✅ ML predictions generated: {predictions}")
        return True
        
    except Exception as e:
        print(f"❌ ML functionality test failed: {e}")
        return False

def run_all_tests():
    """Run all tests and report results."""
    print("🚀 Starting Complete Weather Dashboard Tests")
    print("=" * 50)
    
    tests = [
        ("Import Dependencies", test_imports),
        ("API Key Configuration", test_api_key),
        ("Complete Dashboard", test_complete_dashboard_import),
        ("COBRA Styling", test_cobra_styling_import),
        ("ML Functionality", test_ml_functionality),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ {test_name} test failed with exception: {e}")
            results.append((test_name, False))
    
    print("\n" + "=" * 50)
    print("📊 Test Results Summary:")
    print("=" * 50)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
    
    print("-" * 50)
    print(f"Tests Passed: {passed}/{total}")
    
    if passed == total:
        print("🎉 All tests passed! The application is ready to run.")
        print("\nTo start the complete weather dashboard:")
        print("python complete_weather_dashboard.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing dependencies: pip install -r requirements.txt")
        print("2. Create .env file with your OpenWeatherMap API key")
        print("3. Ensure Python 3.8+ is being used")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
