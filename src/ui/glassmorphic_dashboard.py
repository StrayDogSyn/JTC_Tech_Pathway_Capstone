"""
Glassmorphic Weather Dashboard UI with modern frosted glass design.

This module provides the main weather dashboard UI using glassmorphic design
components for a modern, translucent aesthetic.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, Callable, Dict, Any, List
from datetime import datetime
import threading
import time

# Import glassmorphic components
from .glassmorphic_components import (
    GlassmorphicFrame, GlassmorphicCard, GlassmorphicButton,
    GlassmorphicSearchBar, GlassmorphicProgressBar, GlassmorphicWeatherCard,
    GlassmorphicStyle
)

# Fallback imports for existing components
try:
    from .modern_components import (
        ModernCard, CircularProgress, ModernSearchBar, WeatherGauge,
        NotificationToast, ModernToggleSwitch, LoadingSpinner
    )
except ImportError:
    ModernCard = None
    CircularProgress = None
    ModernSearchBar = None
    WeatherGauge = None
    NotificationToast = None
    ModernToggleSwitch = None
    LoadingSpinner = None


class GlassmorphicWeatherDashboard:
    """Glassmorphic weather dashboard with modern frosted glass design."""
    
    def __init__(self, title: str = "🌦️ Weather Intelligence", theme: str = "dark", size: tuple = (1400, 900)):
        """Initialize the glassmorphic dashboard."""
        self.root = ttk.Window(
            title=title,
            themename="darkly",  # Base theme for contrast
            size=size,
            minsize=(1200, 800)
        )
          # Glassmorphic theme configuration  
        # Map ttkbootstrap themes to glassmorphic themes
        theme_mapping = {
            "darkly": "dark",
            "superhero": "dark", 
            "vapor": "aurora",
            "flatly": "light",
            "litera": "light",
            "minty": "light"
        }
        self.glass_theme = theme_mapping.get(theme, "dark")  # Default to dark theme
        self.colors = GlassmorphicStyle.GLASS_COLORS[self.glass_theme]
        
        # Configure window for glassmorphic appearance
        self.root.configure(bg=self.colors["background"])
        self.root.attributes('-alpha', 0.0)  # Start transparent for fade-in
        
        # Status variables
        self.status_var = tk.StringVar()
        self.status_var.set("🌐 Glass Weather Dashboard - Ready")
        self.loading_var = tk.BooleanVar()
        
        # Callbacks
        self.search_callback: Optional[Callable[[str], None]] = None
        self.theme_change_callback: Optional[Callable[[str], None]] = None
        
        # UI components
        self.search_bar: Optional[GlassmorphicSearchBar] = None
        self.weather_cards: Dict[str, GlassmorphicWeatherCard] = {}
        self.progress_bar: Optional[GlassmorphicProgressBar] = None
        
        # Weather data frames
        self.weather_frame: Optional[GlassmorphicCard] = None
        self.forecast_frame: Optional[GlassmorphicCard] = None
        self.air_quality_frame: Optional[GlassmorphicCard] = None
        self.predictions_frame: Optional[GlassmorphicCard] = None
        
        # Current weather data
        self._current_weather_data: Optional[Dict[str, Any]] = None
        
        # Setup UI
        self._setup_glassmorphic_ui()
        self._setup_glassmorphic_styles()
        self._fade_in_window()
    
    def _fade_in_window(self):
        """Smooth fade-in effect for the window."""
        def fade():
            for i in range(21):
                alpha = i / 20
                try:
                    self.root.attributes('-alpha', alpha)
                    self.root.update()
                    time.sleep(0.03)
                except:
                    break
        
        threading.Thread(target=fade, daemon=True).start()
    
    def _setup_glassmorphic_styles(self):
        """Setup glassmorphic-specific styles."""
        style = ttk.Style()
        
        # Glass frame styles
        style.configure("Glass.TFrame", 
                       background=self.colors["background"],
                       relief="flat", 
                       borderwidth=0)
          # Glass label styles  
        style.configure("Glass.TLabel",
                       background=self.colors["glass_bg"],
                       foreground=self.colors["text_primary"],
                       font=('Segoe UI', 10))
        
        style.configure("GlassTitle.TLabel",
                       background=self.colors["glass_bg"], 
                       foreground=self.colors["text_primary"],
                       font=('Segoe UI', 16, 'bold'))
        
        style.configure("GlassSubtitle.TLabel",
                       background=self.colors["glass_bg"],
                       foreground=self.colors["text_secondary"], 
                       font=('Segoe UI', 11))
    
    def _setup_glassmorphic_ui(self):
        """Setup the main glassmorphic UI layout."""
        # Main container with glassmorphic background
        self.main_container = GlassmorphicFrame(
            self.root, 
            style_theme=self.glass_theme,
            blur_intensity=0.2
        )
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create glassmorphic header
        self._create_glassmorphic_header()        
        # Create main content area
        self._create_glassmorphic_content()
        
        # Create glassmorphic status bar
        self._create_glassmorphic_status_bar()
    
    def _create_glassmorphic_header(self):
        """Create the glassmorphic header with search and branding."""
        header_card = GlassmorphicCard(
            self.main_container.content_frame,
            style_theme=self.glass_theme
        )
        header_card.pack(fill="x", padx=15, pady=(15, 10))
        
        # Header layout frame
        header_layout = ttk.Frame(header_card.content_frame, style="Glass.TFrame")
        header_layout.pack(fill="x", padx=10, pady=10)
        header_layout.grid_columnconfigure(1, weight=1)
        
        # Branding section
        brand_frame = ttk.Frame(header_layout, style="Glass.TFrame")
        brand_frame.grid(row=0, column=0, sticky="w")
        
        # Main title with glassmorphic styling
        title_label = ttk.Label(
            brand_frame,
            text="🌦️ Glass Weather",
            style="GlassTitle.TLabel"
        )
        title_label.pack(anchor="w")
        
        # Subtitle
        subtitle_label = ttk.Label(
            brand_frame,
            text="Transparent Intelligence",
            style="GlassSubtitle.TLabel"
        )
        subtitle_label.pack(anchor="w")
        
        # Search section - Create a proper search frame
        search_frame = ttk.Frame(header_layout, style="Glass.TFrame")
        search_frame.grid(row=0, column=1, sticky="ew", padx=(20, 0))
        
        # Search container with glassmorphic styling
        search_container = GlassmorphicFrame(search_frame, style_theme=self.glass_theme)
        search_container.pack(fill="x")
        
        # Search components frame
        search_components = ttk.Frame(search_container.content_frame)
        search_components.pack(fill="x", padx=8, pady=5)
        search_components.grid_columnconfigure(1, weight=1)
        
        # Search icon
        search_icon = ttk.Label(
            search_components,
            text="🔍",
            font=("Segoe UI", 12),
            foreground=self.colors["text_secondary"]
        )
        search_icon.grid(row=0, column=0, padx=(5, 10))
          # Search entry
        self.city_entry = ttk.Entry(
            search_components,
            font=("Segoe UI", 11),
            width=25
        )
        self.city_entry.grid(row=0, column=1, sticky="ew", pady=2)
        self.city_entry.bind('<Return>', self._on_search_enter)
        
        # Add placeholder text
        self.city_entry.insert(0, "Enter city name...")
        self.city_entry.bind('<FocusIn>', self._on_entry_focus_in)
        self.city_entry.bind('<FocusOut>', self._on_entry_focus_out)
        self._entry_placeholder = True
        
        # Search button
        search_btn = GlassmorphicButton(
            search_components,
            text="Search",
            command=self._on_search_button,
            style_theme=self.glass_theme
        )
        search_btn.grid(row=0, column=2, padx=(10, 5))
        
        # Theme controls
        controls_frame = ttk.Frame(header_layout, style="Glass.TFrame")
        controls_frame.grid(row=0, column=2, sticky="e", padx=(20, 0))
        
        # Theme selection buttons
        theme_buttons = [
            ("🌙", "dark", "Dark Theme"),
            ("☀️", "light", "Light Theme"), 
            ("🌌", "aurora", "Aurora Theme")
        ]
        
        for emoji, theme, tooltip in theme_buttons:
            btn = GlassmorphicButton(
                controls_frame,
                text=emoji,
                command=lambda t=theme: self._change_theme(t),
                style_theme=self.glass_theme
            )
            btn.pack(side="left", padx=2)
    
    def _create_glassmorphic_content(self):
        """Create the main content area with glassmorphic weather cards."""
        # Content container
        content_container = ttk.Frame(self.main_container.content_frame, style="Glass.TFrame")
        content_container.pack(fill="both", expand=True, padx=15, pady=5)
        content_container.grid_columnconfigure(0, weight=1)
        content_container.grid_columnconfigure(1, weight=1)
        content_container.grid_rowconfigure(0, weight=1)
        content_container.grid_rowconfigure(1, weight=1)
        
        # Current Weather Card (Top Left)
        self.weather_frame = GlassmorphicWeatherCard(
            content_container,
            weather_type="current",
            style_theme=self.glass_theme
        )
        self.weather_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 7), pady=(0, 7))
        
        # Forecast Card (Top Right)
        self.forecast_frame = GlassmorphicCard(
            content_container,
            title="📅 5-Day Forecast",
            style_theme=self.glass_theme
        )
        self.forecast_frame.grid(row=0, column=1, sticky="nsew", padx=(7, 0), pady=(0, 7))
        
        # Air Quality Card (Bottom Left)
        self.air_quality_frame = GlassmorphicCard(
            content_container,
            title="💨 Air Quality Index",
            style_theme=self.glass_theme
        )
        self.air_quality_frame.grid(row=1, column=0, sticky="nsew", padx=(0, 7), pady=(7, 0))
        
        # Predictions Card (Bottom Right)
        self.predictions_frame = GlassmorphicCard(
            content_container,
            title="🔮 Weather Insights",
            style_theme=self.glass_theme
        )
        self.predictions_frame.grid(row=1, column=1, sticky="nsew", padx=(7, 0), pady=(7, 0))
        
        # Add placeholder content to cards
        self._add_placeholder_content()
    
    def _add_placeholder_content(self):
        """Add placeholder content to the glassmorphic cards."""
        # Forecast card content
        if self.forecast_frame and self.forecast_frame.content_frame:
            forecast_info = ttk.Label(
                self.forecast_frame.content_frame,
                text="Select a city to view forecast",
                style="GlassSubtitle.TLabel"
            )
            forecast_info.pack(expand=True)
        
        # Air Quality card content
        if self.air_quality_frame and self.air_quality_frame.content_frame:
            aqi_info = ttk.Label(
                self.air_quality_frame.content_frame,
                text="Air quality data will appear here",
                style="GlassSubtitle.TLabel"
            )
            aqi_info.pack(expand=True)
        
        # Predictions card content
        if self.predictions_frame and self.predictions_frame.content_frame:
            pred_info = ttk.Label(
                self.predictions_frame.content_frame,
                text="AI insights and predictions",
                style="GlassSubtitle.TLabel"
            )
            pred_info.pack(expand=True)
    
    def _create_glassmorphic_status_bar(self):
        """Create glassmorphic status bar."""
        status_card = GlassmorphicCard(
            self.main_container.content_frame,
            style_theme=self.glass_theme
        )
        status_card.pack(fill="x", padx=15, pady=(10, 15))
        
        # Status layout
        status_layout = ttk.Frame(status_card.content_frame, style="Glass.TFrame")
        status_layout.pack(fill="x", padx=10, pady=5)
        status_layout.grid_columnconfigure(0, weight=1)
        
        # Status label
        self.status_label = ttk.Label(
            status_layout,
            textvariable=self.status_var,
            style="Glass.TLabel"
        )
        self.status_label.grid(row=0, column=0, sticky="w")
        
        # Loading progress bar
        self.progress_bar = GlassmorphicProgressBar(
            status_layout,
            style_theme=self.glass_theme
        )
        self.progress_bar.grid(row=0, column=1, sticky="e", padx=(10, 0))
        self.progress_bar.configure(width=200, height=25)
    
    def _on_search_enter(self, event=None):
        """Handle search when Enter key is pressed."""
        if hasattr(self, 'city_entry') and self.city_entry:
            query = self.city_entry.get().strip()
            if query and query != "Enter city name...":
                self._on_search(query)
    
    def _on_search_button(self):
        """Handle search when Search button is clicked."""
        if hasattr(self, 'city_entry') and self.city_entry:
            query = self.city_entry.get().strip()
            if query and query != "Enter city name...":
                self._on_search(query)
    
    def _on_search(self, query: Optional[str] = None):
        """Handle search action."""
        if query is None and hasattr(self, 'city_entry') and self.city_entry:
            query = self.city_entry.get().strip()
        
        if query and self.search_callback:
            self.search_callback(query)
            self.update_status(f"🔍 Searching for weather in {query}...")
            if self.progress_bar:
                self.progress_bar.set_progress(0.3)
    
    def _change_theme(self, new_theme: str):
        """Change the glassmorphic theme."""
        if new_theme != self.glass_theme:
            self.glass_theme = new_theme
            self.colors = GlassmorphicStyle.GLASS_COLORS[new_theme]
            
            if self.theme_change_callback:
                self.theme_change_callback(new_theme)
            
            self.show_info("Theme Changed", f"Switched to {new_theme.title()} glass theme")
    
    # Interface methods for compatibility with existing weather core
    def set_search_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for search events."""
        self.search_callback = callback
    
    def set_theme_change_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for theme change events."""
        self.theme_change_callback = callback
    
    def set_city_text(self, city: str) -> None:
        """Set the city in the search bar."""
        if hasattr(self, 'city_entry') and self.city_entry:
            self.city_entry.delete(0, tk.END)
            if city and city.strip():
                self.city_entry.insert(0, city)
                self._entry_placeholder = False
            else:
                self.city_entry.insert(0, "Enter city name...")
                self._entry_placeholder = True
    
    def set_theme(self, theme: str) -> None:
        """Set the UI theme."""
        if theme in GlassmorphicStyle.GLASS_COLORS:
            self._change_theme(theme)
    
    def update_status(self, message: str) -> None:
        """Update the status message."""
        self.status_var.set(message)
        if self.progress_bar:
            self.progress_bar.set_progress(0.6)
    
    def show_info(self, title: str, message: str) -> None:
        """Show info dialog."""
        try:
            from tkinter import messagebox
            messagebox.showinfo(title, message)
        except:
            print(f"{title}: {message}")
    
    def show_error(self, title: str, message: str) -> None:
        """Show error dialog."""
        try:
            from tkinter import messagebox
            messagebox.showerror(title, message)
        except:
            print(f"ERROR - {title}: {message}")
    
    def run(self) -> None:
        """Start the glassmorphic dashboard."""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\\nGlassmorphic dashboard interrupted by user")
        except Exception as e:
            print(f"Dashboard error: {e}")
    
    def _on_entry_focus_in(self, event=None):
        """Handle entry focus in - remove placeholder."""
        if hasattr(self, '_entry_placeholder') and self._entry_placeholder:
            self.city_entry.delete(0, tk.END)
            self._entry_placeholder = False
    
    def _on_entry_focus_out(self, event=None):
        """Handle entry focus out - add placeholder if empty."""
        if not self.city_entry.get().strip():
            self.city_entry.insert(0, "Enter city name...")
            self._entry_placeholder = True


# Compatibility alias for existing code
WeatherDashboardUI = GlassmorphicWeatherDashboard
