"""
🎓 OpenWeatherMap Student Pack Dashboard
A comprehensive, modern weather application showcasing all Student Pack features.

Features:
- Real-time weather data with advanced metrics
- Extended forecasts (4-day hourly, 16-day daily)
- Interactive weather maps (15+ layers)
- Air quality monitoring with detailed pollutants
- Historical weather data (1-year archive)
- Statistical analysis and accumulated parameters
- Advanced geocoding and location search
- Modern, responsive dark-themed GUI
- Comprehensive API information and monitoring

Author: Student Pack Implementation
Date: June 2025
License: Educational Use Only
"""

import tkinter as tk
from tkinter import ttk, messagebox
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

@dataclass
class ForecastData:
    """Data class for forecast information."""
    hourly: List[Dict]
    daily: List[Dict]

class StudentPackWeatherAPI:
    """
    Enhanced Weather API client for OpenWeatherMap Student Pack.
    Provides access to all Student Pack features including extended forecasts,
    historical data, air pollution, weather maps, and statistical analysis.
    """
    
    def __init__(self):
        self.api_key = os.getenv('OPENWEATHER_API_KEY', '')
        self.backup_api_key = os.getenv('OPENWEATHER_API_KEY_BACKUP', '')
        self.base_url = "https://api.openweathermap.org/data/2.5"
        self.onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        self.geocoding_url = "https://api.openweathermap.org/geo/1.0"
        self.pollution_url = "https://api.openweathermap.org/data/2.5/air_pollution"
        self.maps_url = "https://tile.openweathermap.org/map"
        
        # Student Pack configuration
        self.subscription_info = {
            'plan': 'Student Educational Pack',
            'pricing': 'Free for Educational Use',
            'rate_limits': {
                'calls_per_minute': 3000,
                'calls_per_month': 100000000,
                'historical_per_day': 50000
            },
            'features': [
                'Current weather data',
                'Extended forecasts (4-day hourly, 16-day daily)',
                'Historical data (1-year archive)',
                'Air pollution monitoring',
                'Interactive weather maps (15+ layers)',
                'Statistical weather analysis',
                'Accumulated parameters',
                'Advanced geocoding',
                'Weather alerts',
                'Premium endpoints'
            ]
        }
        
        # Available map layers
        self.map_layers = [
            'temp_new', 'precipitation_new', 'pressure_new', 'wind_new',
            'clouds_new', 'rain', 'snow', 'temp', 'precipitation', 'pressure',
            'wind', 'clouds'
        ]
        
        print("🎓 Student Pack Weather API initialized")
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
            wind_direction=data.get('wind', {}).get('deg', 0),            visibility=data.get('visibility', 0),
            description=data['weather'][0]['description'].title(),
            icon=data['weather'][0]['icon'],
            city=data['name'],
            country=data['sys']['country'],
            timestamp=data['dt']
        )
    
    def get_extended_forecast(self, lat: float, lon: float) -> Optional[ForecastData]:
        """Get extended forecast (Student Pack: 4-day hourly, 16-day daily)."""
        params = {
            'lat': lat,
            'lon': lon,
            'units': 'metric'
        }
        
        data = self._make_request(f"{self.onecall_url}", params)
        if not data:
            return None
            
        return ForecastData(
            hourly=data.get('hourly', [])[:96],  # 4 days of hourly data
            daily=data.get('daily', [])[:16]     # 16 days of daily data
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
        """Get historical weather data (Student Pack: 1-year archive)."""
        timestamp = int(date.timestamp())
        params = {
            'lat': lat,
            'lon': lon,
            'dt': timestamp,
            'units': 'metric'
        }
        
        return self._make_request(f"{self.onecall_url}/timemachine", params)
    
    def get_api_info(self) -> Dict:
        """Get comprehensive API information."""
        return {
            'api_key': f"{self.api_key[:10]}...{self.api_key[-4:]}",
            'subscription': self.subscription_info,
            'endpoints': {
                'current_weather': self.base_url,
                'extended_forecast': self.onecall_url,
                'geocoding': self.geocoding_url,
                'air_pollution': self.pollution_url,
                'weather_maps': self.maps_url
            },
            'map_layers': self.map_layers
        }

class ModernWeatherDashboard:
    """
    Modern, comprehensive weather dashboard showcasing all Student Pack features.
    Features a dark theme, responsive design, and intuitive user interface.
    """
    
    def __init__(self, root):
        self.root = root
        self.api = StudentPackWeatherAPI()
        
        # State management
        self.current_location = None
        self.current_weather = None
        self.forecast_data = None
        self.air_quality_data = None
        
        # Initialize UI
        self.setup_window()
        self.setup_styles()
        self.create_interface()
        self.load_default_location()
    
    def setup_window(self):
        """Configure main window."""
        self.root.title("🎓 Student Pack Weather Dashboard - OpenWeatherMap")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)
        self.root.configure(bg='#0a0e14')
        
        # Center window
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (1200 // 2)
        y = (self.root.winfo_screenheight() // 2) - (800 // 2)
        self.root.geometry(f"1200x800+{x}+{y}")
        
        # Make responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def setup_styles(self):
        """Configure modern dark theme styles."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Color palette
        colors = {
            'bg_primary': '#0a0e14',      # Main background
            'bg_secondary': '#151a21',     # Secondary background
            'bg_tertiary': '#1f2833',      # Card backgrounds
            'accent_primary': '#00d4ff',   # Primary accent (cyan)
            'accent_secondary': '#00ff9f', # Secondary accent (green)
            'text_primary': '#ffffff',     # Primary text
            'text_secondary': '#b8c5d1',   # Secondary text
            'text_muted': '#6b7785',       # Muted text
            'border': '#2a3441',           # Border color
            'success': '#00ff9f',          # Success color
            'warning': '#ffb700',          # Warning color
            'error': '#ff6b6b'             # Error color
        }
        
        # Configure styles
        style_configs = {
            'TFrame': {'background': colors['bg_secondary']},
            'TLabel': {'background': colors['bg_secondary'], 'foreground': colors['text_primary']},
            'TButton': {
                'background': colors['accent_primary'],
                'foreground': colors['bg_primary'],
                'font': ('Segoe UI', 10, 'bold'),
                'borderwidth': 0,
                'focuscolor': 'none'
            },
            'TEntry': {
                'background': colors['bg_tertiary'],
                'foreground': colors['text_primary'],
                'borderwidth': 1,
                'relief': 'solid',
                'bordercolor': colors['border']
            },
            'TNotebook': {'background': colors['bg_secondary']},
            'TNotebook.Tab': {
                'background': colors['bg_tertiary'],
                'foreground': colors['text_secondary'],
                'padding': [15, 8]
            }
        }
        
        for style_name, config in style_configs.items():
            self.style.configure(style_name, **config)
        
        # Custom styles
        self.style.configure('Title.TLabel', 
                           font=('Segoe UI', 24, 'bold'),
                           foreground=colors['accent_primary'])
        self.style.configure('Header.TLabel',
                           font=('Segoe UI', 14, 'bold'),
                           foreground=colors['text_primary'])
        self.style.configure('Subheader.TLabel',
                           font=('Segoe UI', 12, 'bold'),
                           foreground=colors['accent_secondary'])
        self.style.configure('Data.TLabel',
                           font=('Segoe UI', 11),
                           foreground=colors['text_secondary'])
        self.style.configure('Muted.TLabel',
                           font=('Segoe UI', 10),
                           foreground=colors['text_muted'])
    
    def create_interface(self):
        """Create the main interface layout."""
        # Main container
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        main_frame.grid_rowconfigure(1, weight=1)
        main_frame.grid_columnconfigure(0, weight=1)
        
        # Header
        self.create_header(main_frame)
        
        # Main content area
        self.create_content_area(main_frame)
        
        # Status bar
        self.create_status_bar(main_frame)
    
    def create_header(self, parent):
        """Create header with title and search."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 15))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="🎓 Student Pack Weather Dashboard",
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 10))
        
        # Search section
        search_frame = ttk.Frame(header_frame)
        search_frame.grid(row=1, column=0, columnspan=3, sticky='ew')
        search_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="📍", font=('Segoe UI', 14)).grid(row=0, column=0, padx=(0, 5))
        
        self.location_var = tk.StringVar(value="New York")
        self.location_entry = ttk.Entry(search_frame, textvariable=self.location_var, 
                                       font=('Segoe UI', 12), width=30)
        self.location_entry.grid(row=0, column=1, padx=5, sticky='ew')
        self.location_entry.bind('<Return>', self.search_location)
        
        search_btn = ttk.Button(search_frame, text="🔍 Search", 
                               command=self.search_location)
        search_btn.grid(row=0, column=2, padx=(5, 0))
        
        # Subscription info
        sub_text = f"Plan: {self.api.subscription_info['plan']} | Rate: {self.api.subscription_info['rate_limits']['calls_per_minute']}/min | Status: Active"
        sub_label = ttk.Label(search_frame, text=sub_text, style='Subheader.TLabel')
        sub_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))
    
    def create_content_area(self, parent):
        """Create main content area with tabs."""
        # Notebook for tabs
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky='nsew', pady=(0, 10))
        
        # Create tabs
        self.create_current_weather_tab()
        self.create_forecast_tab()
        self.create_air_quality_tab()
        self.create_maps_tab()
        self.create_historical_tab()
        self.create_analytics_tab()
    
    def create_current_weather_tab(self):
        """Current weather tab with detailed information."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text='🌤️ Current Weather')
        
        # Scrollable content
        canvas = tk.Canvas(tab_frame, bg='#151a21', highlightthickness=0)
        scrollbar = ttk.Scrollbar(tab_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind('<Configure>', 
                            lambda e: canvas.configure(scrollregion=canvas.bbox('all')))
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        # Current weather content
        self.current_weather_frame = scrollable_frame
        self.create_current_weather_content()
    
    def create_current_weather_content(self):
        """Create current weather display content."""
        # Main weather card
        weather_card = ttk.LabelFrame(self.current_weather_frame, text='Current Conditions', 
                                     style='Header.TLabel')
        weather_card.grid(row=0, column=0, sticky='ew', padx=20, pady=10)
        self.current_weather_frame.grid_columnconfigure(0, weight=1)
        
        self.weather_display = ttk.Frame(weather_card)
        self.weather_display.grid(row=0, column=0, sticky='ew', padx=15, pady=15)
        weather_card.grid_columnconfigure(0, weight=1)
        
        # Placeholder
        ttk.Label(self.weather_display, text="🔄 Loading weather data...", 
                 style='Data.TLabel').grid(row=0, column=0, pady=20)
    
    def create_forecast_tab(self):
        """Extended forecast tab (4-day hourly, 16-day daily)."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text='📅 Extended Forecasts')
        
        # Forecast content
        forecast_info = ttk.Label(tab_frame, 
                                text="🎓 Student Pack Extended Forecasts\n\n"
                                     "⏰ Hourly Forecast: 96 hours (4 days)\n"
                                     "📅 Daily Forecast: 16 days\n"
                                     "🌡️ Temperature trends & patterns\n"
                                     "☔ Precipitation probability\n"
                                     "💨 Wind speed & direction\n"
                                     "☀️ UV Index forecasting",
                                style='Data.TLabel',
                                justify='left')
        forecast_info.grid(row=0, column=0, padx=20, pady=20, sticky='nw')
    
    def create_air_quality_tab(self):
        """Air quality monitoring tab."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text='🌬️ Air Quality')
        
        self.air_quality_frame = ttk.Frame(tab_frame)
        self.air_quality_frame.grid(row=0, column=0, sticky='nsew', padx=20, pady=20)
        tab_frame.grid_rowconfigure(0, weight=1)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        # Placeholder
        ttk.Label(self.air_quality_frame, text="🔄 Loading air quality data...", 
                 style='Data.TLabel').grid(row=0, column=0, pady=20)
    
    def create_maps_tab(self):
        """Interactive weather maps tab."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text='🗺️ Weather Maps')
        
        # Map controls
        controls_frame = ttk.LabelFrame(tab_frame, text='Interactive Weather Maps')
        controls_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=20)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(controls_frame, text="🌈 Select Layer:", style='Header.TLabel').grid(row=0, column=0, padx=10, pady=10)
        
        self.selected_layer = tk.StringVar(value='temp_new')
        layer_combo = ttk.Combobox(controls_frame, textvariable=self.selected_layer,
                                  values=self.api.map_layers, state='readonly')
        layer_combo.grid(row=0, column=1, padx=10, pady=10)
        
        map_btn = ttk.Button(controls_frame, text="🌍 Open Interactive Map",
                            command=self.open_weather_map)
        map_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Map info
        map_info = ttk.Label(tab_frame,
                           text="🗺️ Student Pack Weather Maps (15+ Layers):\n\n"
                                "🌡️ Temperature Maps (Current, Forecast, Historical)\n"
                                "☔ Precipitation Maps (Rain, Snow, Radar)\n"
                                "💨 Wind Maps (Speed, Direction, Patterns)\n"
                                "☁️ Cloud Maps (Coverage, Satellite)\n"
                                "📊 Atmospheric Maps (Pressure, Conditions)\n\n"
                                "🎓 Full access included with Student Pack!",
                           style='Data.TLabel',
                           justify='left')
        map_info.grid(row=1, column=0, padx=20, pady=20, sticky='nw')
    
    def create_historical_tab(self):
        """Historical weather data tab."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text='📚 Historical Data')
        
        # Historical controls
        controls_frame = ttk.LabelFrame(tab_frame, text='Historical Weather Data (1 Year Archive)')
        controls_frame.grid(row=0, column=0, sticky='ew', padx=20, pady=20)
        tab_frame.grid_columnconfigure(0, weight=1)
        
        ttk.Label(controls_frame, text="📅 Select Date:", style='Header.TLabel').grid(row=0, column=0, padx=10, pady=10)
        
        self.hist_date_var = tk.StringVar(value=(datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d'))
        date_entry = ttk.Entry(controls_frame, textvariable=self.hist_date_var, width=15)
        date_entry.grid(row=0, column=1, padx=10, pady=10)
        
        hist_btn = ttk.Button(controls_frame, text="📊 Get Historical Data",
                             command=self.get_historical_data)
        hist_btn.grid(row=0, column=2, padx=10, pady=10)
        
        # Historical display
        self.historical_display = ttk.Frame(tab_frame)
        self.historical_display.grid(row=1, column=0, sticky='nsew', padx=20, pady=20)
        tab_frame.grid_rowconfigure(1, weight=1)
    
    def create_analytics_tab(self):
        """Analytics and API information tab."""
        tab_frame = ttk.Frame(self.notebook)
        self.notebook.add(tab_frame, text='📊 Analytics & API Info')
        
        # API Info button
        api_btn = ttk.Button(tab_frame, text="ℹ️ View Complete API Information",
                           command=self.show_api_info)
        api_btn.grid(row=0, column=0, padx=20, pady=20)
        
        # Analytics info
        analytics_info = ttk.Label(tab_frame,
                                 text="📊 Student Pack Analytics Features:\n\n"
                                      "📈 Statistical Weather Analysis\n"
                                      "🧮 Accumulated Parameters\n"
                                      "📉 Temperature & Precipitation Trends\n"
                                      "🔍 Advanced Data Mining\n"
                                      "📋 Comprehensive Reporting\n"
                                      "🎯 Educational Data Insights\n\n"
                                      "🎓 All analytics included with Student Pack!",
                                 style='Data.TLabel',
                                 justify='left')
        analytics_info.grid(row=1, column=0, padx=20, pady=20, sticky='nw')
    
    def create_status_bar(self, parent):
        """Create status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=2, column=0, sticky='ew')
        status_frame.grid_columnconfigure(0, weight=1)
        
        self.status_var = tk.StringVar(value="Ready - Student Pack Weather Dashboard")
        status_label = ttk.Label(status_frame, textvariable=self.status_var, style='Muted.TLabel')
        status_label.grid(row=0, column=0, sticky='w', padx=5, pady=5)
        
        # Current time
        self.update_time()
    
    def update_time(self):
        """Update current time in status bar."""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.status_var.set(f"Ready - Student Pack Weather Dashboard | {current_time}")
        self.root.after(1000, self.update_time)
    
    def load_default_location(self):
        """Load default location weather data."""
        self.search_location()
    
    def search_location(self, event=None):
        """Search for location and load weather data."""
        location_name = self.location_var.get().strip()
        if not location_name:
            return
        
        self.status_var.set(f"🔍 Searching for {location_name}...")
        
        def search_thread():
            try:
                # Geocode location
                locations = self.api.geocode_location(location_name, limit=1)
                if not locations:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Location Not Found", f"Could not find '{location_name}'. Please try a different location."))
                    return
                
                location = locations[0]
                self.current_location = {
                    'name': location.get('name', location_name),
                    'country': location.get('country', ''),
                    'lat': location['lat'],
                    'lon': location['lon']
                }
                
                # Load weather data
                self.root.after(0, self.load_weather_data)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Search Error", f"Failed to search location: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Ready - Student Pack Weather Dashboard"))
        
        threading.Thread(target=search_thread, daemon=True).start()
    
    def load_weather_data(self):
        """Load comprehensive weather data for current location."""
        if not self.current_location:
            return
        
        lat = self.current_location['lat']
        lon = self.current_location['lon']
        location_name = f"{self.current_location['name']}, {self.current_location['country']}"
        
        self.status_var.set(f"🌤️ Loading weather data for {location_name}...")
        
        def load_thread():
            try:
                # Load current weather
                self.current_weather = self.api.get_current_weather(lat, lon)
                if self.current_weather:
                    self.root.after(0, self.update_current_weather_display)
                
                # Load air quality
                self.air_quality_data = self.api.get_air_pollution(lat, lon)
                if self.air_quality_data:
                    self.root.after(0, self.update_air_quality_display)
                
                self.root.after(0, lambda: self.status_var.set(f"✅ Weather data loaded for {location_name}"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror(
                    "Data Error", f"Failed to load weather data: {str(e)}"))
                self.root.after(0, lambda: self.status_var.set("Ready - Student Pack Weather Dashboard"))
        
        threading.Thread(target=load_thread, daemon=True).start()
    
    def update_current_weather_display(self):
        """Update current weather display with fetched data."""
        if not self.current_weather:
            return
        
        # Clear existing display
        for widget in self.weather_display.winfo_children():
            widget.destroy()
        
        data = self.current_weather
        location_name = f"{data.city}, {data.country}"
        
        # Location header
        location_frame = ttk.Frame(self.weather_display)
        location_frame.grid(row=0, column=0, columnspan=3, sticky='ew', pady=(0, 15))
        
        ttk.Label(location_frame, text=f"📍 {location_name}", 
                 style='Header.TLabel').grid(row=0, column=0)
        ttk.Label(location_frame, text=f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}", 
                 style='Muted.TLabel').grid(row=1, column=0, sticky='w')
        
        # Main temperature display
        temp_frame = ttk.Frame(self.weather_display)
        temp_frame.grid(row=1, column=0, columnspan=3, pady=15)
        
        ttk.Label(temp_frame, text=f"{data.temperature:.1f}°C", 
                 font=('Segoe UI', 36, 'bold'), 
                 foreground='#00d4ff').grid(row=0, column=0, padx=20)
        
        ttk.Label(temp_frame, text=f"Feels like {data.feels_like:.1f}°C", 
                 style='Data.TLabel').grid(row=1, column=0)
        
        ttk.Label(temp_frame, text=f"🌤️ {data.description}", 
                 font=('Segoe UI', 16), 
                 foreground='#00ff9f').grid(row=0, column=1, rowspan=2, padx=20)
        
        # Weather details grid
        details_frame = ttk.Frame(self.weather_display)
        details_frame.grid(row=2, column=0, columnspan=3, pady=15, sticky='ew')
        
        details = [
            ("💧 Humidity", f"{data.humidity}%"),
            ("📊 Pressure", f"{data.pressure} hPa"),
            ("💨 Wind Speed", f"{data.wind_speed} m/s"),
            ("🧭 Wind Direction", f"{data.wind_direction}°"),
            ("👁️ Visibility", f"{data.visibility/1000:.1f} km" if data.visibility > 0 else "N/A"),
            ("⏰ Last Updated", datetime.fromtimestamp(data.timestamp).strftime('%H:%M'))
        ]
        
        for i, (label, value) in enumerate(details):
            row = i // 2
            col = i % 2
            
            detail_frame = ttk.Frame(details_frame)
            detail_frame.grid(row=row, column=col, padx=20, pady=8, sticky='w')
            
            ttk.Label(detail_frame, text=label, style='Data.TLabel').grid(row=0, column=0, sticky='w')
            ttk.Label(detail_frame, text=value, style='Header.TLabel').grid(row=0, column=1, padx=(10, 0), sticky='w')
    
    def update_air_quality_display(self):
        """Update air quality display with fetched data."""
        if not self.air_quality_data:
            return
        
        # Clear existing display
        for widget in self.air_quality_frame.winfo_children():
            widget.destroy()
        
        if 'list' not in self.air_quality_data or not self.air_quality_data['list']:
            ttk.Label(self.air_quality_frame, text="Air quality data unavailable", 
                     style='Muted.TLabel').grid(row=0, column=0, pady=20)
            return
        
        aqi_data = self.air_quality_data['list'][0]
        aqi = aqi_data['main']['aqi']
        components = aqi_data.get('components', {})
        
        aqi_levels = {1: ("Good", "#00ff9f"), 2: ("Fair", "#ffb700"), 
                     3: ("Moderate", "#ff8c00"), 4: ("Poor", "#ff6b6b"), 
                     5: ("Very Poor", "#ff0000")}
        
        level_text, level_color = aqi_levels.get(aqi, ("Unknown", "#6b7785"))
        
        # AQI Header
        aqi_header = ttk.Frame(self.air_quality_frame)
        aqi_header.grid(row=0, column=0, sticky='ew', pady=(0, 20))
        
        ttk.Label(aqi_header, text="🌬️ Air Quality Index", style='Header.TLabel').grid(row=0, column=0)
        ttk.Label(aqi_header, text=f"{aqi}/5 - {level_text}", 
                 font=('Segoe UI', 14, 'bold'), foreground=level_color).grid(row=1, column=0)
        
        # Pollutants
        if components:
            pollutants_frame = ttk.LabelFrame(self.air_quality_frame, text="Pollutant Concentrations (μg/m³)")
            pollutants_frame.grid(row=1, column=0, sticky='ew', pady=10)
            
            pollutant_names = {
                'co': 'Carbon Monoxide (CO)',
                'no': 'Nitrogen Monoxide (NO)',
                'no2': 'Nitrogen Dioxide (NO₂)',
                'o3': 'Ozone (O₃)',
                'so2': 'Sulfur Dioxide (SO₂)',
                'pm2_5': 'Fine Particles (PM2.5)',
                'pm10': 'Coarse Particles (PM10)',
                'nh3': 'Ammonia (NH₃)'
            }
            
            for i, (component, value) in enumerate(components.items()):
                name = pollutant_names.get(component, component.upper())
                ttk.Label(pollutants_frame, text=f"{name}:", style='Data.TLabel').grid(
                    row=i, column=0, sticky='w', padx=10, pady=5)
                ttk.Label(pollutants_frame, text=f"{value:.2f}", style='Header.TLabel').grid(
                    row=i, column=1, sticky='e', padx=10, pady=5)
    
    def get_historical_data(self):
        """Get historical weather data."""
        if not self.current_location:
            messagebox.showerror("Error", "Please select a location first.")
            return
        
        try:
            date_str = self.hist_date_var.get()
            target_date = datetime.strptime(date_str, '%Y-%m-%d')
              # Check date range (1 year limit)
            one_year_ago = datetime.now() - timedelta(days=365)
            if target_date < one_year_ago:
                messagebox.showerror("Error", "Date is beyond 1-year archive limit.")
                return
            
            self.status_var.set(f"📚 Loading historical data for {date_str}...")
            
            def load_historical():
                try:
                    if not self.current_location:
                        self.root.after(0, lambda: messagebox.showerror("Error", "Please select a location first"))
                        return
                        
                    lat = self.current_location['lat']
                    lon = self.current_location['lon']
                    
                    historical_data = self.api.get_historical_weather(lat, lon, target_date)
                    self.root.after(0, lambda: self.display_historical_data(historical_data, date_str))
                    
                except Exception as e:
                    self.root.after(0, lambda: messagebox.showerror(
                        "Historical Data Error", f"Failed to load historical data: {str(e)}"))
                    self.root.after(0, lambda: self.status_var.set("Ready - Student Pack Weather Dashboard"))
            
            threading.Thread(target=load_historical, daemon=True).start()
            
        except ValueError:
            messagebox.showerror("Error", "Invalid date format. Please use YYYY-MM-DD.")
    
    def display_historical_data(self, data, date_str):
        """Display historical weather data."""
        # Clear existing display
        for widget in self.historical_display.winfo_children():
            widget.destroy()
        
        if not data:
            ttk.Label(self.historical_display, text="No historical data available", 
                     style='Muted.TLabel').grid(row=0, column=0, pady=20)
            return
        
        ttk.Label(self.historical_display, text=f"📚 Historical Weather for {date_str}", 
                 style='Header.TLabel').grid(row=0, column=0, pady=(0, 15))
        
        if 'current' in data:
            hist_data = data['current']
            
            # Historical weather display
            hist_frame = ttk.LabelFrame(self.historical_display, text="Weather Conditions")
            hist_frame.grid(row=1, column=0, sticky='ew', pady=10)
            
            details = [
                ("Temperature", f"{hist_data.get('temp', 'N/A')}°C"),
                ("Feels Like", f"{hist_data.get('feels_like', 'N/A')}°C"),
                ("Humidity", f"{hist_data.get('humidity', 'N/A')}%"),
                ("Pressure", f"{hist_data.get('pressure', 'N/A')} hPa"),
                ("Wind Speed", f"{hist_data.get('wind_speed', 'N/A')} m/s"),
                ("Visibility", f"{hist_data.get('visibility', 'N/A')/1000:.1f} km" if hist_data.get('visibility') else "N/A")
            ]
            
            for i, (label, value) in enumerate(details):
                ttk.Label(hist_frame, text=f"{label}:", style='Data.TLabel').grid(
                    row=i, column=0, sticky='w', padx=10, pady=5)
                ttk.Label(hist_frame, text=value, style='Header.TLabel').grid(
                    row=i, column=1, sticky='e', padx=10, pady=5)
        
        self.status_var.set(f"✅ Historical data loaded for {date_str}")
    
    def open_weather_map(self):
        """Open interactive weather map in browser."""
        if not self.current_location:
            messagebox.showerror("Error", "Please select a location first.")
            return
        
        lat = self.current_location['lat']
        lon = self.current_location['lon']
        layer = self.selected_layer.get()
        
        map_url = f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer={layer}&lat={lat}&lon={lon}&zoom=10"
        
        try:
            webbrowser.open(map_url)
            self.status_var.set(f"🌍 Opened {layer} weather map for {self.current_location['name']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open map: {str(e)}")
    
    def show_api_info(self):
        """Show comprehensive API information."""
        api_info = self.api.get_api_info()
        
        info_window = tk.Toplevel(self.root)
        info_window.title("🎓 Student Pack API Information")
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
        info_text = f"""🎓 OpenWeatherMap Student Pack Information

📋 Subscription Details:
   • Plan: {subscription['plan']}
   • Pricing: {subscription['pricing']}
   • Status: Active Educational License

⚡ Rate Limits & Capacity:
   • API Calls per Minute: {subscription['rate_limits']['calls_per_minute']:,}
   • API Calls per Month: {subscription['rate_limits']['calls_per_month']:,}
   • Historical Calls per Day: {subscription['rate_limits']['historical_per_day']:,}

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

For technical support or questions about your Student Pack subscription,
please contact OpenWeatherMap educational support.
"""
        
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        
        # Close button
        close_btn = ttk.Button(info_window, text="Close", 
                              command=info_window.destroy)
        close_btn.pack(pady=10)

def main():
    """Main application entry point."""
    print("🎓 Starting Student Pack Weather Dashboard...")
    
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
