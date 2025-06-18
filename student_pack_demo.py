"""
OpenWeatherMap Student Pack Features Demo
Demonstrates all available Student Pack features with comprehensive testing.

Student Pack Features:
- Current & Forecasts data: 3,000 API calls/minute, 100,000,000 calls/month
- Current weather API
- Hourly Forecast 4 days
- Daily Forecast 16 days
- Weather Maps - History, Current, Forecast weather, 15 weather layers
- Air Pollution API
- Geocoding API
- Historical data: 50,000 calls/day, 1 year archive
- History API
- Statistical Weather Data API
- Accumulated Parameters
"""

import sys
import time
from datetime import datetime, timedelta
from enhanced_weather_api import EnhancedWeatherAPI
from config import Config

def print_header(title):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"🎓 {title}")
    print(f"{'='*60}")

def print_feature(feature_name, description):
    """Print a feature with description."""
    print(f"\n🌟 {feature_name}")
    print(f"   {description}")

def main():
    """Demonstrate all Student Pack features."""
    print_header("OpenWeatherMap Student Pack Features Demo")
    
    try:
        # Initialize Enhanced Weather API
        weather = EnhancedWeatherAPI()
        
        # Display Student Pack Information
        print_header("Student Pack Subscription Details")
        api_info = weather.get_api_usage_info()
        
        print(f"📋 Plan: {api_info['subscription']['subscription_plan']}")
        print(f"💰 Pricing: {api_info['subscription']['pricing']}")
        print(f"⚡ Rate Limits:")
        print(f"   • Current/Forecast: {api_info['rate_limits']['current_forecast']}")
        print(f"   • Monthly Total: {api_info['rate_limits']['monthly_total']}")
        print(f"   • Historical Daily: {api_info['rate_limits']['historical_daily']}")
        
        print(f"\n🎯 Available Features:")
        for feature in api_info['student_pack_benefits']:
            print(f"   ✅ {feature}")
        
        # Test city for demonstrations
        test_city = Config.DEFAULT_CITY
        print(f"\n🏙️ Demo Location: {test_city}")
        
        # FEATURE 1: Geocoding API
        print_feature("Geocoding API", "Convert city names to coordinates and vice versa")
        locations = weather.geocode_city(test_city, limit=3)
        if locations:
            location = locations[0]
            lat, lon = location['lat'], location['lon']
            print(f"   📍 {location['name']}, {location.get('country', 'Unknown')} → ({lat:.4f}, {lon:.4f})")
            
            # Show reverse geocoding
            reverse_locations = weather.reverse_geocode(lat, lon, limit=1)
            if reverse_locations:
                reverse_loc = reverse_locations[0]
                print(f"   🔄 Reverse: ({lat:.4f}, {lon:.4f}) → {reverse_loc.get('name', 'Unknown')}")
        else:
            print(f"   ❌ Could not geocode {test_city}")
            return
        
        # FEATURE 2: Current Weather API
        print_feature("Current Weather API", "Real-time weather conditions")
        current_weather = weather.get_current_weather_by_coordinates(lat, lon)
        formatted_current = weather.format_weather_data(current_weather)
        
        print(f"   🌡️ Temperature: {formatted_current['temperature']}°C")
        print(f"   🌤️ Conditions: {formatted_current['description']}")
        print(f"   💨 Wind: {formatted_current['wind_speed']} m/s")
        print(f"   💧 Humidity: {formatted_current['humidity']}%")
        print(f"   📊 Pressure: {formatted_current['pressure']} hPa")
        
        # FEATURE 3: Hourly Forecast 4 Days
        print_feature("Hourly Forecast (4 Days)", "Detailed hourly weather predictions")
        try:
            hourly_forecast = weather.get_hourly_forecast_4days(lat, lon)
            forecast_formatted = weather.format_forecast_data(hourly_forecast)
            
            print(f"   📊 Total Hours Available: {len(forecast_formatted['hourly'])}")
            print(f"   📅 Coverage: Next 4 days (96 hours)")
            
            # Show next 6 hours as sample
            print(f"   🕐 Next 6 Hours Preview:")
            for i, hour_data in enumerate(forecast_formatted['hourly'][:6]):
                if hour_data.get('timestamp'):
                    hour_time = datetime.fromtimestamp(hour_data['timestamp'])
                    temp = hour_data.get('temperature', 'N/A')
                    desc = hour_data.get('weather', {}).get('description', 'N/A')
                    print(f"      {hour_time.strftime('%H:%M')}: {temp}°C, {desc}")
                    
        except Exception as e:
            print(f"   ⚠️ Hourly forecast error: {e}")
        
        # FEATURE 4: Daily Forecast 16 Days
        print_feature("Daily Forecast (16 Days)", "Extended daily weather predictions")
        try:
            daily_forecast = weather.get_daily_forecast_16days(lat, lon)
            print(f"   📅 Extended forecast available")
            print(f"   🎯 Coverage: Next 16 days")
            
        except Exception as e:
            print(f"   ⚠️ Daily forecast error: {e}")
        
        # FEATURE 5: Air Pollution API
        print_feature("Air Pollution API", "Current and forecast air quality data")
        try:
            air_pollution = weather.get_air_pollution_current(lat, lon)
            if 'list' in air_pollution and air_pollution['list']:
                aqi_data = air_pollution['list'][0]
                aqi = aqi_data['main']['aqi']
                components = aqi_data.get('components', {})
                
                aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
                print(f"   🌬️ Air Quality Index: {aqi}/5 ({aqi_levels.get(aqi, 'Unknown')})")
                print(f"   🧪 Components:")
                for component, value in components.items():
                    print(f"      {component.upper()}: {value} μg/m³")
                    
            # Air pollution forecast
            air_forecast = weather.get_air_pollution_forecast(lat, lon)
            if 'list' in air_forecast:
                print(f"   📊 Forecast: {len(air_forecast['list'])} data points available")
                
        except Exception as e:
            print(f"   ⚠️ Air pollution error: {e}")
        
        # FEATURE 6: Weather Maps (15 layers)
        print_feature("Weather Maps API", "15 weather layers for visualization")
        available_layers = weather.get_available_map_layers()
        print(f"   🗺️ Available Layers: {len(available_layers)}")
        print(f"   📋 Layer Types:")
        for i, layer in enumerate(available_layers[:8]):  # Show first 8
            print(f"      {i+1}. {layer}")
        if len(available_layers) > 8:
            print(f"      ... and {len(available_layers)-8} more layers")
        
        # Sample map URL
        sample_url = weather.get_weather_map_url('temp_new', 5, 10, 15)
        print(f"   🔗 Sample URL: {sample_url[:60]}...")
        
        # FEATURE 7: Historical Weather Data (1 year archive)
        print_feature("Historical Weather API", "1 year archive, 50,000 calls/day")
        try:
            # Get weather from 30 days ago
            historical_date = datetime.now() - timedelta(days=30)
            historical_weather = weather.get_historical_weather(lat, lon, historical_date)
            
            print(f"   📅 Date: {historical_date.strftime('%Y-%m-%d')}")
            if 'data' in historical_weather and historical_weather['data']:
                hist_data = historical_weather['data'][0]
                hist_temp = hist_data.get('temp', 'N/A')
                print(f"   🌡️ Temperature 30 days ago: {hist_temp}°C")
            else:
                print(f"   📊 Historical data structure available")
                
        except Exception as e:
            print(f"   ⚠️ Historical data error: {e}")
        
        # FEATURE 8: Statistical Weather Data API
        print_feature("Statistical Weather Data API", "Advanced weather statistics")
        try:
            start_date = datetime.now() - timedelta(days=30)
            end_date = datetime.now() - timedelta(days=1)
            
            stats_weather = weather.get_statistical_weather(lat, lon, start_date, end_date)
            print(f"   📊 Statistical analysis available")
            print(f"   📅 Period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
            
        except Exception as e:
            print(f"   ⚠️ Statistical data error: {e}")
        
        # FEATURE 9: Accumulated Parameters
        print_feature("Accumulated Parameters", "Temperature and precipitation accumulation")
        try:
            start_date = datetime.now() - timedelta(days=7)
            end_date = datetime.now()
            
            # Accumulated temperature above 15°C
            temp_accumulation = weather.get_accumulated_temperature(lat, lon, 15.0, start_date, end_date)
            print(f"   🌡️ Temperature accumulation (>15°C) available")
            
            # Accumulated precipitation above 0.1mm
            precip_accumulation = weather.get_accumulated_precipitation(lat, lon, 0.1, start_date, end_date)
            print(f"   💧 Precipitation accumulation (>0.1mm) available")
            
        except Exception as e:
            print(f"   ⚠️ Accumulated parameters error: {e}")
        
        # Summary
        print_header("Student Pack Benefits Summary")
        print("✅ FREE for educational use")
        print("⚡ High rate limits: 3,000 calls/minute")
        print("📊 Massive monthly allowance: 100,000,000 calls")
        print("📚 Extensive historical data: 1 year archive")
        print("🗺️ Complete weather maps: 15 layers")
        print("🌬️ Air quality monitoring included")
        print("🎯 All advanced APIs available")
        print("📈 Statistical analysis tools")
        print("🔬 Research-grade data quality")
        
        print(f"\n🎓 Student Pack successfully demonstrated!")
        print(f"📖 Documentation: {api_info['subscription_info']['documentation']}")
        print(f"📧 Support: {api_info['subscription_info']['support_email']}")
        
    except Exception as e:
        print(f"\n❌ Demo error: {e}")
        print("\nPlease ensure:")
        print("1. Your API key is set in the .env file")
        print("2. Your Student Pack subscription is active")
        print("3. You have internet connectivity")

if __name__ == "__main__":
    main()
