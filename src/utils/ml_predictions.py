"""
Machine learning predictions for weather data.

This module provides weather prediction capabilities using scikit-learn
and processes forecast data to generate future predictions.
"""

import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from typing import List, Dict, Optional, Tuple
from datetime import datetime


class WeatherPredictor:
    """Machine learning weather predictor using forecast data."""
    
    def __init__(self):
        """Initialize the weather predictor."""
        self.temperature_model = LinearRegression()
        self.humidity_model = LinearRegression()
        self.pressure_model = LinearRegression()
        self.is_trained = False
    
    def train_models(self, forecast_data: List[Dict]) -> bool:
        """Train prediction models using forecast data."""
        if not forecast_data or len(forecast_data) < 3:
            return False
        
        try:
            # Convert forecast data to DataFrame
            df = pd.DataFrame([
                {
                    "dt": item["dt"],
                    "temp": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "pressure": item["main"]["pressure"]
                }
                for item in forecast_data
            ])
            
            # Create time features
            df["time"] = pd.to_datetime(df["dt"], unit="s")
            df["hour"] = (df["time"] - df["time"].min()).dt.total_seconds() / 3600
            
            # Prepare features and targets
            X = df[["hour"]]
            y_temp = df["temp"]
            y_humidity = df["humidity"]
            y_pressure = df["pressure"]
            
            # Train models
            self.temperature_model.fit(X, y_temp)
            self.humidity_model.fit(X, y_humidity)
            self.pressure_model.fit(X, y_pressure)
            
            self.is_trained = True
            return True
            
        except Exception as e:
            print(f"Error training models: {e}")
            return False
    
    def predict_temperature(self, hours_ahead: int = 6) -> List[float]:
        """Predict future temperatures."""
        if not self.is_trained:
            return []
        
        try:
            # Get the last time point from training
            max_hour = getattr(self, '_max_hour', 0)
            
            # Create future time points
            future_hours = np.array([[max_hour + i] for i in range(1, hours_ahead + 1)])
            
            # Make predictions
            predictions = self.temperature_model.predict(future_hours)
            return predictions.tolist()
            
        except Exception as e:
            print(f"Error predicting temperature: {e}")
            return []
    
    def predict_weather_metrics(self, hours_ahead: int = 6) -> Dict[str, List[float]]:
        """Predict multiple weather metrics."""
        if not self.is_trained:
            return {}
        
        try:
            # Get the last time point from training
            max_hour = getattr(self, '_max_hour', 0)
            
            # Create future time points
            future_hours = np.array([[max_hour + i] for i in range(1, hours_ahead + 1)])
            
            # Make predictions for all metrics
            temp_predictions = self.temperature_model.predict(future_hours)
            humidity_predictions = self.humidity_model.predict(future_hours)
            pressure_predictions = self.pressure_model.predict(future_hours)
            
            return {
                "temperature": temp_predictions.tolist(),
                "humidity": humidity_predictions.tolist(),
                "pressure": pressure_predictions.tolist()
            }
            
        except Exception as e:
            print(f"Error predicting weather metrics: {e}")
            return {}
    
    def get_model_accuracy(self, forecast_data: List[Dict]) -> Dict[str, float]:
        """Calculate model accuracy using test data."""
        if not self.is_trained or not forecast_data:
            return {}
        
        try:
            # Use last 25% of data for testing
            test_size = max(1, len(forecast_data) // 4)
            test_data = forecast_data[-test_size:]
            
            # Convert to DataFrame
            df = pd.DataFrame([
                {
                    "dt": item["dt"],
                    "temp": item["main"]["temp"],
                    "humidity": item["main"]["humidity"],
                    "pressure": item["main"]["pressure"]
                }
                for item in test_data
            ])
            
            # Create time features
            df["time"] = pd.to_datetime(df["dt"], unit="s")
            df["hour"] = (df["time"] - df["time"].min()).dt.total_seconds() / 3600
            
            # Make predictions
            X_test = df[["hour"]]
            temp_pred = self.temperature_model.predict(X_test)
            humidity_pred = self.humidity_model.predict(X_test)
            pressure_pred = self.pressure_model.predict(X_test)
            
            # Calculate R² scores
            from sklearn.metrics import r2_score
            
            temp_r2 = r2_score(df["temp"], temp_pred)
            humidity_r2 = r2_score(df["humidity"], humidity_pred)
            pressure_r2 = r2_score(df["pressure"], pressure_pred)
            
            return {                "temperature_r2": max(0, temp_r2),  # Ensure non-negative
                "humidity_r2": max(0, humidity_r2),
                "pressure_r2": max(0, pressure_r2),
                "overall_r2": max(0, (temp_r2 + humidity_r2 + pressure_r2) / 3)
            }
            
        except Exception as e:
            print(f"Error calculating model accuracy: {e}")
            return {}
    
    def get_trend_analysis(self, forecast_data: List[Dict]) -> Dict[str, str]:
        """Analyze weather trends from forecast data."""
        if not forecast_data or len(forecast_data) < 2:
            return {}
        
        try:
            # Get first and last data points
            first = forecast_data[0]["main"]
            last = forecast_data[-1]["main"]
            
            # Calculate trends
            temp_trend = "rising" if last["temp"] > first["temp"] else "falling"
            humidity_trend = "rising" if last["humidity"] > first["humidity"] else "falling"
            pressure_trend = "rising" if last["pressure"] > first["pressure"] else "falling"
            
            # Calculate magnitude of change
            temp_change = abs(last["temp"] - first["temp"])
            temp_magnitude = "significant" if temp_change > 5 else "moderate" if temp_change > 2 else "slight"
            
            return {
                "temperature_trend": f"{temp_magnitude} {temp_trend}",
                "humidity_trend": humidity_trend,
                "pressure_trend": pressure_trend,
                "forecast_span_hours": f"{len(forecast_data) * 3} hours"  # Convert to string
            }
            
        except Exception as e:
            print(f"Error analyzing trends: {e}")
            return {}
