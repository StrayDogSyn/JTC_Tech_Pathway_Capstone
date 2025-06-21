"""
Main weather dashboard application.

This is the main entry point that coordinates all the modules and provides
a clean separation of concerns.
"""

import sys
import os
import tkinter as tk
from tkinter import messagebox
import ttkbootstrap as ttk
from typing import Optional

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.core.weather_core import WeatherDashboardCore
from src.config.app_config import config, APP_CONFIG
from src.models.weather_models import WeatherData, ForecastData, AirQualityData


class WeatherDashboardApp:
    """Main weather dashboard application."""
    
    def __init__(self):
        """Initialize the weather dashboard application."""
        # Initialize core business logic
        self.core = WeatherDashboardCore()
        
        # Set up callbacks
        self.core.set_status_callback(self._update_status)
        self.core.set_data_update_callback(self._update_displays)
        
        # Initialize GUI
        self._setup_gui()
        
        # Load initial city
        self._load_initial_data()
    
    def _setup_gui(self) -> None:
        """Set up the graphical user interface."""
        # Create main window
        self.root = ttk.Window(
            title=APP_CONFIG["title"],
            themename=config.current_theme,
            size=APP_CONFIG["default_size"],
            minsize=APP_CONFIG["min_size"]
        )
        
        # Status variable
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Create UI components
        self._create_header()
        self._create_main_content()
        self._create_status_bar()
    
    def _create_header(self) -> None:
        """Create the header with search and controls."""
        header_frame = ttk.Frame(self.root)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="🌦️ Complete Weather Dashboard",
            font=('Segoe UI', 18, 'bold')
        )
        title_label.pack(side="left")
        
        # Controls
        controls_frame = ttk.Frame(header_frame)
        controls_frame.pack(side="right")
        
        # City search
        ttk.Label(controls_frame, text="City:").pack(side="left", padx=(0, 5))
        
        self.city_entry = ttk.Entry(controls_frame, width=20)
        self.city_entry.pack(side="left", padx=(0, 5))
        self.city_entry.bind('<Return>', self._on_search)
        
        search_btn = ttk.Button(
            controls_frame,
            text="🔍 Search",
            command=self._on_search
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        # Theme selector
        ttk.Label(controls_frame, text="Theme:").pack(side="left", padx=(0, 5))
        
        self.theme_var = tk.StringVar(value=config.current_theme)
        theme_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.theme_var,
            values=['darkly', 'flatly', 'litera', 'minty', 'lumen', 'sandstone'],
            width=10,
            state="readonly"
        )
        theme_combo.pack(side="left", padx=(0, 5))
        theme_combo.bind('<<ComboboxSelected>>', self._on_theme_change)
    
    def _create_main_content(self) -> None:
        """Create the main content area."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Left panel
        left_panel = ttk.Frame(main_container)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Current weather frame
        self.weather_frame = ttk.LabelFrame(left_panel, text="🌤️ Current Weather", padding=10)
        self.weather_frame.pack(fill="x", pady=(0, 5))
        
        # Predictions frame
        self.predictions_frame = ttk.LabelFrame(left_panel, text="🤖 AI Predictions", padding=10)
        self.predictions_frame.pack(fill="both", expand=True)
        
        # Right panel
        right_panel = ttk.Frame(main_container)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Air quality frame
        self.air_quality_frame = ttk.LabelFrame(right_panel, text="🌬️ Air Quality", padding=10)
        self.air_quality_frame.pack(fill="x", pady=(0, 5))
        
        # Forecast frame
        self.forecast_frame = ttk.LabelFrame(right_panel, text="📊 Forecast", padding=10)
        self.forecast_frame.pack(fill="both", expand=True)
        
        # Initial content
        self._show_initial_content()
    
    def _create_status_bar(self) -> None:
        """Create the status bar."""
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 9)
        )
        status_label.pack(side="left")
        
        # API info button
        api_btn = ttk.Button(
            status_frame,
            text="ℹ️ API Info",
            command=self._show_api_info
        )
        api_btn.pack(side="right")
    
    def _show_initial_content(self) -> None:
        """Show initial content in all frames."""
        # Weather frame
        ttk.Label(self.weather_frame, 
                 text="Enter a city name and click Search to get weather data", 
                 font=('Segoe UI', 12)).pack(pady=20)
        
        # Predictions frame
        ttk.Label(self.predictions_frame, 
                 text="AI predictions will appear here after loading weather data", 
                 font=('Segoe UI', 12)).pack(pady=20)
        
        # Air quality frame
        ttk.Label(self.air_quality_frame, 
                 text="Air quality data will appear here", 
                 font=('Segoe UI', 12)).pack(pady=20)
        
        # Forecast frame
        ttk.Label(self.forecast_frame, 
                 text="Weather forecast charts will appear here", 
                 font=('Segoe UI', 12)).pack(pady=20)
    
    def _load_initial_data(self) -> None:
        """Load initial weather data for the default city."""
        self.city_entry.insert(0, config.current_city)
        if config.current_city and config.current_city != "":
            # Load data for the saved city
            self.core.load_weather_data(config.current_city)
    
    def _on_search(self, event=None) -> None:
        """Handle search button click or Enter key."""
        city = self.city_entry.get().strip()
        if city:
            self.core.load_weather_data(city)
    
    def _on_theme_change(self, event=None) -> None:
        """Handle theme change."""
        theme = self.theme_var.get()
        if theme:
            config.save_settings(theme=theme)
            # Note: In a real app, theme change might require restart
            messagebox.showinfo("Theme Changed", 
                              f"Theme changed to {theme}. Restart the app to see full effect.")
    
    def _update_status(self, message: str) -> None:
        """Update status bar message."""
        self.status_var.set(message)
    
    def _update_displays(self) -> None:
        """Update all display areas with current data."""
        self._update_weather_display()
        self._update_predictions_display()
        self._update_air_quality_display()
        self._update_forecast_display()
    
    def _update_weather_display(self) -> None:
        """Update current weather display."""
        # Clear existing widgets
        for widget in self.weather_frame.winfo_children():
            widget.destroy()
        
        if not self.core.current_weather:
            ttk.Label(self.weather_frame, text="No weather data available").pack(pady=20)
            return
        
        weather = self.core.current_weather
        
        # Temperature display
        temp_frame = ttk.Frame(self.weather_frame)
        temp_frame.pack(pady=10)
        
        ttk.Label(
            temp_frame,
            text=f"{weather.temperature:.1f}°C",
            font=('Segoe UI', 32, 'bold')
        ).pack()
        
        ttk.Label(
            temp_frame,
            text=f"Feels like {weather.feels_like:.1f}°C",
            font=('Segoe UI', 14)
        ).pack()
        
        ttk.Label(
            temp_frame,
            text=weather.description,
            font=('Segoe UI', 16)
        ).pack(pady=5)
        
        # Weather details
        details_frame = ttk.Frame(self.weather_frame)
        details_frame.pack(fill="x", pady=10)
        
        details = [
            ("💧 Humidity:", f"{weather.humidity}%"),
            ("🌬️ Wind:", f"{weather.wind_speed} m/s"),
            ("📊 Pressure:", f"{weather.pressure} hPa"),
            ("☁️ Clouds:", f"{weather.cloudiness}%"),
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
    
    def _update_predictions_display(self) -> None:
        """Update ML predictions display."""
        # Clear existing widgets
        for widget in self.predictions_frame.winfo_children():
            widget.destroy()
        
        if not self.core.forecast_data or not self.core.forecast_data.hourly:
            ttk.Label(self.predictions_frame, text="No forecast data for predictions").pack(pady=20)
            return
        
        # Simple prediction display (would use ML module in full implementation)
        ttk.Label(
            self.predictions_frame,
            text="🤖 Basic Trend Analysis",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Show basic trend from forecast data
        if len(self.core.forecast_data.hourly) >= 2:
            first_temp = self.core.forecast_data.hourly[0]['main']['temp']
            later_temp = self.core.forecast_data.hourly[min(5, len(self.core.forecast_data.hourly)-1)]['main']['temp']
            trend = "rising" if later_temp > first_temp else "falling"
            
            ttk.Label(
                self.predictions_frame,
                text=f"Temperature trend: {trend}",
                font=('Segoe UI', 12)
            ).pack()
    
    def _update_air_quality_display(self) -> None:
        """Update air quality display."""
        # Clear existing widgets
        for widget in self.air_quality_frame.winfo_children():
            widget.destroy()
        
        if not self.core.air_quality_data:
            ttk.Label(self.air_quality_frame, text="No air quality data available").pack(pady=20)
            return
        
        aqi = self.core.air_quality_data.aqi
        aqi_levels = {
            1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"
        }
        aqi_text = aqi_levels.get(aqi, "Unknown")
        
        ttk.Label(
            self.air_quality_frame,
            text=f"AQI: {aqi} ({aqi_text})",
            font=('Segoe UI', 16, 'bold')
        ).pack(pady=10)
        
        # Show key pollutants
        pollutants_frame = ttk.Frame(self.air_quality_frame)
        pollutants_frame.pack(fill="x")
        
        ttk.Label(pollutants_frame, text=f"PM2.5: {self.core.air_quality_data.pm2_5:.1f} μg/m³").pack(anchor="w")
        ttk.Label(pollutants_frame, text=f"PM10: {self.core.air_quality_data.pm10:.1f} μg/m³").pack(anchor="w")
        ttk.Label(pollutants_frame, text=f"NO₂: {self.core.air_quality_data.no2:.1f} μg/m³").pack(anchor="w")
    
    def _update_forecast_display(self) -> None:
        """Update forecast display."""
        # Clear existing widgets
        for widget in self.forecast_frame.winfo_children():
            widget.destroy()
        
        if not self.core.forecast_data or not self.core.forecast_data.daily:
            ttk.Label(self.forecast_frame, text="No forecast data available").pack(pady=20)
            return
        
        ttk.Label(
            self.forecast_frame,
            text="📊 5-Day Forecast",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Show daily forecast
        for i, day in enumerate(self.core.forecast_data.daily[:5]):
            day_frame = ttk.Frame(self.forecast_frame)
            day_frame.pack(fill="x", pady=2)
            
            # Format date
            from datetime import datetime
            date_str = datetime.fromtimestamp(day['dt']).strftime("%a, %b %d")
            
            ttk.Label(day_frame, text=date_str, width=12).pack(side="left")
            ttk.Label(day_frame, text=day['weather'][0]['description'].title(), width=15).pack(side="left")
            
            if 'temp' in day:
                temp_text = f"{day['temp']['max']:.0f}°/{day['temp']['min']:.0f}°"
                ttk.Label(day_frame, text=temp_text).pack(side="left")
    
    def _show_api_info(self) -> None:
        """Show API information dialog."""
        info_text = """
OpenWeatherMap Student Pack Features:

• Current weather data for any location
• 5-day/3-hour weather forecasts  
• Air quality monitoring
• Advanced geocoding
• Weather maps (12+ layers)
• Machine learning predictions
• Extended rate limits for learning

Rate Limits:
• 60 calls per minute
• 1,000,000 calls per month
• Unlimited historical data access

Perfect for learning and development!
        """
        
        messagebox.showinfo("OpenWeatherMap API Information", info_text.strip())
    
    def run(self) -> None:
        """Start the application."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nApplication interrupted by user")
        except Exception as e:
            print(f"Application error: {e}")
            messagebox.showerror("Application Error", f"An error occurred: {e}")


def main():
    """Main entry point."""
    try:
        app = WeatherDashboardApp()
        app.run()
    except Exception as e:
        print(f"Failed to start application: {e}")
        messagebox.showerror("Startup Error", f"Failed to start application: {e}")


if __name__ == "__main__":
    main()
