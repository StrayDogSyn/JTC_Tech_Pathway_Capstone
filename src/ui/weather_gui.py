"""
UI components and widgets for the weather dashboard.

This module contains reusable UI components and the main GUI layout.
"""

import tkinter as tk
from tkinter import messagebox, Toplevel
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, SUCCESS, INFO, WARNING, DANGER
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from typing import Optional, Callable, Dict, Any, List
import threading
import webbrowser

from ..models.weather_models import WeatherData, ForecastData, AirQualityData
from ..utils.ml_predictions import WeatherPredictor


class WeatherDisplayWidget:
    """Widget for displaying current weather information."""
    
    def __init__(self, parent):
        """Initialize the weather display widget."""
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        
    def update_display(self, weather_data: Optional[WeatherData]) -> None:
        """Update the weather display with new data."""
        # Clear existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        if not weather_data:
            ttk.Label(self.frame, text="No weather data available", 
                     font=('Segoe UI', 14)).pack(pady=20)
            return
        
        # Temperature display
        temp_frame = ttk.Frame(self.frame)
        temp_frame.pack(pady=10)
        
        ttk.Label(
            temp_frame,
            text=f"{weather_data.temperature:.1f}°C",
            font=('Segoe UI', 32, 'bold')
        ).pack()
        
        ttk.Label(
            temp_frame,
            text=f"Feels like {weather_data.feels_like:.1f}°C",
            font=('Segoe UI', 14)
        ).pack()
        
        ttk.Label(
            temp_frame,
            text=weather_data.description,
            font=('Segoe UI', 16)
        ).pack(pady=5)
        
        # Weather details grid
        details_frame = ttk.Frame(self.frame)
        details_frame.pack(fill="x", pady=10)
        
        details = [
            ("💧 Humidity:", f"{weather_data.humidity}%"),
            ("🌬️ Wind:", f"{weather_data.wind_speed} m/s"),
            ("📊 Pressure:", f"{weather_data.pressure} hPa"),
            ("☁️ Clouds:", f"{weather_data.cloudiness}%"),
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


class PredictionsDisplayWidget:
    """Widget for displaying ML predictions."""
    
    def __init__(self, parent):
        """Initialize the predictions display widget."""
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.predictor = WeatherPredictor()
        
    def update_display(self, forecast_data: Optional[ForecastData]) -> None:
        """Update predictions display with new forecast data."""
        # Clear existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        if not forecast_data or not forecast_data.hourly:
            ttk.Label(self.frame, text="No forecast data for predictions", 
                     font=('Segoe UI', 14)).pack(pady=20)
            return
        
        # Train the ML model
        if self.predictor.train_models(forecast_data.hourly):
            # Get predictions
            predictions = self.predictor.predict_weather_metrics(hours_ahead=6)
            trends = self.predictor.get_trend_analysis(forecast_data.hourly)
            
            # Display predictions
            pred_frame = ttk.LabelFrame(self.frame, text="🤖 ML Predictions (Next 6 Hours)", padding=10)
            pred_frame.pack(fill="x", pady=5)
            
            if predictions:
                for i, temp in enumerate(predictions.get('temperature', [])[:3]):
                    hour_label = f"Hour {i+1}:"
                    temp_text = f"{temp:.1f}°C"
                    
                    row_frame = ttk.Frame(pred_frame)
                    row_frame.pack(fill="x", pady=2)
                    
                    ttk.Label(row_frame, text=hour_label, width=10).pack(side="left")
                    ttk.Label(row_frame, text=temp_text, font=('Segoe UI', 10, 'bold')).pack(side="left")
            
            # Display trends
            if trends:
                trends_frame = ttk.LabelFrame(self.frame, text="📈 Weather Trends", padding=10)
                trends_frame.pack(fill="x", pady=5)
                
                for key, value in trends.items():
                    if key != 'forecast_span_hours':
                        ttk.Label(trends_frame, text=f"{key.replace('_', ' ').title()}: {value}").pack(anchor="w")
        else:
            ttk.Label(self.frame, text="Insufficient data for ML predictions", 
                     font=('Segoe UI', 12)).pack(pady=20)


class AirQualityDisplayWidget:
    """Widget for displaying air quality information."""
    
    def __init__(self, parent):
        """Initialize the air quality display widget."""
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
    
    def update_display(self, air_quality_data: Optional[AirQualityData]) -> None:
        """Update air quality display with new data."""
        # Clear existing widgets
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        if not air_quality_data:
            ttk.Label(self.frame, text="No air quality data available", 
                     font=('Segoe UI', 14)).pack(pady=20)
            return
        
        # AQI display
        aqi_frame = ttk.LabelFrame(self.frame, text="🌬️ Air Quality Index", padding=10)
        aqi_frame.pack(fill="x", pady=5)
        
        # Determine AQI color and description
        aqi_levels = {
            1: ("Good", "success"),
            2: ("Fair", "info"),
            3: ("Moderate", "warning"),
            4: ("Poor", "warning"),
            5: ("Very Poor", "danger")
        }
        
        aqi_text, aqi_style = aqi_levels.get(air_quality_data.aqi, ("Unknown", "secondary"))
          ttk.Label(
            aqi_frame,
            text=f"AQI: {air_quality_data.aqi} ({aqi_text})",
            font=('Segoe UI', 16, 'bold')
        ).pack()
        
        # Pollutants details
        pollutants_frame = ttk.LabelFrame(self.frame, text="💨 Pollutant Levels (μg/m³)", padding=10)
        pollutants_frame.pack(fill="x", pady=5)
        
        pollutants = [
            ("CO", air_quality_data.co, "Carbon Monoxide"),
            ("NO₂", air_quality_data.no2, "Nitrogen Dioxide"),
            ("O₃", air_quality_data.o3, "Ozone"),
            ("PM2.5", air_quality_data.pm2_5, "Fine Particles"),
            ("PM10", air_quality_data.pm10, "Coarse Particles")
        ]
        
        for i, (symbol, value, name) in enumerate(pollutants):
            row_frame = ttk.Frame(pollutants_frame)
            row_frame.pack(fill="x", pady=1)
            
            ttk.Label(row_frame, text=f"{symbol}:", width=8, font=('Segoe UI', 10, 'bold')).pack(side="left")
            ttk.Label(row_frame, text=f"{value:.1f}", width=8).pack(side="left")
            ttk.Label(row_frame, text=name, font=('Segoe UI', 9)).pack(side="left")


class ForecastChartWidget:
    """Widget for displaying forecast charts."""
    
    def __init__(self, parent: ttk.Widget):
        """Initialize the forecast chart widget."""
        self.parent = parent
        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.figure = None
        self.canvas = None
    
    def update_chart(self, forecast_data: Optional[ForecastData]) -> None:
        """Update the forecast chart with new data."""
        # Clear existing chart
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
        
        if not forecast_data or not forecast_data.hourly:
            ttk.Label(self.frame, text="No forecast data for charts", 
                     font=('Segoe UI', 14)).pack(pady=20)
            return
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(10, 6), dpi=100)
        self.figure.patch.set_facecolor('none')  # Transparent background
        
        # Temperature subplot
        ax1 = self.figure.add_subplot(211)
        hours = list(range(len(forecast_data.hourly[:24])))  # Next 24 hours
        temps = [item['main']['temp'] for item in forecast_data.hourly[:24]]
        
        ax1.plot(hours, temps, 'b-', linewidth=2, marker='o', markersize=4)
        ax1.set_title('24-Hour Temperature Forecast', fontsize=12, fontweight='bold')
        ax1.set_ylabel('Temperature (°C)')
        ax1.grid(True, alpha=0.3)
        
        # Humidity subplot
        ax2 = self.figure.add_subplot(212)
        humidity = [item['main']['humidity'] for item in forecast_data.hourly[:24]]
        
        ax2.plot(hours, humidity, 'g-', linewidth=2, marker='s', markersize=4)
        ax2.set_title('24-Hour Humidity Forecast', fontsize=12, fontweight='bold')
        ax2.set_xlabel('Hours from now')
        ax2.set_ylabel('Humidity (%)')
        ax2.grid(True, alpha=0.3)
        
        # Adjust layout
        self.figure.tight_layout()
        
        # Create canvas and add to frame
        self.canvas = FigureCanvasTkAgg(self.figure, self.frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill="both", expand=True)


