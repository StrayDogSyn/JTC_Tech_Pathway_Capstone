#!/usr/bin/env python3
"""
Advanced UX/UI Features Demo

This script demonstrates the modern UX/UI components and features
implemented for the weather dashboard.
"""

import sys
import os
import time
import threading

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import tkinter as tk
    import ttkbootstrap as ttk
    from src.ui.dashboard_ui import WeatherDashboardUI
    from src.ui.modern_components import (
        ModernCard, CircularProgress, WeatherGauge,
        NotificationToast, ModernToggleSwitch, LoadingSpinner
    )
    print("✅ All advanced UX/UI components imported successfully!")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)


def create_demo_dashboard():
    """Create and launch demo dashboard with advanced features."""
    print("🚀 Launching Advanced UX/UI Demo Dashboard...")
    
    # Create dashboard with enhanced features
    dashboard = WeatherDashboardUI(
        title="🎨 Advanced UX/UI Demo - Weather Intelligence Platform",
        theme="darkly",
        size=(1600, 1000)
    )
    
    # Set up demo callbacks
    dashboard.set_search_callback(lambda city: demo_search(dashboard, city))
    dashboard.set_theme_change_callback(lambda theme: demo_theme_change(dashboard, theme))
    dashboard.set_auto_refresh_callback(lambda enabled: demo_auto_refresh(dashboard, enabled))
    
    # Show demo notification after startup
    def show_startup_demo():
        time.sleep(2)  # Wait for UI to fully load
        try:
            dashboard.show_notification(
                "🎉 Welcome to Advanced UX/UI Demo!",
                "success",
                5000
            )
            
            # Show feature highlights
            time.sleep(3)
            dashboard.show_notification(
                "✨ Try the search suggestions and theme switching!",
                "info",
                4000
            )
            
            time.sleep(2)
            dashboard.update_status("🎨 Demo ready - explore all the modern features!")
            
        except Exception as e:
            print(f"Demo notification error: {e}")
    
    # Start demo notification thread
    threading.Thread(target=show_startup_demo, daemon=True).start()
    
    # Run the dashboard
    dashboard.run()


def demo_search(dashboard, city: str):
    """Demo search functionality."""
    print(f"🔍 Demo search triggered for: {city}")
    
    # Show loading state
    dashboard.set_loading(True)
    dashboard.update_status(f"🔍 Searching for {city}...")
    
    def demo_search_process():
        # Simulate API call delay
        time.sleep(2)
        
        # Hide loading and show result
        dashboard.set_loading(False)
        dashboard.show_notification(
            f"🌤️ Weather data loaded for {city}!",
            "success",
            3000
        )
        dashboard.update_status(f"✅ Showing weather for {city}")
        
        # Update city in search box
        dashboard.set_city_text(city)
    
    # Run search in background
    threading.Thread(target=demo_search_process, daemon=True).start()


def demo_theme_change(dashboard, theme: str):
    """Demo theme change functionality."""
    print(f"🎨 Demo theme change to: {theme}")
    
    dashboard.show_notification(
        f"🎨 Theme changed to {theme}",
        "info",
        2000
    )
    dashboard.update_status(f"🎨 Current theme: {theme}")


def demo_auto_refresh(dashboard, enabled: bool):
    """Demo auto-refresh functionality."""
    status = "enabled" if enabled else "disabled"
    print(f"🔄 Demo auto-refresh {status}")
    
    dashboard.show_notification(
        f"🔄 Auto-refresh {status}",
        "info" if enabled else "warning",
        2000
    )


