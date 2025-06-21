#!/usr/bin/env python3
"""
Launch the Advanced Weather Dashboard with Tabular Components

This demonstrates the Capstone-level project with advanced features.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def main():
    """Launch the advanced weather dashboard."""
    try:
        from src.ui.advanced_dashboard import AdvancedWeatherDashboard
        from src.core.weather_core import WeatherDashboardCore
        
        print("🌦️ Advanced Weather Intelligence Platform - Capstone Demo")
        print("=" * 60)
        print("📊 Advanced Features:")
        print("   ✅ Historical Data Tables (sortable, filterable)")
        print("   ✅ Location Comparison Tables")
        print("   ✅ Analytics & Statistics")
        print("   ✅ Data Export (CSV/JSON)")
        print("   ✅ Advanced Search & Filtering")
        print("   ✅ Real-time Weather Integration")
        print("=" * 60)
        
        # Create the advanced dashboard
        dashboard = AdvancedWeatherDashboard(
            title="🌦️ Advanced Weather Intelligence Platform - Capstone Demo",
            theme="superhero",
            size=(1600, 1000)
        )
        
        # Initialize business logic for weather data
        core = WeatherDashboardCore()
        
        # Set up search callback for real weather data
        def handle_search(city: str):
            print(f"🔍 Fetching weather data for: {city}")
            try:
                # Load weather data
                core.load_weather_data(city)
                
                if core.has_weather_data():
                    # Get weather summary
                    weather_summary = core.get_weather_summary()
                    
                    # Update dashboard with real data
                    dashboard.update_weather_data(weather_summary)
                    
                    # Update air quality if available
                    if core.has_air_quality_data():
                        aqi_data = {
                            'aqi': weather_summary.get('air_quality', {}).get('aqi', 'N/A'),
                            'quality': weather_summary.get('air_quality', {}).get('description', 'Unknown')
                        }
                        dashboard.update_air_quality_data(aqi_data)
                    
                    print(f"✅ Weather data updated for {city}")
                else:
                    print(f"❌ No weather data found for {city}")
            except Exception as e:
                print(f"❌ Error: {e}")
        
        dashboard.set_search_callback(handle_search)
        
        print("🚀 Starting dashboard...")
        print("💡 Try searching for: Austin, London, Tokyo, Paris, New York")
        print("📋 Explore all tabs for advanced features!")
        print()
        
        # Run the dashboard
        dashboard.run()
        
    except Exception as e:
        print(f"❌ Error starting dashboard: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
