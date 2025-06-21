#!/usr/bin/env python3
"""
🌤️ Complete Weather Dashboard - Refactored Version

A comprehensive weather application with proper separation of concerns:
- Real-time weather data with comprehensive metrics
- 5-day/3-hour weather forecasts with machine learning predictions
- Air quality monitoring with detailed pollutants
- Advanced geocoding and location search
- Modern, responsive GUI with theme support
- Modular architecture with clean separation of concerns

This refactored version demonstrates:
- Service layer for API interactions
- Data models for type safety
- Core business logic separation
- Configuration management
- Proper error handling
- Clean UI components

Author: Refactored Implementation
Date: June 2025
License: Educational Use Only
"""

import sys
import os

# Add the src directory to Python path for modular imports
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
if src_dir not in sys.path:
    sys.path.insert(0, src_dir)

# Import the main application
from src.main import main

if __name__ == "__main__":
    print("🌤️ Starting Complete Weather Dashboard (Refactored)")
    print("📁 Using modular architecture with separation of concerns")
    print("-" * 60)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Application closed by user")
    except Exception as e:
        print(f"\n❌ Application error: {e}")
        input("Press Enter to exit...")
