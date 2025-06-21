"""
Enhanced dashboard UI with modern UX/UI components.

This module provides an advanced weather dashboard with modern design elements,
animations, and enhanced user experience features.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, Callable, Dict, Any, List
from datetime import datetime
import threading

from .modern_components import (
    ModernCard, CircularProgress, ModernSearchBar, WeatherGauge,
    NotificationToast, ModernToggleSwitch, LoadingSpinner
)


class EnhancedWeatherDashboardUI:
    """Enhanced weather dashboard with modern UI/UX components."""
    
    def __init__(self, title: str = "🌦️ Weather Dominator Pro", theme: str = "darkly", size: tuple = (1400, 900)):
        """Initialize the enhanced UI."""
        self.root = ttk.Window(
            title=title,
            themename=theme,
            size=size,
            minsize=(1000, 700)
        )
        
        # Configure window
        self.root.attributes('-alpha', 0.0)  # Start transparent for fade-in
        
        # State variables
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.loading_var = tk.BooleanVar()
        self.auto_refresh_var = tk.BooleanVar()
        
        # Callbacks
        self.search_callback: Optional[Callable[[str], None]] = None
        self.theme_change_callback: Optional[Callable[[str], None]] = None
        self.auto_refresh_callback: Optional[Callable[[bool], None]] = None
        
        # UI components
        self.search_bar: Optional[ModernSearchBar] = None
        self.current_weather_card: Optional[ModernCard] = None
        self.forecast_card: Optional[ModernCard] = None
        self.air_quality_card: Optional[ModernCard] = None
        self.predictions_card: Optional[ModernCard] = None
        self.loading_spinner: Optional[LoadingSpinner] = None
        
        # Weather gauges
        self.temp_gauge: Optional[WeatherGauge] = None
        self.humidity_gauge: Optional[WeatherGauge] = None
        self.pressure_gauge: Optional[WeatherGauge] = None
        self.wind_gauge: Optional[WeatherGauge] = None
        
        # Progress indicators
        self.air_quality_progress: Optional[CircularProgress] = None
        
        self._setup_ui()
        self._fade_in()
    
    def _fade_in(self):
        """Fade in the window on startup."""
        def fade():
            for i in range(21):
                alpha = i / 20
                self.root.attributes('-alpha', alpha)
                self.root.update()
                threading.Event().wait(0.02)
        
        threading.Thread(target=fade, daemon=True).start()
    
    def _setup_ui(self):
        """Set up the enhanced user interface."""
        self._create_header()
        self._create_main_dashboard()
        self._create_status_bar()
        self._create_sidebar()
    
    def _create_header(self):
        """Create the enhanced header with modern search."""
        header_frame = ttk.Frame(self.root, padding=(20, 15))
        header_frame.pack(fill="x")
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title with gradient effect
        title_frame = ttk.Frame(header_frame)
        title_frame.grid(row=0, column=0, sticky="w")
        
        title_label = ttk.Label(
            title_frame,
            text="🌦️ Weather Dominator Pro",
            font=('Segoe UI', 24, 'bold'),
            foreground="#2196F3"
        )
        title_label.pack()
        
        subtitle_label = ttk.Label(
            title_frame,
            text="Advanced Weather Intelligence Platform",
            font=('Segoe UI', 11),
            foreground="gray"
        )
        subtitle_label.pack()
        
        # Modern search bar
        search_frame = ttk.Frame(header_frame)
        search_frame.grid(row=0, column=1, sticky="ew", padx=(20, 0))
        search_frame.grid_columnconfigure(0, weight=1)
        
        self.search_bar = ModernSearchBar(
            search_frame,
            placeholder="Search for cities... (e.g., London, Tokyo, New York)"
        )
        self.search_bar.grid(row=0, column=0, sticky="ew")
        
        # Controls panel
        controls_frame = ttk.Frame(header_frame)
        controls_frame.grid(row=0, column=2, sticky="e", padx=(20, 0))
        
        # Theme selector
        theme_frame = ttk.Frame(controls_frame)
        theme_frame.pack(pady=(0, 5))
        
        ttk.Label(theme_frame, text="Theme:", font=('Segoe UI', 10)).pack(side="left", padx=(0, 5))
        
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
        self.auto_refresh_toggle = ModernToggleSwitch(
            controls_frame,
            text="Auto-refresh (5min)",
            initial_state=False
        )
        self.auto_refresh_toggle.pack(pady=(5, 0))
        self.auto_refresh_toggle.set_callback(self._on_auto_refresh_toggle)
        
        # Loading indicator
        self.loading_spinner = LoadingSpinner(controls_frame, size=30)
        self.loading_spinner.pack(pady=(5, 0))
    
    def _create_main_dashboard(self):
        """Create the main dashboard area with cards."""
        main_frame = ttk.Frame(self.root, padding=(20, 10))
        main_frame.pack(fill="both", expand=True)
        main_frame.grid_columnconfigure(0, weight=2)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_rowconfigure(1, weight=1)
        
        # Left panel - Main weather info
        left_panel = ttk.Frame(main_frame)
        left_panel.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=(0, 10))
        left_panel.grid_rowconfigure(0, weight=1)
        left_panel.grid_rowconfigure(1, weight=1)
        left_panel.grid_columnconfigure(0, weight=1)
        
        # Current weather card
        self.current_weather_card = ModernCard(left_panel, title="Current Weather")
        self.current_weather_card.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        
        # Forecast card
        self.forecast_card = ModernCard(left_panel, title="📊 7-Day Forecast")
        self.forecast_card.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        
        # Right panel - Additional info
        right_panel = ttk.Frame(main_frame)
        right_panel.grid(row=0, column=1, rowspan=2, sticky="nsew")
        right_panel.grid_rowconfigure(0, weight=1)
        right_panel.grid_rowconfigure(1, weight=1)
        right_panel.grid_columnconfigure(0, weight=1)
        
        # Air quality card
        self.air_quality_card = ModernCard(right_panel, title="🌬️ Air Quality Index")
        self.air_quality_card.grid(row=0, column=0, sticky="nsew", pady=(0, 5))
        
        # ML Predictions card
        self.predictions_card = ModernCard(right_panel, title="🤖 AI Weather Intelligence")
        self.predictions_card.grid(row=1, column=0, sticky="nsew", pady=(5, 0))
        
        # Initialize card content
        self._setup_card_content()
    
    def _setup_card_content(self):
        """Set up initial content for cards."""
        # Current weather card content
        weather_content = self.current_weather_card.get_content_frame()
        weather_content.grid_columnconfigure(0, weight=1)
        weather_content.grid_columnconfigure(1, weight=1)
        weather_content.grid_rowconfigure(1, weight=1)
        
        # Temperature display area
        temp_display_frame = ttk.Frame(weather_content)
        temp_display_frame.grid(row=0, column=0, columnspan=2, pady=10)
        
        self.temp_label = ttk.Label(
            temp_display_frame,
            text="--°C",
            font=('Segoe UI', 48, 'bold'),
            foreground="#FF6B35"
        )
        self.temp_label.pack()
        
        self.feels_like_label = ttk.Label(
            temp_display_frame,
            text="Feels like --°C",
            font=('Segoe UI', 14),
            foreground="gray"
        )
        self.feels_like_label.pack()
        
        self.description_label = ttk.Label(
            temp_display_frame,
            text="Loading weather data...",
            font=('Segoe UI', 16)
        )
        self.description_label.pack(pady=5)
        
        # Weather gauges
        gauges_frame = ttk.Frame(weather_content)
        gauges_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", pady=10)
        gauges_frame.grid_columnconfigure(0, weight=1)
        gauges_frame.grid_columnconfigure(1, weight=1)
        gauges_frame.grid_rowconfigure(0, weight=1)
        gauges_frame.grid_rowconfigure(1, weight=1)
        
        # Create weather gauges
        self.humidity_gauge = WeatherGauge(
            gauges_frame, size=120, min_val=0, max_val=100, unit="%", title="Humidity"
        )
        self.humidity_gauge.grid(row=0, column=0, padx=5, pady=5)
        
        self.pressure_gauge = WeatherGauge(
            gauges_frame, size=120, min_val=950, max_val=1050, unit=" hPa", title="Pressure"
        )
        self.pressure_gauge.grid(row=0, column=1, padx=5, pady=5)
        
        self.wind_gauge = WeatherGauge(
            gauges_frame, size=120, min_val=0, max_val=30, unit=" m/s", title="Wind Speed"
        )
        self.wind_gauge.grid(row=1, column=0, padx=5, pady=5)
        
        # Cloud coverage gauge\n        cloud_gauge = WeatherGauge(\n            gauges_frame, size=120, min_val=0, max_val=100, unit=\"%\", title=\"Clouds\"\n        )\n        cloud_gauge.grid(row=1, column=1, padx=5, pady=5)\n        self.cloud_gauge = cloud_gauge\n        \n        # Air quality card content\n        air_content = self.air_quality_card.get_content_frame()\n        air_content.grid_columnconfigure(0, weight=1)\n        air_content.grid_rowconfigure(1, weight=1)\n        \n        # AQI progress indicator\n        aqi_frame = ttk.Frame(air_content)\n        aqi_frame.grid(row=0, column=0, pady=20)\n        \n        self.air_quality_progress = CircularProgress(aqi_frame, size=150, thickness=12)\n        self.air_quality_progress.pack()\n        \n        self.aqi_label = ttk.Label(\n            aqi_frame,\n            text=\"AQI: --\",\n            font=('Segoe UI', 18, 'bold')\n        )\n        self.aqi_label.pack(pady=(10, 0))\n        \n        self.aqi_status_label = ttk.Label(\n            aqi_frame,\n            text=\"Loading...\",\n            font=('Segoe UI', 12),\n            foreground=\"gray\"\n        )\n        self.aqi_status_label.pack()\n        \n        # Pollutants details\n        pollutants_frame = ttk.LabelFrame(air_content, text=\"Pollutant Levels\", padding=10)\n        pollutants_frame.grid(row=1, column=0, sticky=\"nsew\", pady=10)\n        \n        self.pollutants_labels = {}\n        pollutants = [\"PM2.5\", \"PM10\", \"NO₂\", \"SO₂\", \"CO\", \"O₃\"]\n        \n        for i, pollutant in enumerate(pollutants):\n            row = i // 2\n            col = i % 2\n            \n            label = ttk.Label(\n                pollutants_frame,\n                text=f\"{pollutant}: -- μg/m³\",\n                font=('Segoe UI', 10)\n            )\n            label.grid(row=row, column=col, sticky=\"w\", padx=10, pady=2)\n            self.pollutants_labels[pollutant] = label\n        \n        # ML Predictions card content\n        predictions_content = self.predictions_card.get_content_frame()\n        predictions_content.grid_columnconfigure(0, weight=1)\n        \n        # AI status indicator\n        ai_status_frame = ttk.Frame(predictions_content)\n        ai_status_frame.grid(row=0, column=0, pady=10)\n        \n        ai_icon = ttk.Label(\n            ai_status_frame,\n            text=\"🧠\",\n            font=('Segoe UI', 24)\n        )\n        ai_icon.pack()\n        \n        self.ai_status_label = ttk.Label(\n            ai_status_frame,\n            text=\"AI Engine: Standby\",\n            font=('Segoe UI', 12, 'bold')\n        )\n        self.ai_status_label.pack()\n        \n        # Predictions list\n        predictions_list_frame = ttk.LabelFrame(\n            predictions_content,\n            text=\"Smart Predictions\",\n            padding=10\n        )\n        predictions_list_frame.grid(row=1, column=0, sticky=\"nsew\", pady=10)\n        predictions_content.grid_rowconfigure(1, weight=1)\n        \n        self.predictions_text = tk.Text(\n            predictions_list_frame,\n            height=8,\n            font=('Segoe UI', 10),\n            wrap=tk.WORD,\n            state=tk.DISABLED\n        )\n        self.predictions_text.pack(fill=\"both\", expand=True)\n        \n        # Forecast card content\n        forecast_content = self.forecast_card.get_content_frame()\n        forecast_content.grid_columnconfigure(0, weight=1)\n        forecast_content.grid_rowconfigure(0, weight=1)\n        \n        # Forecast scroll area\n        forecast_scroll_frame = ttk.Frame(forecast_content)\n        forecast_scroll_frame.grid(row=0, column=0, sticky=\"nsew\")\n        forecast_scroll_frame.grid_columnconfigure(0, weight=1)\n        forecast_scroll_frame.grid_rowconfigure(0, weight=1)\n        \n        # Canvas for custom forecast display\n        self.forecast_canvas = tk.Canvas(\n            forecast_scroll_frame,\n            highlightthickness=0\n        )\n        self.forecast_canvas.grid(row=0, column=0, sticky=\"nsew\")\n        \n        forecast_scrollbar = ttk.Scrollbar(\n            forecast_scroll_frame,\n            orient=\"vertical\",\n            command=self.forecast_canvas.yview\n        )\n        forecast_scrollbar.grid(row=0, column=1, sticky=\"ns\")\n        \n        self.forecast_canvas.configure(yscrollcommand=forecast_scrollbar.set)\n        \n        # Forecast frame inside canvas\n        self.forecast_inner_frame = ttk.Frame(self.forecast_canvas)\n        self.forecast_canvas.create_window((0, 0), window=self.forecast_inner_frame, anchor=\"nw\")\n        \n        # Initial forecast message\n        initial_message = ttk.Label(\n            self.forecast_inner_frame,\n            text=\"📊 Forecast data will appear here after searching for a location\",\n            font=('Segoe UI', 12),\n            foreground=\"gray\"\n        )\n        initial_message.pack(pady=50)\n    \n    def _create_sidebar(self):\n        \"\"\"Create an expandable sidebar with additional features.\"\"\"\n        # Sidebar toggle button\n        self.sidebar_visible = tk.BooleanVar(value=False)\n        \n        toggle_frame = ttk.Frame(self.root)\n        toggle_frame.place(x=0, y=100)\n        \n        self.sidebar_toggle = ttk.Button(\n            toggle_frame,\n            text=\"⚙️\",\n            width=3,\n            command=self._toggle_sidebar\n        )\n        self.sidebar_toggle.pack()\n        \n        # Sidebar frame (initially hidden)\n        self.sidebar_frame = ttk.Frame(self.root, width=250, padding=10)\n        \n        # Sidebar content\n        sidebar_title = ttk.Label(\n            self.sidebar_frame,\n            text=\"⚙️ Settings\",\n            font=('Segoe UI', 14, 'bold')\n        )\n        sidebar_title.pack(pady=(0, 20))\n        \n        # Settings options\n        settings_frame = ttk.LabelFrame(self.sidebar_frame, text=\"Preferences\", padding=10)\n        settings_frame.pack(fill=\"x\", pady=(0, 10))\n        \n        # Temperature unit toggle\n        self.temp_unit_toggle = ModernToggleSwitch(\n            settings_frame,\n            text=\"Use Fahrenheit\",\n            initial_state=False\n        )\n        self.temp_unit_toggle.pack(fill=\"x\", pady=5)\n        \n        # Notifications toggle\n        self.notifications_toggle = ModernToggleSwitch(\n            settings_frame,\n            text=\"Weather Alerts\",\n            initial_state=True\n        )\n        self.notifications_toggle.pack(fill=\"x\", pady=5)\n        \n        # Advanced features\n        advanced_frame = ttk.LabelFrame(self.sidebar_frame, text=\"Advanced\", padding=10)\n        advanced_frame.pack(fill=\"x\", pady=(0, 10))\n        \n        # Export data button\n        export_btn = ttk.Button(\n            advanced_frame,\n            text=\"📄 Export Data\",\n            command=self._export_data\n        )\n        export_btn.pack(fill=\"x\", pady=2)\n        \n        # Weather maps button\n        maps_btn = ttk.Button(\n            advanced_frame,\n            text=\"🗺️ Weather Maps\",\n            command=self._show_weather_maps\n        )\n        maps_btn.pack(fill=\"x\", pady=2)\n        \n        # About button\n        about_btn = ttk.Button(\n            advanced_frame,\n            text=\"ℹ️ About\",\n            command=self._show_about\n        )\n        about_btn.pack(fill=\"x\", pady=2)\n    \n    def _toggle_sidebar(self):\n        \"\"\"Toggle sidebar visibility with animation.\"\"\"\n        if self.sidebar_visible.get():\n            # Hide sidebar\n            self.sidebar_frame.place_forget()\n            self.sidebar_toggle.configure(text=\"⚙️\")\n            self.sidebar_visible.set(False)\n        else:\n            # Show sidebar\n            self.sidebar_frame.place(x=0, y=0, relheight=1)\n            self.sidebar_toggle.configure(text=\"✕\")\n            self.sidebar_visible.set(True)\n    \n    def _create_status_bar(self):\n        \"\"\"Create an enhanced status bar.\"\"\"\n        status_frame = ttk.Frame(self.root, padding=(20, 5))\n        status_frame.pack(fill=\"x\", side=\"bottom\")\n        status_frame.grid_columnconfigure(1, weight=1)\n        \n        # Status indicator\n        status_indicator = ttk.Label(\n            status_frame,\n            text=\"🟢\",\n            font=('Segoe UI', 12)\n        )\n        status_indicator.grid(row=0, column=0, padx=(0, 5))\n        \n        # Status text\n        status_label = ttk.Label(\n            status_frame,\n            textvariable=self.status_var,\n            font=('Segoe UI', 10)\n        )\n        status_label.grid(row=0, column=1, sticky=\"w\")\n        \n        # Last update time\n        self.last_update_label = ttk.Label(\n            status_frame,\n            text=\"Last update: Never\",\n            font=('Segoe UI', 9),\n            foreground=\"gray\"\n        )\n        self.last_update_label.grid(row=0, column=2, sticky=\"e\")\n        \n        # API info button\n        api_btn = ttk.Button(\n            status_frame,\n            text=\"ℹ️ API Info\",\n            command=self._show_api_info\n        )\n        api_btn.grid(row=0, column=3, padx=(10, 0))\n    \n    # Callback setters\n    def set_search_callback(self, callback: Callable[[str], None]):\n        \"\"\"Set search callback.\"\"\"\n        self.search_callback = callback\n        if self.search_bar:\n            self.search_bar.set_search_callback(callback)\n    \n    def set_theme_change_callback(self, callback: Callable[[str], None]):\n        \"\"\"Set theme change callback.\"\"\"\n        self.theme_change_callback = callback\n    \n    def set_auto_refresh_callback(self, callback: Callable[[bool], None]):\n        \"\"\"Set auto-refresh callback.\"\"\"\n        self.auto_refresh_callback = callback\n    \n    def set_suggestions_callback(self, callback: Callable[[str], List[str]]):\n        \"\"\"Set city suggestions callback.\"\"\"\n        if self.search_bar:\n            self.search_bar.set_suggestions_callback(callback)\n    \n    # Event handlers\n    def _on_theme_change(self, event=None):\n        \"\"\"Handle theme change.\"\"\"\n        theme = self.theme_var.get()\n        if theme and self.theme_change_callback:\n            self.theme_change_callback(theme)\n    \n    def _on_auto_refresh_toggle(self, enabled: bool):\n        \"\"\"Handle auto-refresh toggle.\"\"\"\n        if self.auto_refresh_callback:\n            self.auto_refresh_callback(enabled)\n    \n    # UI update methods\n    def update_status(self, message: str):\n        \"\"\"Update status bar message.\"\"\"\n        self.status_var.set(message)\n        self.last_update_label.configure(text=f\"Last update: {datetime.now().strftime('%H:%M:%S')}\")\n    \n    def show_loading(self, show: bool = True):\n        \"\"\"Show or hide loading indicator.\"\"\"\n        if show:\n            self.loading_spinner.start_spinning()\n        else:\n            self.loading_spinner.stop_spinning()\n    \n    def show_notification(self, message: str, notification_type: str = \"info\", duration: float = 3.0):\n        \"\"\"Show a notification toast.\"\"\"\n        NotificationToast(self.root, message, notification_type, duration)\n    \n    def update_weather_display(self, weather_data):\n        \"\"\"Update the weather display with new data.\"\"\"\n        if not weather_data:\n            return\n        \n        # Update temperature display\n        self.temp_label.configure(text=f\"{weather_data.temperature:.1f}°C\")\n        self.feels_like_label.configure(text=f\"Feels like {weather_data.feels_like:.1f}°C\")\n        self.description_label.configure(text=weather_data.description.title())\n        \n        # Update gauges with animation\n        if self.humidity_gauge:\n            self.humidity_gauge.set_value(weather_data.humidity)\n        if self.pressure_gauge:\n            self.pressure_gauge.set_value(weather_data.pressure)\n        if self.wind_gauge:\n            self.wind_gauge.set_value(weather_data.wind_speed)\n        if hasattr(self, 'cloud_gauge'):\n            self.cloud_gauge.set_value(weather_data.cloudiness)\n    \n    def update_air_quality_display(self, aqi_data):\n        \"\"\"Update the air quality display.\"\"\"\n        if not aqi_data:\n            return\n        \n        # Update AQI progress\n        aqi_normalized = aqi_data.aqi / 5.0  # Normalize to 0-1\n        if self.air_quality_progress:\n            self.air_quality_progress.set_progress(aqi_normalized)\n        \n        # Update labels\n        aqi_levels = {\n            1: \"Good\", 2: \"Fair\", 3: \"Moderate\", 4: \"Poor\", 5: \"Very Poor\"\n        }\n        aqi_text = aqi_levels.get(aqi_data.aqi, \"Unknown\")\n        \n        self.aqi_label.configure(text=f\"AQI: {aqi_data.aqi}\")\n        self.aqi_status_label.configure(text=aqi_text)\n        \n        # Update pollutant levels\n        pollutant_values = {\n            \"PM2.5\": aqi_data.pm2_5,\n            \"PM10\": aqi_data.pm10,\n            \"NO₂\": aqi_data.no2,\n            \"SO₂\": getattr(aqi_data, 'so2', 0),\n            \"CO\": getattr(aqi_data, 'co', 0),\n            \"O₃\": getattr(aqi_data, 'o3', 0)\n        }\n        \n        for pollutant, value in pollutant_values.items():\n            if pollutant in self.pollutants_labels:\n                self.pollutants_labels[pollutant].configure(\n                    text=f\"{pollutant}: {value:.1f} μg/m³\"\n                )\n    \n    def update_predictions_display(self, predictions: str):\n        \"\"\"Update the AI predictions display.\"\"\"\n        self.ai_status_label.configure(text=\"AI Engine: Active\")\n        \n        self.predictions_text.configure(state=tk.NORMAL)\n        self.predictions_text.delete(1.0, tk.END)\n        self.predictions_text.insert(tk.END, predictions)\n        self.predictions_text.configure(state=tk.DISABLED)\n    \n    def update_forecast_display(self, forecast_data):\n        \"\"\"Update the forecast display.\"\"\"\n        # Clear existing forecast\n        for widget in self.forecast_inner_frame.winfo_children():\n            widget.destroy()\n        \n        if not forecast_data or not forecast_data.daily:\n            no_data_label = ttk.Label(\n                self.forecast_inner_frame,\n                text=\"No forecast data available\",\n                font=('Segoe UI', 12),\n                foreground=\"gray\"\n            )\n            no_data_label.pack(pady=20)\n            return\n        \n        # Create forecast items\n        for i, day_data in enumerate(forecast_data.daily[:7]):\n            day_frame = ttk.Frame(self.forecast_inner_frame, padding=10)\n            day_frame.pack(fill=\"x\", pady=2)\n            day_frame.grid_columnconfigure(2, weight=1)\n            \n            # Date\n            date_obj = datetime.fromtimestamp(day_data['dt'])\n            date_str = date_obj.strftime(\"%a, %b %d\")\n            \n            date_label = ttk.Label(\n                day_frame,\n                text=date_str,\n                font=('Segoe UI', 11, 'bold'),\n                width=12\n            )\n            date_label.grid(row=0, column=0, sticky=\"w\")\n            \n            # Weather icon (emoji)\n            weather_main = day_data['weather'][0]['main'].lower()\n            weather_icons = {\n                'clear': '☀️',\n                'clouds': '☁️',\n                'rain': '🌧️',\n                'snow': '❄️',\n                'thunderstorm': '⛈️',\n                'drizzle': '🌦️',\n                'mist': '🌫️',\n                'fog': '🌫️'\n            }\n            icon = weather_icons.get(weather_main, '🌤️')\n            \n            icon_label = ttk.Label(\n                day_frame,\n                text=icon,\n                font=('Segoe UI', 16)\n            )\n            icon_label.grid(row=0, column=1, padx=10)\n            \n            # Description\n            desc_label = ttk.Label(\n                day_frame,\n                text=day_data['weather'][0]['description'].title(),\n                font=('Segoe UI', 10),\n                foreground=\"gray\"\n            )\n            desc_label.grid(row=0, column=2, sticky=\"w\")\n            \n            # Temperature\n            if 'temp' in day_data:\n                temp_text = f\"{day_data['temp']['max']:.0f}° / {day_data['temp']['min']:.0f}°\"\n            else:\n                temp_text = \"--° / --°\"\n            \n            temp_label = ttk.Label(\n                day_frame,\n                text=temp_text,\n                font=('Segoe UI', 11, 'bold')\n            )\n            temp_label.grid(row=0, column=3, sticky=\"e\")\n        \n        # Update scroll region\n        self.forecast_inner_frame.update_idletasks()\n        self.forecast_canvas.configure(scrollregion=self.forecast_canvas.bbox(\"all\"))\n    \n    # Utility methods\n    def _export_data(self):\n        \"\"\"Export weather data.\"\"\"\n        self.show_notification(\"Export feature coming soon!\", \"info\")\n    \n    def _show_weather_maps(self):\n        \"\"\"Show weather maps.\"\"\"\n        self.show_notification(\"Weather maps feature coming soon!\", \"info\")\n    \n    def _show_about(self):\n        \"\"\"Show about dialog.\"\"\"\n        about_text = \"\"\"Weather Dominator Pro v2.0\n        \nAdvanced Weather Intelligence Platform\nFeaturing AI-powered predictions and modern UI.\n        \nDeveloped with ❤️ using Python & ttkbootstrap\"\"\"\n        \n        # Create about window\n        about_window = ttk.Toplevel(self.root)\n        about_window.title(\"About Weather Dominator Pro\")\n        about_window.geometry(\"400x200\")\n        about_window.resizable(False, False)\n        \n        # Center the window\n        about_window.transient(self.root)\n        about_window.grab_set()\n        \n        about_label = ttk.Label(\n            about_window,\n            text=about_text,\n            font=('Segoe UI', 10),\n            justify=\"center\"\n        )\n        about_label.pack(expand=True, pady=20)\n        \n        close_btn = ttk.Button(\n            about_window,\n            text=\"Close\",\n            command=about_window.destroy\n        )\n        close_btn.pack(pady=(0, 20))\n    \n    def _show_api_info(self):\n        \"\"\"Show API information.\"\"\"\n        info_text = \"\"\"OpenWeatherMap API Features:\n        \n• Current weather data for any location\n• 7-day detailed weather forecasts\n• Air quality monitoring with pollutant data\n• Advanced geocoding for city suggestions\n• Weather maps and satellite imagery\n• Historical weather data access\n        \nRate Limits:\n• 60 calls per minute\n• 1,000,000 calls per month\n• Optimized for learning and development\n        \nPerfect for weather intelligence applications!\"\"\"\n        \n        self.show_notification(\"Check console for API details\", \"info\")\n        print(info_text)\n    \n    def run(self):\n        \"\"\"Start the application.\"\"\"\n        try:\n            self.root.mainloop()\n        except KeyboardInterrupt:\n            print(\"\\nApplication interrupted by user\")\n        except Exception as e:\n            print(f\"Application error: {e}\")\n            self.show_notification(f\"Application error: {e}\", \"error\")\n    \n    def show_error(self, title: str, message: str):\n        \"\"\"Show error notification.\"\"\"\n        self.show_notification(f\"{title}: {message}\", \"error\")\n    \n    def show_info(self, title: str, message: str):\n        \"\"\"Show info notification.\"\"\"\n        self.show_notification(f\"{title}: {message}\", \"info\")\n    \n    # Property getters for compatibility\n    @property\n    def weather_frame(self):\n        \"\"\"Get weather frame for compatibility.\"\"\"\n        return self.current_weather_card.get_content_frame() if self.current_weather_card else None\n    \n    @property\n    def air_quality_frame(self):\n        \"\"\"Get air quality frame for compatibility.\"\"\"\n        return self.air_quality_card.get_content_frame() if self.air_quality_card else None\n    \n    @property\n    def forecast_frame(self):\n        \"\"\"Get forecast frame for compatibility.\"\"\"\n        return self.forecast_card.get_content_frame() if self.forecast_card else None\n    \n    @property\n    def predictions_frame(self):\n        \"\"\"Get predictions frame for compatibility.\"\"\"\n        return self.predictions_card.get_content_frame() if self.predictions_card else None
