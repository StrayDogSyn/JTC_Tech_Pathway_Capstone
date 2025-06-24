"""
Visual features for weather display: icons, graphs, and theme management.

This module handles canvas-based weather icons, matplotlib graphs, and theme switching.
"""

import tkinter as tk
from tkinter import Canvas
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
import random
import math

from ..utils.logging import get_logger
from ..utils.data_storage import storage

logger = get_logger()


class WeatherIcon:
    """Canvas-based weather icon renderer with animations."""
    
    def __init__(self, canvas: Canvas, x: int, y: int, size: int = 80):
        """Initialize weather icon renderer."""
        self.canvas = canvas
        self.x = x
        self.y = y
        self.size = size
        self.animation_id = None
        self.animation_frame = 0
        
    def clear(self):
        """Clear the icon from canvas."""
        if self.animation_id:
            self.canvas.after_cancel(self.animation_id)
        # Clear the icon area
        self.canvas.delete(f"icon_{self.x}_{self.y}")
    
    def draw_sunny(self, animated: bool = True):
        """Draw animated sunny weather icon."""
        self.clear()
        center_x, center_y = self.x, self.y
        sun_radius = self.size // 4
        
        # Sun circle
        sun_color = "#FFD700" if not animated else self._get_animated_sun_color()
        self.canvas.create_oval(
            center_x - sun_radius, center_y - sun_radius,
            center_x + sun_radius, center_y + sun_radius,
            fill=sun_color, outline="#FFA500", width=2,
            tags=f"icon_{self.x}_{self.y}"
        )
        
        # Sun rays
        ray_length = self.size // 3
        for i in range(8):
            angle = i * 45 * math.pi / 180
            start_x = center_x + (sun_radius + 5) * math.cos(angle)
            start_y = center_y + (sun_radius + 5) * math.sin(angle)
            end_x = center_x + ray_length * math.cos(angle)
            end_y = center_y + ray_length * math.sin(angle)
            
            self.canvas.create_line(
                start_x, start_y, end_x, end_y,
                fill="#FFD700", width=3, capstyle="round",
                tags=f"icon_{self.x}_{self.y}"
            )
        
        if animated:
            self.animation_frame += 1
            self.animation_id = self.canvas.after(100, lambda: self.draw_sunny(animated))
    
    def draw_cloudy(self, animated: bool = True):
        """Draw animated cloudy weather icon."""
        self.clear()
        center_x, center_y = self.x, self.y
        
        # Main cloud
        cloud_color = "#E6E6FA" if not animated else self._get_animated_cloud_color()
        
        # Cloud parts (overlapping ovals)
        clouds = [
            (center_x - 15, center_y - 5, 25, 20),
            (center_x + 5, center_y - 10, 30, 25),
            (center_x - 5, center_y + 5, 28, 22)
        ]
        
        for i, (x, y, w, h) in enumerate(clouds):
            offset = math.sin((self.animation_frame + i * 20) * 0.1) * 2 if animated else 0
            self.canvas.create_oval(
                x - w//2, y - h//2 + offset,
                x + w//2, y + h//2 + offset,
                fill=cloud_color, outline="#D3D3D3", width=2,
                tags=f"icon_{self.x}_{self.y}"
            )
        
        if animated:
            self.animation_frame += 1
            self.animation_id = self.canvas.after(150, lambda: self.draw_cloudy(animated))
    
    def draw_rainy(self, animated: bool = True):
        """Draw animated rainy weather icon."""
        self.clear()
        center_x, center_y = self.x, self.y
        
        # Cloud
        self._draw_simple_cloud(center_x, center_y - 10, "#8B8B8B")
        
        # Rain drops
        for i in range(6):
            x = center_x + (i - 3) * 8 + random.randint(-3, 3)
            y_offset = (self.animation_frame + i * 10) % 40 if animated else 20
            y = center_y + 15 + y_offset
            
            self.canvas.create_line(
                x, y, x, y + 8,
                fill="#4169E1", width=2,
                tags=f"icon_{self.x}_{self.y}"
            )
        
        if animated:
            self.animation_frame += 1
            self.animation_id = self.canvas.after(100, lambda: self.draw_rainy(animated))
    
    def draw_snowy(self, animated: bool = True):
        """Draw animated snowy weather icon."""
        self.clear()
        center_x, center_y = self.x, self.y
        
        # Cloud
        self._draw_simple_cloud(center_x, center_y - 10, "#D3D3D3")
        
        # Snowflakes
        for i in range(8):
            x = center_x + (i - 4) * 10 + random.randint(-5, 5)
            y_offset = (self.animation_frame + i * 15) % 50 if animated else 25
            y = center_y + 10 + y_offset
            
            # Simple snowflake
            self.canvas.create_text(
                x, y, text="❄", fill="white", font=("Arial", 12),
                tags=f"icon_{self.x}_{self.y}"
            )
        
        if animated:
            self.animation_frame += 1
            self.animation_id = self.canvas.after(200, lambda: self.draw_snowy(animated))
    
    def draw_stormy(self, animated: bool = True):
        """Draw animated stormy weather icon."""
        self.clear()
        center_x, center_y = self.x, self.y
        
        # Dark cloud
        self._draw_simple_cloud(center_x, center_y - 10, "#696969")
        
        # Lightning bolt
        lightning_color = "#FFFF00" if not animated or self.animation_frame % 20 < 10 else "#FFA500"
        points = [
            center_x - 5, center_y + 5,
            center_x + 2, center_y + 15,
            center_x - 2, center_y + 15,
            center_x + 8, center_y + 30
        ]
        
        if animated and self.animation_frame % 40 < 5:  # Flash effect
            self.canvas.create_polygon(
                points, fill=lightning_color, outline="#FFD700", width=2,
                tags=f"icon_{self.x}_{self.y}"
            )
        
        if animated:
            self.animation_frame += 1
            self.animation_id = self.canvas.after(100, lambda: self.draw_stormy(animated))
    
    def _draw_simple_cloud(self, x: int, y: int, color: str):
        """Draw a simple cloud shape."""
        self.canvas.create_oval(
            x - 20, y - 10, x + 20, y + 10,
            fill=color, outline="#A9A9A9", width=2,
            tags=f"icon_{self.x}_{self.y}"
        )
        self.canvas.create_oval(
            x - 15, y - 15, x + 15, y + 5,
            fill=color, outline="#A9A9A9", width=2,
            tags=f"icon_{self.x}_{self.y}"
        )
    
    def _get_animated_sun_color(self) -> str:
        """Get animated sun color that pulses."""
        colors = ["#FFD700", "#FFA500", "#FF8C00"]
        return colors[self.animation_frame % len(colors)]
    
    def _get_animated_cloud_color(self) -> str:
        """Get animated cloud color that shifts slightly."""
        colors = ["#E6E6FA", "#D3D3D3", "#C0C0C0"]
        return colors[self.animation_frame % len(colors)]
    
    def draw_icon_for_weather(self, weather_description: str, animated: bool = True):
        """Draw appropriate icon based on weather description."""
        weather_lower = weather_description.lower()
        
        if 'sun' in weather_lower or 'clear' in weather_lower:
            self.draw_sunny(animated)
        elif 'rain' in weather_lower or 'drizzle' in weather_lower:
            self.draw_rainy(animated)
        elif 'snow' in weather_lower:
            self.draw_snowy(animated)
        elif 'storm' in weather_lower or 'thunder' in weather_lower:
            self.draw_stormy(animated)
        elif 'cloud' in weather_lower:
            self.draw_cloudy(animated)
        else:
            self.draw_cloudy(animated)  # Default


