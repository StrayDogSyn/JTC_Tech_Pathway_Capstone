#!/usr/bin/env python3
"""
Test script to verify the Student Pack GUI can be imported and initialized
"""

try:
    print("Testing Student Pack GUI import...")
    from student_pack_gui import StudentPackWeatherGUI
    print("✅ Successfully imported StudentPackWeatherGUI")
    
    # Test basic initialization without starting mainloop
    import tkinter as tk
    root = tk.Tk()
    root.withdraw()  # Hide the window
    
    print("Creating GUI instance...")
    app = StudentPackWeatherGUI(root)
    print("✅ Successfully created GUI instance")
    
    # Test API info method
    print("Testing API info retrieval...")
    api_info = app.weather_api.get_api_usage_info()
    print(f"✅ API Plan: {api_info['subscription']['subscription_plan']}")
    
    print("Testing map layers...")
    layers = app.weather_api.get_available_map_layers()
    print(f"✅ Available layers: {len(layers)} layers")
    
    root.destroy()
    print("✅ All tests passed! Student Pack GUI is working correctly.")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
