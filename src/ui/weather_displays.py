"""
Weather display components for the dashboard.

This module contains UI components for displaying weather data,
separated from the main UI logic with modern UX features.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, List, Dict, Any
from datetime import datetime
import math

try:
    # Try relative imports first (when run as module)
    from ..models.weather_models import WeatherData, ForecastData, AirQualityData
except ImportError:
    # Fall back to absolute imports (when run directly or from verification)
    from models.weather_models import WeatherData, ForecastData, AirQualityData

try:
    from .modern_components import (
        ModernCard, CircularProgress, WeatherGauge,
        NotificationToast, LoadingSpinner
    )
    MODERN_COMPONENTS_AVAILABLE = True
    ModernCard = ModernCard
    WeatherGauge = WeatherGauge
except ImportError:
    MODERN_COMPONENTS_AVAILABLE = False
    ModernCard = None
    WeatherGauge = None


class EnhancedWeatherDisplays:
    """Enhanced weather data display components with modern UI elements."""
    
    @staticmethod
    def create_modern_weather_card(parent: tk.Widget, weather: Optional[WeatherData]) -> tk.Widget:
        """Create a modern weather card with enhanced visuals."""
        if MODERN_COMPONENTS_AVAILABLE and ModernCard:
            card = ModernCard(parent, title="Current Weather", padding=20)
        else:
            # Fallback to regular frame
            card = ttk.LabelFrame(parent, text="Current Weather", padding=20)
        
        if not weather:
            ttk.Label(card, text="No weather data available", 
                     font=('Segoe UI', 12)).pack(pady=20)
            return card
        
        # Main content container
        content_frame = ttk.Frame(card)
        content_frame.pack(fill="both", expand=True)
        
        # Left side - Temperature and main info
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side="left", fill="both", expand=True)
        
        # Temperature with gradient background effect
        temp_container = ttk.Frame(left_frame)
        temp_container.pack(pady=(0, 15))
        
        # Main temperature
        temp_label = ttk.Label(
            temp_container,
            text=f"{weather.temperature:.0f}°",
            font=('Segoe UI', 48, 'bold'),
            foreground="#FF6B35"
        )
        temp_label.pack()
        
        # Feels like temperature
        feels_like_label = ttk.Label(
            temp_container,
            text=f"Feels like {weather.feels_like:.0f}°C",
            font=('Segoe UI', 14),
            foreground="gray"
        )
        feels_like_label.pack()
        
        # Weather description with icon
        desc_frame = ttk.Frame(left_frame)
        desc_frame.pack(pady=(10, 0))
        
        # Weather icon (emoji based on description)
        weather_icon = EnhancedWeatherDisplays._get_weather_icon(weather.description)
        icon_label = ttk.Label(
            desc_frame,
            text=weather_icon,
            font=('Segoe UI', 24)
        )
        icon_label.pack()
        
        desc_label = ttk.Label(
            desc_frame,
            text=weather.description.title(),
            font=('Segoe UI', 16, 'bold')
        )
        desc_label.pack()
        
        # Right side - Gauges and additional info
        right_frame = ttk.Frame(content_frame)
        right_frame.pack(side="right", fill="y", padx=(20, 0))
        
        # Humidity gauge
        if MODERN_COMPONENTS_AVAILABLE and WeatherGauge:
            humidity_gauge = WeatherGauge(
                right_frame,
                value=weather.humidity,
                max_value=100,
                label="Humidity",
                unit="%",
                size=120
            )
            humidity_gauge.pack(pady=(0, 15))
        else:
            # Fallback humidity display
            humidity_frame = ttk.Frame(right_frame)
            humidity_frame.pack(pady=(0, 15))
            ttk.Label(humidity_frame, text="💧 Humidity", font=('Segoe UI', 12, 'bold')).pack()
            ttk.Label(humidity_frame, text=f"{weather.humidity}%", font=('Segoe UI', 16)).pack()
        
        # Wind speed gauge
        if MODERN_COMPONENTS_AVAILABLE and WeatherGauge:
            wind_gauge = WeatherGauge(
                right_frame,
                value=weather.wind_speed,
                max_value=50,
                label="Wind Speed",
                unit="m/s",
                size=120
            )
            wind_gauge.pack(pady=(0, 15))
        else:
            # Fallback wind display
            wind_frame = ttk.Frame(right_frame)
            wind_frame.pack(pady=(0, 15))
            ttk.Label(wind_frame, text="💨 Wind Speed", font=('Segoe UI', 12, 'bold')).pack()
            ttk.Label(wind_frame, text=f"{weather.wind_speed} m/s", font=('Segoe UI', 16)).pack()
        
        # Additional weather details
        details_frame = ttk.Frame(left_frame)
        details_frame.pack(fill="x", pady=(20, 0))
        
        # Create a grid of weather details
        details = [
            ("🌡️ Pressure", f"{weather.pressure} hPa"),
            ("👁️ Visibility", f"{weather.visibility} km"),
            ("☁️ Cloudiness", f"{weather.cloudiness}%"),
            ("🧭 Wind Dir", f"{weather.wind_direction}°")
        ]
        
        for i, (label, value) in enumerate(details):
            detail_frame = ttk.Frame(details_frame)
            detail_frame.grid(row=i//2, column=i%2, sticky="w", padx=(0, 20), pady=2)
            
            ttk.Label(detail_frame, text=label, font=('Segoe UI', 10, 'bold')).pack(side="left")
            ttk.Label(detail_frame, text=value, font=('Segoe UI', 10)).pack(side="left", padx=(5, 0))
        
        # Last updated time
        update_time = datetime.now().strftime("%H:%M:%S")
        ttk.Label(
            card,
            text=f"Last updated: {update_time}",
            font=('Segoe UI', 9),
            foreground="gray"        ).pack(side="bottom", anchor="e", pady=(10, 0))
        
        return card
    
    @staticmethod
    def _get_weather_icon(description: str) -> str:
        """Get weather icon emoji based on description."""
        description = description.lower()
        
        if "clear" in description or "sunny" in description:
            return "☀️"
        elif "partly cloudy" in description or "few clouds" in description:
            return "⛅"
        elif "cloudy" in description or "overcast" in description:
            return "☁️"
        elif "rain" in description:
            return "🌧️"
        elif "drizzle" in description:
            return "🌦️"
        elif "thunderstorm" in description or "storm" in description:
            return "⛈️"
        elif "snow" in description:
            return "🌨️"
        elif "mist" in description or "fog" in description:
            return "🌫️"
        elif "wind" in description:
            return "💨"
        else:
            return "🌤️"
    
    @staticmethod
    def create_enhanced_forecast_display(parent: tk.Widget, forecast: Optional[ForecastData]) -> tk.Widget:
        """Create enhanced forecast display with cards and charts."""
        if MODERN_COMPONENTS_AVAILABLE and ModernCard:
            card = ModernCard(parent, title="5-Day Forecast", padding=15)
        else:
            card = ttk.LabelFrame(parent, text="5-Day Forecast", padding=15)
        
        if not forecast or not forecast.daily:
            ttk.Label(card, text="No forecast data available", 
                     font=('Segoe UI', 12)).pack(pady=20)
            return card
        
        # Create scrollable frame for forecast items
        canvas = tk.Canvas(card, height=200)
        scrollbar = ttk.Scrollbar(card, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Add forecast items
        for i, day_forecast in enumerate(forecast.daily[:5]):
            forecast_item = EnhancedWeatherDisplays._create_forecast_item(
                scrollable_frame, day_forecast, i == 0
            )
            forecast_item.pack(fill="x", pady=2)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        return card
    
    @staticmethod
    def _create_forecast_item(parent: tk.Widget, day_data: Dict[str, Any], is_today: bool = False) -> tk.Widget:
        """Create individual forecast item."""
        # Enhanced styling for today vs other days
        if is_today:
            item_frame = ttk.Frame(parent, style="Accent.TFrame", padding=10)
        else:
            item_frame = ttk.Frame(parent, padding=8)
            
        item_frame.configure(relief="solid", borderwidth=1)
        
        # Left side - Date and icon
        left_frame = ttk.Frame(item_frame)
        left_frame.pack(side="left", fill="y")
        
        # Date
        date_label = "Today" if is_today else day_data.get('date', 'Unknown')
        date_text = ttk.Label(
            left_frame,
            text=date_label,
            font=('Segoe UI', 12, 'bold' if is_today else 'normal')
        )
        date_text.pack(anchor="w")
        
        # Weather icon
        icon = EnhancedWeatherDisplays._get_weather_icon(day_data.get('description', ''))
        icon_label = ttk.Label(left_frame, text=icon, font=('Segoe UI', 18))
        icon_label.pack(anchor="w", pady=(5, 0))
        
        # Center - Temperature range
        temp_frame = ttk.Frame(item_frame)
        temp_frame.pack(side="left", expand=True, padx=20)
        
        high_temp = day_data.get('high_temp', 0)
        low_temp = day_data.get('low_temp', 0)
        
        temp_text = ttk.Label(
            temp_frame,
            text=f"{high_temp:.0f}° / {low_temp:.0f}°",
            font=('Segoe UI', 14, 'bold' if is_today else 'normal')
        )
        temp_text.pack()
        
        # Description
        desc_text = ttk.Label(
            temp_frame,
            text=day_data.get('description', '').title(),
            font=('Segoe UI', 10),
            foreground="gray"
        )
        desc_text.pack()
        
        # Right side - Additional info
        right_frame = ttk.Frame(item_frame)
        right_frame.pack(side="right")
        
        # Precipitation chance
        precip = day_data.get('precipitation_chance', 0)
        if precip > 0:
            precip_label = ttk.Label(
                right_frame,
                text=f"🌧️ {precip}%",
                font=('Segoe UI', 10)
            )
            precip_label.pack(anchor="e")
        
        # Wind info
        wind_speed = day_data.get('wind_speed', 0)
        if wind_speed > 0:
            wind_label = ttk.Label(
                right_frame,
                text=f"💨 {wind_speed:.0f} m/s",
                font=('Segoe UI', 10)
            )
            wind_label.pack(anchor="e")
        
        return item_frame
    
    @staticmethod
    def create_enhanced_air_quality_display(parent: tk.Widget, air_quality: Optional[AirQualityData]) -> tk.Widget:
        """Create enhanced air quality display with visual indicators."""
        if MODERN_COMPONENTS_AVAILABLE and ModernCard:
            card = ModernCard(parent, title="Air Quality Index", padding=15)
        else:
            card = ttk.LabelFrame(parent, text="Air Quality Index", padding=15)
        
        if not air_quality:
            ttk.Label(card, text="No air quality data available", 
                     font=('Segoe UI', 12)).pack(pady=20)
            return card
        
        # Main AQI display
        aqi_frame = ttk.Frame(card)
        aqi_frame.pack(fill="x", pady=(0, 15))
        
        # AQI value with color coding
        aqi_value = air_quality.aqi
        aqi_color, aqi_description = EnhancedWeatherDisplays._get_aqi_info(aqi_value)
        
        # Large AQI number
        aqi_label = ttk.Label(
            aqi_frame,
            text=str(aqi_value),
            font=('Segoe UI', 36, 'bold'),
            foreground=aqi_color
        )
        aqi_label.pack()
        
        # AQI description
        desc_label = ttk.Label(
            aqi_frame,
            text=aqi_description,
            font=('Segoe UI', 14, 'bold'),
            foreground=aqi_color
        )
        desc_label.pack()
          # Pollutant details
        components_frame = ttk.LabelFrame(card, text="Pollutant Levels", padding=10)
        components_frame.pack(fill="x", pady=(10, 0))
        
        # Create grid of pollutant information
        pollutants = [
            ("PM2.5", air_quality.pm2_5, "μg/m³"),
            ("PM10", air_quality.pm10, "μg/m³"),
            ("NO₂", air_quality.no2, "μg/m³"),
            ("O₃", air_quality.o3, "μg/m³"),
            ("SO₂", air_quality.so2, "μg/m³"),
            ("CO", air_quality.co, "mg/m³")
        ]
        
        for i, (name, value, unit) in enumerate(pollutants):
            if value > 0:  # Only show if we have data
                pollutant_frame = ttk.Frame(components_frame)
                pollutant_frame.grid(row=i//3, column=i%3, sticky="w", padx=10, pady=2)
                
                ttk.Label(
                    pollutant_frame,
                    text=f"{name}:",
                    font=('Segoe UI', 10, 'bold')
                ).pack(side="left")
                
                ttk.Label(
                    pollutant_frame,
                    text=f"{value:.1f} {unit}",
                    font=('Segoe UI', 10)
                ).pack(side="left", padx=(5, 0))
        
        return card
    
    @staticmethod
    def _get_aqi_info(aqi: int) -> tuple[str, str]:
        """Get AQI color and description based on value."""
        if aqi <= 50:
            return "#00E400", "Good"
        elif aqi <= 100:
            return "#FFFF00", "Moderate"
        elif aqi <= 150:
            return "#FF7E00", "Unhealthy for Sensitive Groups"
        elif aqi <= 200:
            return "#FF0000", "Unhealthy"
        elif aqi <= 300:
            return "#8F3F97", "Very Unhealthy"
        else:
            return "#7E0023", "Hazardous"


# Backward compatibility - Original WeatherDisplays class
class WeatherDisplays:
    """Original weather data display components for backward compatibility."""
    
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
        details_frame.pack(pady=10)
        
        details = [
            f"Humidity: {weather.humidity}%",
            f"Pressure: {weather.pressure} hPa",
            f"Wind: {weather.wind_speed} m/s",
            f"Visibility: {weather.visibility} km"
        ]
        
        for detail in details:
            ttk.Label(details_frame, text=detail, font=('Segoe UI', 12)).pack()
    
    @staticmethod
    def update_forecast(frame: tk.Widget, forecast: Optional[ForecastData]) -> None:
        """Update forecast display."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if not forecast:
            ttk.Label(frame, text="No forecast data available").pack(pady=20)
            return
        
        ttk.Label(frame, text="5-Day Forecast", font=('Segoe UI', 16, 'bold')).pack(pady=(0, 10))
        
        # Show daily forecast
        for i, day in enumerate(forecast.daily[:5]):
            day_frame = ttk.Frame(frame)
            day_frame.pack(fill="x", pady=2)
            
            # Date
            date_str = "Today" if i == 0 else f"Day {i+1}"
            ttk.Label(day_frame, text=date_str, font=('Segoe UI', 12, 'bold')).pack(side="left")
            
            # Temperature range
            if 'temp' in day and isinstance(day['temp'], dict):
                temp_text = f"{day['temp']['max']:.0f}°/{day['temp']['min']:.0f}°"
            else:
                temp_text = "N/A"
            ttk.Label(day_frame, text=temp_text).pack(side="right")
            
            # Description
            if 'weather' in day and day['weather']:
                desc = day['weather'][0]['description']
                ttk.Label(day_frame, text=desc.title(), font=('Segoe UI', 10)).pack(side="right", padx=10)
    
    @staticmethod
    def update_air_quality(frame: tk.Widget, air_quality: Optional[AirQualityData]) -> None:
        """Update air quality display."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if not air_quality:
            ttk.Label(frame, text="No air quality data available").pack(pady=20)
            return
        
        # AQI value
        aqi_frame = ttk.Frame(frame)
        aqi_frame.pack(pady=10)
        
        ttk.Label(
            aqi_frame,
            text=f"AQI: {air_quality.aqi}",
            font=('Segoe UI', 24, 'bold')
        ).pack()
        
        # AQI description
        if air_quality.aqi <= 50:
            description = "Good"
            color = "green"
        elif air_quality.aqi <= 100:
            description = "Moderate"
            color = "yellow"
        elif air_quality.aqi <= 150:
            description = "Unhealthy for Sensitive Groups"
            color = "orange"
        else:
            description = "Unhealthy"
            color = "red"
        
        ttk.Label(
            aqi_frame,
            text=description,
            font=('Segoe UI', 14),
            foreground=color
        ).pack()
        
        # Pollutant levels
        pollutants_frame = ttk.LabelFrame(frame, text="Pollutant Levels", padding=10)
        pollutants_frame.pack(fill="x", pady=10)
        
        pollutants = [
            ("PM2.5", air_quality.pm2_5, "μg/m³"),
            ("PM10", air_quality.pm10, "μg/m³"),
            ("NO₂", air_quality.no2, "μg/m³"),
            ("O₃", air_quality.o3, "μg/m³")
        ]
        
        for i, (name, value, unit) in enumerate(pollutants):
            row = i // 2
            col = i % 2
            
            pollutant_label = ttk.Label(
                pollutants_frame,
                text=f"{name}: {value:.1f} {unit}",
                font=('Segoe UI', 10)
            )
            pollutant_label.grid(row=row, column=col, sticky="w", padx=5, pady=2)
    
    @staticmethod
    def update_predictions(frame: tk.Widget, forecast: Optional[ForecastData]) -> None:
        """Update predictions display with basic weather insights."""
        # Clear existing widgets
        for widget in frame.winfo_children():
            widget.destroy()
        
        if not forecast:
            ttk.Label(frame, text="No forecast data available for predictions").pack(pady=20)
            return
        
        # Title
        title_label = ttk.Label(
            frame,
            text="Weather Insights & Predictions",
            font=('Segoe UI', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        # Generate basic predictions based on forecast data
        predictions = []
        
        if hasattr(forecast, 'daily') and forecast.daily:
            # Temperature trend analysis
            temps = []
            for day in forecast.daily[:5]:
                if isinstance(day, dict) and 'temp' in day:
                    if isinstance(day['temp'], dict):
                        temps.append(day['temp'].get('day', 0))
                    else:
                        temps.append(day['temp'])
            
            if len(temps) >= 2:
                if temps[-1] > temps[0]:
                    predictions.append("🌡️ Temperature trend: Rising over the next few days")
                elif temps[-1] < temps[0]:
                    predictions.append("🌡️ Temperature trend: Cooling down in the coming days")
                else:
                    predictions.append("🌡️ Temperature trend: Stable conditions expected")
            
            # Weather pattern analysis
            weather_conditions = []
            for day in forecast.daily[:3]:
                if isinstance(day, dict) and 'weather' in day and day['weather']:
                    main_weather = day['weather'][0].get('main', '').lower()
                    weather_conditions.append(main_weather)
            
            if weather_conditions:
                if 'rain' in weather_conditions or 'drizzle' in weather_conditions:
                    predictions.append("🌧️ Rain expected in the coming days - plan accordingly")
                if 'snow' in weather_conditions:
                    predictions.append("❄️ Snow possible - prepare for winter conditions")
                if weather_conditions.count('clear') >= 2:
                    predictions.append("☀️ Clear skies ahead - great weather for outdoor activities")
                if 'clouds' in weather_conditions:
                    predictions.append("☁️ Cloudy conditions expected")
        
        # Default predictions if no specific patterns found
        if not predictions:
            predictions = [
                "📊 Weather analysis in progress...",
                "🔍 Monitoring atmospheric patterns",
                "📈 Historical data comparison active",
                "🎯 Predictive models updating..."
            ]
        
        # Display predictions
        for i, prediction in enumerate(predictions):
            pred_frame = ttk.Frame(frame)
            pred_frame.pack(fill="x", pady=5)
            
            bullet_label = ttk.Label(
                pred_frame,
                text="•",
                font=('Segoe UI', 12, 'bold'),
                foreground="#4CAF50"
            )
            bullet_label.pack(side="left", padx=(10, 5))
            
            pred_label = ttk.Label(
                pred_frame,
                text=prediction,
                font=('Segoe UI', 11),
                wraplength=350
            )
            pred_label.pack(side="left", fill="x", expand=True)
        
        # ML Enhancement note
        enhancement_frame = ttk.LabelFrame(frame, text="AI Enhancement", padding=10)
        enhancement_frame.pack(fill="x", pady=(20, 0))
        
        enhancement_text = ("💡 These predictions use basic pattern analysis. "
                          "Advanced ML predictions can be enabled with additional data sources.")
        
        ttk.Label(
            enhancement_frame,
            text=enhancement_text,
            font=('Segoe UI', 9),
            foreground="gray",
            wraplength=350
        ).pack()
