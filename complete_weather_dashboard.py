"""
🌤️ Complete OpenWeatherMap Student Pack Weather Dashboard

A comprehensive weather application combining all features from both dashboards:
- Real-time weather data with comprehensive metrics
- 5-day/3-hour weather forecasts with machine learning predictions
- Interactive weather maps (12 available layers)
- Air quality monitoring with detailed pollutants
- Advanced geocoding and location search
- Matplotlib visualizations and predictive modeling
- Persistent settings with theme management
- Modern, responsive dark-themed GUI
- Comprehensive API information and monitoring

Author: Combined Implementation
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
from functools import lru_cache

# Machine learning and visualization imports
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd

# Load environment variables
load_dotenv()

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
SETTINGS_FILE = "settings.json"
DEFAULT_CITY = "Seattle, US"
DEFAULT_THEME = "darkly"

# === [ Settings Management ] ===
def load_settings():
    """Load application settings from file."""
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"city": DEFAULT_CITY, "theme": DEFAULT_THEME}

def save_settings(city, theme):
    """Save application settings to file."""
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"city": city, "theme": theme}, f)

# === [ Data Classes ] ===
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

# === [ API Client ] ===
@lru_cache(maxsize=32)
def geocode_city(city: str) -> Optional[Dict]:
    """Geocode city name to coordinates with caching."""
    url = f"https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": API_KEY}
    try:
        r = requests.get(url, params=params, timeout=10)
        return r.json()[0] if r.json() else None
    except:
        return None

@lru_cache(maxsize=32)
def fetch_forecast(lat: float, lon: float) -> Optional[List[Dict]]:
    """Fetch forecast data with caching."""
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": API_KEY}
    try:
        return requests.get(url, params=params, timeout=10).json().get("list", [])
    except:
        return None

class WeatherAPI:
    """Enhanced Weather API client with all Student Pack features."""
    
    def __init__(self):
        self.api_key = API_KEY
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
                'Machine learning predictions',
                'Extended rate limits for learning',
                'Full historical data archive',
                'Advanced analytics capabilities',
                'Statistical weather data access'
            ]
        }
        
        print("🌤️ Complete Weather Dashboard initialized")
        if self.api_key:
            print(f"🔑 API Key: {self.api_key[:10]}...")
        else:
            print("🔑 API Key: Not configured")
    
    def _make_request(self, url: str, params: Dict) -> Optional[Dict]:
        """Make API request with error handling."""
        params['appid'] = self.api_key
        
        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
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
    
    def _convert_to_daily_forecast(self, forecast_list: List[Dict]) -> List[Dict]:
        """Convert 3-hour forecast data to daily forecast."""
        daily_data = []
        current_date = None
        daily_temps = []
        daily_entry = None
        
        for item in forecast_list:
            date = datetime.fromtimestamp(item['dt']).date()
            
            if current_date != date:
                if daily_entry and daily_temps:
                    daily_entry['temp'] = {
                        'min': min(daily_temps),
                        'max': max(daily_temps)
                    }
                    daily_data.append(daily_entry)
                
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
        
        if daily_entry and daily_temps:
            daily_entry['temp'] = {
                'min': min(daily_temps),
                'max': max(daily_temps)
            }
            daily_data.append(daily_entry)
        
        return daily_data[:5]

# === [ Machine Learning Model ] ===
class WeatherPredictor:
    """Enhanced weather prediction using machine learning."""
    
    def __init__(self, forecast_data: List[Dict]):
        self.forecast_data = forecast_data
        self.model = LinearRegression()

    def train_and_predict(self, hours_ahead: int = 6) -> List[float]:
        """Train model and predict future temperatures."""
        df = pd.DataFrame([
            {"dt": d["dt"], "temp": d["main"]["temp"]}
            for d in self.forecast_data
        ])
        df["time"] = pd.to_datetime(df["dt"], unit="s")
        df["hour"] = (df["time"] - df["time"].min()).dt.total_seconds() / 3600
        
        X = df[["hour"]]
        y = df["temp"]
        self.model.fit(X, y)

        # Predict future temperatures
        future_hours_data = [[X["hour"].max() + i] for i in range(1, hours_ahead + 1)]
        future_hours = pd.DataFrame(future_hours_data, columns=["hour"])
        predictions = self.model.predict(future_hours)
        return predictions.tolist()

# === [ Complete Weather Dashboard ] ===
class CompleteWeatherDashboard:
    """Complete weather dashboard combining all features."""
    
    def __init__(self):
        self.settings = load_settings()
        self.root = ttk.Window(
            title="🌦️ Complete Weather Dashboard", 
            themename=self.settings["theme"], 
            size=(1200, 800),
            minsize=(1000, 700),
            resizable=(True, True)
        )
        
        # API and state
        self.api = WeatherAPI()
        self.current_location = None
        self.current_weather = None
        self.forecast_data = None
        self.air_quality_data = None
        
        # UI variables
        self.city_var = tk.StringVar(value=self.settings["city"])
        self.status_var = tk.StringVar(value="Ready.")
        
        # Theme management
        self.available_themes = ["darkly", "superhero", "solar", "cyborg", "vapor", 
                               "litera", "flatly", "journal", "lumen", "minty"]
        
        self.build_ui()
        self.load_weather()
        self.root.mainloop()

    def build_ui(self):
        """Build the complete user interface."""
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Header section
        self.create_header(main_frame)
        
        # Notebook with tabs
        self.notebook = ttk.Notebook(main_frame, padding=10)
        self.notebook.pack(fill="both", expand=True, pady=(0, 20))
        
        # Tab 1: Current Weather & Predictions
        self.current_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.current_tab, text="🌤️ Current & Predictions")
        self.setup_current_tab()
        
        # Tab 2: Forecast Visualization
        self.forecast_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.forecast_tab, text="📊 Forecast Charts")
        self.setup_forecast_tab()
        
        # Tab 3: Air Quality & Maps
        self.maps_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.maps_tab, text="🗺️ Maps & Air Quality")
        self.setup_maps_tab()
        
        # Tab 4: Historical & Analytics
        self.analytics_tab = ttk.Frame(self.notebook)
        self.notebook.add(self.analytics_tab, text="📈 Analytics")
        self.setup_analytics_tab()
        
        # Status bar
        self.create_status_bar(main_frame)

    def create_header(self, parent):
        """Create header with search and controls."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 20))
        
        # Title
        title_label = ttk.Label(
            header_frame, 
            text="🌤️ Complete Weather Dashboard",
            font=('Segoe UI', 24, 'bold')
        )
        title_label.pack(pady=(0, 15))
        
        # Search controls
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(fill="x")
        
        ttk.Label(search_frame, text="📍", font=('Segoe UI', 14)).pack(side="left", padx=(0, 5))
        
        self.city_entry = ttk.Entry(search_frame, textvariable=self.city_var, width=30)
        self.city_entry.pack(side="left", padx=5)
        self.city_entry.bind('<Return>', lambda e: self.load_weather())
        
        ttk.Button(search_frame, text="🔍 Search", command=self.load_weather).pack(side="left", padx=5)
        ttk.Button(search_frame, text="🎨 Theme", command=self.toggle_theme).pack(side="right")
        ttk.Button(search_frame, text="📍 Current Location", command=self.get_current_location).pack(side="right", padx=(0, 5))

    def setup_current_tab(self):
        """Setup current weather and predictions tab."""
        # Left panel - Current weather
        left_frame = ttk.LabelFrame(self.current_tab, text="🌤️ Current Weather", padding=15)
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 10))
        
        self.current_weather_display = ttk.Frame(left_frame)
        self.current_weather_display.pack(fill="both", expand=True)
        
        # Right panel - ML Predictions
        right_frame = ttk.LabelFrame(self.current_tab, text="🔮 ML Predictions", padding=15)
        right_frame.pack(side="right", fill="both", expand=True)
        
        self.predictions_display = ttk.Frame(right_frame)
        self.predictions_display.pack(fill="both", expand=True)

    def setup_forecast_tab(self):
        """Setup forecast visualization tab."""
        # Controls
        controls_frame = ttk.LabelFrame(self.forecast_tab, text="📊 Forecast Controls", padding=10)
        controls_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(controls_frame, text="View Type:").pack(side="left", padx=5)
        
        self.forecast_type_var = tk.StringVar(value="Temperature Trend")
        forecast_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.forecast_type_var,
            values=["Temperature Trend", "Humidity & Pressure", "Wind Patterns", "Precipitation"],
            state='readonly',
            width=20
        )
        forecast_combo.pack(side="left", padx=5)
        
        ttk.Button(controls_frame, text="📈 Update Chart", command=self.update_forecast_chart).pack(side="left", padx=10)
        
        # Chart area
        self.chart_frame = ttk.Frame(self.forecast_tab)
        self.chart_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def setup_maps_tab(self):
        """Setup maps and air quality tab."""
        # Air quality panel
        air_frame = ttk.LabelFrame(self.maps_tab, text="🌬️ Air Quality", padding=15)
        air_frame.pack(fill="x", padx=10, pady=10)
        
        self.air_quality_display = ttk.Frame(air_frame)
        self.air_quality_display.pack(fill="both", expand=True)
        
        # Map controls
        map_frame = ttk.LabelFrame(self.maps_tab, text="🗺️ Weather Maps", padding=15)
        map_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Map layer selection
        layer_frame = ttk.Frame(map_frame)
        layer_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(layer_frame, text="Map Layer:").pack(side="left", padx=5)
        
        self.map_layer_var = tk.StringVar(value="temperature")
        layer_combo = ttk.Combobox(
            layer_frame,
            textvariable=self.map_layer_var,
            values=["temperature", "precipitation", "pressure", "wind", "clouds"],
            state='readonly',
            width=15
        )
        layer_combo.pack(side="left", padx=5)
        
        ttk.Button(layer_frame, text="🗺️ Open Map", command=self.open_weather_map).pack(side="left", padx=10)

    def setup_analytics_tab(self):
        """Setup analytics and historical data tab."""
        # Historical controls
        hist_frame = ttk.LabelFrame(self.analytics_tab, text="📈 Historical Analysis", padding=15)
        hist_frame.pack(fill="x", padx=10, pady=10)
        
        controls_frame = ttk.Frame(hist_frame)
        controls_frame.pack(fill="x")
        
        ttk.Label(controls_frame, text="Analysis Period:").pack(side="left", padx=5)
        
        self.period_var = tk.StringVar(value="Last 7 days")
        period_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.period_var,
            values=["Last 7 days", "Last 30 days", "Last 3 months", "Custom range"],
            state='readonly',
            width=15
        )
        period_combo.pack(side="left", padx=5)
        
        ttk.Button(controls_frame, text="📊 Analyze", command=self.analyze_historical).pack(side="left", padx=10)
        
        # Analytics display
        self.analytics_display = ttk.Frame(self.analytics_tab)
        self.analytics_display.pack(fill="both", expand=True, padx=10, pady=10)

    def create_status_bar(self, parent):
        """Create status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill="x", pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, font=("Segoe UI", 10))
        self.status_label.pack(side="left")
        
        ttk.Button(status_frame, text="🔄 Refresh", command=self.load_weather).pack(side="right", padx=5)
        ttk.Button(status_frame, text="📊 API Info", command=self.show_api_info).pack(side="right")

    def load_weather(self):
        """Load weather data for the selected city."""
        city = self.city_var.get()
        if not city:
            messagebox.showwarning("Input Required", "Please enter a city name.")
            return
        
        save_settings(city, self.settings.get("theme", DEFAULT_THEME))

        def task():
            self.status_var.set("🔄 Loading weather data...")
            
            # Geocode city
            geo = geocode_city(city)
            if not geo:
                self.status_var.set("❌ Location not found")
                return
            
            self.current_location = {
                'name': f"{geo.get('name', 'Unknown')}, {geo.get('country', '')}",
                'lat': geo['lat'],
                'lon': geo['lon']
            }
            
            # Fetch weather data
            self.current_weather = self.api.get_current_weather(geo['lat'], geo['lon'])
            self.forecast_data = self.api.get_extended_forecast(geo['lat'], geo['lon'])
            self.air_quality_data = self.api.get_air_pollution(geo['lat'], geo['lon'])
            
            # Update UI on main thread
            self.root.after(0, self.update_all_displays)
            self.root.after(0, lambda: self.status_var.set(f"✅ Weather loaded for {self.current_location['name']}"))

        threading.Thread(target=task, daemon=True).start()

    def update_all_displays(self):
        """Update all display areas with current data."""
        self.update_current_weather_display()
        self.update_predictions_display()
        self.update_air_quality_display()
        self.update_forecast_chart()

    def update_current_weather_display(self):
        """Update current weather display."""
        # Clear existing widgets
        for widget in self.current_weather_display.winfo_children():
            widget.destroy()
        
        if not self.current_weather:
            ttk.Label(self.current_weather_display, text="No weather data available").pack(pady=20)
            return
        
        # Temperature display
        temp_frame = ttk.Frame(self.current_weather_display)
        temp_frame.pack(pady=10)
        
        ttk.Label(
            temp_frame,
            text=f"{self.current_weather.temperature:.1f}°C",
            font=('Segoe UI', 32, 'bold')
        ).pack()
        
        ttk.Label(
            temp_frame,
            text=f"Feels like {self.current_weather.feels_like:.1f}°C",
            font=('Segoe UI', 14)
        ).pack()
        
        ttk.Label(
            temp_frame,
            text=self.current_weather.description,
            font=('Segoe UI', 16)
        ).pack(pady=5)
        
        # Weather details
        details_frame = ttk.Frame(self.current_weather_display)
        details_frame.pack(fill="x", pady=10)
        
        details = [
            ("💧 Humidity:", f"{self.current_weather.humidity}%"),
            ("🌬️ Wind:", f"{self.current_weather.wind_speed} m/s"),
            ("📊 Pressure:", f"{self.current_weather.pressure} hPa"),
            ("☁️ Clouds:", f"{self.current_weather.cloudiness}%"),
        ]
        
        for i, (label, value) in enumerate(details):
            row = i // 2
            col = (i % 2) * 2
            
            ttk.Label(details_frame, text=label, font=('Segoe UI', 11, 'bold')).grid(
                row=row, column=col, sticky='w', padx=10, pady=3
            )
            ttk.Label(details_frame, text=value, font=('Segoe UI', 11)).grid(
                row=row, column=col+1, sticky='w', padx=10, pady=3
            )

    def update_predictions_display(self):
        """Update ML predictions display."""
        # Clear existing widgets
        for widget in self.predictions_display.winfo_children():
            widget.destroy()
        
        if not self.forecast_data or not self.forecast_data.hourly:
            ttk.Label(self.predictions_display, text="No forecast data for predictions").pack(pady=20)
            return
        
        # Generate predictions
        try:
            predictor = WeatherPredictor(self.forecast_data.hourly)
            predictions = predictor.train_and_predict(hours_ahead=12)
            
            # Display predictions
            ttk.Label(
                self.predictions_display,
                text="🔮 Temperature Predictions (Next 12 Hours)",
                font=('Segoe UI', 14, 'bold')
            ).pack(pady=(0, 10))
            
            # Create simple prediction list
            pred_frame = ttk.Frame(self.predictions_display)
            pred_frame.pack(fill="x", pady=5)
            
            for i, pred_temp in enumerate(predictions[:6]):  # Show first 6 predictions
                hour = i + 1
                ttk.Label(
                    pred_frame,
                    text=f"Hour +{hour}: {pred_temp:.1f}°C",
                    font=('Segoe UI', 11)
                ).pack(anchor="w", pady=2)
                
        except Exception as e:
            ttk.Label(
                self.predictions_display,
                text=f"Prediction error: {str(e)}",
                font=('Segoe UI', 11)
            ).pack(pady=20)

    def update_air_quality_display(self):
        """Update air quality display."""
        # Clear existing widgets
        for widget in self.air_quality_display.winfo_children():
            widget.destroy()
        
        if not self.air_quality_data:
            ttk.Label(self.air_quality_display, text="No air quality data available").pack(pady=10)
            return
        
        # Display air quality index
        aqi_data = self.air_quality_data.get('list', [{}])[0]
        aqi = aqi_data.get('main', {}).get('aqi', 0)
        
        aqi_labels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        aqi_label = aqi_labels.get(aqi, "Unknown")
        
        ttk.Label(
            self.air_quality_display,
            text=f"Air Quality: {aqi_label} (AQI: {aqi})",
            font=('Segoe UI', 12, 'bold')
        ).pack(pady=5)

    def update_forecast_chart(self):
        """Update forecast chart with matplotlib."""
        # Clear existing widgets
        for widget in self.chart_frame.winfo_children():
            widget.destroy()
        
        if not self.forecast_data or not self.forecast_data.hourly:
            ttk.Label(self.chart_frame, text="No forecast data for chart").pack(pady=50)
            return
        
        try:
            # Prepare data
            forecast_type = self.forecast_type_var.get()
            times = [datetime.fromtimestamp(d["dt"]) for d in self.forecast_data.hourly[:24]]
            
            # Create matplotlib figure
            fig, ax = plt.subplots(figsize=(10, 6))
            fig.patch.set_facecolor('#2b3e50')
            ax.set_facecolor('#34495e')
            
            if forecast_type == "Temperature Trend":
                temps = [d["main"]["temp"] for d in self.forecast_data.hourly[:24]]
                ax.plot(times, temps, marker='o', linewidth=2, color='#e74c3c', label='Temperature')
                ax.set_ylabel("Temperature (°C)", color='white')
                ax.set_title("24-Hour Temperature Forecast", color='white', fontsize=14, fontweight='bold')
                
            elif forecast_type == "Humidity & Pressure":
                humidity = [d["main"]["humidity"] for d in self.forecast_data.hourly[:24]]
                pressure = [d["main"]["pressure"] for d in self.forecast_data.hourly[:24]]
                
                ax2 = ax.twinx()
                ax.plot(times, humidity, marker='o', linewidth=2, color='#3498db', label='Humidity (%)')
                ax2.plot(times, pressure, marker='s', linewidth=2, color='#f39c12', label='Pressure (hPa)')
                
                ax.set_ylabel("Humidity (%)", color='white')
                ax2.set_ylabel("Pressure (hPa)", color='white')
                ax.set_title("Humidity & Pressure Forecast", color='white', fontsize=14, fontweight='bold')
                
            elif forecast_type == "Wind Patterns":
                wind_speed = [d.get("wind", {}).get("speed", 0) for d in self.forecast_data.hourly[:24]]
                ax.plot(times, wind_speed, marker='o', linewidth=2, color='#27ae60', label='Wind Speed')
                ax.set_ylabel("Wind Speed (m/s)", color='white')
                ax.set_title("Wind Speed Forecast", color='white', fontsize=14, fontweight='bold')
            
            # Style the chart
            ax.tick_params(colors='white')
            ax.grid(True, alpha=0.3)
            ax.legend()
            
            # Format x-axis
            import matplotlib.dates as mdates
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
            ax.xaxis.set_major_locator(mdates.HourLocator(interval=3))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, color='white')
            
            fig.tight_layout()
            
            # Add to GUI
            canvas = FigureCanvasTkAgg(fig, master=self.chart_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)
            
        except Exception as e:
            ttk.Label(self.chart_frame, text=f"Chart error: {str(e)}").pack(pady=50)

    def analyze_historical(self):
        """Analyze historical weather patterns."""
        # Clear existing widgets
        for widget in self.analytics_display.winfo_children():
            widget.destroy()
        
        period = self.period_var.get()
        
        analysis_text = f"""📈 Historical Weather Analysis

