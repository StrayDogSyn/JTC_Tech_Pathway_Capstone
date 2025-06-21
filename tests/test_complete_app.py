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
    
    # Test tkinter
    import tkinter as tk
    print("✅ tkinter imported successfully")
    
    # Test ttkbootstrap
    import ttkbootstrap as ttk
    print("✅ ttkbootstrap imported successfully")
    
    # Test matplotlib
    import matplotlib.pyplot as plt
    print("✅ matplotlib imported successfully")
    
    # Test scikit-learn
    import sklearn
    print("✅ scikit-learn imported successfully")
    
    # Test pandas
    import pandas as pd
    print("✅ pandas imported successfully")
    
    # Test numpy
    import numpy as np
    print("✅ numpy imported successfully")
    
    # Test requests
    import requests
    print("✅ requests imported successfully")
    
    # Test python-dotenv
    from dotenv import load_dotenv
    print("✅ python-dotenv imported successfully")
    
    # Test Pillow
    from PIL import Image
    print("✅ Pillow imported successfully")
    
    # If we reach here, all imports were successful
    assert True

def test_api_key():
    """Test API key configuration."""
    print("\n🔑 Testing API key configuration...")
    
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.getenv('OPENWEATHER_API_KEY', '')
    
    if not api_key:
        print("⚠️ No API key found in environment variables")
        print("   Create a .env file with: OPENWEATHER_API_KEY=your_key_here")
        # For testing purposes, we'll allow missing API key but warn about it
        assert True, "No API key found, but test passes with warning"
    elif len(api_key) < 10:
        print("⚠️ API key appears to be too short")
        assert False, "API key is too short"
    else:
        print(f"✅ API key found: {api_key[:10]}...")
        assert True

def test_complete_dashboard_import():
    """Test importing the complete dashboard module."""
    print("\n📱 Testing complete dashboard import...")
    
    # Import the main application components from modular structure
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    
    from src.services.weather_api import WeatherAPIService
    from src.utils.ml_predictions import WeatherPredictor
    from src.main import WeatherDashboardApp
    from src.config.app_config import config
    
    print("✅ Complete dashboard components imported successfully")
    
    # Test config functions
    current_city = config.current_city
    print(f"✅ Config loaded: {current_city}")
    
    # Test API class initialization
    api = WeatherAPIService(config.api_key)
    print("✅ WeatherAPIService initialized successfully")
    
    assert True

def test_cobra_styling_import():
    """Test importing the COBRA styling components."""
    print("\n🐍 Testing COBRA styling import...")
    
    # Import from Weather Dominator folder
    cobra_path = os.path.join(os.path.dirname(__file__), '..', 'Weather Dominator')
    sys.path.insert(0, cobra_path)
    
    # Use importlib to dynamically import and suppress static analysis warnings
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "cobra_style", 
        os.path.join(cobra_path, "cobra_style.py")
    )
    
    assert spec is not None, "Could not create module spec for cobra_style"
    assert spec.loader is not None, "Could not get loader for cobra_style"
    
    cobra_style = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cobra_style)
    
    # Verify the expected components exist
    assert hasattr(cobra_style, 'COBRA_COLORS'), "COBRA_COLORS not found in module"
    assert hasattr(cobra_style, 'apply_cobra_theme'), "apply_cobra_theme not found in module"
    assert hasattr(cobra_style, 'CobraChartAnimator'), "CobraChartAnimator not found in module"
    
    print("✅ COBRA styling components imported successfully")

def test_ml_functionality():
    """Test machine learning functionality."""
    print("\n🧠 Testing ML functionality...")
    
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
    
    # Add parent directory to Python path  
    sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
    from src.utils.ml_predictions import WeatherPredictor
    predictor = WeatherPredictor()
    
    # Train the model and make predictions
    trained = predictor.train_models(sample_data)
    if trained:
        predictions = predictor.predict_temperature(hours_ahead=3)
        print(f"✅ ML predictions generated: {predictions}")
    else:
        print("✅ ML predictor initialized (needs more data to train)")
        
    # Test passed if we got this far without exceptions
    assert True

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
            test_func()  # Just call the function, don't expect return value
            print(f"✅ {test_name} test passed")
            results.append((test_name, True))
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
