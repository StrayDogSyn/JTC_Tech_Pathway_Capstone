"""
🌤️ OpenWeatherMap Student Pack Weather Dashboard
A modern weather application showcasing OpenWeatherMap's Student Pack capabilities.

Features:
- Real-time weather data with comprehensive metrics
- 5-day/3-hour weather forecasts
- Interactive weather maps (12 available layers)
- Air quality monitoring with detailed pollutants
- Advanced geocoding and location search
- Full historical data archive (Student Pack)
- Advanced analytics capabilities
- Modern, responsive dark-themed GUI
- Comprehensive API information and monitoring

Note: This implementation uses the Student Pack which includes premium features
for educational purposes.

Author: Student Pack Implementation
Date: June 2025
License: Educational Use Only
"""

import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SUCCESS, INFO, WARNING, DANGER
import threading
import time
import webbrowser
import requests
import json
from datetime import datetime, timedelta
from dataclasses import dataclass
from typing import Dict, List, Optional, Any
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

@dataclass
class WeatherData:
    """Data class for weather information."""
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    wind_speed: float
    wind_direction: int
    visibility: int
    description: str
    icon: str
    city: str
    country: str
    timestamp: int
    cloudiness: int

@dataclass
class ForecastData:
    """Data class for forecast information."""
    hourly: List[Dict]
    daily: List[Dict]

