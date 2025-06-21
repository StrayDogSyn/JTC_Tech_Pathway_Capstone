#!/usr/bin/env python3
"""
Test script for Advanced Weather Dashboard with Tabular Components

This demonstrates the Capstone-level advanced tabular features including:
- Historical weather data tables with sorting/filtering
- Location comparison tables with rankings
- Analytics tables with trend analysis
- Advanced data management with export capabilities
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

def test_advanced_dashboard():
    """Test the advanced dashboard with tabular components."""
    try:
        from src.ui.advanced_dashboard import AdvancedWeatherDashboard
        from src.core.weather_core import WeatherDashboardCore
        
        print("🌦️ Starting Advanced Weather Intelligence Platform...")
        print("📊 Features: Historical Data • Location Comparison • Analytics • Data Export")
        print("=" * 80)
        
        # Create and configure the advanced dashboard
        dashboard = AdvancedWeatherDashboard(
            title="🌦️ Advanced Weather Intelligence Platform - Capstone Demo",
            theme="superhero",
            size=(1600, 1000)
        )
        
        # Initialize business logic for actual weather data
        core = WeatherDashboardCore()
          # Set up search callback to connect dashboard to weather API
        def handle_search(city: str):
            print(f"🔍 Searching weather for: {city}")
            try:
                # Load weather data using the core
                core.load_weather_data(city)
                
                # Check if we have weather data
                if core.has_weather_data():
                    # Get weather summary and convert to format expected by dashboard
                    weather_summary = core.get_weather_summary()
                    
                    # Update the dashboard with real data
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
                print(f"❌ Error getting weather data: {e}")
        
        dashboard.set_search_callback(handle_search)
        
        print("🚀 Dashboard initialized with sample data")
        print("📋 Available tabs:")
        print("   • 🌦️ Live Dashboard - Real-time weather display")
        print("   • 📈 Historical Data - Sortable/filterable weather history")
        print("   • 🔄 Comparisons - Multi-location and time period analysis")
        print("   • 📊 Analytics - Statistical analysis and trends")
        print("   • 🗂️ Data Management - Import/Export and data quality tools")
        print()
        print("💡 Try searching for cities like: Austin, London, Tokyo, Paris")
        print("📤 Use Export buttons to save data in CSV/JSON formats")
        print("🔍 Use Advanced Filter options for detailed analysis")
        print("=" * 80)
        
        # Run the dashboard
        dashboard.run()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure all required packages are installed:")
        print("pip install ttkbootstrap tkinter pandas")
    except Exception as e:
        print(f"❌ Error starting advanced dashboard: {e}")
        import traceback
        traceback.print_exc()


def test_tabular_components_only():
    """Test just the tabular components independently."""
    try:
        from src.ui.tabular_components import (
            WeatherDataTable, ComparisonTable, AnalyticsTable, 
            generate_sample_weather_data, generate_sample_comparison_data
        )
        import ttkbootstrap as ttk
        
        print("🧪 Testing Tabular Components...")
        
        # Create a test window
        root = ttk.Window("🌦️ Advanced Weather Tables Demo", "darkly", size=(1400, 800))
        
        # Create notebook for tabs
        notebook = ttk.Notebook(root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Weather Data Table tab
        weather_frame = ttk.Frame(notebook)
        notebook.add(weather_frame, text="📊 Weather History")
        weather_table = WeatherDataTable(weather_frame)
        weather_table.set_data(generate_sample_weather_data(30))
        
        # Comparison Table tab
        comparison_frame = ttk.Frame(notebook)
        notebook.add(comparison_frame, text="🌍 Comparison")
        comparison_table = ComparisonTable(comparison_frame)
        comparison_table.set_data(generate_sample_comparison_data())
        
        # Analytics Table tab
        analytics_frame = ttk.Frame(notebook)
        notebook.add(analytics_frame, text="📈 Analytics")
        analytics_table = AnalyticsTable(analytics_frame)
        
        print("✅ Tabular components loaded successfully!")
        print("📊 Features demonstrated:")
        print("   • Sortable columns (click headers)")
        print("   • Search and filtering")
        print("   • Data export (CSV/JSON)")
        print("   • Weather-specific controls")
        print("   • Analytics and statistics")
        
        root.mainloop()
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
    except Exception as e:
        print(f"❌ Error testing tabular components: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("🌦️ Advanced Weather Dashboard - Capstone Level Testing")
    print("=" * 60)
    print("Choose test option:")
    print("1. Full Advanced Dashboard (recommended)")
    print("2. Tabular Components Only")
    print("3. Exit")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            test_advanced_dashboard()
        elif choice == "2":
            test_tabular_components_only()
        elif choice == "3":
            print("👋 Goodbye!")
        else:
            print("❌ Invalid choice. Running full dashboard...")
            test_advanced_dashboard()
            
    except KeyboardInterrupt:
        print("\n👋 Test cancelled by user")
    except Exception as e:
        print(f"❌ Test error: {e}")
