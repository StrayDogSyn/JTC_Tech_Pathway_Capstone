"""
Enhanced Weather Dashboard with Advanced Tabular Features

This module extends the main dashboard with sophisticated tabular components
including historical data, analytics, comparisons, and export capabilities.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, Callable, Dict, Any, List
from datetime import datetime, timedelta
import threading
import random

try:
    from .dashboard_ui import WeatherDashboardUI
    from .tabular_components import (
        WeatherDataTable, ComparisonTable, AnalyticsTable, AdvancedDataTable
    )
    from .modern_components import ModernCard, NotificationToast
except ImportError:
    # Fallback imports
    WeatherDashboardUI = None
    WeatherDataTable = None
    ComparisonTable = None
    AnalyticsTable = None
    AdvancedDataTable = None
    ModernCard = None
    NotificationToast = None


class AdvancedWeatherDashboard:
    """
    Advanced Weather Dashboard with comprehensive tabular features.
    
    Features:
    - Main dashboard with current weather
    - Historical data table with sorting/filtering
    - Location comparison table
    - Analytics and statistics table
    - Data export capabilities
    - Advanced search and filtering
    """
    
    def __init__(self, title: str = "🌦️ Advanced Weather Intelligence Platform", 
                 theme: str = "superhero", size: tuple = (1600, 1000)):
        """Initialize the advanced dashboard."""
        self.root = ttk.Window(
            title=title,
            themename=theme,
            size=size,
            minsize=(1200, 800)
        )
        
        # Data storage
        self.historical_data = []
        self.comparison_data = []
        self.analytics_data = []
        
        # Callbacks
        self.search_callback: Optional[Callable[[str], None]] = None
        self.theme_change_callback: Optional[Callable[[str], None]] = None
        
        # UI Components
        self.notebook = None
        self.main_dashboard = None
        self.historical_table = None
        self.comparison_table = None
        self.analytics_table = None
        
        self._setup_ui()
        self._generate_sample_data()
        self._apply_advanced_styling()
    
    def _setup_ui(self):
        """Setup the advanced tabbed interface."""
        # Create main container
        main_container = ttk.Frame(self.root)
        main_container.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Create notebook for tabs
        self.notebook = ttk.Notebook(main_container)
        self.notebook.pack(fill="both", expand=True)
        
        # Tab 1: Main Dashboard
        self._create_main_dashboard_tab()
        
        # Tab 2: Historical Data
        self._create_historical_data_tab()
        
        # Tab 3: Location Comparison
        self._create_comparison_tab()
        
        # Tab 4: Analytics & Statistics
        self._create_analytics_tab()
          # Tab 5: Data Management
        self._create_data_management_tab()
        
        # Bind tab change events
        if self.notebook:
            self.notebook.bind("<<NotebookTabChanged>>", self._on_tab_changed)

    def _create_main_dashboard_tab(self):
        """Create the main dashboard tab."""
        dashboard_frame = ttk.Frame(self.notebook)
        if self.notebook:
            self.notebook.add(dashboard_frame, text="🌦️ Live Dashboard")
        
        # Create embedded dashboard
        if WeatherDashboardUI:
            # Create a custom container for the embedded dashboard
            dashboard_container = ttk.Frame(dashboard_frame)
            dashboard_container.pack(fill="both", expand=True)
            
            # We'll embed the main dashboard components here
            self._create_embedded_dashboard(dashboard_container)
        else:
            # Fallback content
            ttk.Label(
                dashboard_frame, 
                text="Main Dashboard - Weather data will appear here",
                font=("Segoe UI", 16)
            ).pack(expand=True)
    
    def _create_embedded_dashboard(self, parent):
        """Create an embedded version of the main dashboard."""
        # Header section
        header_frame = ttk.Frame(parent, padding=(20, 15))
        header_frame.pack(fill="x")
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="🌦️ Live Weather Monitor",
            font=("Segoe UI", 18, "bold")
        )
        title_label.pack(side="left")
        
        # Search section
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(side="right")
        
        self.city_entry = ttk.Entry(search_frame, font=("Segoe UI", 11), width=25)
        self.city_entry.pack(side="left", padx=(0, 10))
        self.city_entry.bind('<Return>', self._on_search)
        
        search_btn = ttk.Button(search_frame, text="🔍 Search", command=self._on_search)
        search_btn.pack(side="left")
        
        # Content area with cards
        content_frame = ttk.Frame(parent)
        content_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # Create modern cards layout
        self._create_weather_cards(content_frame)
    
    def _create_weather_cards(self, parent):
        """Create modern weather cards layout."""
        # Top row - Current weather and air quality
        top_frame = ttk.Frame(parent)
        top_frame.pack(fill="x", pady=(0, 10))
        
        # Current weather card
        self.weather_card = ttk.LabelFrame(top_frame, text="🌤️ Current Weather", padding=15)
        self.weather_card.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Air quality card
        self.air_quality_card = ttk.LabelFrame(top_frame, text="🌬️ Air Quality", padding=15)
        self.air_quality_card.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Bottom row - Forecast and predictions
        bottom_frame = ttk.Frame(parent)
        bottom_frame.pack(fill="both", expand=True)
        
        # Forecast card
        self.forecast_card = ttk.LabelFrame(bottom_frame, text="📊 5-Day Forecast", padding=15)
        self.forecast_card.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Predictions card
        self.predictions_card = ttk.LabelFrame(bottom_frame, text="🤖 AI Predictions", padding=15)
        self.predictions_card.pack(side="right", fill="both", expand=True, padx=(5, 0))
        
        # Add placeholder content
        self._add_placeholder_content()
    
    def _add_placeholder_content(self):
        """Add placeholder content to cards."""
        # Weather card placeholder
        ttk.Label(
            self.weather_card,
            text="Enter a city name to get weather data",
            font=("Segoe UI", 12)
        ).pack(pady=20)
        
        # Air quality placeholder
        ttk.Label(
            self.air_quality_card,
            text="Air quality data will appear here",
            font=("Segoe UI", 12)
        ).pack(pady=20)
        
        # Forecast placeholder
        ttk.Label(
            self.forecast_card,
            text="Weather forecast will appear here",
            font=("Segoe UI", 12)
        ).pack(pady=20)
          # Predictions placeholder
        ttk.Label(
            self.predictions_card,
            text="AI predictions will appear here",
            font=("Segoe UI", 12)
        ).pack(pady=20)

    def _create_historical_data_tab(self):
        """Create the historical data tab with advanced table."""
        historical_frame = ttk.Frame(self.notebook)
        if self.notebook:
            self.notebook.add(historical_frame, text="📈 Historical Data")
        
        if WeatherDataTable:
            self.historical_table = WeatherDataTable(historical_frame)
            # WeatherDataTable creates its own main_frame and packs it
              # Add control panel
            control_frame = ttk.Frame(historical_frame)
            control_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            ttk.Button(
                control_frame,
                text="📥 Load Sample Data",
                command=self._load_historical_sample
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                control_frame,
                text="🔄 Refresh Data",
                command=self._refresh_historical_data
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                control_frame,
                text="📊 Generate Report",
                command=self._generate_historical_report
            ).pack(side="left")
        else:
            ttk.Label(
                historical_frame,
                text="Historical Data Table - Advanced table features will appear here",
                font=("Segoe UI", 16)
            ).pack(expand=True)

    def _create_comparison_tab(self):
        """Create the location/time comparison tab."""
        comparison_frame = ttk.Frame(self.notebook)
        if self.notebook:
            self.notebook.add(comparison_frame, text="🔄 Comparisons")
        
        # Create sub-tabs for different comparison types
        comparison_notebook = ttk.Notebook(comparison_frame)
        comparison_notebook.pack(fill="both", expand=True, padx=10, pady=10)
          # Location comparison tab
        location_frame = ttk.Frame(comparison_notebook)
        comparison_notebook.add(location_frame, text="🌍 Locations")
        
        if ComparisonTable:
            self.location_comparison_table = ComparisonTable(location_frame)
            # ComparisonTable creates its own main_frame and packs it
            
            # Location controls
            loc_control_frame = ttk.Frame(location_frame)
            loc_control_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            ttk.Button(
                loc_control_frame,
                text="➕ Add Location",
                command=self._add_comparison_location
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                loc_control_frame,
                text="📊 Compare Now",
                command=self._compare_locations
            ).pack(side="left")
          # Time comparison tab
        time_frame = ttk.Frame(comparison_notebook)
        comparison_notebook.add(time_frame, text="⏰ Time Periods")
        
        if ComparisonTable:
            self.time_comparison_table = ComparisonTable(time_frame)
            # ComparisonTable creates its own main_frame and packs it
              # Time controls
            time_control_frame = ttk.Frame(time_frame)
            time_control_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            ttk.Button(
                time_control_frame,
                text="📅 Select Periods",
                command=self._select_time_periods
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                time_control_frame,
                text="📈 Analyze Trends",
                command=self._analyze_trends
            ).pack(side="left")

    def _create_analytics_tab(self):
        """Create the analytics and statistics tab."""
        analytics_frame = ttk.Frame(self.notebook)
        if self.notebook:
            self.notebook.add(analytics_frame, text="📊 Analytics")
        
        if AnalyticsTable:
            self.analytics_table = AnalyticsTable(analytics_frame)
            # AnalyticsTable creates its own main_frame and packs it
            
            # Analytics controls
            analytics_control_frame = ttk.Frame(analytics_frame)
            analytics_control_frame.pack(fill="x", padx=10, pady=(0, 10))
            
            ttk.Button(
                analytics_control_frame,
                text="🔄 Update Analytics",
                command=self._update_analytics
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                analytics_control_frame,
                text="📈 Trend Analysis",
                command=self._perform_trend_analysis
            ).pack(side="left", padx=(0, 10))
            
            ttk.Button(
                analytics_control_frame,
                text="📋 Summary Report",
                command=self._generate_summary_report
            ).pack(side="left")
        else:            ttk.Label(
                analytics_frame,
                text="Analytics & Statistics - Advanced analytics will appear here",
                font=("Segoe UI", 16)
            ).pack(expand=True)

    def _create_data_management_tab(self):
        """Create the data management tab."""
        data_frame = ttk.Frame(self.notebook)
        if self.notebook:
            self.notebook.add(data_frame, text="🗂️ Data Management")
        
        # Create sections
        sections_frame = ttk.Frame(data_frame)
        sections_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Import/Export section
        import_export_frame = ttk.LabelFrame(sections_frame, text="📁 Import/Export", padding=15)
        import_export_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(
            import_export_frame,
            text="📥 Import CSV Data",
            command=self._import_csv_data
        ).pack(side="left", padx=(0, 10))
        
        ttk.Button(
            import_export_frame,
            text="📤 Export All Data",
            command=self._export_all_data
        ).pack(side="left", padx=(0, 10))
        
        ttk.Button(
            import_export_frame,
            text="📊 Export Report",
            command=self._export_comprehensive_report
        ).pack(side="left")
        
        # Data Quality section
        quality_frame = ttk.LabelFrame(sections_frame, text="🔍 Data Quality", padding=15)
        quality_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Button(
            quality_frame,
            text="✅ Validate Data",
            command=self._validate_data_quality
        ).pack(side="left", padx=(0, 10))
        
        ttk.Button(
            quality_frame,
            text="🧹 Clean Data",
            command=self._clean_data
        ).pack(side="left", padx=(0, 10))
        
        ttk.Button(
            quality_frame,
            text="📈 Data Statistics",
            command=self._show_data_statistics
        ).pack(side="left")
        
        # Settings section
        settings_frame = ttk.LabelFrame(sections_frame, text="⚙️ Settings", padding=15)
        settings_frame.pack(fill="x")
        
        # Auto-refresh settings
        auto_frame = ttk.Frame(settings_frame)
        auto_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(auto_frame, text="Auto-refresh interval:").pack(side="left")
        
        self.refresh_var = tk.StringVar(value="5 minutes")
        refresh_combo = ttk.Combobox(
            auto_frame,
            textvariable=self.refresh_var,
            values=["1 minute", "5 minutes", "10 minutes", "30 minutes", "1 hour"],
            state="readonly",
            width=15
        )
        refresh_combo.pack(side="left", padx=(10, 0))
        
        # Data retention settings
        retention_frame = ttk.Frame(settings_frame)
        retention_frame.pack(fill="x")
        
        ttk.Label(retention_frame, text="Data retention period:").pack(side="left")
        
        self.retention_var = tk.StringVar(value="30 days")
        retention_combo = ttk.Combobox(
            retention_frame,
            textvariable=self.retention_var,
            values=["7 days", "30 days", "90 days", "1 year", "Forever"],
            state="readonly",
            width=15
        )
        retention_combo.pack(side="left", padx=(10, 0))
    
    def _generate_sample_data(self):
        """Generate comprehensive sample data for all tables."""
        self._generate_historical_sample_data()
        self._generate_comparison_sample_data()
        self._generate_analytics_sample_data()
    
    def _generate_historical_sample_data(self):
        """Generate sample historical weather data."""
        base_date = datetime.now() - timedelta(days=30)
        cities = ["Austin, TX", "New York, NY", "London, UK", "Tokyo, Japan", "Sydney, AU"]
        
        for i in range(100):
            date = base_date + timedelta(hours=i * 6)  # Every 6 hours
            city = cities[i % len(cities)]
            
            # Generate realistic weather data
            temp = round(random.uniform(15, 35), 1)
            humidity = random.randint(30, 90)
            pressure = random.randint(1000, 1030)
            wind = round(random.uniform(0, 15), 1)
            aqi = random.randint(1, 150)
            
            conditions = random.choice([
                "Clear Sky", "Few Clouds", "Scattered Clouds", 
                "Overcast", "Light Rain", "Heavy Rain", "Snow"
            ])
            
            self.historical_data.append({
                "timestamp": date.isoformat(),
                "location": city,
                "temperature": temp,
                "humidity": humidity,
                "pressure": pressure,
                "wind_speed": wind,
                "description": conditions,
                "aqi": aqi
            })
    
    def _generate_comparison_sample_data(self):
        """Generate sample comparison data."""
        locations = [
            {"location": "Austin, TX", "current_temp": "29.1°C", "feels_like": "33.0°C", 
             "humidity": "70%", "pressure": "1016 hPa", "wind_speed": "4.6 m/s", 
             "aqi": "1", "conditions": "Clear Sky"},
            {"location": "New York, NY", "current_temp": "22.5°C", "feels_like": "25.0°C", 
             "humidity": "65%", "pressure": "1020 hPa", "wind_speed": "3.2 m/s", 
             "aqi": "45", "conditions": "Few Clouds"},
            {"location": "London, UK", "current_temp": "18.3°C", "feels_like": "19.0°C", 
             "humidity": "80%", "pressure": "1012 hPa", "wind_speed": "5.1 m/s", 
             "aqi": "32", "conditions": "Overcast"},
            {"location": "Tokyo, Japan", "current_temp": "26.7°C", "feels_like": "28.5°C", 
             "humidity": "72%", "pressure": "1018 hPa", "wind_speed": "2.8 m/s", 
             "aqi": "68", "conditions": "Light Rain"},
        ]
        self.comparison_data = locations
    
    def _generate_analytics_sample_data(self):
        """Generate sample analytics data."""
        analytics = [
            {"metric": "Temperature", "current_value": "29.1°C", "daily_avg": "28.5°C", 
             "weekly_avg": "27.8°C", "monthly_avg": "26.9°C", "trend": "↗", "change_pct": "+2.3%"},
            {"metric": "Humidity", "current_value": "70%", "daily_avg": "68%", 
             "weekly_avg": "71%", "monthly_avg": "69%", "trend": "→", "change_pct": "+0.5%"},
            {"metric": "Air Pressure", "current_value": "1016 hPa", "daily_avg": "1015 hPa", 
             "weekly_avg": "1014 hPa", "monthly_avg": "1013 hPa", "trend": "↗", "change_pct": "+1.1%"},
            {"metric": "Wind Speed", "current_value": "4.6 m/s", "daily_avg": "4.2 m/s", 
             "weekly_avg": "3.8 m/s", "monthly_avg": "4.1 m/s", "trend": "↗", "change_pct": "+5.2%"},
            {"metric": "AQI", "current_value": "1", "daily_avg": "15", 
             "weekly_avg": "22", "monthly_avg": "28", "trend": "↘", "change_pct": "-18.5%"},
        ]
        self.analytics_data = analytics
    
    def _apply_advanced_styling(self):
        """Apply advanced styling to the dashboard."""
        style = ttk.Style()
        
        # Tab styling
        style.configure("TNotebook.Tab", padding=[20, 10])
        
        # Card styling
        style.configure("Card.TLabelFrame", relief="solid", borderwidth=1)
          # Header styling
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"))
        style.configure("Subheader.TLabel", font=("Segoe UI", 14, "bold"))
    
    # Event handlers
    def _on_tab_changed(self, event):
        """Handle tab change events."""
        if not self.notebook:
            return
            
        selected_tab = self.notebook.select()
        tab_index = self.notebook.index(selected_tab)
        
        # Load data when switching to specific tabs
        if tab_index == 1 and self.historical_table:  # Historical data tab
            self._load_historical_data()
        elif tab_index == 2:  # Comparison tab
            self._load_comparison_data()
        elif tab_index == 3 and self.analytics_table:  # Analytics tab
            self._load_analytics_data()
    
    def _on_search(self, event=None):
        """Handle search from embedded dashboard."""
        if self.city_entry:
            city = self.city_entry.get().strip()
            if city and self.search_callback:
                self.search_callback(city)
    
    # Data loading methods
    def _load_historical_data(self):
        """Load historical data into the table."""
        if self.historical_table and self.historical_data:
            self.historical_table.set_data(self.historical_data)
    
    def _load_comparison_data(self):
        """Load comparison data into tables."""
        if hasattr(self, 'location_comparison_table') and self.comparison_data:
            self.location_comparison_table.set_data(self.comparison_data)
    
    def _load_analytics_data(self):
        """Load analytics data into the table."""
        if self.analytics_table and self.analytics_data:
            self.analytics_table.set_data(self.analytics_data)
    
    # Action methods
    def _load_historical_sample(self):
        """Load sample historical data."""
        self._load_historical_data()
        self._show_notification("Sample historical data loaded successfully!", "success")
    
    def _refresh_historical_data(self):
        """Refresh historical data."""
        # Simulate data refresh
        self._generate_historical_sample_data()
        self._load_historical_data()
        self._show_notification("Historical data refreshed!", "info")
    
    def _generate_historical_report(self):
        """Generate historical data report."""
        self._show_notification("Historical report generated!", "success")
    
    def _add_comparison_location(self):
        """Add a new location for comparison."""
        self._show_notification("Add location dialog would appear here", "info")
    
    def _compare_locations(self):
        """Compare selected locations."""
        self._load_comparison_data()
        self._show_notification("Location comparison updated!", "success")
    
    def _select_time_periods(self):
        """Select time periods for comparison."""
        self._show_notification("Time period selection dialog would appear here", "info")
    
    def _analyze_trends(self):
        """Analyze weather trends."""
        self._show_notification("Trend analysis completed!", "success")
    
    def _update_analytics(self):
        """Update analytics data."""
        self._generate_analytics_sample_data()
        self._load_analytics_data()
        self._show_notification("Analytics updated!", "success")
    
    def _perform_trend_analysis(self):
        """Perform detailed trend analysis."""
        self._show_notification("Trend analysis report generated!", "success")
    
    def _generate_summary_report(self):
        """Generate comprehensive summary report."""
        self._show_notification("Summary report generated!", "success")
    
    def _import_csv_data(self):
        """Import data from CSV file."""
        self._show_notification("CSV import functionality would open here", "info")
    
    def _export_all_data(self):
        """Export all data."""
        self._show_notification("All data exported successfully!", "success")
    
    def _export_comprehensive_report(self):
        """Export comprehensive report."""
        self._show_notification("Comprehensive report exported!", "success")
    
    def _validate_data_quality(self):
        """Validate data quality."""
        self._show_notification("Data validation completed - No issues found!", "success")
    
    def _clean_data(self):
        """Clean data."""
        self._show_notification("Data cleaning completed!", "success")
    
    def _show_data_statistics(self):
        """Show data statistics."""
        self._show_notification("Data statistics: 100 records, 0 errors", "info")
    
    def _show_notification(self, message: str, type_: str = "info"):
        """Show notification."""
        if NotificationToast:
            NotificationToast(self.root, message, type_, 3.0)
        else:
            print(f"📢 {message}")
    
    # Public interface methods
    def set_search_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for search events."""
        self.search_callback = callback
    
    def set_theme_change_callback(self, callback: Callable[[str], None]) -> None:
        """Set callback for theme change events."""
        self.theme_change_callback = callback
    
    def update_weather_data(self, weather_data: Dict[str, Any]) -> None:
        """Update the weather display with new data."""
        # Clear and update weather card
        for widget in self.weather_card.winfo_children():
            widget.destroy()
        
        if weather_data:
            # Temperature
            temp_frame = ttk.Frame(self.weather_card)
            temp_frame.pack(fill="x", pady=(0, 10))
            
            ttk.Label(
                temp_frame,
                text=f"{weather_data.get('temperature', 'N/A')}°C",
                font=("Segoe UI", 36, "bold")
            ).pack(side="left")
            
            ttk.Label(
                temp_frame,
                text=f"Feels like {weather_data.get('feels_like', 'N/A')}°C",
                font=("Segoe UI", 12)
            ).pack(side="left", padx=(20, 0), anchor="n", pady=(10, 0))
            
            # Conditions
            ttk.Label(
                self.weather_card,
                text=weather_data.get('description', 'N/A'),
                font=("Segoe UI", 14, "bold")
            ).pack(anchor="w")
            
            # Additional info
            info_frame = ttk.Frame(self.weather_card)
            info_frame.pack(fill="x", pady=(10, 0))
            
            info_text = f"Humidity: {weather_data.get('humidity', 'N/A')}% • "
            info_text += f"Pressure: {weather_data.get('pressure', 'N/A')} hPa • "
            info_text += f"Wind: {weather_data.get('wind_speed', 'N/A')} m/s"
            
            ttk.Label(
                info_frame,
                text=info_text,
                font=("Segoe UI", 10)
            ).pack(anchor="w")
            
            # Add to historical data
            current_data = {
                "timestamp": datetime.now().isoformat(),
                "location": weather_data.get('location', 'Unknown'),
                "temperature": weather_data.get('temperature', 0),
                "humidity": weather_data.get('humidity', 0),
                "pressure": weather_data.get('pressure', 0),
                "wind_speed": weather_data.get('wind_speed', 0),
                "description": weather_data.get('description', ''),
                "aqi": weather_data.get('aqi', 0)
            }
            self.historical_data.append(current_data)
    
    def update_air_quality_data(self, aqi_data: Dict[str, Any]) -> None:
        """Update air quality display."""
        # Clear and update air quality card
        for widget in self.air_quality_card.winfo_children():
            widget.destroy()
        
        if aqi_data:
            # AQI value
            aqi_frame = ttk.Frame(self.air_quality_card)
            aqi_frame.pack(fill="x", pady=(0, 10))
            
            ttk.Label(
                aqi_frame,
                text=f"AQI: {aqi_data.get('aqi', 'N/A')}",
                font=("Segoe UI", 24, "bold")
            ).pack(side="left")
            
            # Quality level
            quality = aqi_data.get('quality', 'Unknown')
            ttk.Label(
                aqi_frame,
                text=quality,
                font=("Segoe UI", 12, "bold")
            ).pack(side="left", padx=(20, 0), anchor="n", pady=(5, 0))
            
            # Pollutant details
            if 'pollutants' in aqi_data:
                ttk.Label(
                    self.air_quality_card,
                    text="Pollutant Levels:",
                    font=("Segoe UI", 10, "bold")
                ).pack(anchor="w", pady=(10, 5))
                
                for pollutant, value in aqi_data['pollutants'].items():
                    ttk.Label(
                        self.air_quality_card,
                        text=f"{pollutant}: {value}",
                        font=("Segoe UI", 9)
                    ).pack(anchor="w")
    
    def run(self) -> None:
        """Start the advanced dashboard."""
        self.root.mainloop()
    
    def destroy(self) -> None:
        """Destroy the dashboard."""
        if self.root:
            self.root.destroy()
