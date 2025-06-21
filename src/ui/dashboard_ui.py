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
    from .tabular_components import (
        WeatherDataTable, ComparisonTable, AnalyticsTable, AdvancedDataTable
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
    WeatherDataTable = None
    ComparisonTable = None
    AnalyticsTable = None
    AdvancedDataTable = None


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
        self.auto_refresh_callback: Optional[Callable[[bool], None]] = None        # UI components
        self.city_entry: Optional[ttk.Entry] = None
        self.theme_var: Optional[tk.StringVar] = None
        self.weather_frame: Optional[tk.Widget] = None
        self.predictions_frame: Optional[tk.Widget] = None
        self.air_quality_frame: Optional[tk.Widget] = None
        self.forecast_frame: Optional[tk.Widget] = None
        
        # Advanced UI components
        self.loading_spinner = None  # Will be LoadingSpinner if available
        self.weather_cards: List[Any] = []  # ModernCard instances
        self.progress_gauges: Dict[str, Any] = {}  # CircularProgress instances
        self.weather_gauges: Dict[str, Any] = {}  # WeatherGauge instances
        
        # Enhanced features
        self.favorites_list: List[str] = []
        self.recent_searches: List[str] = []
        self.search_suggestions: List[str] = [
            "London, UK", "New York, NY", "Tokyo, Japan", "Paris, France",
            "Sydney, Australia", "Berlin, Germany", "Moscow, Russia",
            "Dubai, UAE", "Singapore", "Mumbai, India"
        ]
          # Advanced settings
        self.settings: Dict[str, Any] = {
            'temperature_unit': 'C',
            'wind_speed_unit': 'km/h',
            'pressure_unit': 'hPa',
            'auto_save_favorites': True,
            'show_animations': True,
            'update_interval': 300,  # 5 minutes
            'show_notifications': True
        }
          # Additional UI variables
        self.temp_unit_var: tk.StringVar = tk.StringVar(value="°C")
        
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
          # Enhanced search button with loading state
        self.search_btn = ttk.Button(
            search_container,
            text="Search",
            command=self._on_search,
            style="Modern.TButton"
        )
        self.search_btn.grid(row=0, column=2, padx=(8, 5))
        
        # Advanced search controls
        advanced_search_frame = ttk.Frame(search_container)
        advanced_search_frame.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(5, 0))
        
        # Quick location buttons
        quick_locations = ["Current Location", "New York", "London", "Tokyo"]
        for i, location in enumerate(quick_locations):
            btn = ttk.Button(
                advanced_search_frame,
                text=location,
                command=lambda loc=location: self._quick_search(loc),
                style="Outline.TButton"
            )
            btn.pack(side="left", padx=(0, 5))
          # Enhanced controls with modern components
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=0, column=2, sticky="e", padx=(20, 0))
        
        # Settings button
        settings_btn = ttk.Button(
            controls_frame,
            text="⚙️",
            command=self._show_settings,
            style="Modern.TButton",
            width=3
        )
        settings_btn.pack(side="top", pady=(0, 5))
        
        # Favorites button
        favorites_btn = ttk.Button(
            controls_frame,
            text="⭐",
            command=self._show_favorites,
            style="Modern.TButton",
            width=3
        )
        favorites_btn.pack(side="top", pady=(0, 5))
        
        # Units toggle frame
        units_frame = ttk.Frame(controls_frame)
        units_frame.pack(pady=(0, 8))
        
        ttk.Label(units_frame, text="🌡️", font=('Segoe UI', 12)).pack(side="left")
        self.temp_unit_var = tk.StringVar(value="°C")
        temp_toggle = ttk.Button(
            units_frame,
            textvariable=self.temp_unit_var,
            command=self._toggle_temperature_unit,
            style="Outline.TButton",
            width=4
        )
        temp_toggle.pack(side="left", padx=(2, 0))
        
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
        else:            # Fallback loading label
            self.loading_label = ttk.Label(controls_frame, text="⏳", font=('Segoe UI', 16))
            self.loading_label.pack(pady=(8, 0))
            self.loading_label.pack_forget()  # Hide initially

    def _create_main_content(self) -> None:
        """Create the main content area with enhanced tabular components."""
        # Main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Create notebook for tabbed interface
        self.main_notebook = ttk.Notebook(main_container)
        self.main_notebook.pack(fill="both", expand=True)        
        # Dashboard Tab (original content)
        self._create_dashboard_tab()
        
        # Advanced Tables Tabs
        self._create_tables_tabs()
        
    def _create_dashboard_tab(self) -> None:
        """Create the main dashboard tab with enhanced modern components."""
        dashboard_frame = ttk.Frame(self.main_notebook)
        self.main_notebook.add(dashboard_frame, text="🏠 Dashboard")
        
        # Create modern grid layout
        dashboard_frame.grid_columnconfigure(0, weight=1)
        dashboard_frame.grid_columnconfigure(1, weight=1)
        dashboard_frame.grid_rowconfigure(0, weight=0)  # Top stats row
        dashboard_frame.grid_rowconfigure(1, weight=1)  # Main content row
        dashboard_frame.grid_rowconfigure(2, weight=0)  # Quick actions row
        
        # Top statistics cards row
        stats_frame = ttk.Frame(dashboard_frame)
        stats_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self._create_stats_cards(stats_frame)
        
        # Left panel - Current Weather & AI Predictions
        left_panel = ttk.Frame(dashboard_frame)
        left_panel.grid(row=1, column=0, sticky="nsew", padx=(10, 5), pady=5)
        left_panel.grid_rowconfigure(0, weight=0)
        left_panel.grid_rowconfigure(1, weight=1)        # Enhanced current weather with modern card
        if ModernCard:
            self.weather_card = ModernCard(
                left_panel,
                title="🌤️ Current Weather"
            )
            self.weather_card.grid(row=0, column=0, sticky="ew", pady=(0, 5))
            self.weather_frame = self.weather_card.content_frame
        else:
            self.weather_frame = ttk.LabelFrame(left_panel, text="🌤️ Current Weather", padding=10)
            self.weather_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))        # Enhanced AI predictions with modern card
        if ModernCard:
            self.predictions_card = ModernCard(
                left_panel,
                title="🤖 AI Weather Intelligence"
            )
            self.predictions_card.grid(row=1, column=0, sticky="nsew")
            self.predictions_frame = self.predictions_card.content_frame
        else:
            self.predictions_frame = ttk.LabelFrame(left_panel, text="🤖 AI Predictions", padding=10)
            self.predictions_frame.grid(row=1, column=0, sticky="nsew")
        
        # Right panel - Air Quality & Forecast
        right_panel = ttk.Frame(dashboard_frame)
        right_panel.grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=5)
        right_panel.grid_rowconfigure(0, weight=0)
        right_panel.grid_rowconfigure(1, weight=1)        # Enhanced air quality with modern card and gauge
        if ModernCard:
            self.air_quality_card = ModernCard(
                right_panel,
                title="🌬️ Air Quality Index"
            )
            self.air_quality_card.grid(row=0, column=0, sticky="ew", pady=(0, 5))
            self.air_quality_frame = self.air_quality_card.content_frame
        else:
            self.air_quality_frame = ttk.LabelFrame(right_panel, text="🌬️ Air Quality", padding=10)
            self.air_quality_frame.grid(row=0, column=0, sticky="ew", pady=(0, 5))        # Enhanced forecast with modern card
        if ModernCard:
            self.forecast_card = ModernCard(
                right_panel,
                title="📊 Weather Forecast"
            )
            self.forecast_card.grid(row=1, column=0, sticky="nsew")
            self.forecast_frame = self.forecast_card.content_frame
        else:
            self.forecast_frame = ttk.LabelFrame(right_panel, text="📊 Forecast", padding=10)
            self.forecast_frame.grid(row=1, column=0, sticky="nsew")
        
        # Quick actions row
        actions_frame = ttk.Frame(dashboard_frame)
        actions_frame.grid(row=2, column=0, columnspan=2, sticky="ew", padx=10, pady=5)
        self._create_quick_actions(actions_frame)
        
        # Show initial content
        self._show_initial_content()
        
    def _create_tables_tabs(self) -> None:
        """Create advanced tabular components tabs."""
        # Weather History Tab
        if WeatherDataTable:
            history_frame = ttk.Frame(self.main_notebook)
            self.main_notebook.add(history_frame, text="📊 Weather History")
            self.weather_data_table = WeatherDataTable(history_frame)
        
        # Location Comparison Tab
        if ComparisonTable:
            comparison_frame = ttk.Frame(self.main_notebook)
            self.main_notebook.add(comparison_frame, text="🌍 Comparison")
            self.comparison_table = ComparisonTable(comparison_frame)
        
        # Analytics Tab
        if AnalyticsTable:
            analytics_frame = ttk.Frame(self.main_notebook)
            self.main_notebook.add(analytics_frame, text="📈 Analytics")
            self.analytics_table = AnalyticsTable(analytics_frame)
            
        # Advanced Data Tab (for custom data tables)
        if AdvancedDataTable:
            advanced_frame = ttk.Frame(self.main_notebook)
            self.main_notebook.add(advanced_frame, text="🛠️ Advanced Data")
            
            # Create custom data table with sample columns
            columns = [
                {'text': 'Timestamp', 'key': 'timestamp', 'width': 150, 'anchor': 'center'},
                {'text': 'Event Type', 'key': 'event_type', 'width': 120, 'anchor': 'w'},
                {'text': 'Location', 'key': 'location', 'width': 120, 'anchor': 'w'},
                {'text': 'Value', 'key': 'value', 'width': 100, 'anchor': 'center'},
                {'text': 'Status', 'key': 'status', 'width': 100, 'anchor': 'center'},
                {'text': 'Notes', 'key': 'notes', 'width': 200, 'anchor': 'w'},
            ]
            self.advanced_data_table = AdvancedDataTable(
                advanced_frame, columns, title="🛠️ Advanced Weather Data Management"
            )
    
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
    
    def _quick_search(self, location: str) -> None:
        """Handle quick location search."""
        if location == "Current Location":
            self.show_notification("Getting current location...", "info")
            # In a real app, you'd use geolocation here
            location = "Current Location (GPS)"
        
        if self.city_entry:
            self.city_entry.delete(0, tk.END)
            self.city_entry.insert(0, location)
            self.city_entry.configure(foreground="")
        
        self._on_search()
    
    def _show_settings(self) -> None:
        """Show advanced settings dialog."""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ Advanced Settings")
        settings_window.geometry("500x600")
        settings_window.transient(self.root)
        settings_window.grab_set()
        
        # Settings notebook
        settings_notebook = ttk.Notebook(settings_window)
        settings_notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # General settings tab
        general_frame = ttk.Frame(settings_notebook)
        settings_notebook.add(general_frame, text="🔧 General")
        
        # Units section
        units_section = ttk.LabelFrame(general_frame, text="📊 Units", padding=10)
        units_section.pack(fill="x", pady=(0, 10))
        
        # Temperature unit
        ttk.Label(units_section, text="Temperature:").grid(row=0, column=0, sticky="w", pady=2)
        temp_var = tk.StringVar(value=self.settings['temperature_unit'])
        temp_combo = ttk.Combobox(units_section, textvariable=temp_var, values=['C', 'F'], state="readonly", width=10)
        temp_combo.grid(row=0, column=1, sticky="w", padx=(10, 0), pady=2)
        
        # Wind speed unit
        ttk.Label(units_section, text="Wind Speed:").grid(row=1, column=0, sticky="w", pady=2)
        wind_var = tk.StringVar(value=self.settings['wind_speed_unit'])
        wind_combo = ttk.Combobox(units_section, textvariable=wind_var, values=['km/h', 'mph', 'm/s'], state="readonly", width=10)
        wind_combo.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=2)
        
        # Pressure unit
        ttk.Label(units_section, text="Pressure:").grid(row=2, column=0, sticky="w", pady=2)
        pressure_var = tk.StringVar(value=self.settings['pressure_unit'])
        pressure_combo = ttk.Combobox(units_section, textvariable=pressure_var, values=['hPa', 'inHg', 'mmHg'], state="readonly", width=10)
        pressure_combo.grid(row=2, column=1, sticky="w", padx=(10, 0), pady=2)
        
        # Behavior section
        behavior_section = ttk.LabelFrame(general_frame, text="🎯 Behavior", padding=10)
        behavior_section.pack(fill="x", pady=(0, 10))
        
        auto_save_var = tk.BooleanVar(value=self.settings['auto_save_favorites'])
        ttk.Checkbutton(behavior_section, text="Auto-save favorite locations", variable=auto_save_var).pack(anchor="w", pady=2)
        
        animations_var = tk.BooleanVar(value=self.settings['show_animations'])
        ttk.Checkbutton(behavior_section, text="Show animations", variable=animations_var).pack(anchor="w", pady=2)
        
        notifications_var = tk.BooleanVar(value=self.settings['show_notifications'])
        ttk.Checkbutton(behavior_section, text="Show notifications", variable=notifications_var).pack(anchor="w", pady=2)
        
        # Update interval
        ttk.Label(behavior_section, text="Auto-refresh interval (seconds):").pack(anchor="w", pady=(10, 2))
        interval_var = tk.IntVar(value=self.settings['update_interval'])
        interval_spin = ttk.Spinbox(behavior_section, from_=30, to=3600, textvariable=interval_var, width=10)
        interval_spin.pack(anchor="w", pady=2)
        
        # Buttons
        button_frame = ttk.Frame(settings_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        def save_settings():
            self.settings.update({
                'temperature_unit': temp_var.get(),
                'wind_speed_unit': wind_var.get(),
                'pressure_unit': pressure_var.get(),
                'auto_save_favorites': auto_save_var.get(),
                'show_animations': animations_var.get(),
                'show_notifications': notifications_var.get(),
                'update_interval': interval_var.get()
            })
            self.show_notification("Settings saved successfully!", "success")
            settings_window.destroy()
        
        ttk.Button(button_frame, text="Save", command=save_settings, style="Accent.TButton").pack(side="right", padx=(5, 0))
        ttk.Button(button_frame, text="Cancel", command=settings_window.destroy).pack(side="right")
    
    def _show_favorites(self) -> None:
        """Show favorites management dialog."""
        favorites_window = tk.Toplevel(self.root)
        favorites_window.title("⭐ Favorite Locations")
        favorites_window.geometry("400x500")
        favorites_window.transient(self.root)
        favorites_window.grab_set()
        
        # Header
        header_frame = ttk.Frame(favorites_window)
        header_frame.pack(fill="x", padx=10, pady=10)
        
        ttk.Label(header_frame, text="⭐ Favorite Locations", font=('Segoe UI', 14, 'bold')).pack(side="left")
        
        # Add current location button
        if hasattr(self, 'city_entry') and self.city_entry and self.city_entry.get().strip():
            current_city = self.city_entry.get().strip()
            if current_city not in self.favorites_list:
                add_btn = ttk.Button(
                    header_frame,
                    text=f"+ Add '{current_city}'",
                    command=lambda: self._add_to_favorites(current_city, favorites_listbox)
                )
                add_btn.pack(side="right")
        
        # Favorites list
        list_frame = ttk.LabelFrame(favorites_window, text="Saved Locations", padding=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Listbox with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill="both", expand=True)
        
        favorites_listbox = tk.Listbox(list_container, font=('Segoe UI', 10))
        scrollbar = ttk.Scrollbar(list_container, orient="vertical", command=favorites_listbox.yview)
        favorites_listbox.configure(yscrollcommand=scrollbar.set)
        
        favorites_listbox.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Populate favorites
        for favorite in self.favorites_list:
            favorites_listbox.insert(tk.END, favorite)
        
        # Buttons
        button_frame = ttk.Frame(favorites_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        def load_selected():
            if favorites_listbox.curselection():
                selected = favorites_listbox.get(favorites_listbox.curselection()[0])
                if self.city_entry:
                    self.city_entry.delete(0, tk.END)
                    self.city_entry.insert(0, selected)
                favorites_window.destroy()
                self._on_search()
        
        def remove_selected():
            if favorites_listbox.curselection():
                index = favorites_listbox.curselection()[0]
                selected = favorites_listbox.get(index)
                self.favorites_list.remove(selected)
                favorites_listbox.delete(index)
                self.show_notification(f"Removed '{selected}' from favorites", "info")
        
        ttk.Button(button_frame, text="Load", command=load_selected, style="Accent.TButton").pack(side="left")
        ttk.Button(button_frame, text="Remove", command=remove_selected).pack(side="left", padx=(5, 0))
        ttk.Button(button_frame, text="Close", command=favorites_window.destroy).pack(side="right")
    
    def _add_to_favorites(self, location: str, listbox: tk.Listbox) -> None:
        """Add location to favorites."""
        if location not in self.favorites_list:
            self.favorites_list.append(location)
            listbox.insert(tk.END, location)
            self.show_notification(f"Added '{location}' to favorites!", "success")
    
    def _toggle_temperature_unit(self) -> None:
        """Toggle between Celsius and Fahrenheit."""
        current = self.temp_unit_var.get()
        if current == "°C":
            self.temp_unit_var.set("°F")
            self.settings['temperature_unit'] = 'F'
        else:
            self.temp_unit_var.set("°C")
            self.settings['temperature_unit'] = 'C'
        
        self.show_notification(f"Temperature unit changed to {self.temp_unit_var.get()}", "info")
    
    def _create_stats_cards(self, parent: tk.Widget) -> None:
        """Create statistics cards at the top of the dashboard."""
        stats = [
            {"title": "Locations Tracked", "value": "12", "icon": "🌍", "trend": "+2"},
            {"title": "API Calls Today", "value": "847", "icon": "🔄", "trend": "+156"},
            {"title": "Avg Response Time", "value": "245ms", "icon": "⚡", "trend": "-12ms"},
            {"title": "Data Accuracy", "value": "99.8%", "icon": "🎯", "trend": "+0.1%"}
        ]
        
        for i, stat in enumerate(stats):
            if ModernCard:
                card = ModernCard(
                    parent,
                    title=f"{stat['icon']} {stat['value']}"
                )
                card.pack(side="left", fill="x", expand=True, padx=(0, 5) if i < 3 else (0, 0))
                
                # Add subtitle and trend in content frame
                content_frame = ttk.Frame(card.content_frame)
                content_frame.pack(fill="both", expand=True, pady=(0, 8))
                
                ttk.Label(content_frame, text=stat["title"], font=('Segoe UI', 10), foreground="gray").pack()
                ttk.Label(content_frame, text=stat["trend"], font=('Segoe UI', 10), foreground="green").pack()
            else:
                # Fallback card
                card_frame = ttk.LabelFrame(parent, text=stat["title"], padding=5)
                card_frame.pack(side="left", fill="x", expand=True, padx=(0, 5) if i < 3 else (0, 0))
                
                ttk.Label(card_frame, text=f"{stat['icon']} {stat['value']}", font=('Segoe UI', 14, 'bold')).pack()
                ttk.Label(card_frame, text=stat["trend"], font=('Segoe UI', 10), foreground="green").pack()
    
    def _create_quick_actions(self, parent: tk.Widget) -> None:
        """Create quick action buttons."""
        actions = [
            {"text": "📊 Export Data", "command": self._export_data},
            {"text": "📱 Share Weather", "command": self._share_weather},
            {"text": "🔔 Set Alert", "command": self._set_weather_alert},
            {"text": "📈 View Trends", "command": self._view_trends},
            {"text": "🌐 Weather Map", "command": self._show_weather_map}
        ]
        
        for action in actions:
            btn = ttk.Button(
                parent,
                text=action["text"],
                command=action["command"],
                style="Outline.TButton"
            )
            btn.pack(side="left", padx=(0, 10))
    
    def _export_data(self) -> None:
        """Export weather data."""
        self.show_notification("Data export feature coming soon!", "info")
    
    def _share_weather(self) -> None:
        """Share current weather."""
        self.show_notification("Weather sharing feature coming soon!", "info")
    
    def _set_weather_alert(self) -> None:
        """Set weather alert."""
        self.show_notification("Weather alerts feature coming soon!", "info")
    
    def _view_trends(self) -> None:
        """View weather trends."""
        # Switch to analytics tab if available
        if hasattr(self, 'main_notebook'):
            for i in range(self.main_notebook.index("end")):
                if "Analytics" in self.main_notebook.tab(i, "text"):
                    self.main_notebook.select(i)
                    self.show_notification("Switched to Analytics view", "success")
                    return
        self.show_notification("Analytics view not available", "warning")
    
    def _show_weather_map(self) -> None:
        """Show weather map."""
        self.show_notification("Weather map feature coming soon!", "info")
    
    def update_weather_display(self, weather_data: Dict[str, Any]) -> None:
        """Update the weather display with modern components."""
        if not self.weather_frame:
            return
            
        self._clear_frame(self.weather_frame)
        
        # Create main weather display with modern layout
        main_container = ttk.Frame(self.weather_frame)
        main_container.pack(fill="both", expand=True)
        
        # Left side - Temperature and basic info
        temp_frame = ttk.Frame(main_container)
        temp_frame.pack(side="left", fill="y", padx=(0, 20))
        
        # Large temperature display
        temp_value = weather_data.get('temperature', 0)
        unit_symbol = "°C" if self.settings['temperature_unit'] == 'C' else "°F"
        
        temp_label = ttk.Label(
            temp_frame,
            text=f"{temp_value}{unit_symbol}",
            style="Temperature.TLabel"
        )
        temp_label.pack()
        
        # Feels like temperature
        feels_like = weather_data.get('feels_like', temp_value)
        feels_like_label = ttk.Label(
            temp_frame,
            text=f"Feels like {feels_like}{unit_symbol}",
            style="FeelsLike.TLabel"
        )
        feels_like_label.pack()
        
        # Weather description
        description = weather_data.get('description', 'Unknown').title()
        desc_label = ttk.Label(
            temp_frame,
            text=description,
            style="Description.TLabel"
        )
        desc_label.pack(pady=(10, 0))
        
        # Right side - Weather details with gauges
        details_frame = ttk.Frame(main_container)
        details_frame.pack(side="right", fill="both", expand=True)
        
        # Create weather gauges if available
        if WeatherGauge:
            gauges_frame = ttk.Frame(details_frame)
            gauges_frame.pack(fill="x", pady=(0, 10))
            
            # Humidity gauge
            humidity = weather_data.get('humidity', 0)
            humidity_gauge = WeatherGauge(
                gauges_frame,
                title="Humidity",
                value=humidity,
                unit="%",
                min_val=0,
                max_val=100,
                size=80
            )
            humidity_gauge.pack(side="left", padx=(0, 10))
            
            # Pressure gauge (normalized to 0-100 scale)
            pressure = weather_data.get('pressure', 1013)
            pressure_normalized = ((pressure - 980) / (1050 - 980)) * 100
            pressure_gauge = WeatherGauge(
                gauges_frame,
                title="Pressure",
                value=pressure_normalized,
                unit="hPa",
                min_val=0,
                max_val=100,
                size=80
            )
            pressure_gauge.pack(side="left", padx=(0, 10))
            
            # Wind speed gauge
            wind_speed = weather_data.get('wind_speed', 0)
            wind_gauge = WeatherGauge(
                gauges_frame,
                title="Wind",
                value=min(wind_speed, 50),  # Cap at 50 for display
                unit=self.settings['wind_speed_unit'],
                min_val=0,
                max_val=50,
                size=80
            )
            wind_gauge.pack(side="left")
        
        # Weather details list
        details_list = ttk.Frame(details_frame)
        details_list.pack(fill="both", expand=True)
        
        details = [
            ("🌡️ Temperature", f"{temp_value}{unit_symbol}"),
            ("💧 Humidity", f"{weather_data.get('humidity', 0)}%"),
            ("🌪️ Pressure", f"{weather_data.get('pressure', 0)} {self.settings['pressure_unit']}"),
            ("💨 Wind Speed", f"{weather_data.get('wind_speed', 0)} {self.settings['wind_speed_unit']}"),
            ("🧭 Wind Direction", f"{weather_data.get('wind_direction', 0)}°"),
            ("👁️ Visibility", f"{weather_data.get('visibility', 0)} km"),
            ("☁️ Cloud Cover", f"{weather_data.get('clouds', 0)}%"),
        ]
        
        for i, (label, value) in enumerate(details):
            detail_frame = ttk.Frame(details_list)
            detail_frame.pack(fill="x", pady=2)
            
            ttk.Label(detail_frame, text=label, width=15).pack(side="left")
            ttk.Label(detail_frame, text=value, font=('Segoe UI', 10, 'bold')).pack(side="left", padx=(10, 0))
          # Add to recent searches if not already there
        location = weather_data.get('location', 'Unknown')
        if location not in self.recent_searches:
            self.recent_searches.insert(0, location)
            self.recent_searches = self.recent_searches[:10]  # Keep last 10
    
    def add_weather_to_history(self, weather_data: Dict[str, Any]) -> None:
        """Add weather data to history table if available."""
        if hasattr(self, 'weather_data_table') and self.weather_data_table:
            try:
                location = weather_data.get('location', 'Unknown Location')
                self.weather_data_table.add_weather_data(weather_data, location)
            except Exception as e:
                print(f"Error adding to weather history: {e}")
    
    def add_location_comparison(self, weather_data: Dict[str, Any]) -> None:
        """Add location to comparison table if available."""
        if hasattr(self, 'comparison_table') and self.comparison_table:
            try:
                location = weather_data.get('location', 'Unknown Location')
                self.comparison_table.add_location_data(location, weather_data)
            except Exception as e:
                print(f"Error adding to comparison: {e}")
    
    def update_analytics(self, weather_data: Dict[str, Any]) -> None:
        """Update analytics table if available."""
        if hasattr(self, 'analytics_table') and self.analytics_table:
            try:
                self.analytics_table.update_analytics(weather_data)
            except Exception as e:
                print(f"Error updating analytics: {e}")
    
    def _debug_moderncard_creation(self, *args, **kwargs):
        """Debug helper for ModernCard creation."""
        print(f"Creating ModernCard with args: {args}, kwargs: {kwargs}")
        if ModernCard:
            return ModernCard(*args, **kwargs)
        return None
