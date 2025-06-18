"""
Enhanced Weather GUI with Student Pack Features - Fixed Version
Modern, comprehensive weather application showcasing all OpenWeatherMap Student Pack capabilities.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime, timedelta
import webbrowser
from enhanced_weather_api import EnhancedWeatherAPI
from config import Config

class StudentPackWeatherGUI:
    def __init__(self, root):
        self.root = root
        self.weather_api = EnhancedWeatherAPI()
        
        # State variables
        self.current_location = None
        self.current_weather_data = None
        self.forecast_data = None
        
        self.setup_window()
        self.setup_styles()
        self.create_widgets()
        self.load_default_location()
        
    def setup_window(self):
        """Configure the main window."""
        self.root.title("Student Pack Weather Dashboard - OpenWeatherMap")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        self.root.configure(bg='#0f1419')
        
        # Make window responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
    def setup_styles(self):
        """Configure modern styling."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define color scheme
        colors = {
            'bg_dark': '#0f1419',
            'bg_medium': '#1e2328',
            'bg_light': '#2d3136',
            'accent': '#00d4ff',
            'success': '#00ff9f',
            'warning': '#ffb700',
            'error': '#ff6b6b',
            'text_light': '#ffffff',
            'text_medium': '#c9d1d9',
            'text_dark': '#8b949e'
        }
        
        # Configure styles
        self.style.configure('Title.TLabel', 
                           background=colors['bg_dark'], 
                           foreground=colors['accent'],
                           font=('Segoe UI', 16, 'bold'))
        
        self.style.configure('Header.TLabel', 
                           background=colors['bg_medium'], 
                           foreground=colors['text_light'],
                           font=('Segoe UI', 11, 'bold'))
        
        self.style.configure('Data.TLabel', 
                           background=colors['bg_medium'], 
                           foreground=colors['text_medium'],
                           font=('Segoe UI', 9))
        
        self.style.configure('Success.TLabel', 
                           background=colors['bg_medium'], 
                           foreground=colors['success'],
                           font=('Segoe UI', 9, 'bold'))
        
        self.style.configure('Custom.TFrame', 
                           background=colors['bg_medium'],
                           relief='flat',
                           borderwidth=1)
        
        self.style.configure('Card.TFrame', 
                           background=colors['bg_light'],
                           relief='solid',
                           borderwidth=1)
        
    def create_widgets(self):
        """Create the main GUI layout."""
        # Main container
        main_container = ttk.Frame(self.root, style='Custom.TFrame')
        main_container.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
        main_container.grid_rowconfigure(1, weight=1)
        main_container.grid_columnconfigure(0, weight=1)
        
        # Header section
        self.create_header(main_container)
        
        # Create notebook for tabs
        self.create_notebook(main_container)
        
        # Status bar
        self.create_status_bar(main_container)
        
    def create_header(self, parent):
        """Create the header section with title and search."""
        header_frame = ttk.Frame(parent, style='Custom.TFrame')
        header_frame.grid(row=0, column=0, sticky='ew', pady=(0, 10))
        header_frame.grid_columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(header_frame, 
                               text="🎓 Student Pack Weather Dashboard", 
                               style='Title.TLabel')
        title_label.grid(row=0, column=0, columnspan=3, pady=5)
        
        # Search section
        search_frame = ttk.Frame(header_frame, style='Custom.TFrame')
        search_frame.grid(row=1, column=0, columnspan=3, sticky='ew', pady=5)
        search_frame.grid_columnconfigure(1, weight=1)
        
        ttk.Label(search_frame, text="📍 Location:", style='Header.TLabel').grid(row=0, column=0, padx=(0, 5))
        
        self.location_var = tk.StringVar(value=Config.DEFAULT_CITY)
        self.location_entry = ttk.Entry(search_frame, textvariable=self.location_var, width=30)
        self.location_entry.grid(row=0, column=1, padx=5, sticky='ew')
        self.location_entry.bind('<Return>', self.search_location)
        
        search_btn = ttk.Button(search_frame, text="🔍 Search", command=self.search_location)
        search_btn.grid(row=0, column=2, padx=5)
        
        # Subscription info
        api_info = self.weather_api.get_api_usage_info()
        sub_text = (f"Plan: {api_info['subscription']['subscription_plan']} | "
                   f"Rate: {api_info['rate_limits']['current_forecast']} | "
                   f"Free for Education")
        
        sub_label = ttk.Label(search_frame, text=sub_text, style='Success.TLabel')
        sub_label.grid(row=1, column=0, columnspan=3, pady=5)
        
    def create_notebook(self, parent):
        """Create tabbed interface for different features."""
        self.notebook = ttk.Notebook(parent)
        self.notebook.grid(row=1, column=0, sticky='nsew', padx=5, pady=5)
        
        # Tab 1: Current Weather & Forecasts
        self.create_current_tab()
        
        # Tab 2: Air Pollution
        self.create_pollution_tab()
        
        # Tab 3: Weather Maps
        self.create_maps_tab()
        
    def create_current_tab(self):
        """Create current weather and forecast tab."""
        current_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(current_frame, text='🌤️ Current & Forecasts')
        
        # Create scrollable canvas
        canvas = tk.Canvas(current_frame, bg='#1e2328', highlightthickness=0)
        scrollbar = ttk.Scrollbar(current_frame, orient='vertical', command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas, style='Custom.TFrame')
        
        scrollable_frame.bind(
            '<Configure>',
            lambda e: canvas.configure(scrollregion=canvas.bbox('all'))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.grid(row=0, column=0, sticky='nsew')
        scrollbar.grid(row=0, column=1, sticky='ns')
        
        current_frame.grid_rowconfigure(0, weight=1)
        current_frame.grid_columnconfigure(0, weight=1)
        
        # Current weather section
        self.create_current_weather_section(scrollable_frame)
        
        # Forecast sections
        self.create_forecast_section(scrollable_frame)
        
    def create_current_weather_section(self, parent):
        """Create current weather display."""
        current_card = ttk.LabelFrame(parent, text='📊 Current Weather', style='Card.TFrame')
        current_card.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        parent.grid_columnconfigure(0, weight=1)
        
        # Current weather data display
        self.current_weather_frame = ttk.Frame(current_card, style='Card.TFrame')
        self.current_weather_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        current_card.grid_columnconfigure(0, weight=1)
        
        # Placeholder text
        self.current_weather_label = ttk.Label(self.current_weather_frame, 
                                             text="Loading current weather...", 
                                             style='Data.TLabel')
        self.current_weather_label.grid(row=0, column=0, pady=10)
        
    def create_forecast_section(self, parent):
        """Create forecast section."""
        forecast_card = ttk.LabelFrame(parent, text='📅 Student Pack Forecasts', style='Card.TFrame')
        forecast_card.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        
        # Forecast info
        self.forecast_frame = ttk.Frame(forecast_card, style='Card.TFrame')
        self.forecast_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        forecast_card.grid_columnconfigure(0, weight=1)
        
        # Feature list
        features_text = (
            "🎓 Student Pack Forecast Features:\n\n"
            "⏰ Hourly Forecast: 4 days (96 hours)\n"
            "📅 Daily Forecast: 16 days extended\n"
            "🌡️ Temperature trends & patterns\n"
            "☔ Precipitation probability\n"
            "💨 Wind speed & direction\n"
            "💧 Humidity & pressure\n"
            "☀️ UV Index forecasting\n"
            "🌤️ Weather condition details"
        )
        
        features_label = ttk.Label(self.forecast_frame, text=features_text, 
                                 style='Data.TLabel', justify='left')
        features_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
    def create_pollution_tab(self):
        """Create air pollution monitoring tab."""
        pollution_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(pollution_frame, text='🌬️ Air Quality')
        
        # Current air quality
        current_aqi_frame = ttk.LabelFrame(pollution_frame, text='🌬️ Current Air Quality', style='Card.TFrame')
        current_aqi_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        pollution_frame.grid_columnconfigure(0, weight=1)
        
        self.aqi_display = ttk.Frame(current_aqi_frame, style='Card.TFrame')
        self.aqi_display.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        current_aqi_frame.grid_columnconfigure(0, weight=1)
        
        # Air quality info
        aqi_info_text = (
            "🌬️ Student Pack Air Quality Features:\n\n"
            "📊 Real-time Air Quality Index (AQI)\n"
            "🧪 Detailed pollutant breakdown:\n"
            "   • CO (Carbon Monoxide)\n"
            "   • NO (Nitrogen Monoxide)\n"
            "   • NO2 (Nitrogen Dioxide)\n"
            "   • O3 (Ozone)\n"
            "   • SO2 (Sulfur Dioxide)\n"
            "   • PM2.5 (Fine Particles)\n"
            "   • PM10 (Coarse Particles)\n"
            "   • NH3 (Ammonia)\n\n"
            "📈 5-day air quality forecast\n"
            "📚 Historical air pollution data\n"
            "🎯 Health recommendations based on AQI"
        )
        
        aqi_info_label = ttk.Label(self.aqi_display, text=aqi_info_text, 
                                 style='Data.TLabel', justify='left')
        aqi_info_label.grid(row=0, column=0, sticky='w', padx=10, pady=10)
        
    def create_maps_tab(self):
        """Create weather maps tab."""
        maps_frame = ttk.Frame(self.notebook, style='Custom.TFrame')
        self.notebook.add(maps_frame, text='🗺️ Weather Maps (15 Layers)')
        
        # Map layer selection
        layer_frame = ttk.LabelFrame(maps_frame, text='🎨 Interactive Weather Maps', style='Card.TFrame')
        layer_frame.grid(row=0, column=0, sticky='ew', padx=10, pady=10)
        maps_frame.grid_columnconfigure(0, weight=1)
        
        # Available layers
        layers = self.weather_api.get_available_map_layers()
        self.selected_layer = tk.StringVar(value=layers[0] if layers else 'temp_new')
        
        ttk.Label(layer_frame, text="🌈 Select Layer:", style='Header.TLabel').grid(row=0, column=0, padx=5, pady=5)
        
        layer_combo = ttk.Combobox(layer_frame, textvariable=self.selected_layer, values=layers, state='readonly')
        layer_combo.grid(row=0, column=1, padx=5, pady=5)
        
        map_btn = ttk.Button(layer_frame, text="🌍 Open Interactive Map", command=self.open_weather_map)
        map_btn.grid(row=0, column=2, padx=5, pady=5)
        
        # Map information
        map_info_frame = ttk.Frame(maps_frame, style='Card.TFrame')
        map_info_frame.grid(row=1, column=0, sticky='nsew', padx=10, pady=10)
        maps_frame.grid_rowconfigure(1, weight=1)
        
        map_info_text = (
            "🗺️ Student Pack Weather Maps (15 Layers):\n\n"
            "🌡️ Temperature Maps:\n"
            "   • Current temperature\n"
            "   • Temperature forecasts\n"
            "   • Historical temperature\n\n"
            "☔ Precipitation Maps:\n"
            "   • Precipitation radar\n"
            "   • Rain forecasts\n"
            "   • Snow coverage\n\n"
            "💨 Wind Maps:\n"
            "   • Wind speed\n"
            "   • Wind direction\n"
            "   • Wind patterns\n\n"
            "☁️ Cloud Maps:\n"
            "   • Cloud coverage\n"
            "   • Satellite imagery\n\n"
            "📊 Atmospheric Maps:\n"
            "   • Pressure systems\n"
            "   • Atmospheric conditions\n\n"
            "🎓 Full access included with Student Pack!"
        )
        
        info_label = ttk.Label(map_info_frame, text=map_info_text, style='Data.TLabel', justify='left')
        info_label.grid(row=0, column=0, padx=10, pady=10, sticky='nw')
        
    def create_status_bar(self, parent):
        """Create status bar."""
        self.status_frame = ttk.Frame(parent, style='Custom.TFrame')
        self.status_frame.grid(row=2, column=0, sticky='ew', pady=(5, 0))
        
        self.status_var = tk.StringVar(value="Ready - Student Pack Weather Dashboard")
        self.status_label = ttk.Label(self.status_frame, textvariable=self.status_var, style='Data.TLabel')
        self.status_label.grid(row=0, column=0, sticky='w', padx=5)
        
        # API info
        api_info_btn = ttk.Button(self.status_frame, text="ℹ️ API Info", command=self.show_api_info)
        api_info_btn.grid(row=0, column=1, sticky='e', padx=5)
        
        self.status_frame.grid_columnconfigure(0, weight=1)
        
    def update_status(self, message):
        """Update status bar message."""
        self.status_var.set(f"{datetime.now().strftime('%H:%M:%S')} - {message}")
        self.root.update_idletasks()
        
    def load_default_location(self):
        """Load weather data for default location."""
        self.search_location()
        
    def search_location(self, event=None):
        """Search for location and load weather data."""
        location_name = self.location_var.get().strip()
        if not location_name:
            return
            
        self.update_status(f"Searching for {location_name}...")
        
        def search_thread():
            try:
                # Geocode the location
                locations = self.weather_api.geocode_city(location_name, limit=1)
                if not locations:
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Location '{location_name}' not found."))
                    return
                    
                location = locations[0]
                self.current_location = {
                    'name': location.get('name', location_name),
                    'country': location.get('country', ''),
                    'lat': location['lat'],
                    'lon': location['lon']
                }
                
                # Load all weather data
                self.root.after(0, self.load_weather_data)
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to search location: {e}"))
                self.root.after(0, lambda: self.update_status("Ready"))
                
        threading.Thread(target=search_thread, daemon=True).start()
        
    def load_weather_data(self):
        """Load comprehensive weather data for current location."""
        if not self.current_location:
            return
            
        lat = self.current_location['lat']
        lon = self.current_location['lon']
        location_name = f"{self.current_location['name']}, {self.current_location['country']}"
        
        self.update_status(f"Loading weather data for {location_name}...")
        
        def load_thread():
            try:
                # Load current weather
                current_weather = self.weather_api.get_current_weather_by_coordinates(lat, lon)
                self.current_weather_data = self.weather_api.format_weather_data(current_weather)
                self.root.after(0, self.update_current_weather_display)
                
                # Load air pollution
                try:
                    air_pollution = self.weather_api.get_air_pollution_current(lat, lon)
                    self.root.after(0, lambda: self.update_air_quality_display(air_pollution))
                except Exception as e:
                    print(f"Air pollution error: {e}")
                
                self.root.after(0, lambda: self.update_status(f"Weather data loaded for {location_name}"))
                
            except Exception as e:
                self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to load weather data: {e}"))
                self.root.after(0, lambda: self.update_status("Ready"))
                
        threading.Thread(target=load_thread, daemon=True).start()
        
    def update_current_weather_display(self):
        """Update current weather display."""
        if not self.current_weather_data:
            return
            
        # Clear existing display
        for widget in self.current_weather_frame.winfo_children():
            widget.destroy()
            
        data = self.current_weather_data
        location_name = f"{data['city']}, {data['country']}"
        
        # Main weather info
        main_frame = ttk.Frame(self.current_weather_frame, style='Card.TFrame')
        main_frame.grid(row=0, column=0, sticky='ew', pady=5)
        self.current_weather_frame.grid_columnconfigure(0, weight=1)
        
        # Location and time
        ttk.Label(main_frame, text=f"📍 {location_name}", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=5)
        ttk.Label(main_frame, text=f"🕐 {datetime.now().strftime('%Y-%m-%d %H:%M')}", style='Data.TLabel').grid(row=1, column=0, columnspan=2, pady=2)
        
        # Temperature and conditions
        temp_frame = ttk.Frame(main_frame, style='Card.TFrame')
        temp_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        ttk.Label(temp_frame, text=f"{data['temperature']:.1f}°C", 
                 font=('Segoe UI', 20, 'bold'), style='Success.TLabel').grid(row=0, column=0, padx=10)
        ttk.Label(temp_frame, text=f"Feels like {data['feels_like']:.1f}°C", 
                 style='Data.TLabel').grid(row=1, column=0, padx=10)
        ttk.Label(temp_frame, text=f"🌤️ {data['description']}", 
                 font=('Segoe UI', 12), style='Header.TLabel').grid(row=0, column=1, rowspan=2, padx=20)
        
        # Additional details
        details_frame = ttk.Frame(main_frame, style='Card.TFrame')
        details_frame.grid(row=3, column=0, columnspan=2, pady=10, sticky='ew')
        
        details = [
            ("💧 Humidity", f"{data['humidity']}%"),
            ("📊 Pressure", f"{data['pressure']} hPa"),
            ("💨 Wind", f"{data['wind_speed']} m/s"),
            ("👁️ Visibility", f"{data['visibility']/1000:.1f} km" if data['visibility'] != 'N/A' else 'N/A')
        ]
        
        for i, (label, value) in enumerate(details):
            row = i // 2
            col = i % 2
            detail_frame = ttk.Frame(details_frame, style='Card.TFrame')
            detail_frame.grid(row=row, column=col, padx=10, pady=5, sticky='w')
            ttk.Label(detail_frame, text=label, style='Header.TLabel').grid(row=0, column=0)
            ttk.Label(detail_frame, text=value, style='Data.TLabel').grid(row=0, column=1, padx=(5, 0))
            
    def update_air_quality_display(self, air_data):
        """Update air quality display."""
        # Clear existing display
        for widget in self.aqi_display.winfo_children():
            widget.destroy()
            
        if not air_data or 'list' not in air_data or not air_data['list']:
            ttk.Label(self.aqi_display, text="Air quality data will be displayed here when available", style='Data.TLabel').grid(row=0, column=0)
            return
            
        aqi_data = air_data['list'][0]
        aqi = aqi_data['main']['aqi']
        components = aqi_data.get('components', {})
        
        aqi_levels = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        
        # AQI Level
        aqi_frame = ttk.Frame(self.aqi_display, style='Card.TFrame')
        aqi_frame.grid(row=0, column=0, sticky='ew', pady=5)
        self.aqi_display.grid_columnconfigure(0, weight=1)
        
        ttk.Label(aqi_frame, text=f"Air Quality Index: {aqi}/5", style='Header.TLabel').grid(row=0, column=0)
        ttk.Label(aqi_frame, text=f"Status: {aqi_levels.get(aqi, 'Unknown')}", style='Data.TLabel').grid(row=1, column=0)
        
        # Components
        if components:
            comp_frame = ttk.Frame(self.aqi_display, style='Card.TFrame')
            comp_frame.grid(row=1, column=0, sticky='ew', pady=5)
            
            ttk.Label(comp_frame, text="Pollutant Concentrations (μg/m³):", style='Header.TLabel').grid(row=0, column=0, columnspan=2, pady=5)
            
            row = 1
            for component, value in list(components.items())[:6]:  # Show first 6 components
                ttk.Label(comp_frame, text=f"{component.upper()}:", style='Data.TLabel').grid(row=row, column=0, sticky='w', padx=5)
                ttk.Label(comp_frame, text=f"{value:.2f}", style='Data.TLabel').grid(row=row, column=1, sticky='w', padx=5)
                row += 1
                
    def open_weather_map(self):
        """Open interactive weather map in browser."""
        if not self.current_location:
            messagebox.showerror("Error", "Please select a location first.")
            return
            
        lat = self.current_location['lat']
        lon = self.current_location['lon']
        layer = self.selected_layer.get()
        
        # OpenWeatherMap interactive map URL
        map_url = f"https://openweathermap.org/weathermap?basemap=map&cities=true&layer={layer}&lat={lat}&lon={lon}&zoom=10"
        
        try:
            webbrowser.open(map_url)
            self.update_status(f"Opened {layer} weather map for {self.current_location['name']}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open map: {e}")
            
    def show_api_info(self):
        """Show comprehensive API information."""
        api_info = self.weather_api.get_api_usage_info()
        
        info_window = tk.Toplevel(self.root)
        info_window.title("Student Pack API Information")
        info_window.geometry("600x500")
        info_window.configure(bg='#1e2328')
        
        # Create scrollable text widget
        text_frame = ttk.Frame(info_window)
        text_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side='right', fill='y')
        
        text_widget = tk.Text(text_frame, wrap='word', yscrollcommand=scrollbar.set,
                             bg='#2d3136', fg='#c9d1d9', font=('Segoe UI', 10),
                             relief='flat', borderwidth=5)
        text_widget.pack(side='left', fill='both', expand=True)
        
        scrollbar.config(command=text_widget.yview)
        
        # Format API information
        info_text = f"""
🎓 OpenWeatherMap Student Pack Information

📋 Subscription Details:
   • Plan: {api_info['subscription']['subscription_plan']}
   • Pricing: {api_info['subscription']['pricing']}
   • Type: {api_info['subscription']['subscription_type']}

⚡ Rate Limits:
   • Current/Forecast: {api_info['rate_limits']['current_forecast']}
   • Monthly Total: {api_info['rate_limits']['monthly_total']} 
   • Historical Daily: {api_info['rate_limits']['historical_daily']}

🌟 Available Features:
"""
        
        for benefit in api_info['student_pack_benefits']:
            info_text += f"   ✅ {benefit}\n"
            
        info_text += f"""
🔗 API Endpoints:
   • Current Weather: {api_info['endpoints']['current_weather']}
   • One Call API: {api_info['endpoints']['forecast_onecall']}
   • Historical: {api_info['endpoints']['historical']}
   • Geocoding: {api_info['endpoints']['geocoding']}
   • Air Pollution: {api_info['endpoints']['air_pollution']}
   • Weather Maps: {api_info['endpoints']['weather_maps']}
   • Statistics: {api_info['endpoints']['statistics']}

📚 Documentation & Support:
   • Documentation: {api_info['subscription_info']['documentation']}
   • Support Email: {api_info['subscription_info']['support_email']}
   • Subscription URL: {api_info['subscription_info']['subscription_url']}

🔑 API Key: {api_info['api_key']}

🎯 This application demonstrates all Student Pack features including:
   • Real-time weather data
   • Extended forecasts (4-day hourly, 16-day daily)
   • Historical data (1 year archive)
   • Air pollution monitoring
   • Interactive weather maps (15 layers)
   • Statistical analysis
   • Accumulated parameters
   • Advanced geocoding
"""
        
        text_widget.insert('1.0', info_text)
        text_widget.config(state='disabled')

def main():
    """Main application entry point."""
    root = tk.Tk()
    app = StudentPackWeatherGUI(root)
    
    try:
        root.mainloop()
    except KeyboardInterrupt:
        print("\\nApplication terminated by user.")
    except Exception as e:
        print(f"Application error: {e}")

if __name__ == "__main__":
    main()
