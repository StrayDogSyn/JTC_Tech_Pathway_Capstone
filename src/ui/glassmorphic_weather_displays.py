"""
Glassmorphic weather display components for the dashboard.

This module provides glassmorphic weather display components that integrate
with the glassmorphic dashboard design system.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, List, Dict, Any
from datetime import datetime
import math

# Import glassmorphic components
from .glassmorphic_components import (
    GlassmorphicCard, GlassmorphicFrame, GlassmorphicStyle
)

# Import weather models
try:
    from ..models.weather_models import WeatherData, ForecastData, AirQualityData
except ImportError:
    from models.weather_models import WeatherData, ForecastData, AirQualityData


class GlassmorphicWeatherDisplays:
    """Glassmorphic weather display components with frosted glass aesthetics."""
    
    @staticmethod
    def update_current_weather(card: GlassmorphicCard, weather: Optional[WeatherData]) -> None:
        """Update current weather display in a glassmorphic card."""
        if not card or not card.content_frame:
            return
        
        # Clear existing content
        for widget in card.content_frame.winfo_children():
            if not isinstance(widget, ttk.Label) or widget.cget("text") != card.title:
                widget.destroy()
        
        if not weather:
            no_data_label = ttk.Label(
                card.content_frame,
                text="🌫️ No weather data available",
                font=("Segoe UI", 12),
                foreground=card.colors["text_secondary"]
            )
            no_data_label.pack(expand=True)
            return
        
        # Main weather info frame
        main_frame = ttk.Frame(card.content_frame)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Temperature and condition section
        temp_section = ttk.Frame(main_frame)
        temp_section.pack(fill="x", pady=(0, 15))
        
        # Large temperature display
        temp_label = ttk.Label(
            temp_section,
            text=f"{weather.temperature:.0f}°",
            font=("Segoe UI", 48, "bold"),
            foreground=card.colors["accent"]
        )
        temp_label.pack(side="left")
        
        # Weather condition and icon
        condition_frame = ttk.Frame(temp_section)
        condition_frame.pack(side="right", anchor="ne")
        
        # Weather icon (emoji representation)
        weather_icon = GlassmorphicWeatherDisplays._get_weather_emoji(weather.description)
        icon_label = ttk.Label(
            condition_frame,
            text=weather_icon,
            font=("Segoe UI", 32)
        )
        icon_label.pack()
        
        condition_label = ttk.Label(
            condition_frame,
            text=weather.description.title(),
            font=("Segoe UI", 11),
            foreground=card.colors["text_secondary"]
        )
        condition_label.pack()
        
        # Weather details in glassmorphic style
        details_frame = GlassmorphicFrame(main_frame, style_theme=card.style_theme)
        details_frame.pack(fill="x", pady=(0, 10))
        
        details_container = ttk.Frame(details_frame.content_frame)
        details_container.pack(fill="x", padx=10, pady=8)
        details_container.grid_columnconfigure(0, weight=1)
        details_container.grid_columnconfigure(1, weight=1)
        
        # Details data
        details = [
            ("🌡️ Feels Like", f"{weather.feels_like:.0f}°"),
            ("💧 Humidity", f"{weather.humidity}%"),
            ("🌬️ Wind", f"{weather.wind_speed:.1f} km/h"),
            ("🧭 Pressure", f"{weather.pressure} hPa")
        ]
        
        for i, (label, value) in enumerate(details):
            row = i // 2
            col = i % 2
            
            detail_frame = ttk.Frame(details_container)
            detail_frame.grid(row=row, column=col, sticky="w", padx=5, pady=2)
            
            ttk.Label(
                detail_frame,
                text=label,
                font=("Segoe UI", 9),
                foreground=card.colors["text_secondary"]
            ).pack(anchor="w")
            
            ttk.Label(
                detail_frame,
                text=value,
                font=("Segoe UI", 11, "bold"),
                foreground=card.colors["text_primary"]
            ).pack(anchor="w")
    @staticmethod
    def update_forecast(card: GlassmorphicCard, forecast: Optional[ForecastData]) -> None:
        """Update forecast display in a glassmorphic card."""
        if not card or not card.content_frame:
            return
        
        # Clear existing content (except title)
        for widget in card.content_frame.winfo_children():
            if not isinstance(widget, ttk.Label) or widget.cget("text") != card.title:
                widget.destroy()
        
        if not forecast or not forecast.daily:
            no_data_label = ttk.Label(
                card.content_frame,
                text="📅 No forecast data available",
                font=("Segoe UI", 12),
                foreground=card.colors["text_secondary"]
            )
            no_data_label.pack(expand=True)
            return
        
        # Forecast container
        forecast_container = ttk.Frame(card.content_frame)
        forecast_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Take first 5 days of forecast
        for i, day_data in enumerate(forecast.daily[:5]):
            day_frame = GlassmorphicFrame(
                forecast_container, 
                style_theme=card.style_theme,
                blur_intensity=0.08
            )
            day_frame.pack(fill="x", pady=2)
            
            day_content = ttk.Frame(day_frame.content_frame)
            day_content.pack(fill="x", padx=8, pady=4)
            day_content.grid_columnconfigure(1, weight=1)
            
            # Day name
            day_name = datetime.fromtimestamp(day_data['dt']).strftime("%a")
            day_label = ttk.Label(
                day_content,
                text=day_name,
                font=("Segoe UI", 10, "bold"),
                foreground=card.colors["text_primary"]
            )
            day_label.grid(row=0, column=0, sticky="w", padx=(0, 10))
            
            # Weather icon
            icon = GlassmorphicWeatherDisplays._get_weather_emoji(day_data['weather'][0]['description'])
            icon_label = ttk.Label(
                day_content,
                text=icon,
                font=("Segoe UI", 16)
            )
            icon_label.grid(row=0, column=1, padx=10)
            
            # Temperature range
            temp_max = day_data['temp']['max']
            temp_min = day_data['temp']['min']
            temp_label = ttk.Label(
                day_content,
                text=f"{temp_max:.0f}°/{temp_min:.0f}°",
                font=("Segoe UI", 10),
                foreground=card.colors["text_primary"]
            )
            temp_label.grid(row=0, column=2, sticky="e")
    
    @staticmethod
    def update_air_quality(card: GlassmorphicCard, air_quality: Optional[AirQualityData]) -> None:
        """Update air quality display in a glassmorphic card."""
        if not card or not card.content_frame:
            return
        
        # Clear existing content (except title)
        for widget in card.content_frame.winfo_children():
            if not isinstance(widget, ttk.Label) or widget.cget("text") != card.title:
                widget.destroy()
        
        if not air_quality:
            no_data_label = ttk.Label(
                card.content_frame,
                text="💨 No air quality data available",
                font=("Segoe UI", 12),
                foreground=card.colors["text_secondary"]
            )
            no_data_label.pack(expand=True)
            return
        
        # Air quality container
        aqi_container = ttk.Frame(card.content_frame)
        aqi_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # AQI value display
        aqi_frame = GlassmorphicFrame(aqi_container, style_theme=card.style_theme)
        aqi_frame.pack(fill="x", pady=(0, 10))
        
        aqi_content = ttk.Frame(aqi_frame.content_frame)
        aqi_content.pack(fill="x", padx=10, pady=8)
        
        # AQI number and status
        aqi_status = GlassmorphicWeatherDisplays._get_aqi_status(air_quality.aqi)
        aqi_color = GlassmorphicWeatherDisplays._get_aqi_color(air_quality.aqi)
        
        aqi_label = ttk.Label(
            aqi_content,
            text=f"AQI: {air_quality.aqi}",
            font=("Segoe UI", 24, "bold"),
            foreground=aqi_color
        )
        aqi_label.pack()
        
        status_label = ttk.Label(
            aqi_content,
            text=aqi_status,
            font=("Segoe UI", 12),
            foreground=card.colors["text_secondary"]        )
        status_label.pack()
        
        # Pollutant details
        components_frame = GlassmorphicFrame(aqi_container, style_theme=card.style_theme)
        components_frame.pack(fill="x")
        
        comp_content = ttk.Frame(components_frame.content_frame)
        comp_content.pack(fill="x", padx=10, pady=8)
        
        pollutants = [
            ("PM2.5", air_quality.pm2_5),
            ("PM10", air_quality.pm10),
            ("O₃", air_quality.o3),
            ("NO₂", air_quality.no2)
        ]
        
        row_frame = None
        for i, (name, value) in enumerate(pollutants):
            if i % 2 == 0:
                row_frame = ttk.Frame(comp_content)
                row_frame.pack(fill="x", pady=1)
            
            if row_frame:
                pollutant_frame = ttk.Frame(row_frame)
                pollutant_frame.pack(side="left", fill="x", expand=True, padx=5)
                
                ttk.Label(
                    pollutant_frame,
                    text=f"{name}: {value:.1f}",
                    font=("Segoe UI", 9),
                    foreground=card.colors["text_primary"]
                ).pack(anchor="w")
    @staticmethod
    def update_predictions(card: GlassmorphicCard, forecast: Optional[ForecastData]) -> None:
        """Update weather predictions display in a glassmorphic card."""
        if not card or not card.content_frame:
            return
        
        # Clear existing content (except title)
        for widget in card.content_frame.winfo_children():
            if not isinstance(widget, ttk.Label) or widget.cget("text") != card.title:
                widget.destroy()
        
        # Predictions container
        pred_container = ttk.Frame(card.content_frame)
        pred_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        if not forecast or not forecast.daily:
            no_data_label = ttk.Label(
                pred_container,
                text="🔮 No prediction data available",
                font=("Segoe UI", 12),
                foreground=card.colors["text_secondary"]
            )
            no_data_label.pack(expand=True)
            return
        
        # Generate simple predictions based on forecast data
        predictions = GlassmorphicWeatherDisplays._generate_predictions(forecast)
        
        for prediction in predictions:
            pred_frame = GlassmorphicFrame(pred_container, style_theme=card.style_theme)
            pred_frame.pack(fill="x", pady=2)
            
            pred_content = ttk.Frame(pred_frame.content_frame)
            pred_content.pack(fill="x", padx=8, pady=4)
            
            # Prediction icon and text
            icon_label = ttk.Label(
                pred_content,
                text=prediction["icon"],
                font=("Segoe UI", 16)
            )
            icon_label.pack(side="left", padx=(0, 10))
            
            text_label = ttk.Label(
                pred_content,
                text=prediction["text"],
                font=("Segoe UI", 10),
                foreground=card.colors["text_primary"],
                wraplength=200
            )
            text_label.pack(side="left", fill="x", expand=True)
    
    @staticmethod
    def _get_weather_emoji(description: str) -> str:
        """Get weather emoji based on description."""
        description = description.lower()
        
        if "clear" in description:
            return "☀️"
        elif "cloud" in description:
            return "☁️"
        elif "rain" in description or "drizzle" in description:
            return "🌧️"
        elif "snow" in description:
            return "❄️"
        elif "storm" in description or "thunder" in description:
            return "⛈️"
        elif "mist" in description or "fog" in description:
            return "🌫️"
        elif "wind" in description:
            return "💨"
        else:
            return "🌤️"
    
    @staticmethod
    def _get_aqi_status(aqi: int) -> str:
        """Get AQI status text."""
        if aqi <= 50:
            return "Good"
        elif aqi <= 100:
            return "Moderate"
        elif aqi <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "Unhealthy"
        elif aqi <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"
    
    @staticmethod
    def _get_aqi_color(aqi: int) -> str:
        """Get AQI color based on value."""
        if aqi <= 50:
            return "#00e400"  # Green
        elif aqi <= 100:
            return "#ffff00"  # Yellow
        elif aqi <= 150:
            return "#ff7e00"  # Orange
        elif aqi <= 200:
            return "#ff0000"  # Red
        elif aqi <= 300:
            return "#8f3f97"  # Purple
        else:
            return "#7e0023"  # Maroon
    @staticmethod
    def _generate_predictions(forecast: ForecastData) -> List[Dict[str, str]]:
        """Generate simple weather predictions from forecast data."""
        predictions = []
        
        if len(forecast.daily) >= 2:
            # Compare temperatures between first two days
            temp1_avg = (forecast.daily[0]['temp']['max'] + forecast.daily[0]['temp']['min']) / 2
            temp2_avg = (forecast.daily[1]['temp']['max'] + forecast.daily[1]['temp']['min']) / 2
            temp_trend = temp2_avg - temp1_avg
            
            if temp_trend > 2:
                predictions.append({
                    "icon": "📈",
                    "text": "Temperature rising - expect warmer weather ahead"
                })
            elif temp_trend < -2:
                predictions.append({
                    "icon": "📉", 
                    "text": "Temperature dropping - cooler weather approaching"
                })
        
        # Check for rain probability in daily forecast
        rainy_days = sum(1 for day in forecast.daily[:3] 
                        if "rain" in day['weather'][0]['description'].lower())
        if rainy_days >= 2:
            predictions.append({
                "icon": "🌧️",
                "text": "High chance of rain in the coming days - carry an umbrella"
            })
        
        # Check for clear weather
        clear_days = sum(1 for day in forecast.daily[:3] 
                        if "clear" in day['weather'][0]['description'].lower())
        if clear_days >= 2:
            predictions.append({
                "icon": "☀️",
                "text": "Clear skies ahead - great weather for outdoor activities"
            })
        
        if not predictions:
            predictions.append({
                "icon": "🔮",
                "text": "Weather patterns are stable - no significant changes expected"
            })
        
        return predictions[:3]  # Return max 3 predictions


# Create compatibility class for existing code
class WeatherDisplays:
    """Compatibility wrapper for glassmorphic weather displays."""
    
    @staticmethod
    def update_current_weather(frame, weather_data):
        """Update current weather display."""
        if isinstance(frame, GlassmorphicCard):
            GlassmorphicWeatherDisplays.update_current_weather(frame, weather_data)
        # Add fallback for non-glassmorphic frames if needed
    
    @staticmethod
    def update_forecast(frame, forecast_data):
        """Update forecast display."""
        if isinstance(frame, GlassmorphicCard):
            GlassmorphicWeatherDisplays.update_forecast(frame, forecast_data)
    
    @staticmethod
    def update_air_quality(frame, air_quality_data):
        """Update air quality display.""" 
        if isinstance(frame, GlassmorphicCard):
            GlassmorphicWeatherDisplays.update_air_quality(frame, air_quality_data)
    
    @staticmethod
    def update_predictions(frame, forecast_data):
        """Update predictions display."""
        if isinstance(frame, GlassmorphicCard):
            GlassmorphicWeatherDisplays.update_predictions(frame, forecast_data)