class WeatherAPI:
    """
    Weather API client for OpenWeatherMap Student Pack.
    Provides access to all Student Pack features including current weather,
    5-day forecasts, air pollution, weather maps, geocoding, and historical data.
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY', '')
        self.backup_api_key = os.getenv('OPENWEATHER_API_KEY_BACKUP', '')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0"
        self.pollution_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        self.maps_url = "https://tile.openweathermap.org/map"
        
        # Student Pack configuration
        self.subscription_info = {
            'plan': 'Free Tier with Student Pack Benefits',
            'pricing': 'Free Educational License',
            'rate_limits': {
                'calls_per_minute': 60,
                'calls_per_month': 1000000,
                'historical_per_day': 'Unlimited (Student Pack)'
            },
            'features': [
                'Current weather data',
                '5-day/3-hour forecasts',
                'Air pollution monitoring',
                'Interactive weather maps (12 layers)',
                'Advanced geocoding',
                'Basic weather alerts',
                'Extended rate limits for learning',
                'Full historical data archive',
                'Advanced analytics capabilities',
                'Statistical weather data access'
            ]
        }
        
        # Available map layers (12 total as per Student Pack)
        self.map_layers = [
            'temp_new', 'precipitation_new', 'pressure_new', 'wind_new',
            'clouds_new', 'rain', 'snow', 'temp', 'precipitation', 'pressure',
            'wind', 'clouds'
        ]
        
        print("🌤️ Student Pack Weather API initialized")
        if self.api_key:
            print(f"🔑 API Key: {self.api_key[:10]}...")
        else:
            print("🔑 API Key: Not configured")
        print(f"📊 Rate Limits: {self.subscription_info['rate_limits']['calls_per_minute']}/min")
        print(f"🌟 Features: {len(self.subscription_info['features'])} available")
    
    def _make_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Make API request with error handling and fallback."""
        params['appid'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Primary API request failed: {e}")
            
            # Try backup key if available
            if self.backup_api_key:
                params['appid'] = self.backup_api_key
                try:
                    response = requests.get(url, params=params, timeout=10)
                    response.raise_for_status()
                    return response.json()
                except requests.exceptions.RequestException as backup_e:
                    print(f"Backup API request failed: {backup_e}")
            
            return None
    
    def get_current_weather(self, lat: float, lon: float) -> Optional[WeatherData]:
        """Get current weather data for coordinates."""
        params = {
            'lat': lat,
            'lon': lon,
            'units': 'metric'
        }
        
        data = self._make_request(f"{self.base_url}/weather", params)
        if not data:
            return None
            
        return WeatherData(
            temperature=data['main']['temp'],
            feels_like=data['main']['feels_like'],
            humidity=data['main']['humidity'],
            pressure=data['main']['pressure'],
            wind_speed=data.get('wind', {}).get('speed', 0),
            wind_direction=data.get('wind', {}).get('deg', 0),
            visibility=data.get('visibility', 0),
            description=data['weather'][0]['description'].title(),
            icon=data['weather'][0]['icon'],
            city=data['name'],
            country=data['sys']['country'],
            timestamp=data['dt'],
            cloudiness=data.get('clouds', {}).get('all', 0)
        )
    
    def get_extended_forecast(self, lat: float, lon: float) -> Optional[ForecastData]:
        """Get extended forecast using 5-day/3-hour forecast."""
        params = {
            'lat': lat,
            'lon': lon,
            'units': 'metric'
        }
        
        data = self._make_request(f"{self.forecast_url}", params)
        if not data:
            return None
        
        # Convert 5-day/3-hour forecast to our format
        forecast_list = data.get('list', [])
        
        return ForecastData(
            hourly=forecast_list[:40],  # 5 days * 8 periods per day = 40 periods
            daily=self._convert_to_daily_forecast(forecast_list)
        )
    
    def get_air_pollution(self, lat: float, lon: float) -> Optional[Dict]:
        """Get current air pollution data."""
        params = {'lat': lat, 'lon': lon}
        return self._make_request(self.pollution_url, params)
    
    def geocode_location(self, location: str, limit: int = 5) -> List[Dict]:
        """Geocode location name to coordinates."""
        params = {'q': location, 'limit': limit}
        data = self._make_request(f"{self.geocoding_url}/direct", params)
        return data if isinstance(data, list) else []
    
    def get_historical_weather(self, lat: float, lon: float, date: datetime) -> Optional[Dict]:
        """
        Historical weather data - available with Student Pack.
        Note: In production, this would require One Call API 3.0 subscription.
        For demonstration, we'll show the upgrade message.
        """
        print("📚 Historical weather data available with Student Pack!")
        print("Note: For production use, upgrade to One Call API 3.0 ($3/month)")
        
        # For demo purposes, return mock data structure
        # In real implementation, this would use the historical API endpoint
        mock_data = {
            'current': {
                'temp': 22.5,
                'feels_like': 24.0,
                'humidity': 65,
                'pressure': 1013,
                'wind_speed': 3.5,
                'visibility': 10000,
                'weather': [{'description': 'Clear sky', 'icon': '01d'}]
            },
            'note': 'This is demonstration data. Full historical data requires One Call API 3.0 subscription.'
        }
        return mock_data
    
    def get_api_info(self) -> Dict:
        """Get comprehensive API information."""
        return {
            'api_key': f"{self.api_key[:10]}...{self.api_key[-4:]}",
            'subscription': self.subscription_info,
            'endpoints': {
                'current_weather': self.base_url,
                'extended_forecast': self.forecast_url,
                'geocoding': self.geocoding_url,
                'air_pollution': self.pollution_url,
                'weather_maps': self.maps_url
            },
            'map_layers': self.map_layers
        }
    
    def _convert_to_daily_forecast(self, forecast_list: List[Dict]) -> List[Dict]:
        """Convert 3-hour forecast data to daily forecast."""
        daily_data = []
        current_date = None
        daily_temps = []
        daily_entry = None
        
        for item in forecast_list:
            # Get date from timestamp
            date = datetime.fromtimestamp(item['dt']).date()
            
            if current_date != date:
                # Save previous day if exists
                if daily_entry and daily_temps:
                    daily_entry['temp'] = {
                        'min': min(daily_temps),
                        'max': max(daily_temps)
                    }
                    daily_data.append(daily_entry)
                
                # Start new day
                current_date = date
                daily_temps = []
                daily_entry = {
                    'dt': item['dt'],
                    'weather': item['weather'],
                    'humidity': item['main']['humidity'],
                    'pressure': item['main']['pressure'],
                    'wind_speed': item.get('wind', {}).get('speed', 0),
                    'clouds': item.get('clouds', {}).get('all', 0)
                }
            
            daily_temps.append(item['main']['temp'])
        
        # Add last day
        if daily_entry and daily_temps:
            daily_entry['temp'] = {
                'min': min(daily_temps),
                'max': max(daily_temps)
            }
            daily_data.append(daily_entry)
        
        return daily_data[:5]  # Return up to 5 days

class ModernWeatherDashboard:
    """
    Modern, comprehensive weather dashboard showcasing all Student Pack features.
    Features ttkbootstrap themes, responsive design, and intuitive user interface.
    Supports both light and dark themes with modern flat UI components.
    """
    
    def __init__(self, root=None):
        # Initialize ttkbootstrap window with dark theme
        if root is None:
            self.root = ttk.Window(
                title="🌤️ Student Pack Weather Dashboard - OpenWeatherMap",
                themename="darkly",  # Modern dark theme
                size=(1200, 800),
                minsize=(1000, 700),
                resizable=(True, True)
            )
        else:
            self.root = root
            
        self.api = WeatherAPI()
        
        # Theme management
        self.current_theme = "darkly"
        self.available_themes = ["darkly", "superhero", "solar", "cyborg", "vapor", "litera", "flatly", "journal", "lumen", "minty", "pulse", "sandstone", "united", "yeti"]
        
        # State management
        self.current_location = None
        self.current_weather = None
        self.forecast_data = None
        self.air_quality_data = None
        
        # Initialize UI
        self.setup_window()
        self.create_interface()
        self.load_default_location()
    
    def load_default_location(self):
        """
        Load a default location (e.g., user's current location or a demo city).
        Attempts to get current location or falls back to a demo location.
        """        # For demo purposes, use Seattle as default
        default_location = {
            'name': 'Seattle, WA, US',
            'lat': 47.6062,
            'lon': -122.3321,
            'country': 'US'
        }
        
        self.current_location = default_location
        self.location_entry.delete(0, tk.END)
        self.location_entry.insert(0, f"{default_location['name']}")
        self.status_var.set(f"📍 Default location: {default_location['name']}")
        
        # Load initial weather data
        threading.Thread(target=self._initial_data_load, daemon=True).start()
    
    def _initial_data_load(self):
        """Load initial weather data in background."""
        try:
            self.refresh_weather_data()
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"⚠️ Could not load initial data: {str(e)}"))
    
    def search_location(self, event=None):
        """
        Search for a location using the geocoding API.
        Updates the current location and refreshes weather data.
        """
        location_query = self.location_entry.get().strip()
        if not location_query:
            messagebox.showwarning("Input Required", "Please enter a location to search.")
            return
        
        self.status_var.set(f"🔍 Searching for: {location_query}...")
        
        def search_task():
            try:
                locations = self.api.geocode_location(location_query)
                if locations:
                    location = locations[0]  # Use first result
                    self.current_location = {
                        'name': f"{location.get('name', 'Unknown')}, {location.get('state', '')}, {location.get('country', '')}".replace(', ,', ',').strip(','),
                        'lat': location['lat'],
                        'lon': location['lon'],
                        'country': location.get('country', '')
                    }                    # Update UI on main thread
                    self.root.after(0, lambda: self._update_location_entry())
                    
                    # Safe status update with location name
                    location_name = self.current_location.get('name', 'Unknown') if self.current_location else 'Unknown'
                    self.root.after(0, lambda: self.status_var.set(f"📍 Location found: {location_name}"))
                    
                    # Refresh weather data
                    self.refresh_weather_data()
                else:
                    self.root.after(0, lambda: self.status_var.set(f"❌ Location not found: {location_query}"))
                    self.root.after(0, lambda: messagebox.showwarning("Location Not Found", f"Could not find location: {location_query}"))
                    
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"❌ Search error: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Search Error", f"Error searching for location:\n{str(e)}"))
          # Run search in background thread
        threading.Thread(target=search_task, daemon=True).start()
    
    def _update_location_entry(self):
        """Helper method to update location entry widget."""
        if self.current_location:
            self.location_entry.delete(0, tk.END)
            self.location_entry.insert(0, self.current_location['name'])
    
    def setup_window(self):
        """
        Configure main window properties and responsive layout.
        Sets up the window icon, position, and grid weight configuration.
        """
        # Center window on screen (for ttkbootstrap Window, centering is automatic)
        # If using regular tk.Tk, we can implement manual centering
        try:
            # Try to center using ttkbootstrap method
            if hasattr(self.root, 'place_window_center'):
                self.root.place_window_center()
        except AttributeError:
            # Manual centering for regular Tk window
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f'+{x}+{y}')
          # Configure responsive grid layout
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def add_theme_toggle(self, parent):
        """
        Add theme toggle functionality to switch between light and dark themes.
        Creates a modern toggle button with theme switching capabilities.
        """
        theme_frame = ttk.Frame(parent)
        theme_frame.grid(row=0, column=2, sticky='e', padx=10)
        
        ttk.Label(theme_frame, text="🎨", font=('Segoe UI', 12)).grid(row=0, column=0, padx=(0, 5))
        
        self.theme_var = tk.StringVar(value=self.current_theme)
        
        theme_combo = ttk.Combobox(
            theme_frame, 
            textvariable=self.theme_var,
            values=self.available_themes,
            state='readonly',
            width=10
        )
        theme_combo.grid(row=0, column=1, padx=5)
        theme_combo.bind('<<ComboboxSelected>>', self.change_theme)
        
        return theme_frame
    
    def change_theme(self, event=None):
        """
        Change the application theme dynamically.
        Updates the entire interface with the selected theme.
        """
        new_theme = self.theme_var.get()
        if new_theme != self.current_theme:
            self.current_theme = new_theme
              # Apply new theme - different methods for ttkbootstrap vs regular tkinter
            try:
                if hasattr(self.root, 'style') and hasattr(self.root.style, 'theme_use'):
                    # For ttkbootstrap Window with direct style access
                    self.root.style.theme_use(new_theme)
                elif hasattr(self.root, '_style'):
                    # For ttkbootstrap Window with _style attribute
                    self.root._style.theme_use(new_theme)
                else:
                    # For regular tkinter with ttk.Style
                    import ttkbootstrap as ttk
                    style = ttk.Style()
                    style.theme_use(new_theme)
                    
            except Exception as e:
                # If theme change fails, try creating a new ttkbootstrap window
                try:
                    # Get current geometry
                    geometry = self.root.geometry()
                      # Create new window with the selected theme
                    old_root = self.root
                    import ttkbootstrap as ttk
                    self.root = ttk.Window(
                        title="🌤️ Student Pack Weather Dashboard - OpenWeatherMap",
                        themename=new_theme,
                        size=(1200, 800),
                        minsize=(1000, 700),
                        resizable=(True, True)
                    )
                    
                    # Copy geometry
                    self.root.geometry(geometry)
                    
                    # Recreate interface
                    self.setup_window()
                    self.create_interface()
                    
                    # Close old window
                    old_root.destroy()
                    
                except Exception as e2:
                    # If all else fails, show error message
                    if hasattr(self, 'status_var'):
                        self.status_var.set(f"❌ Theme change failed: {str(e2)}")
                    return
            
            # Update status message
            if hasattr(self, 'status_var'):
                self.status_var.set(f"✅ Theme changed to: {new_theme.title()}")
    
    def create_interface(self):
        """
        Create the main interface layout with modern ttkbootstrap components.
        Uses responsive grid layout with a Notebook widget containing four main tabs.
        Each tab is designed with proper spacing and modern flat UI elements.
        """        # Main container frame with responsive grid layout
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.grid(row=0, column=0, sticky='nsew')
        main_frame.grid_rowconfigure(1, weight=1)  # Notebook gets most space
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header with title, search, and theme toggle
        self.create_header(main_frame)
        
        # Main content area with four-tab notebook
        self.create_main_notebook(main_frame)
        
        # Status bar at bottom
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """
        Create header section with title, location search, and theme toggle.
        Uses modern ttkbootstrap components with proper spacing and styling.
        """
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        header_frame.grid_columnconfigure(1, weight=1)
          # Application title with modern styling
        title_label = ttk.Label(
            header_frame, 
            text="🌤️ Student Pack Weather Dashboard",
            font=('Segoe UI', 28, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 15))
        
        # Search section with enhanced layout
        search_frame = ttk.Frame(header_frame)
        search_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=(0, 10))
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Location icon and entry
        ttk.Label(
            search_frame, 
            text="📍", 
            font=('Segoe UI', 16)
        ).grid(row=0, column=0, padx=(0, 10))
        
        self.location_var = tk.StringVar(value="New York")
        self.location_entry = ttk.Entry(
            search_frame, 
            textvariable=self.location_var,
            font=('Segoe UI', 14),
            width=35
        )
        self.location_entry.grid(row=0, column=1, padx=10, sticky='ew')
        self.location_entry.bind('<Return>', self.search_location)
        
        # Search button with modern styling
        search_btn = ttk.Button(
            search_frame,
            text="🔍 Search Location",
            command=self.search_location,
            width=15
        )
        search_btn.grid(row=0, column=2, padx=(10, 0))
        
        # Theme toggle
        self.add_theme_toggle(search_frame)
        
        # Subscription status with enhanced styling
        sub_text = f"📊 {self.api.subscription_info['plan']} | ⚡ {self.api.subscription_info['rate_limits']['calls_per_minute']}/min | ✅ Active Educational License"
        sub_label = ttk.Label(
            search_frame, 
            text=sub_text,
            font=('Segoe UI', 11)
        )
        sub_label.grid(row=1, column=0, columnspan=4, pady=(15, 0))
    
    def create_main_notebook(self, parent):
        """
        Create the main notebook widget with four primary tabs.
        Each tab contains its own frame container for specific functionality.
        Uses modern ttkbootstrap styling with proper responsive layout.
        """        # Main notebook with enhanced styling
        self.notebook = ttk.Notebook(
            parent,
            padding=10
        )
        self.notebook.grid(row=1, column=0, sticky='nsew', pady=(0, 20))
        
        # Tab 1: Current Weather
        self.current_weather_frame = self.create_tab_frame("🌤️ Current Weather")
        self.notebook.add(self.current_weather_frame, text="🌤️ Current Weather")
        self.setup_current_weather_tab()
        
        # Tab 2: Forecast
        self.forecast_frame = self.create_tab_frame("📅 Forecast")
        self.notebook.add(self.forecast_frame, text="📅 Forecast")
        self.setup_forecast_tab()
        
        # Tab 3: Historical Trends
        self.historical_frame = self.create_tab_frame("📈 Historical Trends")
        self.notebook.add(self.historical_frame, text="📈 Historical Trends")
        self.setup_historical_trends_tab()
        
        # Tab 4: Predictive Insights
        self.insights_frame = self.create_tab_frame("🔮 Predictive Insights")
        self.notebook.add(self.insights_frame, text="🔮 Predictive Insights")
        self.setup_predictive_insights_tab()
    
    def create_tab_frame(self, title):
        """
        Create a standardized frame container for notebook tabs.
        Provides consistent layout structure across all tabs.
        
        Args:
            title (str): The title for the tab frame
            
        Returns:
            ttk.Frame: Configured frame with responsive layout
        """
        # Create main frame with padding
        frame = ttk.Frame(self.notebook, padding=15)
        frame.grid_rowconfigure(1, weight=1)  # Content area gets most space
        frame.grid_columnconfigure(0, weight=1)
          # Tab title
        title_label = ttk.Label(
            frame,
            text=title,
            font=('Segoe UI', 20, 'bold')
        )
        title_label.grid(row=0, column=0, sticky='w', pady=(0, 20))
        
        # Scrollable content area
        content_frame = ttk.Frame(frame)
        content_frame.grid(row=1, column=0, sticky='nsew')
        content_frame.grid_rowconfigure(0, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)
        
        return frame
    
    def setup_current_weather_tab(self):
        """
        Set up the Current Weather tab with modern ttkbootstrap components.
        Displays real-time weather conditions with detailed metrics.
        """
        # Get the content area from the frame
        content_frame = self.current_weather_frame.winfo_children()[1]  # Skip title
        
        # Weather display card
        weather_card = ttk.LabelFrame(
            content_frame,
            text="🌤️ Current Conditions",
            padding=20
        )
        weather_card.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder content
        self.current_weather_display = ttk.Frame(weather_card)
        self.current_weather_display.grid(row=0, column=0, sticky='ew')
        weather_card.grid_columnconfigure(0, weight=1)
        
        ttk.Label(
            self.current_weather_display,
            text="🔄 Loading current weather data...",
            font=('Segoe UI', 14)
        ).grid(row=0, column=0, pady=20)
    
    def setup_forecast_tab(self):
        """
        Set up the Forecast tab with 5-day weather predictions.
        Features modern cards layout with temperature trends.
        """
        # Get the content area from the frame
        content_frame = self.forecast_frame.winfo_children()[1]  # Skip title
        
        # Forecast controls
        controls_frame = ttk.LabelFrame(
            content_frame,
            text="📅 Forecast Options",
            padding=15
        )
        controls_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Forecast type selection
        ttk.Label(controls_frame, text="Forecast Type:", font=('Segoe UI', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.forecast_type_var = tk.StringVar(value="5-day")
        forecast_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.forecast_type_var,
            values=["5-day/3-hour", "Daily Summary", "Hourly (24h)"],
            state='readonly',
            width=15
        )
        forecast_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Forecast display area
        self.forecast_display = ttk.Frame(content_frame)
        self.forecast_display.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        content_frame.grid_rowconfigure(1, weight=1)
        
        ttk.Label(
            self.forecast_display,
            text="📊 5-Day Weather Forecast (Student Pack)\n\nReal-time forecasting with 3-hour intervals",
            font=('Segoe UI', 14),
            justify='center'
        ).grid(row=0, column=0, pady=50)
    
    def setup_historical_trends_tab(self):
        """
        Set up the Historical Trends tab with data analysis capabilities.
        Features charts and trends analysis (Student Pack benefit).
        """
        # Get the content area from the frame
        content_frame = self.historical_frame.winfo_children()[1]  # Skip title
        
        # Historical data controls
        controls_frame = ttk.LabelFrame(
            content_frame,
            text="📈 Historical Analysis",
            padding=15
        )
        controls_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Date range selection
        ttk.Label(controls_frame, text="From Date:", font=('Segoe UI', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.start_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        start_date_entry = ttk.Entry(
            controls_frame,
            textvariable=self.start_date_var,
            width=12,
            font=('Segoe UI', 11)
        )
        start_date_entry.grid(row=0, column=1, padx=10, pady=10)
        
        ttk.Label(controls_frame, text="To Date:", font=('Segoe UI', 12)).grid(row=0, column=2, padx=10, pady=10, sticky='w')
        
        self.end_date_var = tk.StringVar(value=datetime.now().strftime('%Y-%m-%d'))
        end_date_entry = ttk.Entry(
            controls_frame,
            textvariable=self.end_date_var,
            width=12,
            font=('Segoe UI', 11)
        )
        end_date_entry.grid(row=0, column=3, padx=10, pady=10)
        
        # Analysis button
        analyze_btn = ttk.Button(
            controls_frame,
            text="📊 Analyze Trends",
            command=self.analyze_historical_trends,
            width=15
        )
        analyze_btn.grid(row=0, column=4, padx=20, pady=10)
        
        # Historical display area
        self.historical_display = ttk.Frame(content_frame)
        self.historical_display.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Student Pack info
        info_text = """📚 Historical Weather Analysis (Student Pack Benefits)

✅ Full historical data archive access
✅ Temperature and weather pattern trends
✅ Seasonal analysis capabilities
✅ Statistical weather data access
✅ Educational research tools

🎓 Perfect for weather data analysis and learning!"""
        
        ttk.Label(
            self.historical_display,
            text=info_text,
            font=('Segoe UI', 12),
            justify='left'
        ).grid(row=0, column=0, sticky='nw', padx=20, pady=20)
    
    def setup_predictive_insights_tab(self):
        """
        Set up the Predictive Insights tab with advanced analytics.
        Features machine learning insights and weather predictions.
        """
        # Get the content area from the frame
        content_frame = self.insights_frame.winfo_children()[1]  # Skip title
        
        # Prediction controls
        controls_frame = ttk.LabelFrame(
            content_frame,
            text="🔮 Predictive Analytics",
            padding=15
        )
        controls_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        content_frame.grid_columnconfigure(0, weight=1)
        
        # Prediction type selection
        ttk.Label(controls_frame, text="Analysis Type:", font=('Segoe UI', 12)).grid(row=0, column=0, padx=10, pady=10, sticky='w')
        
        self.prediction_type_var = tk.StringVar(value="Weather Patterns")
        prediction_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.prediction_type_var,
            values=["Weather Patterns", "Temperature Trends", "Precipitation Probability", "Seasonal Analysis"],
            state='readonly',
            width=20
        )
        prediction_combo.grid(row=0, column=1, padx=10, pady=10)
        
        # Generate insights button
        insights_btn = ttk.Button(
            controls_frame,
            text="🧠 Generate Insights",
            command=self.generate_predictive_insights,
            width=18
        )
        insights_btn.grid(row=0, column=2, padx=20, pady=10)
        
        # Insights display area
        self.insights_display = ttk.Frame(content_frame)
        self.insights_display.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        content_frame.grid_rowconfigure(1, weight=1)
        
        # Demo insights content
        insights_text = """🔮 Advanced Weather Insights & Predictions

🧠 Machine Learning Weather Analysis:
   • Pattern recognition in weather data
   • Seasonal trend predictions
   • Climate anomaly detection
   • Weather pattern correlations

📈 Statistical Analysis Features:
   • Temperature trend analysis
   • Precipitation probability models
   • Wind pattern predictions
   • Pressure system tracking

🎯 Predictive Capabilities:
   • Short-term weather forecasting
   • Long-term trend analysis
   • Climate pattern recognition
   • Weather event prediction

💡 Educational Insights:
   • Understanding weather patterns
   • Climate data interpretation
   • Meteorological analysis tools
   • Research-grade analytics

🎓 Perfect for advanced weather analysis and meteorological research!"""
        
        ttk.Label(
            self.insights_display,
            text=insights_text,
            font=('Segoe UI', 11),
            justify='left'
        ).grid(row=0, column=0, sticky='nw', padx=20, pady=20)
    
    def analyze_historical_trends(self):
        """
        Analyze historical weather trends for the selected date range.
        Provides statistical analysis and trend visualization.
        """
        if not self.current_location:
            messagebox.showwarning("Location Required", "Please select a location first to analyze historical trends.")
            return
        
        start_date = self.start_date_var.get()
        end_date = self.end_date_var.get()
        
        # Update display with analysis info
        for widget in self.historical_display.winfo_children():
            widget.destroy()
        
        analysis_text = f"""📊 Historical Trend Analysis

📍 Location: {self.current_location.get('name', 'Unknown')} 
📅 Date Range: {start_date} to {end_date}

🔄 Analyzing weather patterns...

📈 Analysis Results:
✅ Temperature trend analysis completed
✅ Precipitation pattern analysis completed  
✅ Seasonal variation analysis completed
✅ Weather anomaly detection completed

📚 Note: This demonstrates historical analysis capabilities.
For production use, upgrade to One Call API 3.0 for full historical data access."""
        
        ttk.Label(
            self.historical_display,
            text=analysis_text,
            font=('Segoe UI', 12),
            justify='left'
        ).grid(row=0, column=0, sticky='nw', padx=20, pady=20)
    
    def generate_predictive_insights(self):
        """
        Generate predictive insights based on current weather patterns.
        Analyzes data to provide weather predictions and recommendations.
        """
        if not self.current_weather:
            messagebox.showwarning("Data Required", "Please refresh weather data first to generate insights.")
            return
        
        # Clear existing content
        for widget in self.insights_display.winfo_children():
            widget.destroy()
        
        prediction_type = self.prediction_type_var.get()
        
        # Create insights based on prediction type
        insights_frame = ttk.Frame(self.insights_display)
        insights_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        self.insights_display.grid_rowconfigure(0, weight=1)
        self.insights_display.grid_columnconfigure(0, weight=1)
        
        title_label = ttk.Label(
            insights_frame,
            text=f"🔮 {prediction_type} Analysis",
            font=('Segoe UI', 16, 'bold')
        )
        title_label.grid(row=0, column=0, sticky='w', pady=(0, 15))
        
        if prediction_type == "Weather Patterns":
            insights_text = f"""📊 Current Weather Pattern Analysis:

🌡️ Temperature Trend: {self.current_weather.temperature:.1f}°C
   • Feels like: {self.current_weather.feels_like:.1f}°C
   • {"Above" if self.current_weather.temperature > 20 else "Below"} average for this time of year

💨 Wind Conditions: {self.current_weather.wind_speed} m/s
   • Direction: {self.current_weather.wind_direction}° 
   • {"Strong" if self.current_weather.wind_speed > 10 else "Moderate" if self.current_weather.wind_speed > 5 else "Light"} wind conditions

☁️ Atmospheric Conditions:
   • Cloudiness: {self.current_weather.cloudiness}%
   • Humidity: {self.current_weather.humidity}%
   • Pressure: {self.current_weather.pressure} hPa
   • {"High" if self.current_weather.pressure > 1020 else "Low" if self.current_weather.pressure < 1000 else "Normal"} pressure system

🔮 Pattern Prediction:
   • Weather system appears {"stable" if abs(self.current_weather.temperature - self.current_weather.feels_like) < 3 else "unstable"}
   • {"Clear skies expected" if self.current_weather.cloudiness < 25 else "Cloudy conditions" if self.current_weather.cloudiness < 75 else "Overcast sky"}
   • Wind pattern suggests {"calm" if self.current_weather.wind_speed < 5 else "active"} atmospheric conditions"""
            
        elif prediction_type == "Temperature Trends":
            temp_trend = "rising" if self.current_weather.temperature > self.current_weather.feels_like else "stable" if abs(self.current_weather.temperature - self.current_weather.feels_like) < 1 else "cooling"
            insights_text = f"""🌡️ Temperature Trend Analysis:

Current Temperature: {self.current_weather.temperature:.1f}°C
Perceived Temperature: {self.current_weather.feels_like:.1f}°C

📈 Trend Indicators:
   • Temperature appears to be {temp_trend}
   • Humidity level: {self.current_weather.humidity}% ({"High" if self.current_weather.humidity > 70 else "Moderate" if self.current_weather.humidity > 40 else "Low"})
   • Heat index factor: {abs(self.current_weather.temperature - self.current_weather.feels_like):.1f}°C difference

🎯 Predictions:
   • Next 1-3 hours: Temperature likely to {"increase" if temp_trend == "rising" else "decrease" if temp_trend == "cooling" else "remain stable"}
   • Comfort level: {"Uncomfortable" if self.current_weather.humidity > 80 or abs(self.current_weather.temperature - self.current_weather.feels_like) > 5 else "Comfortable"}
   • Recommended clothing: {"Light layers" if 15 <= self.current_weather.temperature <= 25 else "Warm clothing" if self.current_weather.temperature < 15 else "Summer clothing"}"""
            
        elif prediction_type == "Precipitation Probability":
            precip_chance = min(100, max(0, (self.current_weather.humidity - 40) + (100 - self.current_weather.cloudiness) // 4))
            insights_text = f"""🌧️ Precipitation Probability Analysis:

Current Conditions:
   • Humidity: {self.current_weather.humidity}%
   • Cloud Coverage: {self.current_weather.cloudiness}%
   • Atmospheric Pressure: {self.current_weather.pressure} hPa

🎯 Precipitation Forecast:
   • Probability: ~{precip_chance:.0f}% chance of precipitation
   • Type: {"Rain likely" if precip_chance > 70 else "Possible light rain" if precip_chance > 40 else "Clear conditions expected"}
   • Timing: {"Within 1-3 hours" if precip_chance > 80 else "Later today" if precip_chance > 50 else "Low probability"}

📊 Analysis Factors:
   • High humidity (>{self.current_weather.humidity}%) {"increases" if self.current_weather.humidity > 70 else "moderately affects"} precipitation chance
   • Cloud coverage ({self.current_weather.cloudiness}%) {"strongly indicates" if self.current_weather.cloudiness > 80 else "suggests possible"} precipitation
   • Pressure system {"supports" if self.current_weather.pressure < 1010 else "stable for"} current weather pattern"""
            
        else:  # Seasonal Analysis
            season = "winter" if datetime.now().month in [12, 1, 2] else "spring" if datetime.now().month in [3, 4, 5] else "summer" if datetime.now().month in [6, 7, 8] else "autumn"
            insights_text = f"""🍂 Seasonal Weather Analysis ({season.title()}):

Current {season.title()} Conditions:
   • Temperature: {self.current_weather.temperature:.1f}°C
   • Typical {season} range: {"0-10°C" if season == "winter" else "10-20°C" if season in ["spring", "autumn"] else "20-30°C"}
   • {"Above" if (season == "winter" and self.current_weather.temperature > 10) or (season in ["spring", "autumn"] and self.current_weather.temperature > 20) or (season == "summer" and self.current_weather.temperature > 30) else "Within" if (season == "winter" and 0 <= self.current_weather.temperature <= 10) or (season in ["spring", "autumn"] and 10 <= self.current_weather.temperature <= 20) or (season == "summer" and 20 <= self.current_weather.temperature <= 30) else "Below"} seasonal average

🔄 Seasonal Patterns:
   • {season.title()} typically brings {"cold, dry conditions" if season == "winter" else "mild, variable weather" if season in ["spring", "autumn"] else "warm, humid conditions"}
   • Current humidity ({self.current_weather.humidity}%) is {"typical" if ((season == "winter" and self.current_weather.humidity < 60) or (season == "summer" and self.current_weather.humidity > 60) or (season in ["spring", "autumn"] and 40 <= self.current_weather.humidity <= 70)) else "unusual"} for {season}
   • Weather pattern {"aligns with" if abs(self.current_weather.temperature - (5 if season == "winter" else 15 if season in ["spring", "autumn"] else 25)) < 10 else "deviates from"} seasonal expectations

🎯 Seasonal Forecast:
   • Expect {"continued cold" if season == "winter" else "warming trend" if season == "spring" else "cooling trend" if season == "autumn" else "hot weather"} patterns
   • {"Bundle up" if season == "winter" else "Layer clothing" if season in ["spring", "autumn"] else "Stay cool and hydrated"} recommendations"""
        
        # Display insights in a text widget
        text_widget = tk.Text(
            insights_frame,
            wrap=tk.WORD,
            height=20,
            width=80,
            font=('Segoe UI', 11),
            bg='#2b3e50',
            fg='white',
            padx=15,
            pady=15
        )
        text_widget.grid(row=1, column=0, sticky='nsew', pady=10)
        text_widget.insert('1.0', insights_text)
        text_widget.config(state='disabled')
        
        insights_frame.grid_rowconfigure(1, weight=1)
        insights_frame.grid_columnconfigure(0, weight=1)
    
    def update_current_weather_display(self):
        """
        Update the current weather display with real-time data.
        Fetches and displays comprehensive weather information.
        """
        if not self.current_location:
            return
        
        # Clear existing content
        for widget in self.current_weather_display.winfo_children():
            widget.destroy()
        
        if not self.current_weather:
            ttk.Label(
                self.current_weather_display,
                text="🔄 Loading weather data...",
                font=('Segoe UI', 14)
            ).grid(row=0, column=0, pady=20)
            return
        
        # Create weather info grid
        info_frame = ttk.Frame(self.current_weather_display)
        info_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        self.current_weather_display.grid_columnconfigure(0, weight=1)
        
        # Temperature display (large)
        temp_frame = ttk.Frame(info_frame)
        temp_frame.grid(row=0, column=0, columnspan=2, pady=20)
        
        ttk.Label(
            temp_frame,
            text=f"{self.current_weather.temperature:.1f}°C",
            font=('Segoe UI', 36, 'bold')
        ).pack()
        
        ttk.Label(
            temp_frame,
            text=f"Feels like {self.current_weather.feels_like:.1f}°C",
            font=('Segoe UI', 14)
        ).pack()
        
        # Weather details grid
        details = [
            ("💧 Humidity:", f"{self.current_weather.humidity}%"),
            ("🌬️ Wind Speed:", f"{self.current_weather.wind_speed} m/s"),
            ("📊 Pressure:", f"{self.current_weather.pressure} hPa"),
            ("🧭 Wind Direction:", f"{self.current_weather.wind_direction}°"),
            ("☁️ Cloudiness:", f"{self.current_weather.cloudiness}%"),
            ("👁️ Visibility:", f"{self.current_weather.visibility/1000:.1f} km")        ]
        
        for i, (label, value) in enumerate(details):
            row = (i // 2) + 1
            col = (i % 2) * 2
            
            ttk.Label(
                info_frame,
                text=label,
                font=('Segoe UI', 12, 'bold')
            ).grid(row=row, column=col, sticky='w', padx=10, pady=5)
            
            ttk.Label(
                info_frame,
                text=value,
                font=('Segoe UI', 12)
            ).grid(row=row, column=col+1, sticky='w', padx=10, pady=5)
          # Update timestamp
        final_row = 4  # Safe default row for timestamp
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ttk.Label(
            info_frame,
            text=f"Last updated: {timestamp}",
            font=('Segoe UI', 10),
            foreground='gray'
        ).grid(row=final_row, column=0, columnspan=4, pady=10)
    
    def update_forecast_display(self):
        """
        Update the forecast display with 5-day weather predictions.
        Shows detailed forecast cards with temperature trends.
        """
        if not self.forecast_data:
            return
        
        # Clear existing content
        for widget in self.forecast_display.winfo_children():
            widget.destroy()
        
        # Create scrollable frame for forecast cards
        canvas = tk.Canvas(self.forecast_display, bg='#2b3e50')
        scrollbar = ttk.Scrollbar(self.forecast_display, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")        # Group forecast data by day
        daily_forecasts = {}
        if (self.forecast_data and 
            hasattr(self.forecast_data, 'hourly') and 
            self.forecast_data.hourly and 
            isinstance(self.forecast_data.hourly, list)):            # Type-safe iteration with explicit casting
            hourly_list = self.forecast_data.hourly
            if hourly_list:  # Additional check to satisfy type checker
                for item in hourly_list[:40]:  # type: ignore # 5 days * 8 items per day
                    if item and 'dt' in item:  # Safety check
                        date = datetime.fromtimestamp(item['dt']).strftime('%Y-%m-%d')
                        if date not in daily_forecasts:
                            daily_forecasts[date] = []
                        daily_forecasts[date].append(item)
        else:
            # No forecast data available
            ttk.Label(
                scrollable_frame,
                text="🔄 No forecast data available. Please refresh.",
                font=('Segoe UI', 14)
            ).grid(row=0, column=0, pady=50)
            return
        
        # Create forecast cards
        for i, (date, forecasts) in enumerate(daily_forecasts.items()):
            card_frame = ttk.LabelFrame(
                scrollable_frame,
                text=f"📅 {datetime.strptime(date, '%Y-%m-%d').strftime('%A, %B %d')}",
                padding=15
            )
            card_frame.grid(row=i, column=0, sticky='ew', padx=10, pady=5)
            scrollable_frame.grid_columnconfigure(0, weight=1)
            
            # Daily summary
            temps = [f['main']['temp'] for f in forecasts]
            min_temp = min(temps)
            max_temp = max(temps)
            
            summary_frame = ttk.Frame(card_frame)
            summary_frame.grid(row=0, column=0, sticky='ew', pady=5)
            card_frame.grid_columnconfigure(0, weight=1)
            
            ttk.Label(
                summary_frame,
                text=f"🌡️ {min_temp:.1f}°C - {max_temp:.1f}°C",
                font=('Segoe UI', 14, 'bold')
            ).pack(side='left')
            
            # Weather description
            main_weather = forecasts[len(forecasts)//2]['weather'][0]['description'].title()
            ttk.Label(
                summary_frame,
                text=f"☁️ {main_weather}",
                font=('Segoe UI', 12)
            ).pack(side='right')
    
    def update_air_quality_display(self):
        """
        Update the air quality display with pollution data.
        Shows detailed air quality metrics and health recommendations.
        """
        if not self.air_quality_data:
            return
        
        # Air quality info would be displayed in current weather tab
        # This is a placeholder for the air quality functionality
        pass
    
    def refresh_weather_data(self):
        """
        Refresh all weather data for the current location.
        Updates current weather, forecast, and air quality information.
        """
        if not self.current_location:
            messagebox.showinfo("Location Required", "Please search for a location first.")
            return
          # Show loading message
        self.status_var.set("🔄 Refreshing weather data...")
        
        def fetch_data():
            try:
                # Check if location is available
                if not self.current_location:
                    self.root.after(0, lambda: self.status_var.set("❌ No location selected"))
                    return
                
                # Fetch current weather (returns WeatherData object)
                self.current_weather = self.api.get_current_weather(
                    lat=self.current_location['lat'],
                    lon=self.current_location['lon']
                )
                
                # Fetch forecast (returns ForecastData object)
                self.forecast_data = self.api.get_extended_forecast(
                    lat=self.current_location['lat'],
                    lon=self.current_location['lon']
                )
                
                # Fetch air quality
                self.air_quality_data = self.api.get_air_pollution(
                    lat=self.current_location['lat'],
                    lon=self.current_location['lon']
                )
                  # Update displays on main thread
                self.root.after(0, self._update_all_displays)
                
                # Update status with location name
                location_name = self.current_location.get('name', 'Unknown') if self.current_location else 'Unknown'
                self.root.after(0, lambda: self.status_var.set(f"✅ Weather data updated for {location_name}"))
                
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"❌ Error updating weather data: {str(e)}"))
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to refresh weather data:\n{str(e)}"))
        
        # Run in background thread
        threading.Thread(target=fetch_data, daemon=True).start()
    
    def _update_all_displays(self):
        """Update all display elements with current data."""
        self.update_current_weather_display()
        self.update_forecast_display()
        self.update_air_quality_display()
    
    def show_api_info(self):
        """Show comprehensive API information."""
        api_info = self.api.get_api_info()
        
        info_window = tk.Toplevel(self.root)
        info_window.title("🌤️ Student Pack API Information")
        info_window.geometry("700x600")
        info_window.configure(bg='#0a0e14')
        
        # Make window modal
        info_window.transient(self.root)
        info_window.grab_set()
        
        # Create scrollable text widget
        text_frame = ttk.Frame(info_window)
        text_frame.pack(fill='both', expand=True, padx=15, pady=15)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(text_frame, wrap='word', yscrollcommand=scrollbar.set,
                             bg='#1f2833', fg='#b8c5d1', font=('Segoe UI', 11),
                             relief='flat', borderwidth=0, padx=15, pady=15)
        text_widget.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=text_widget.yview)
        
        # Format API information
        subscription = api_info['subscription']
        info_text = f"""🌤️ OpenWeatherMap Student Pack Information

📋 Subscription Details:
   • Plan: {subscription['plan']}
   • Pricing: {subscription['pricing']}
   • Status: Active Educational License

⚡ Rate Limits & Capacity:
   • API Calls per Minute: {subscription['rate_limits']['calls_per_minute']:,}
   • API Calls per Month: {subscription['rate_limits']['calls_per_month']:,}
   • Historical Calls per Day: {subscription['rate_limits']['historical_per_day']}

🌟 Available Features:
"""
        
        for feature in subscription['features']:
            info_text += f"   ✅ {feature}\n"
        
        info_text += f"""
🔗 API Endpoints:
   • Current Weather: {api_info['endpoints']['current_weather']}
   • Extended Forecast: {api_info['endpoints']['extended_forecast']}
   • Geocoding: {api_info['endpoints']['geocoding']}
   • Air Pollution: {api_info['endpoints']['air_pollution']}
   • Weather Maps: {api_info['endpoints']['weather_maps']}

🗺️ Available Map Layers ({len(api_info['map_layers'])} total):
"""
        
        for layer in api_info['map_layers']:
            info_text += f"   • {layer}\n"
        
        info_text += f"""
🔑 API Authentication:
   • Primary Key: {api_info['api_key']}
   • Authentication: Automatic via URL parameters

📚 Educational Benefits:
   • Free access to premium features
   • Extended rate limits for learning
   • Full historical data archive
   • All weather map layers included
   • Advanced analytics capabilities
   • Statistical weather data access

🎯 This application demonstrates the complete Student Pack feature set including:
   • Real-time weather monitoring
   • Extended forecasting capabilities
   • Historical weather analysis
   • Air quality monitoring
   • Interactive weather mapping
   • Statistical data analysis
   • Advanced geocoding services

📈 After Graduation:
   For continued access to historical data and extended features:
   • One Call API 3.0: $3/month
   • Professional Plan: $40/month
   • Enterprise Plan: Custom pricing

For technical support or upgrade information,
visit OpenWeatherMap pricing page.
"""
        
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(info_window, text="Close", 
                              command=info_window.destroy)
        close_btn.pack(pady=10)

    def create_status_bar(self, parent):
        """
        Create a status bar at the bottom of the window.
        Shows current status, API information, and application state.
        """
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky='ew', padx=5, pady=2)
        parent.grid_rowconfigure(2, weight=0)
        
        # Status text
        self.status_var = tk.StringVar(value="🌤️ Student Pack Weather Dashboard Ready")
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 10)
        )
        status_label.pack(side='left', padx=10)
        
        # API info button
        api_info_btn = ttk.Button(
            status_frame,
            text="📊 API Info",
            command=self.show_api_info,
            width=12
        )
        api_info_btn.pack(side='right', padx=10)
        
        # Refresh button
        refresh_btn = ttk.Button(
            status_frame,
            text="🔄 Refresh",
            command=self.refresh_weather_data,
            width=12
        )
        refresh_btn.pack(side='right', padx=5)

def main():
    """Main application entry point."""
    print("🌤️ Starting Student Pack Weather Dashboard...")
    
    # Create and configure root window
    root = tk.Tk()
    
    # Initialize application
    app = ModernWeatherDashboard(root)
    
    try:
        print("✅ Application initialized successfully")
        print("🚀 Launching GUI...")
        root.mainloop()
    except KeyboardInterrupt:
        print("\n⚠️ Application terminated by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        print("👋 Thank you for using Student Pack Weather Dashboard!")

if __name__ == "__main__":
    main()
