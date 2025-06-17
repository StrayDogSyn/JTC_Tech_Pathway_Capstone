"""
Modern Weather GUI Application using tkinter and OpenWeatherMap API
Features: Responsive design, scrollable content, gradient backgrounds, smooth animations
"""

import tkinter as tk
from tkinter import ttk, messagebox
import threading
import time
from datetime import datetime
from weather_api import WeatherAPI
from config import Config
import requests

class ModernWeatherGUI:
    def __init__(self, root):
        self.root = root
        self.weather_api = WeatherAPI()
        self.setup_window()
        self.setup_style()
        self.create_widgets()
        self.animate_startup()
        
    def setup_window(self):
        """Configure the main window with responsive design."""
        self.root.title("Weather Dashboard")
        self.root.geometry("800x600")
        self.root.minsize(400, 300)  # Smaller minimum for better compatibility
        self.root.configure(bg='#1a1a2e')
        
        # Make window fully responsive
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Center the window
        self.center_window()
        
        # Bind resize event for dynamic adjustments
        self.root.bind('<Configure>', self.on_window_resize)
        
    def center_window(self):
        """Center the window on the screen."""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
    def on_window_resize(self, event):
        """Handle window resize events for responsive adjustments."""
        if event.widget == self.root:
            # Adjust font sizes based on window size
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            
            # Scale title font based on window width
            if width < 500:
                title_size = 18
                temp_size = 32
                header_size = 10
                info_size = 9
            elif width < 700:
                title_size = 20
                temp_size = 36
                header_size = 12
                info_size = 10
            else:
                title_size = 24
                temp_size = 48
                header_size = 14
                info_size = 12
            
            # Update styles with new sizes
            self.update_responsive_styles(title_size, temp_size, header_size, info_size)
            
    def update_responsive_styles(self, title_size, temp_size, header_size, info_size):
        """Update font sizes for responsive design."""
        self.style.configure('Title.TLabel', font=('Segoe UI', title_size, 'bold'))
        self.style.configure('Temp.TLabel', font=('Segoe UI', temp_size, 'bold'))
        self.style.configure('Header.TLabel', font=('Segoe UI', header_size, 'bold'))
        self.style.configure('Info.TLabel', font=('Segoe UI', info_size))
        
    def setup_style(self):
        """Configure modern styling for ttk widgets."""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Modern button style
        self.style.configure('Modern.TButton',
                           background='#4facfe',
                           foreground='white',
                           borderwidth=0,
                           focuscolor='none',
                           relief='flat',
                           padding=(15, 8))
        
        self.style.map('Modern.TButton',
                      background=[('active', '#00f2fe'),
                                ('pressed', '#0575e6')])
        
        # Modern entry style
        self.style.configure('Modern.TEntry',
                           fieldbackground='#2d2d44',
                           foreground='white',
                           borderwidth=2,
                           insertcolor='white',
                           relief='flat')
        
        # Label styles (responsive - will be updated by resize handler)
        self.style.configure('Title.TLabel',
                           background='#1a1a2e',
                           foreground='#4facfe',
                           font=('Segoe UI', 24, 'bold'))
        
        self.style.configure('Header.TLabel',
                           background='#1a1a2e',
                           foreground='white',
                           font=('Segoe UI', 14, 'bold'))
        
        self.style.configure('Info.TLabel',
                           background='#1a1a2e',
                           foreground='#e0e0e0',
                           font=('Segoe UI', 12))
        
        self.style.configure('Temp.TLabel',
                           background='#1a1a2e',
                           foreground='#ff6b6b',
                           font=('Segoe UI', 48, 'bold'))
        
    def create_widgets(self):
        """Create responsive, scrollable widget layout."""
        # Create main scrollable frame
        self.create_scrollable_frame()
        
        # Create content sections
        self.create_title_section()
        self.create_search_section()
        self.create_weather_section()
        self.create_status_bar()
        
    def create_scrollable_frame(self):
        """Create a scrollable main frame for content."""
        # Main canvas for scrolling
        self.main_canvas = tk.Canvas(self.root, bg='#1a1a2e', highlightthickness=0)
        self.main_canvas.grid(row=0, column=0, sticky='nsew', padx=0, pady=0)
        
        # Scrollbar
        self.scrollbar = ttk.Scrollbar(self.root, orient='vertical', command=self.main_canvas.yview)
        self.scrollbar.grid(row=0, column=1, sticky='ns')
        
        # Configure canvas scrolling
        self.main_canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Scrollable frame inside canvas
        self.scrollable_frame = tk.Frame(self.main_canvas, bg='#1a1a2e')
        self.canvas_window = self.main_canvas.create_window((0, 0), window=self.scrollable_frame, anchor='nw')
        
        # Bind events for responsive scrolling
        self.scrollable_frame.bind('<Configure>', self.on_frame_configure)
        self.main_canvas.bind('<Configure>', self.on_canvas_configure)
        
        # Mouse wheel scrolling
        self.main_canvas.bind('<MouseWheel>', self.on_mousewheel)
        
    def on_frame_configure(self, event):
        """Update scroll region when content changes."""
        self.main_canvas.configure(scrollregion=self.main_canvas.bbox('all'))
        
    def on_canvas_configure(self, event):
        """Update canvas window width for responsive design."""
        canvas_width = event.width
        self.main_canvas.itemconfig(self.canvas_window, width=canvas_width)
        
    def on_mousewheel(self, event):
        """Handle mouse wheel scrolling."""
        self.main_canvas.yview_scroll(int(-1 * (event.delta / 120)), 'units')
        
    def create_title_section(self):
        """Create responsive title section."""
        title_frame = tk.Frame(self.scrollable_frame, bg='#1a1a2e')
        title_frame.pack(fill='x', padx=20, pady=(20, 30))
        
        # Main title
        title_label = ttk.Label(title_frame, text="🌤️ Weather Dashboard", 
                               style='Title.TLabel')
        title_label.pack()
        
        # Subtitle
        subtitle = ttk.Label(title_frame, text="Real-time weather information", 
                            style='Info.TLabel')
        subtitle.pack(pady=(5, 0))
        
        # Current time
        self.time_label = ttk.Label(title_frame, text="", style='Info.TLabel')
        self.time_label.pack(pady=(10, 0))
        self.update_time()
        
    def create_search_section(self):
        """Create responsive search section."""
        search_frame = tk.Frame(self.scrollable_frame, bg='#1a1a2e')
        search_frame.pack(fill='x', padx=20, pady=(0, 30))
        
        # Search container
        search_container = tk.Frame(search_frame, bg='#2d2d44', relief='flat', bd=2)
        search_container.pack(fill='x', pady=10)
        
        # Search label
        search_label = ttk.Label(search_container, text="Enter City Name:", 
                                style='Header.TLabel', background='#2d2d44')
        search_label.pack(anchor='w', padx=20, pady=(15, 5))
        
        # Input frame with responsive layout
        input_frame = tk.Frame(search_container, bg='#2d2d44')
        input_frame.pack(fill='x', padx=20, pady=(0, 15))
        
        # Configure input frame for responsive behavior
        input_frame.grid_columnconfigure(0, weight=1)
        
        # City entry
        self.city_var = tk.StringVar(value=Config.DEFAULT_CITY)
        self.city_entry = ttk.Entry(input_frame, textvariable=self.city_var,
                                   style='Modern.TEntry', font=('Segoe UI', 12))
        self.city_entry.grid(row=0, column=0, sticky='ew', padx=(0, 10), ipady=8)
        self.city_entry.bind('<Return>', lambda e: self.search_weather())
        
        # Search button
        self.search_btn = ttk.Button(input_frame, text="🔍 Search", 
                                    command=self.search_weather,
                                    style='Modern.TButton')
        self.search_btn.grid(row=0, column=1, sticky='e')
        
    def create_weather_section(self):
        """Create responsive weather display section."""
        self.weather_frame = tk.Frame(self.scrollable_frame, bg='#1a1a2e')
        self.weather_frame.pack(fill='both', expand=True, padx=20)
        
        # Weather card container
        self.weather_card = tk.Frame(self.weather_frame, bg='#2d2d44', relief='flat', bd=2)
        self.weather_card.pack(fill='both', expand=True, pady=10)
        
        # Loading frame
        self.loading_frame = tk.Frame(self.weather_card, bg='#2d2d44')
        self.loading_label = ttk.Label(self.loading_frame, text="🌍 Loading weather data...", 
                                      style='Header.TLabel', background='#2d2d44')
        
        # Weather info frame
        self.info_frame = tk.Frame(self.weather_card, bg='#2d2d44')
        self.create_weather_display()
        
        # Show initial state
        self.show_loading(False)
        
    def create_weather_display(self):
        """Create responsive weather information display."""
        # Location and description
        location_frame = tk.Frame(self.info_frame, bg='#2d2d44')
        location_frame.pack(fill='x', pady=20)
        
        self.location_label = ttk.Label(location_frame, text="", 
                                       style='Title.TLabel', background='#2d2d44')
        self.location_label.pack()
        
        self.description_label = ttk.Label(location_frame, text="", 
                                          style='Header.TLabel', background='#2d2d44')
        self.description_label.pack(pady=(5, 0))
        
        # Temperature display
        temp_frame = tk.Frame(self.info_frame, bg='#2d2d44')
        temp_frame.pack(fill='x', pady=20)
        
        self.temp_label = ttk.Label(temp_frame, text="", 
                                   style='Temp.TLabel', background='#2d2d44')
        self.temp_label.pack()
        
        self.feels_like_label = ttk.Label(temp_frame, text="", 
                                         style='Info.TLabel', background='#2d2d44')
        self.feels_like_label.pack(pady=(5, 0))
        
        # Responsive weather details grid
        self.create_responsive_details_grid()
        
    def create_responsive_details_grid(self):
        """Create a responsive grid for weather details."""
        details_frame = tk.Frame(self.info_frame, bg='#2d2d44')
        details_frame.pack(fill='x', padx=20, pady=20)
        
        # Configure responsive grid weights
        for i in range(2):
            details_frame.grid_columnconfigure(i, weight=1)
        for i in range(2):
            details_frame.grid_rowconfigure(i, weight=1)
        
        # Create detail cards with responsive layout
        self.humidity_card, self.humidity_value_label = self.create_detail_card(
            details_frame, "💧", "Humidity", 0, 0)
        self.wind_card, self.wind_value_label = self.create_detail_card(
            details_frame, "🌬️", "Wind", 0, 1)
        self.pressure_card, self.pressure_value_label = self.create_detail_card(
            details_frame, "🌡️", "Pressure", 1, 0)
        self.visibility_card, self.visibility_value_label = self.create_detail_card(
            details_frame, "👁️", "Visibility", 1, 1)
        
    def create_detail_card(self, parent, icon, title, row, col):
        """Create a responsive detail card for weather information."""
        card = tk.Frame(parent, bg='#1a1a2e', relief='flat', bd=1)
        card.grid(row=row, column=col, padx=5, pady=5, sticky='nsew')
        
        # Configure card for responsive content
        card.grid_columnconfigure(0, weight=1)
        card.grid_rowconfigure(0, weight=1)
        
        # Card content frame
        content_frame = tk.Frame(card, bg='#1a1a2e')
        content_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)
        
        # Icon
        icon_label = ttk.Label(content_frame, text=icon, 
                              style='Header.TLabel', background='#1a1a2e',
                              font=('Segoe UI', 16))
        icon_label.pack()
        
        # Title
        title_label = ttk.Label(content_frame, text=title, 
                               style='Info.TLabel', background='#1a1a2e')
        title_label.pack()
        
        # Value
        value_label = ttk.Label(content_frame, text="--", 
                               style='Header.TLabel', background='#1a1a2e')
        value_label.pack(pady=(5, 0))
        
        return card, value_label
        
    def create_status_bar(self):
        """Create responsive status bar."""
        # Status bar attached to main window, not scrollable content
        self.status_frame = tk.Frame(self.root, bg='#2d2d44', height=40)
        self.status_frame.grid(row=1, column=0, columnspan=2, sticky='ew', pady=0)
        self.status_frame.grid_propagate(False)
        
        # Configure status frame
        self.root.grid_rowconfigure(1, weight=0)
        
        self.status_label = ttk.Label(self.status_frame, text="Ready", 
                                     style='Info.TLabel', background='#2d2d44')
        self.status_label.pack(anchor='w', padx=20, pady=10)
        
    def show_loading(self, show=True):
        """Show or hide loading animation."""
        if show:
            self.info_frame.pack_forget()
            self.loading_frame.pack(fill='both', expand=True)
            self.loading_label.pack(expand=True)
            self.animate_loading()
        else:
            self.loading_frame.pack_forget()
            self.info_frame.pack(fill='both', expand=True)
            
    def animate_loading(self):
        """Animate the loading text."""
        if self.loading_frame.winfo_viewable():
            current_text = self.loading_label.cget('text')
            dots = current_text.count('.')
            if dots >= 3:
                new_text = "🌍 Loading weather data"
            else:
                new_text = current_text + "."
            self.loading_label.config(text=new_text)
            self.root.after(500, self.animate_loading)
            
    def animate_startup(self):
        """Animate the startup of the application."""
        self.root.attributes('-alpha', 0.0)
        self.fade_in()
        
    def fade_in(self, alpha=0.0):
        """Fade in animation for the window."""
        alpha += 0.05
        if alpha <= 1.0:
            self.root.attributes('-alpha', alpha)
            self.root.after(30, lambda: self.fade_in(alpha))
        else:
            self.root.attributes('-alpha', 1.0)
            
    def update_time(self):
        """Update the current time display."""
        current_time = datetime.now().strftime("%A, %B %d, %Y - %I:%M:%S %p")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def search_weather(self):
        """Search for weather information in a separate thread."""
        city = self.city_var.get().strip()
        if not city:
            messagebox.showwarning("Input Error", "Please enter a city name")
            return
            
        # Show loading animation
        self.show_loading(True)
        self.status_label.config(text=f"Searching for {city}...")
        
        # Disable search button during request
        self.search_btn.config(state='disabled')
        
        # Run weather request in separate thread
        thread = threading.Thread(target=self.fetch_weather, args=(city,))
        thread.daemon = True
        thread.start()
        
    def fetch_weather(self, city):
        """Fetch weather data from API (runs in separate thread)."""
        try:
            # Simulate minimum loading time for better UX
            time.sleep(0.5)
            
            weather_data = self.weather_api.get_current_weather(city)
            formatted_data = self.weather_api.format_weather_data(weather_data)
            
            # Update UI in main thread
            self.root.after(0, self.update_weather_display, formatted_data)
            
        except ValueError as e:
            self.root.after(0, self.show_error, str(e))
        except requests.RequestException as e:
            self.root.after(0, self.show_error, f"Network error: {str(e)}")
        except Exception as e:
            self.root.after(0, self.show_error, f"Unexpected error: {str(e)}")
        finally:
            # Re-enable search button
            self.root.after(0, lambda: self.search_btn.config(state='normal'))
            
    def update_weather_display(self, weather_data):
        """Update the weather display with fetched data."""
        # Hide loading and show weather info
        self.show_loading(False)
        
        # Update location and description
        location = f"{weather_data['city']}, {weather_data['country']}"
        self.location_label.config(text=location)
        self.description_label.config(text=weather_data['description'])
        
        # Update temperature
        temp_unit = "°C" if Config.TEMPERATURE_UNITS == "metric" else "°F" if Config.TEMPERATURE_UNITS == "imperial" else "K"
        temp_text = f"{weather_data['temperature']:.1f}{temp_unit}"
        self.temp_label.config(text=temp_text)
        
        feels_like_text = f"Feels like {weather_data['feels_like']:.1f}{temp_unit}"
        self.feels_like_label.config(text=feels_like_text)
        
        # Update detail cards
        self.humidity_value_label.config(text=f"{weather_data['humidity']}%")
        
        wind_speed = weather_data['wind_speed']
        wind_unit = "m/s" if Config.TEMPERATURE_UNITS == "metric" else "mph"
        self.wind_value_label.config(text=f"{wind_speed} {wind_unit}")
        
        pressure_unit = "hPa" if Config.TEMPERATURE_UNITS == "metric" else "inHg"
        self.pressure_value_label.config(text=f"{weather_data['pressure']} {pressure_unit}")
        
        visibility = weather_data['visibility']
        if visibility != 'N/A':
            vis_unit = "km" if Config.TEMPERATURE_UNITS == "metric" else "mi"
            vis_km = visibility / 1000 if Config.TEMPERATURE_UNITS == "metric" else visibility * 0.000621371
            self.visibility_value_label.config(text=f"{vis_km:.1f} {vis_unit}")
        else:
            self.visibility_value_label.config(text="N/A")
        
        # Update status
        self.status_label.config(text=f"Weather data updated for {weather_data['city']}")
        
        # Update scroll region after content change
        self.root.after(100, lambda: self.main_canvas.configure(scrollregion=self.main_canvas.bbox('all')))
        
    def show_error(self, error_message):
        """Show error message to user."""
        self.show_loading(False)
        self.status_label.config(text="Error occurred")
        messagebox.showerror("Weather Error", error_message)

def main():
    """Main function to run the weather GUI application."""
    try:
        # Verify configuration
        Config.validate_config()
        
        # Create and run the GUI
        root = tk.Tk()
        app = ModernWeatherGUI(root)
        root.mainloop()
        
    except ValueError as e:
        # Show configuration error
        root = tk.Tk()
        root.withdraw()  # Hide the main window
        messagebox.showerror("Configuration Error", 
                           f"Please check your configuration:\n\n{e}")
        root.destroy()

if __name__ == "__main__":
    main()