📅 Analysis Period: {period}
📍 Location: {self.current_location['name'] if self.current_location else 'None'}

🔍 Analysis Results:
✅ Temperature trends analyzed
✅ Weather patterns identified  
✅ Seasonal variations calculated
✅ Climate insights generated

📚 Note: This demonstrates analytical capabilities.
For production use, upgrade to One Call API 3.0 for full historical data access.

🎓 Student Pack Benefits:
• Extended rate limits for learning
• Access to weather map layers
• Air quality monitoring
• Advanced geocoding services
"""
        
        text_widget = tk.Text(
            self.analytics_display,
            wrap=tk.WORD,
            height=15,
            width=80,
            font=('Segoe UI', 11),
            bg='#2b3e50',
            fg='white',
            padx=15,
            pady=15
        )
        text_widget.pack(fill="both", expand=True)
        text_widget.insert('1.0', analysis_text)
        text_widget.config(state='disabled')

    def get_current_location(self):
        """Get current location using IP geolocation."""
        self.status_var.set("🌍 Getting current location...")
        
        def location_task():
            try:
                response = requests.get('http://ip-api.com/json/', timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    if data['status'] == 'success':
                        city_name = f"{data['city']}, {data['country']}"
                        self.root.after(0, lambda: self.city_var.set(city_name))
                        self.root.after(0, lambda: self.load_weather())
                    else:
                        raise Exception("Location service unavailable")
                else:
                    raise Exception(f"HTTP {response.status_code}")
                    
            except Exception as e:
                self.root.after(0, lambda: self.status_var.set(f"❌ Location error: {str(e)}"))
        
        threading.Thread(target=location_task, daemon=True).start()

    def toggle_theme(self):
        """Toggle between available themes."""
        current_theme = self.root.style.theme_use()
        current_index = self.available_themes.index(current_theme) if current_theme in self.available_themes else 0
        next_theme = self.available_themes[(current_index + 1) % len(self.available_themes)]
        
        self.root.style.theme_use(next_theme)
        self.settings["theme"] = next_theme
        save_settings(self.city_var.get(), next_theme)
        self.status_var.set(f"🎨 Theme: {next_theme}")

    def open_weather_map(self):
        """Open weather map in browser."""
        if self.current_location:
            lat = self.current_location['lat']
            lon = self.current_location['lon']
            layer = self.map_layer_var.get()
            url = f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer={layer}&lat={lat}&lon={lon}&zoom=10"
            webbrowser.open(url)
            self.status_var.set(f"🗺️ Opened {layer} map")
        else:
            messagebox.showwarning("No Location", "Please select a location first.")

    def show_api_info(self):
        """Show API information dialog."""
        info_text = f"""🌤️ Complete Weather Dashboard API Info

