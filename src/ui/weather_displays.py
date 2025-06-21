"""
Weather display components for the dashboard.

This module contains UI components for displaying weather data,
separated from the main UI logic.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, List, Dict, Any
from datetime import datetime

from ..models.weather_models import WeatherData, ForecastData, AirQualityData


class WeatherDisplays:
    """Weather data display components."""
    
    @staticmethod
    def update_current_weather(frame: tk.Widget, weather: Optional[WeatherData]) -> None:
        """Update current weather display."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if not weather:
            ttk.Label(frame, text="No weather data available").pack(pady=20)
            return
        
        # Temperature display
        temp_frame = ttk.Frame(frame)
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
        details_frame = ttk.Frame(frame)
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
    
    @staticmethod
    def update_air_quality(frame: tk.Widget, air_quality: Optional[AirQualityData]) -> None:
        """Update air quality display."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if not air_quality:
            ttk.Label(frame, text="No air quality data available").pack(pady=20)
            return
        
        aqi = air_quality.aqi
        aqi_levels = {
            1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"
        }
        aqi_text = aqi_levels.get(aqi, "Unknown")
        
        # AQI header
        ttk.Label(
            frame,
            text=f"AQI: {aqi} ({aqi_text})",
            font=('Segoe UI', 16, 'bold')
        ).pack(pady=10)
        
        # Show key pollutants
        pollutants_frame = ttk.Frame(frame)
        pollutants_frame.pack(fill="x")
        
        pollutants = [
            ("PM2.5:", f"{air_quality.pm2_5:.1f} μg/m³"),
            ("PM10:", f"{air_quality.pm10:.1f} μg/m³"),
            ("NO₂:", f"{air_quality.no2:.1f} μg/m³"),
            ("O₃:", f"{air_quality.o3:.1f} μg/m³"),
        ]
        
        for label, value in pollutants:
            pollutant_frame = ttk.Frame(pollutants_frame)
            pollutant_frame.pack(fill="x", pady=1)
            
            ttk.Label(pollutant_frame, text=label, font=('Segoe UI', 10, 'bold')).pack(side="left")
            ttk.Label(pollutant_frame, text=value, font=('Segoe UI', 10)).pack(side="right")
    
    @staticmethod
    def update_forecast(frame: tk.Widget, forecast: Optional[ForecastData]) -> None:
        """Update forecast display."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if not forecast or not forecast.daily:
            ttk.Label(frame, text="No forecast data available").pack(pady=20)
            return
        
        # Header
        ttk.Label(
            frame,
            text="📊 5-Day Forecast",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Show daily forecast
        for i, day in enumerate(forecast.daily[:5]):
            day_frame = ttk.Frame(frame)
            day_frame.pack(fill="x", pady=2)
            
            # Format date
            date_str = datetime.fromtimestamp(day['dt']).strftime("%a, %b %d")
            
            # Date column
            date_label = ttk.Label(day_frame, text=date_str, width=12, font=('Segoe UI', 10))
            date_label.pack(side="left")
            
            # Weather description
            description = day['weather'][0]['description'].title()
            desc_label = ttk.Label(day_frame, text=description, width=15, font=('Segoe UI', 10))
            desc_label.pack(side="left")
            
            # Temperature
            if 'temp' in day:
                temp_text = f"{day['temp']['max']:.0f}°/{day['temp']['min']:.0f}°"
                temp_label = ttk.Label(day_frame, text=temp_text, font=('Segoe UI', 10))
                temp_label.pack(side="left")
    
    @staticmethod
    def update_predictions(frame: tk.Widget, forecast: Optional[ForecastData], 
                          predictions: Optional[Dict[str, Any]] = None) -> None:
        """Update ML predictions display."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if not forecast or not forecast.hourly:
            ttk.Label(frame, text="No forecast data for predictions").pack(pady=20)
            return
        
        # Header
        ttk.Label(
            frame,
            text="🤖 Weather Analysis",
            font=('Segoe UI', 14, 'bold')
        ).pack(pady=10)
        
        # Basic trend analysis from forecast data
        if len(forecast.hourly) >= 2:
            first_temp = forecast.hourly[0]['main']['temp']
            later_temp = forecast.hourly[min(5, len(forecast.hourly)-1)]['main']['temp']
            trend = "rising" if later_temp > first_temp else "falling" if later_temp < first_temp else "stable"
            
            trend_frame = ttk.Frame(frame)
            trend_frame.pack(fill="x", pady=5)
            
            ttk.Label(
                trend_frame,
                text="Temperature Trend:",
                font=('Segoe UI', 11, 'bold')
            ).pack(side="left")
            
            ttk.Label(
                trend_frame,
                text=trend.title(),
                font=('Segoe UI', 11)
            ).pack(side="right")
        
        # Show predictions if available
        if predictions:
            for key, value in predictions.items():
                pred_frame = ttk.Frame(frame)
                pred_frame.pack(fill="x", pady=2)
                
                ttk.Label(
                    pred_frame,
                    text=f"{key}:",
                    font=('Segoe UI', 10, 'bold')
                ).pack(side="left")
                
                ttk.Label(
                    pred_frame,
                    text=str(value),
                    font=('Segoe UI', 10)
                ).pack(side="right")
        else:
            # Show placeholder for future ML features
            ttk.Label(
                frame,
                text="Advanced ML predictions coming soon...",
                font=('Segoe UI', 10, 'italic')
            ).pack(pady=10)
