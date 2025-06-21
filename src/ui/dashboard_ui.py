"""
Enhanced dashboard UI components with modern UX features.

This module contains the main weather dashboard UI components with modern design,
animations, and enhanced user experience features.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, Callable, Dict, Any, List
from datetime import datetime
import threading
import time

try:
    from .modern_components import (
        ModernCard, CircularProgress, ModernSearchBar, WeatherGauge,
        NotificationToast, ModernToggleSwitch, LoadingSpinner
    )
except ImportError:
    # Fallback if modern components are not available
    ModernCard = None
    CircularProgress = None
    ModernSearchBar = None
    WeatherGauge = None
    NotificationToast = None
    ModernToggleSwitch = None
    LoadingSpinner = None


class WeatherDashboardUI:
    """Enhanced weather dashboard user interface with modern UX features."""
    
    def __init__(self, title: str = "🌦️ Weather Dominator Pro", theme: str = "darkly", size: tuple = (1400, 900)):
        """Initialize the enhanced UI."""
        self.root = ttk.Window(
            title=title,
            themename=theme,
            size=size,
            minsize=(1000, 700)
        )
        
        # Configure window for modern appearance
        self.root.attributes('-alpha', 0.0)  # Start transparent for fade-in
        
        # Enhanced status variables
        self.status_var = tk.StringVar()
        self.status_var.set("🚀 Weather Dominator Pro - Ready")
        self.loading_var = tk.BooleanVar()
        self.auto_refresh_var = tk.BooleanVar()
        
        # Callbacks
        self.search_callback: Optional[Callable[[str], None]] = None
        self.theme_change_callback: Optional[Callable[[str], None]] = None
        self.auto_refresh_callback: Optional[Callable[[bool], None]] = None
        
        # UI components
        self.city_entry: Optional[ttk.Entry] = None
        self.theme_var: Optional[tk.StringVar] = None
        self.weather_frame: Optional[ttk.LabelFrame] = None
        self.predictions_frame: Optional[ttk.LabelFrame] = None
        self.air_quality_frame: Optional[ttk.LabelFrame] = None
        self.forecast_frame: Optional[ttk.LabelFrame] = None
          # Enhanced components
        self.loading_spinner = None  # Will be LoadingSpinner if available
        self.search_suggestions: List[str] = [
            "London, UK", "New York, NY", "Tokyo, Japan", "Paris, France",
            "Sydney, Australia", "Berlin, Germany", "Moscow, Russia",
            "Dubai, UAE", "Singapore", "Mumbai, India"        ]
        
        self._setup_ui()
        self._apply_modern_styling()
        self._fade_in_window()
    
    def _fade_in_window(self):
        """Fade in the window on startup for smooth appearance."""
        def fade():
            for i in range(21):
                alpha = i / 20
                try:
                    self.root.attributes('-alpha', alpha)
                    self.root.update()
                    time.sleep(0.02)
                except:
                    break
        
        threading.Thread(target=fade, daemon=True).start()
    
    def _apply_modern_styling(self):
        """Apply modern styling to the interface."""
        # Configure modern styles
        style = ttk.Style()
        
        # Enhanced card styles
        style.configure("Card.TFrame", relief="solid", borderwidth=1)
        style.configure("Header.TLabel", font=('Segoe UI', 18, 'bold'))
        style.configure("Subtitle.TLabel", font=('Segoe UI', 11), foreground="gray")
        style.configure("Modern.TButton", padding=(10, 5))
        # Weather data styles
        style.configure("Temperature.TLabel", font=('Segoe UI', 48, 'bold'), foreground="#FF6B35")
        style.configure("FeelsLike.TLabel", font=('Segoe UI', 14), foreground="gray")
        style.configure("Description.TLabel", font=('Segoe UI', 16))
        # Status styles  
        style.configure("Status.TLabel", font=('Segoe UI', 10))
        style.configure("Small.TLabel", font=('Segoe UI', 9), foreground="gray")
    
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
        """Create the enhanced header with modern search and controls."""
        header_frame = ttk.Frame(self.root, padding=(20, 15))
        header_frame.pack(fill="x")
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Enhanced title section
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        title_label = ttk.Label(
            title_frame,
            text="🌦️ Weather Dominator Pro",
            style="Header.TLabel",
            foreground="#2196F3"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Advanced Weather Intelligence Platform",
            style="Subtitle.TLabel"
        )
        subtitle_label.pack()
        
        # Enhanced search section
        search_frame = ttk.Frame(header_frame)
        search_frame.grid(row=0, column=1, sticky="ew", padx=(20, 0))
        search_frame.grid_columnconfigure(0, weight=1)
        
        # Modern search container
        search_container = ttk.Frame(search_frame, style="Card.TFrame", padding=8)
        search_container.grid(row=0, column=0, sticky="ew")
        search_container.grid_columnconfigure(1, weight=1)
        
        # Search icon
        search_icon = ttk.Label(search_container, text="🔍", font=('Segoe UI', 14))
        search_icon.grid(row=0, column=0, padx=(5, 8))
        
        # Enhanced city entry with placeholder effect
        self.city_entry = ttk.Entry(
            search_container,
            font=('Segoe UI', 11),
            width=30
        )
        self.city_entry.grid(row=0, column=1, sticky="ew", pady=2)
        self.city_entry.bind('<Return>', self._on_search)
        self.city_entry.bind('<KeyRelease>', self._on_search_key_release)
        self.city_entry.bind('<FocusIn>', self._on_search_focus_in)
        self.city_entry.bind('<FocusOut>', self._on_search_focus_out)
        
        # Set placeholder
        self._set_search_placeholder()
        
        # Search suggestions dropdown (initially hidden)
        self.suggestions_frame = ttk.Frame(search_frame)
        self.suggestions_listbox = tk.Listbox(
            self.suggestions_frame,
            height=6,
            font=('Segoe UI', 10),
            activestyle="none",
            selectmode=tk.SINGLE
        )
        self.suggestions_listbox.pack(fill="both", expand=True)
        self.suggestions_listbox.bind('<Double-Button-1>', self._on_suggestion_select)
        
        # Enhanced search button
        search_btn = ttk.Button(
            search_container,
            text="Search",
            command=self._on_search,
            style="Modern.TButton"
        )
        search_btn.grid(row=0, column=2, padx=(8, 5))
        
        # Controls panel with modern styling
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=0, column=2, sticky="e", padx=(20, 0))
        
        # Theme selector with label
        theme_frame = ttk.Frame(controls_frame)
        theme_frame.pack(pady=(0, 8))
        
        ttk.Label(theme_frame, text="🎨 Theme:", font=('Segoe UI', 10)).pack(side="left", padx=(0, 5))
        
        self.theme_var = tk.StringVar(value="darkly")
        theme_combo = ttk.Combobox(
            theme_frame,
            textvariable=self.theme_var,
            values=['darkly', 'flatly', 'litera', 'minty', 'lumen', 'sandstone', 'superhero', 'vapor'],
            width=12,
            state="readonly",
            font=('Segoe UI', 9)
        )
        theme_combo.pack(side="left")
        theme_combo.bind('<<ComboboxSelected>>', self._on_theme_change)
        
        # Auto-refresh toggle
        if ModernToggleSwitch:
            self.auto_refresh_toggle = ModernToggleSwitch(
                controls_frame,
                text="🔄 Auto-refresh (5min)",
                initial_state=False
            )
            self.auto_refresh_toggle.pack()
            self.auto_refresh_toggle.set_callback(self._on_auto_refresh_toggle)
        else:
            # Fallback checkbox
            self.auto_refresh_var = tk.BooleanVar()
            auto_refresh_cb = ttk.Checkbutton(
                controls_frame,
                text="🔄 Auto-refresh",
                variable=self.auto_refresh_var,
                command=self._on_auto_refresh_fallback
            )
            auto_refresh_cb.pack()
        
        # Loading indicator
        if LoadingSpinner:
            self.loading_spinner = LoadingSpinner(controls_frame, size=25)
            self.loading_spinner.pack(pady=(8, 0))
        else:
            # Fallback loading label
            self.loading_label = ttk.Label(controls_frame, text="⏳", font=('Segoe UI', 16))
            self.loading_label.pack(pady=(8, 0))
            self.loading_label.pack_forget()  # Hide initially
    
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

Perfect for learning and development!        """
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
    
    def _on_search_key_release(self, event=None) -> None:
        """Handle key release in search entry for suggestions."""
        if not self.city_entry:
            return
            
        current_text = self.city_entry.get().strip().lower()
        
        if len(current_text) >= 2:  # Show suggestions after 2 characters
            matching_suggestions = [
                city for city in self.search_suggestions
                if current_text in city.lower()
            ]
            
            if matching_suggestions:
                self._show_suggestions(matching_suggestions[:6])  # Show max 6
            else:
                self._hide_suggestions()
        else:
            self._hide_suggestions()
    
    def _on_search_focus_in(self, event=None) -> None:
        """Handle search entry focus in event."""
        if self.city_entry and self.city_entry.get() == "Enter city name...":
            self.city_entry.delete(0, tk.END)
            self.city_entry.configure(foreground="")
    
    def _on_search_focus_out(self, event=None) -> None:
        """Handle search entry focus out event."""
        if self.city_entry and not self.city_entry.get().strip():
            self._set_search_placeholder()
        self._hide_suggestions()
    
    def _set_search_placeholder(self) -> None:
        """Set placeholder text in search entry."""
        if self.city_entry:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, "Enter city name...")
            self.city_entry.configure(foreground="gray")
    
    def _show_suggestions(self, suggestions: List[str]) -> None:
        """Show search suggestions dropdown."""
        if not hasattr(self, 'suggestions_frame'):
            return
            
        # Clear existing suggestions
        self.suggestions_listbox.delete(0, tk.END)
        
        # Add new suggestions
        for suggestion in suggestions:
            self.suggestions_listbox.insert(tk.END, suggestion)
          # Position and show the suggestions frame
        self.suggestions_frame.grid(row=1, column=0, sticky="ew", pady=(2, 0))
        self.suggestions_frame.lift()
    
    def _hide_suggestions(self) -> None:
        """Hide search suggestions dropdown."""
        if hasattr(self, 'suggestions_frame'):
            self.suggestions_frame.grid_forget()
    
    def _on_suggestion_select(self, event=None) -> None:
        """Handle suggestion selection."""
        if not self.suggestions_listbox.curselection():
            return
            
        selected_index = self.suggestions_listbox.curselection()[0]
        selected_city = self.suggestions_listbox.get(selected_index)
        
        if self.city_entry:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, selected_city)
            self.city_entry.configure(foreground="")
        
        self._hide_suggestions()
        self._on_search()  # Automatically search for selected city
    
    def _on_auto_refresh_toggle(self, enabled: bool) -> None:
        """Handle auto-refresh toggle change."""
        self.auto_refresh_var.set(enabled)
        if self.auto_refresh_callback:
            self.auto_refresh_callback(enabled)
            
        # Update status
        if enabled:
            self.update_status("🔄 Auto-refresh enabled (5 minutes)")
        else:
            self.update_status("⏸️ Auto-refresh disabled")
    
    def _on_auto_refresh_fallback(self) -> None:
        """Handle fallback auto-refresh checkbox."""
        enabled = self.auto_refresh_var.get()
        if self.auto_refresh_callback:
            self.auto_refresh_callback(enabled)
            
        if enabled:
            self.update_status("🔄 Auto-refresh enabled")
        else:
            self.update_status("⏸️ Auto-refresh disabled")
    
    def set_loading(self, loading: bool) -> None:
        """Set loading state with spinner or fallback indicator."""
        if hasattr(self, 'loading_spinner') and self.loading_spinner:
            if loading:
                self.loading_spinner.start_spinning()
            else:
                self.loading_spinner.stop_spinning()
        elif hasattr(self, 'loading_label'):
            if loading:
                self.loading_label.pack(pady=(8, 0))
            else:
                self.loading_label.pack_forget()
        
        self.loading_var.set(loading)
    
    def show_notification(self, message: str, type_: str = "info", duration: int = 3000) -> None:
        """Show notification toast if available."""
        if NotificationToast:
            # NotificationToast automatically shows itself
            NotificationToast(self.root, message, type_, duration / 1000.0)
        else:
            # Fallback to status message
            self.update_status(f"📢 {message}")
    
    def set_auto_refresh_callback(self, callback: Callable[[bool], None]) -> None:
        """Set callback for auto-refresh events."""
        self.auto_refresh_callback = callback
    
    def run(self) -> None:
        """Start the UI main loop."""
        self.root.mainloop()
    
    def destroy(self) -> None:
        """Destroy the UI."""
        if self.root:
            self.root.destroy()
