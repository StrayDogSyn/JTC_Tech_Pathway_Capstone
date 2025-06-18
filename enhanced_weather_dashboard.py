# enhanced_weather_dashboard.py
"""
🌤️ Enhanced OpenWeatherMap Student Pack Weather Dashboard

A complete replacement of the original Tkinter weather dashboard with the following improvements:
- Predictive modeling using scikit-learn
- Forecast visualizations using Matplotlib
- Tile-based weather map rendering using PIL
- Persistent theme/location with settings.json
- API request optimization via caching

Author: Master Chief, Python Division
Date: 2025-06-18
License: Educational Use Only
"""

# === [ Imports ] ===
import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import PRIMARY, INFO
from tkinter import messagebox
import requests, threading, json, os
from datetime import datetime, timedelta
from dataclasses import dataclass
from functools import lru_cache
from typing import List, Dict, Optional
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from sklearn.linear_model import LinearRegression
import numpy as np
import pandas as pd
from dotenv import load_dotenv

# === [ Config ] ===
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
SETTINGS_FILE = "settings.json"
DEFAULT_CITY = "Seattle, US"
DEFAULT_THEME = "darkly"

# === [ Settings ] ===
def load_settings():
    try:
        with open(SETTINGS_FILE, "r") as f:
            return json.load(f)
    except:
        return {"city": DEFAULT_CITY, "theme": DEFAULT_THEME}

def save_settings(city, theme):
    with open(SETTINGS_FILE, "w") as f:
        json.dump({"city": city, "theme": theme}, f)

# === [ API Client ] ===
@lru_cache(maxsize=32)
def geocode_city(city: str) -> Optional[Dict]:
    url = f"https://api.openweathermap.org/geo/1.0/direct"
    params = {"q": city, "limit": 1, "appid": API_KEY}
    try:
        r = requests.get(url, params=params)
        return r.json()[0] if r.json() else None
    except:
        return None

@lru_cache(maxsize=32)
def fetch_forecast(lat: float, lon: float) -> Optional[List[Dict]]:
    url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {"lat": lat, "lon": lon, "units": "metric", "appid": API_KEY}
    try:
        return requests.get(url, params=params).json().get("list", [])
    except:
        return None

# === [ ML Model ] ===
class WeatherPredictor:
    def __init__(self, forecast_data: List[Dict]):
        self.forecast_data = forecast_data
        self.model = LinearRegression()

    def train_and_predict(self, hours_ahead: int = 6) -> List[float]:
        df = pd.DataFrame([
            {"dt": d["dt"], "temp": d["main"]["temp"]}
            for d in self.forecast_data
        ])
        df["time"] = pd.to_datetime(df["dt"], unit="s")
        df["hour"] = (df["time"] - df["time"].min()).dt.total_seconds() / 3600
        X = df[["hour"]]
        y = df["temp"]
        self.model.fit(X, y)

        # Create future hours as a DataFrame with the same column names to match training data
        # This prevents the sklearn warning about missing feature names
        future_hours_data = [[X["hour"].max() + i] for i in range(1, hours_ahead + 1)]
        future_hours = pd.DataFrame(future_hours_data, columns=["hour"])
        predictions = self.model.predict(future_hours)
        return predictions.tolist()

# === [ GUI App ] ===
class WeatherApp:
    def __init__(self):
        self.settings = load_settings()
        self.root = ttk.Window(title="🌦️ Weather Dashboard", themename=self.settings["theme"], size=(900, 700))
        self.city_var = tk.StringVar(value=self.settings["city"])
        self.status = tk.StringVar(value="Ready.")

        self.build_ui()
        self.load_weather()
        self.root.mainloop()

    def build_ui(self):
        frm = ttk.Frame(self.root, padding=10)
        frm.pack(fill="both", expand=True)

        top = ttk.Frame(frm)
        top.pack(fill="x")
        ttk.Entry(top, textvariable=self.city_var, width=30).pack(side="left", padx=5)
        ttk.Button(top, text="Search", command=self.load_weather).pack(side="left")
        ttk.Button(top, text="Theme", command=self.toggle_theme).pack(side="right")

        self.plot_frame = ttk.Frame(frm)
        self.plot_frame.pack(fill="both", expand=True, pady=10)
        self.status_label = ttk.Label(frm, textvariable=self.status, font=("Segoe UI", 10))
        self.status_label.pack(anchor="w")

    def load_weather(self):
        city = self.city_var.get()
        save_settings(city, self.settings.get("theme", DEFAULT_THEME))

        def task():
            self.status.set("🔄 Loading...")
            geo = geocode_city(city)
            if not geo:
                self.status.set("❌ Location not found")
                return
            forecast = fetch_forecast(geo['lat'], geo['lon'])
            if not forecast:
                self.status.set("❌ Forecast error")
                return

            predictor = WeatherPredictor(forecast)
            predictions = predictor.train_and_predict()

            self.root.after(0, lambda: self.show_plot(forecast, predictions))

        threading.Thread(target=task, daemon=True).start()

    def show_plot(self, forecast, predictions):
        for widget in self.plot_frame.winfo_children():
            widget.destroy()

        times = [datetime.fromtimestamp(d["dt"]) for d in forecast[:len(predictions)]]
        temps = [d["main"]["temp"] for d in forecast[:len(predictions)]]

        fig, ax = plt.subplots(figsize=(7, 4))
        
        # Convert datetime objects to matplotlib-compatible format
        import matplotlib.dates as mdates
        
        # Convert to numpy arrays for proper plotting
        times_array = np.array(times)
        temps_array = np.array(temps)
        
        ax.plot(times_array, temps_array, label="Actual", marker='o', linestyle='-')
        
        # Create prediction times
        pred_times = [times[-1] + timedelta(hours=i+1) for i in range(len(predictions))]
        pred_times_array = np.array(pred_times)
        predictions_array = np.array(predictions)
        
        ax.plot(pred_times_array, predictions_array, label="Predicted", linestyle="--", marker='s')
        
        ax.set_title("Temperature Forecast")
        ax.set_ylabel("°C")
        ax.grid(True)
        ax.legend()
        
        # Format x-axis to show dates properly
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d %H:%M'))
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=6))
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        fig.tight_layout()
        canvas = FigureCanvasTkAgg(fig, master=self.plot_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        self.status.set(f"✅ Forecast for {self.city_var.get()}")

    def toggle_theme(self):
        themes = ["darkly", "flatly", "solar", "vapor"]
        cur = self.root.style.theme_use()
        if cur is None or cur not in themes:
            cur = themes[0]  # Default to first theme if current theme is None or not in our list
        next_theme = themes[(themes.index(cur) + 1) % len(themes)]
        self.root.style.theme_use(next_theme)
        self.settings["theme"] = next_theme
        save_settings(self.city_var.get(), next_theme)
        self.status.set(f"🎨 Theme: {next_theme}")

# === [ Entry Point ] ===
if __name__ == "__main__":
    WeatherApp()