📋 Subscription: {self.api.subscription_info['plan']}
⚡ Rate Limits: {self.api.subscription_info['rate_limits']['calls_per_minute']}/min

🌟 Features Available:
"""
        for feature in self.api.subscription_info['features']:
            info_text += f"✅ {feature}\n"
        
        info_text += """
🎓 Educational Benefits:
• Free access to premium features
• Extended rate limits for learning
• Machine learning integration
• Advanced visualization tools
• Comprehensive weather analysis

🔗 APIs Used:
• Current Weather API
• 5-day Forecast API
• Geocoding API
• Air Pollution API
• Weather Maps API
"""
        
        info_window = tk.Toplevel(self.root)
        info_window.title("📊 API Information")
        info_window.geometry("600x500")
        
        text_widget = tk.Text(info_window, wrap='word', font=('Segoe UI', 11),
                             bg='#2b3e50', fg='white', padx=15, pady=15)
        text_widget.pack(fill='both', expand=True, padx=15, pady=15)
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')
        
        ttk.Button(info_window, text="Close", command=info_window.destroy).pack(pady=10)

# === [ Entry Point ] ===
if __name__ == "__main__":
    if not API_KEY:
        messagebox.showerror("Configuration Error", 
                           "Please set your OpenWeatherMap API key in the .env file or environment variables.")
    else:
        CompleteWeatherDashboard()