class MainWindow:
    """Main application window."""
    
    def __init__(self, title: str, theme: str, size: tuple, min_size: tuple):
        """Initialize the main window."""
        self.root = ttk.Window(
            title=title,
            themename=theme,
            size=size,
            minsize=min_size
        )
        
        # Status variable
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Callbacks
        self.search_callback: Optional[Callable[[str], None]] = None
        self.theme_change_callback: Optional[Callable[[str], None]] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Header
        self._create_header(main_container)
        
        # Content area
        content_area = ttk.Frame(main_container)
        content_area.pack(fill="both", expand=True, pady=(10, 0))
        
        # Left panel (current weather and predictions)
        left_panel = ttk.Frame(content_area)
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Current weather
        weather_frame = ttk.LabelFrame(left_panel, text="🌤️ Current Weather", padding=10)
        weather_frame.pack(fill="x", pady=(0, 5))
        self.weather_display = WeatherDisplayWidget(weather_frame)
        
        # ML Predictions
        predictions_frame = ttk.LabelFrame(left_panel, text="🤖 AI Predictions", padding=10)
        predictions_frame.pack(fill="both", expand=True)
        self.predictions_display = PredictionsDisplayWidget(predictions_frame)
        
        # Right panel (air quality and charts)
        right_panel = ttk.Frame(content_area)
        right_panel.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Air quality
        air_quality_frame = ttk.LabelFrame(right_panel, text="🌬️ Air Quality", padding=10)
        air_quality_frame.pack(fill="x", pady=(0, 5))
        self.air_quality_display = AirQualityDisplayWidget(air_quality_frame)
        
        # Forecast charts
        chart_frame = ttk.LabelFrame(right_panel, text="📊 Forecast Charts", padding=10)
        chart_frame.pack(fill="both", expand=True)
        self.forecast_chart = ForecastChartWidget(chart_frame)
        
        # Status bar
        self._create_status_bar(main_container)
    
    def _create_header(self, parent: ttk.Widget) -> None:
        """Create the header with search and controls."""
        header_frame = ttk.Frame(parent)
        header_frame.pack(fill="x", pady=(0, 10))
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="🌦️ Complete Weather Dashboard",
            font=('Segoe UI', 18, 'bold')
        )
        title_label.pack(side="left")
        
        # Controls frame
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
            command=self._on_search,
            bootstyle="primary"
        )
        search_btn.pack(side="left", padx=(0, 10))
        
        # Theme selector
        ttk.Label(controls_frame, text="Theme:").pack(side="left", padx=(0, 5))
        
        self.theme_var = tk.StringVar()
        theme_combo = ttk.Combobox(
            controls_frame,
            textvariable=self.theme_var,
            values=['darkly', 'flatly', 'litera', 'minty', 'lumen', 'sandstone'],
            width=10,
            state="readonly"
        )
        theme_combo.pack(side="left", padx=(0, 5))
        theme_combo.bind('<<ComboboxSelected>>', self._on_theme_change)
        
        # API Info button
        api_btn = ttk.Button(
            controls_frame,
            text="ℹ️ API",
            command=self._show_api_info
        )
        api_btn.pack(side="left")
    
    def _create_status_bar(self, parent: ttk.Widget) -> None:
        """Create the status bar."""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill="x", pady=(10, 0))
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_var,
            font=('Segoe UI', 9)
        )
        status_label.pack(side="left")
    
    def _on_search(self, event=None) -> None:
        """Handle search button click or Enter key."""
        city = self.city_entry.get().strip()
        if city and self.search_callback:
            self.search_callback(city)
    
    def _on_theme_change(self, event=None) -> None:
        """Handle theme change."""
        theme = self.theme_var.get()
        if theme and self.theme_change_callback:
            self.theme_change_callback(theme)
    
    def _show_api_info(self) -> None:
        """Show API information window."""
        info_window = ttk.Toplevel(self.root)
        info_window.title("OpenWeatherMap API Information")
        info_window.geometry("500x400")
        
        # Content
        content = ttk.Frame(info_window)
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(
            content,
            text="🌤️ OpenWeatherMap Student Pack",
            font=('Segoe UI', 16, 'bold')
        ).pack(pady=(0, 10))
        
        features_text = """
Features Available:
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
        
        ttk.Label(
            content,
            text=features_text.strip(),
            font=('Segoe UI', 10),
            justify="left"
        ).pack(anchor="w")
        
        # Buttons
        btn_frame = ttk.Frame(content)
        btn_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(
            btn_frame,
            text="📖 Learn More",
            command=lambda: webbrowser.open("https://openweathermap.org/api")
        ).pack(side="left")
        
        ttk.Button(
            btn_frame,
            text="Close",
            command=info_window.destroy
        ).pack(side="right")
    
    def set_search_callback(self, callback: Callable[[str], None]) -> None:
        """Set the search callback function."""
        self.search_callback = callback
    
    def set_theme_change_callback(self, callback: Callable[[str], None]) -> None:
        """Set the theme change callback function."""
        self.theme_change_callback = callback
    
    def update_status(self, message: str) -> None:
        """Update the status bar message."""
        self.status_var.set(message)
    
    def update_weather_display(self, weather_data: Optional[WeatherData]) -> None:
        """Update the weather display."""
        self.weather_display.update_display(weather_data)
    
    def update_predictions_display(self, forecast_data: Optional[ForecastData]) -> None:
        """Update the predictions display."""
        self.predictions_display.update_display(forecast_data)
    
    def update_air_quality_display(self, air_quality_data: Optional[AirQualityData]) -> None:
        """Update the air quality display."""
        self.air_quality_display.update_display(air_quality_data)
    
    def update_forecast_chart(self, forecast_data: Optional[ForecastData]) -> None:
        """Update the forecast chart."""
        self.forecast_chart.update_chart(forecast_data)
    
    def set_city(self, city: str) -> None:
        """Set the city in the search field."""
        self.city_entry.delete(0, tk.END)
        self.city_entry.insert(0, city)
    
    def set_theme(self, theme: str) -> None:
        """Set the theme selector value."""
        self.theme_var.set(theme)
    
    def run(self) -> None:
        """Start the main event loop."""
        self.root.mainloop()