def create_components_showcase():
    """Create a showcase of all modern components."""
    print("🧩 Creating Modern Components Showcase...")
    
    # Create showcase window
    root = ttk.Window(
        title="🧩 Modern Components Showcase",
        themename="darkly",
        size=(1200, 800)
    )
    
    # Main container
    main_frame = ttk.Frame(root, padding=20)
    main_frame.pack(fill="both", expand=True)
    
    # Title
    title_label = ttk.Label(
        main_frame,
        text="🧩 Modern UI Components Showcase",
        font=('Segoe UI', 20, 'bold')
    )
    title_label.pack(pady=(0, 20))
    
    # Create notebook for component categories
    notebook = ttk.Notebook(main_frame)
    notebook.pack(fill="both", expand=True, pady=(0, 20))
    
    # Cards Tab
    cards_frame = ttk.Frame(notebook)
    notebook.add(cards_frame, text="🃏 Cards")
    create_cards_demo(cards_frame)
    
    # Gauges Tab
    gauges_frame = ttk.Frame(notebook)
    notebook.add(gauges_frame, text="📊 Gauges")
    create_gauges_demo(gauges_frame)
    
    # Controls Tab
    controls_frame = ttk.Frame(notebook)
    notebook.add(controls_frame, text="🎛️ Controls")
    create_controls_demo(controls_frame)
    
    # Animations Tab
    animations_frame = ttk.Frame(notebook)
    notebook.add(animations_frame, text="✨ Animations")
    create_animations_demo(animations_frame)
    
    # Close button
    ttk.Button(
        main_frame,
        text="❌ Close Showcase",
        command=root.quit,
        style="Accent.TButton"
    ).pack(pady=10)
    
    print("✅ Showcase window created - explore the tabs!")
    root.mainloop()


def create_cards_demo(parent):
    """Create cards demonstration."""
    container = ttk.Frame(parent, padding=20)
    container.pack(fill="both", expand=True)
    
    # Create sample cards
    card1 = ModernCard(container, title="Weather Card", padding=15)
    card1.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
    
    ttk.Label(card1, text="🌤️ 22°C", font=('Segoe UI', 18, 'bold')).pack()
    ttk.Label(card1, text="Partly Cloudy").pack()
    ttk.Label(card1, text="Feels like 24°C").pack()
    
    card2 = ModernCard(container, title="Forecast Card", padding=15)
    card2.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
    
    ttk.Label(card2, text="📊 5-Day Forecast", font=('Segoe UI', 14, 'bold')).pack()
    ttk.Label(card2, text="Tomorrow: 25°C / 18°C").pack()
    ttk.Label(card2, text="Sunny with clouds").pack()
    
    card3 = ModernCard(container, title="Air Quality", padding=15)
    card3.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
    
    ttk.Label(card3, text="🌬️ AQI: 45", font=('Segoe UI', 16, 'bold')).pack()
    ttk.Label(card3, text="Good", foreground="green").pack()
    
    # Configure grid weights
    container.grid_columnconfigure(0, weight=1)
    container.grid_columnconfigure(1, weight=1)


def create_gauges_demo(parent):
    """Create gauges demonstration."""
    container = ttk.Frame(parent, padding=20)
    container.pack(fill="both", expand=True)
    
    # Humidity gauge
    humidity_gauge = WeatherGauge(
        container,
        value=75,
        max_value=100,
        label="Humidity",
        unit="%",
        size=150
    )
    humidity_gauge.grid(row=0, column=0, padx=20, pady=20)
    
    # Wind speed gauge
    wind_gauge = WeatherGauge(
        container,
        value=12,
        max_value=50,
        label="Wind Speed",
        unit="m/s",
        size=150
    )
    wind_gauge.grid(row=0, column=1, padx=20, pady=20)
    
    # Pressure gauge
    pressure_gauge = WeatherGauge(
        container,
        value=1013,
        max_value=1100,
        label="Pressure",
        unit="hPa",
        size=150
    )
    pressure_gauge.grid(row=0, column=2, padx=20, pady=20)
    
    # Circular progress
    progress = CircularProgress(container, value=85, max_value=100)
    progress.grid(row=1, column=1, padx=20, pady=20)
    
    ttk.Label(container, text="Data Loading Progress", font=('Segoe UI', 12)).grid(row=2, column=1)