class TemperatureGraph:
    """Temperature history graph using matplotlib."""
    
    def __init__(self, parent_frame: tk.Widget):
        """Initialize the temperature graph."""
        self.parent_frame = parent_frame
        self.figure = Figure(figsize=(8, 4), dpi=100)
        self.figure.patch.set_facecolor('#2b2b2b')  # Dark theme background
        self.ax = self.figure.add_subplot(111)
        
        # Style the plot
        self.ax.set_facecolor('#3b3b3b')
        self.ax.tick_params(colors='white')
        self.ax.xaxis.label.set_color('white')
        self.ax.yaxis.label.set_color('white')
        self.ax.title.set_color('white')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.figure, parent_frame)
        self.canvas.get_tk_widget().pack(fill="both", expand=True)
        
    def update_graph(self, days: int = 7):
        """Update the temperature graph with recent data."""
        self.ax.clear()
        
        # Get weather history
        history = storage.get_weather_history(days)
        
        if not history:
            self.ax.text(0.5, 0.5, 'No data available', 
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=14, color='white')
            self.canvas.draw()
            return
        
        # Prepare data
        dates = []
        temperatures = []
        
        for record in reversed(history):  # Chronological order
            try:
                date = datetime.strptime(record['date'], '%Y-%m-%d %H:%M:%S')
                dates.append(date)
                temperatures.append(record['temperature'])
            except:
                continue
        
        if not dates:
            self.ax.text(0.5, 0.5, 'Invalid data format', 
                        transform=self.ax.transAxes, ha='center', va='center',
                        fontsize=14, color='white')
            self.canvas.draw()
            return
        
        # Plot the data
        self.ax.plot(dates, temperatures, 'o-', color='#00d4aa', linewidth=2, markersize=6)
        
        # Styling
        self.ax.set_title(f'Temperature History ({days} days)', color='white', fontsize=14)
        self.ax.set_xlabel('Date', color='white')
        self.ax.set_ylabel('Temperature (°C)', color='white')
        self.ax.grid(True, alpha=0.3, color='white')
        
        # Format x-axis
        self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
        self.ax.xaxis.set_major_locator(mdates.DayLocator(interval=max(1, days//7)))
        
        # Rotate labels for better readability
        plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
        
        # Style the plot area
        self.ax.set_facecolor('#3b3b3b')
        self.ax.tick_params(colors='white')
        
        # Add min/max annotations
        if temperatures:
            min_temp = min(temperatures)
            max_temp = max(temperatures)
            min_idx = temperatures.index(min_temp)
            max_idx = temperatures.index(max_temp)
            
            self.ax.annotate(f'Min: {min_temp}°C', 
                           xy=(dates[min_idx], min_temp),
                           xytext=(10, 10), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.5', fc='#ff6b6b', alpha=0.8),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                           color='white', fontsize=10)
            
            self.ax.annotate(f'Max: {max_temp}°C', 
                           xy=(dates[max_idx], max_temp),
                           xytext=(10, -10), textcoords='offset points',
                           bbox=dict(boxstyle='round,pad=0.5', fc='#ff9500', alpha=0.8),
                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'),
                           color='white', fontsize=10)
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def set_theme(self, theme: str):
        """Change the graph theme."""
        if theme == 'light':
            self.figure.patch.set_facecolor('white')
            self.ax.set_facecolor('#f8f9fa')
            text_color = 'black'
            grid_color = 'black'
        else:  # dark theme
            self.figure.patch.set_facecolor('#2b2b2b')
            self.ax.set_facecolor('#3b3b3b')
            text_color = 'white'
            grid_color = 'white'
        
        self.ax.tick_params(colors=text_color)
        self.ax.xaxis.label.set_color(text_color)
        self.ax.yaxis.label.set_color(text_color)
        self.ax.title.set_color(text_color)
        self.ax.grid(True, alpha=0.3, color=grid_color)
        
        self.canvas.draw()


class ThemeManager:
    """Manages application themes and color schemes."""
    
    def __init__(self):
        """Initialize theme manager."""
        self.current_theme = "dark"
        self.themes = {
            'dark': {
                'bg': '#2b2b2b',
                'fg': '#ffffff',
                'card_bg': '#3b3b3b',
                'accent': '#00d4aa',
                'secondary': '#ff6b6b',
                'button_bg': '#4b4b4b',
                'button_fg': '#ffffff',
                'entry_bg': '#4b4b4b',
                'entry_fg': '#ffffff'
            },
            'light': {
                'bg': '#ffffff',
                'fg': '#333333',
                'card_bg': '#f8f9fa',
                'accent': '#007bff',
                'secondary': '#fd7e14',
                'button_bg': '#e9ecef',
                'button_fg': '#333333',
                'entry_bg': '#ffffff',
                'entry_fg': '#333333'
            },
            'auto': {
                # Weather-based theme that changes based on conditions
                'sunny': {
                    'bg': '#FFF8DC',
                    'fg': '#8B4513',
                    'card_bg': '#FFFACD',
                    'accent': '#FF8C00',
                    'secondary': '#FFD700'
                },
                'cloudy': {
                    'bg': '#F5F5F5',
                    'fg': '#696969',
                    'card_bg': '#E6E6FA',
                    'accent': '#708090',
                    'secondary': '#B0C4DE'
                },
                'rainy': {
                    'bg': '#2F4F4F',
                    'fg': '#E0FFFF',
                    'card_bg': '#36454F',
                    'accent': '#4682B4',
                    'secondary': '#87CEEB'
                },
                'night': {
                    'bg': '#191970',
                    'fg': '#F0F8FF',
                    'card_bg': '#1C1C1C',
                    'accent': '#6495ED',
                    'secondary': '#9370DB'
                }
            }
        }
    
    def get_theme_colors(self, theme_name: Optional[str] = None, weather_condition: Optional[str] = None) -> Dict[str, str]:
        """Get color scheme for specified theme."""
        if theme_name is None:
            theme_name = self.current_theme
        
        if theme_name == 'auto' and weather_condition:
            # Weather-based theming
            weather_lower = weather_condition.lower()
            current_hour = datetime.now().hour
            
            if current_hour < 6 or current_hour > 20:
                return self.themes['auto']['night']
            elif 'sun' in weather_lower or 'clear' in weather_lower:
                return self.themes['auto']['sunny']
            elif 'rain' in weather_lower or 'storm' in weather_lower:
                return self.themes['auto']['rainy']
            else:
                return self.themes['auto']['cloudy']
        
        return self.themes.get(theme_name, self.themes['dark'])
    
    def set_theme(self, theme_name: str):
        """Set the current theme."""
        if theme_name in self.themes or theme_name == 'auto':
            self.current_theme = theme_name
            logger.info(f"Theme changed to: {theme_name}")
    
    def get_weather_based_colors(self, weather_description: str, temperature: float) -> Dict[str, str]:
        """Get colors based on weather conditions."""
        weather_lower = weather_description.lower()
        
        # Base colors
        if 'sun' in weather_lower or 'clear' in weather_lower:
            base_colors = {
                'primary': '#FFD700',
                'secondary': '#FF8C00',
                'background': '#FFF8DC' if temperature > 15 else '#F0E68C'
            }
        elif 'rain' in weather_lower:
            base_colors = {
                'primary': '#4682B4',
                'secondary': '#87CEEB',
                'background': '#2F4F4F'
            }
        elif 'snow' in weather_lower:
            base_colors = {
                'primary': '#F0F8FF',
                'secondary': '#E6E6FA',
                'background': '#B0C4DE'
            }
        elif 'storm' in weather_lower:
            base_colors = {
                'primary': '#9370DB',
                'secondary': '#6A5ACD',
                'background': '#2E2E2E'
            }
        else:  # cloudy
            base_colors = {
                'primary': '#708090',
                'secondary': '#B0C4DE',
                'background': '#F5F5F5'
            }
        
        return base_colors


# Global instances
theme_manager = ThemeManager()
