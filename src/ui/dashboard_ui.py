"""
Main dashboard UI components.

This module contains the main weather dashboard UI components,
separated from business logic.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, Callable, Dict, Any
from datetime import datetime


class WeatherDashboardUI:
    """Main weather dashboard user interface."""
    
    def __init__(self, title: str = "Weather Dashboard", theme: str = "darkly", size: tuple = (1200, 800)):
        """Initialize the main UI."""
        self.root = ttk.Window(
            title=title,
            themename=theme,
            size=size,
            minsize=(800, 600)
        )
        
        # Status variable
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        
        # Callbacks
        self.search_callback: Optional[Callable[[str], None]] = None
        self.theme_change_callback: Optional[Callable[[str], None]] = None
        
        # UI components
        self.city_entry: Optional[ttk.Entry] = None
        self.theme_var: Optional[tk.StringVar] = None
        self.weather_frame: Optional[ttk.LabelFrame] = None
        self.predictions_frame: Optional[ttk.LabelFrame] = None
        self.air_quality_frame: Optional[ttk.LabelFrame] = None
        self.forecast_frame: Optional[ttk.LabelFrame] = None
        
        self._setup_ui()
    
    def set_search_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for search events."""
        self.search_callback = callback
    
    def set_theme_change_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for theme change events."""
        self.theme_change_callback = callback
    
    def _setup_ui(self) -> None:
        """Set up the user interface."""
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
        
        self.theme_var = tk.StringVar(value="darkly")
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
        
        # Show initial placeholders
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
        """Show initial placeholder content."""
        self._clear_frame(self.weather_frame)
        ttk.Label(self.weather_frame, 
                 text="Enter a city name and click Search to get weather data", 
                 font=('Segoe UI', 12)).pack(pady=20)
        
        self._clear_frame(self.predictions_frame)
        ttk.Label(self.predictions_frame, 
                 text="AI predictions will appear here after loading weather data", 
                 font=('Segoe UI', 12)).pack(pady=20)
        
        self._clear_frame(self.air_quality_frame)
        ttk.Label(self.air_quality_frame, 
                 text="Air quality data will appear here", 
                 font=('Segoe UI', 12)).pack(pady=20)        
        self._clear_frame(self.forecast_frame)
        ttk.Label(self.forecast_frame, 
                 text="Weather forecast charts will appear here", 
                 font=('Segoe UI', 12)).pack(pady=20)
    
    def _clear_frame(self, frame: Optional[tk.Widget]) -> None:
        """Clear all widgets from a frame."""
        if frame:
            for widget in frame.winfo_children():
                widget.destroy()
    
    def _on_search(self, event=None) -> None:
        """Handle search button click or Enter key."""
        if self.search_callback and self.city_entry:
            city = self.city_entry.get().strip()
            if city:
                self.search_callback(city)
    
    def _on_theme_change(self, event=None) -> None:
        """Handle theme change."""
        if self.theme_change_callback and self.theme_var:
            theme = self.theme_var.get()
            if theme:
                self.theme_change_callback(theme)
    
    def _show_api_info(self) -> None:
        """Show API information dialog."""
        from tkinter import messagebox
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
    
    def set_city_text(self, city: str) -> None:
        """Set the city entry text."""
        if self.city_entry:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, city)
    
    def set_theme(self, theme: str) -> None:
        """Set the theme selector value."""
        if self.theme_var:
            self.theme_var.set(theme)
    
    def update_status(self, message: str) -> None:
        """Update status bar message."""
        self.status_var.set(message)
    
    def show_error(self, title: str, message: str) -> None:
        """Show error dialog."""
        from tkinter import messagebox
        messagebox.showerror(title, message)
    
    def show_info(self, title: str, message: str) -> None:
        """Show info dialog."""
        from tkinter import messagebox
        messagebox.showinfo(title, message)
    
    def run(self) -> None:
        """Start the UI main loop."""
        self.root.mainloop()
    
    def destroy(self) -> None:
        """Destroy the UI."""
        if self.root:
            self.root.destroy()