def create_controls_demo(parent):
    """Create controls demonstration."""
    container = ttk.Frame(parent, padding=20)
    container.pack(fill="both", expand=True)
    
    # Toggle switches
    toggle_frame = ttk.LabelFrame(container, text="Toggle Switches", padding=15)
    toggle_frame.pack(fill="x", pady=(0, 20))
    
    auto_refresh_toggle = ModernToggleSwitch(
        toggle_frame,
        text="🔄 Auto-refresh Weather Data"
    )
    auto_refresh_toggle.pack(pady=5)
    auto_refresh_toggle.set_callback(lambda state: print(f"Auto-refresh: {state}"))
    
    notifications_toggle = ModernToggleSwitch(
        toggle_frame,
        text="🔔 Enable Notifications"
    )
    notifications_toggle.pack(pady=5)
    notifications_toggle.set_state(True)
    
    # Loading spinner
    spinner_frame = ttk.LabelFrame(container, text="Loading Indicators", padding=15)
    spinner_frame.pack(fill="x", pady=(0, 20))
    
    spinner = LoadingSpinner(spinner_frame, size=40)
    spinner.pack(pady=10)
    spinner.start_spinning()
    
    ttk.Label(spinner_frame, text="Loading weather data...", font=('Segoe UI', 12)).pack()
    
    # Notification demo
    notification_frame = ttk.LabelFrame(container, text="Notifications", padding=15)
    notification_frame.pack(fill="x")
    
    def show_demo_notification(msg_type):
        messages = {
            "success": "✅ Weather data updated successfully!",
            "info": "ℹ️ Auto-refresh enabled for 5 minutes",
            "warning": "⚠️ API rate limit approaching",
            "error": "❌ Failed to connect to weather service"
        }
        NotificationToast(container, messages[msg_type], msg_type, 3.0)
    
    button_frame = ttk.Frame(notification_frame)
    button_frame.pack()
    
    ttk.Button(button_frame, text="Success", 
              command=lambda: show_demo_notification("success")).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Info", 
              command=lambda: show_demo_notification("info")).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Warning", 
              command=lambda: show_demo_notification("warning")).pack(side="left", padx=5)
    ttk.Button(button_frame, text="Error", 
              command=lambda: show_demo_notification("error")).pack(side="left", padx=5)


def create_animations_demo(parent):
    """Create animations demonstration."""
    container = ttk.Frame(parent, padding=20)
    container.pack(fill="both", expand=True)
    
    # Animation info
    info_label = ttk.Label(
        container,
        text="✨ Animation Features",
        font=('Segoe UI', 16, 'bold')
    )
    info_label.pack(pady=(0, 20))
    
    # Animation features list
    features = [
        "🌊 Smooth fade-in/fade-out transitions",
        "🔄 Rotating loading spinners", 
        "📈 Animated gauge needle movements",
        "💫 Card hover effects",
        "🎨 Theme transition animations",
        "📱 Responsive layout adjustments",
        "⚡ 60 FPS smooth animations",
        "🎯 Eased animation curves"
    ]
    
    for feature in features:
        feature_label = ttk.Label(
            container,
            text=feature,
            font=('Segoe UI', 12)
        )
        feature_label.pack(anchor="w", pady=2)
    
    # Demo button
    demo_button = ttk.Button(
        container,
        text="🎬 See Animations in Main Dashboard",
        command=lambda: print("Launch main dashboard to see animations!"),
        style="Accent.TButton"
    )
    demo_button.pack(pady=20)


def main():
    """Main demo function."""
    print("🎨 Advanced Weather Dashboard - UX/UI Features Demo")
    print("=" * 60)
    print()
    print("Choose a demo option:")
    print("1. 🌦️ Enhanced Weather Dashboard (Full Experience)")
    print("2. 🧩 Modern Components Showcase")
    print("3. ❌ Exit")
    print()
    
    try:
        choice = input("Enter your choice (1-3): ").strip()
        
        if choice == "1":
            create_demo_dashboard()
        elif choice == "2":
            create_components_showcase()
        elif choice == "3":
            print("👋 Demo ended. Thank you!")
        else:
            print("❌ Invalid choice. Please run the demo again.")
            
    except KeyboardInterrupt:
        print("\n👋 Demo interrupted. Thank you!")
    except Exception as e:
        print(f"❌ Demo error: {e}")


if __name__ == "__main__":
    main()
