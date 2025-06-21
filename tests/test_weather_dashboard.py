"""
Comprehensive test suite for the weather dashboard application.

This module provides unit tests, integration tests, and end-to-end tests
for all components of the weather dashboard.
"""

import unittest
import pytest
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile
import os
from typing import Dict, Any

# Import application modules
from src.config.config import ConfigurationManager, validate_api_key, validate_coordinates
from src.core.weather_core import WeatherDashboardCore
from src.services.weather_api import WeatherAPIService
from src.models.weather_models import WeatherData, ForecastData, LocationData, AirQualityData
from src.utils.exceptions import APIError, ConfigurationError, DataValidationError
from src.utils.logging import get_logger


class TestConfigurationManager(unittest.TestCase):
    """Test cases for the configuration management system."""
    
    def setUp(self):
        """Set up test environment."""
        self.temp_config_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_config_file.close()
        self.config_manager = ConfigurationManager(self.temp_config_file.name)
    
    def tearDown(self):
        """Clean up test environment."""
        if os.path.exists(self.temp_config_file.name):
            os.unlink(self.temp_config_file.name)
    
    def test_default_configuration(self):
        """Test that default configuration is properly loaded."""
        self.assertEqual(self.config_manager.config.ui.theme, "darkly")
        self.assertEqual(self.config_manager.config.default_city, "Seattle, US")
        self.assertEqual(self.config_manager.config.temperature_unit, "C")
    
    def test_save_and_load_configuration(self):
        """Test saving and loading configuration."""
        # Modify configuration
        self.config_manager.config.ui.theme = "flatly"
        self.config_manager.config.default_city = "New York, NY"
        self.config_manager.save_configuration()
        
        # Create new manager with same config file
        new_manager = ConfigurationManager(self.temp_config_file.name)
        
        # Verify settings were persisted
        self.assertEqual(new_manager.config.ui.theme, "flatly")
        self.assertEqual(new_manager.config.default_city, "New York, NY")
    
    def test_update_setting(self):
        """Test updating individual settings."""
        result = self.config_manager.update_setting("ui", "theme", "superhero")
        self.assertTrue(result)
        self.assertEqual(self.config_manager.config.ui.theme, "superhero")
    
    def test_invalid_setting_update(self):
        """Test handling of invalid setting updates."""
        result = self.config_manager.update_setting("invalid", "setting", "value")
        self.assertFalse(result)
    
    def test_api_key_validation(self):
        """Test API key validation."""
        # Valid API key
        valid_key = "a" * 32
        self.assertTrue(validate_api_key(valid_key))
        
        # Invalid API keys
        with self.assertRaises(ConfigurationError):
            validate_api_key("")
        
        with self.assertRaises(ConfigurationError):
            validate_api_key("short")
    
    def test_coordinate_validation(self):
        """Test coordinate validation."""
        # Valid coordinates
        self.assertTrue(validate_coordinates(40.7128, -74.0060))  # NYC
        
        # Invalid coordinates
        with self.assertRaises(DataValidationError):
            validate_coordinates(91.0, 0.0)  # Invalid latitude
        
        with self.assertRaises(DataValidationError):
            validate_coordinates(0.0, 181.0)  # Invalid longitude


class TestWeatherAPIService(unittest.TestCase):
    """Test cases for the weather API service."""
    
    def setUp(self):
        """Set up test environment."""
        self.api_service = WeatherAPIService("test_api_key")
    
    @patch('src.services.weather_api.requests.get')
    def test_successful_api_request(self, mock_get):
        """Test successful API request handling."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"test": "data"}
        mock_get.return_value = mock_response
        
        result = self.api_service._make_request("http://test.com", {"param": "value"})
        
        self.assertEqual(result, {"test": "data"})
        mock_get.assert_called_once()
    
    @patch('src.services.weather_api.requests.get')
    def test_api_request_failure(self, mock_get):
        """Test API request failure handling."""
        # Mock failed response
        mock_get.side_effect = Exception("Connection error")
        
        result = self.api_service._make_request("http://test.com", {"param": "value"})
        
        self.assertIsNone(result)
    
    def test_get_current_weather_with_valid_coords(self):
        """Test getting current weather with valid coordinates."""
        with patch.object(self.api_service, '_make_request') as mock_request:
            mock_request.return_value = {"weather": "data"}
            
            result = self.api_service.get_current_weather(40.7128, -74.0060)
            
            self.assertEqual(result, {"weather": "data"})
            mock_request.assert_called_once()
    
    def test_geocode_location(self):
        """Test location geocoding."""
        with patch.object(self.api_service, '_make_request') as mock_request:
            mock_request.return_value = [{"name": "New York", "lat": 40.7128, "lon": -74.0060}]
            
            result = self.api_service.geocode_location("New York")
            
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["name"], "New York")


class TestWeatherDataModels(unittest.TestCase):
    """Test cases for weather data models."""
    
    def test_weather_data_creation(self):
        """Test WeatherData model creation from API response."""
        api_response = {
            "main": {
                "temp": 20.5,
                "feels_like": 22.0,
                "humidity": 65,
                "pressure": 1013
            },
            "weather": [{"description": "Clear Sky", "icon": "01d"}],
            "wind": {"speed": 3.5, "deg": 180},
            "visibility": 10000,
            "name": "Test City",
            "sys": {"country": "US"},
            "dt": 1640995200,
            "clouds": {"all": 20}
        }
        
        weather_data = WeatherData.from_api_response(api_response)
        
        self.assertEqual(weather_data.temperature, 20.5)
        self.assertEqual(weather_data.feels_like, 22.0)
        self.assertEqual(weather_data.humidity, 65)
        self.assertEqual(weather_data.description, "Clear Sky")
        self.assertEqual(weather_data.city, "Test City")
    
    def test_location_data_creation(self):
        """Test LocationData model creation."""
        api_response = {
            "name": "New York",
            "lat": 40.7128,
            "lon": -74.0060,
            "country": "US",
            "state": "NY"
        }
        
        location_data = LocationData.from_api_response(api_response)
        
        self.assertEqual(location_data.name, "New York")
        self.assertEqual(location_data.lat, 40.7128)
        self.assertEqual(location_data.lon, -74.0060)
        self.assertEqual(location_data.country, "US")


class TestWeatherDashboardCore(unittest.TestCase):
    """Test cases for the weather dashboard core logic."""
    
    def setUp(self):
        """Set up test environment."""
        with patch('src.core.weather_core.config_manager') as mock_config:
            mock_config.api_key = "test_api_key"
            self.core = WeatherDashboardCore()
    
    def test_initialization(self):
        """Test core initialization."""
        self.assertIsNotNone(self.core.api_service)
        self.assertIsNone(self.core.current_weather)
        self.assertIsNone(self.core.forecast_data)
    
    def test_status_callback(self):
        """Test status callback functionality."""
        callback_mock = Mock()
        self.core.set_status_callback(callback_mock)
        
        self.core._update_status("Test message")
        
        callback_mock.assert_called_once_with("Test message")
    
    def test_data_update_callback(self):
        """Test data update callback functionality."""
        callback_mock = Mock()
        self.core.set_data_update_callback(callback_mock)
        
        self.core._notify_data_update()
        
        callback_mock.assert_called_once()
    
    @patch('src.core.weather_core.threading.Thread')
    def test_load_weather_data(self, mock_thread):
        """Test weather data loading."""
        self.core.load_weather_data("New York")
        
        # Verify that a thread was started
        mock_thread.assert_called_once()
        mock_thread.return_value.start.assert_called_once()
    
    def test_empty_city_handling(self):
        """Test handling of empty city names."""
        status_callback = Mock()
        self.core.set_status_callback(status_callback)
        
        self.core.load_weather_data("")
        
        status_callback.assert_called_with("❌ Please enter a city name")
    
    def test_weather_summary(self):
        """Test weather summary generation."""
        # Mock weather data
        mock_weather = Mock()
        mock_weather.temperature = 25.0
        mock_weather.feels_like = 27.0
        mock_weather.description = "Sunny"
        mock_weather.humidity = 60
        mock_weather.pressure = 1015
        mock_weather.wind_speed = 5.0
        mock_weather.cloudiness = 10
        mock_weather.timestamp = 1640995200
        
        self.core.current_weather = mock_weather
        
        with patch.object(self.core, 'get_location_display_name', return_value="Test City"):
            summary = self.core.get_weather_summary()
        
        self.assertEqual(summary['temperature'], 25.0)
        self.assertEqual(summary['description'], "Sunny")
        self.assertEqual(summary['location'], "Test City")


class TestErrorHandling(unittest.TestCase):
    """Test cases for error handling and exceptions."""
    
    def test_api_error_creation(self):
        """Test API error creation."""
        error = APIError("Test API error", status_code=404, url="http://test.com")
        
        self.assertEqual(str(error), "Test API error")
        self.assertEqual(error.status_code, 404)
        self.assertEqual(error.url, "http://test.com")
        self.assertEqual(error.error_code, "API_ERROR")
    
    def test_configuration_error_creation(self):
        """Test configuration error creation."""
        error = ConfigurationError("Invalid setting", setting_name="theme", setting_value="invalid")
        
        self.assertEqual(str(error), "Invalid setting")
        self.assertEqual(error.setting_name, "theme")
        self.assertEqual(error.setting_value, "invalid")
    
    def test_data_validation_error(self):
        """Test data validation error creation."""
        error = DataValidationError("Invalid data", field_name="temperature", field_value=-300)
        
        self.assertEqual(str(error), "Invalid data")
        self.assertEqual(error.field_name, "temperature")
        self.assertEqual(error.field_value, -300)


class TestLoggingSystem(unittest.TestCase):
    """Test cases for the logging system."""
    
    def test_logger_creation(self):
        """Test logger creation."""
        logger = get_logger()
        self.assertIsNotNone(logger)
        self.assertEqual(logger.logger.name, "weather_dashboard")
    
    def test_log_levels(self):
        """Test different log levels."""
        logger = get_logger()
        
        # These should not raise exceptions
        logger.debug("Debug message")
        logger.info("Info message")
        logger.warning("Warning message")
        logger.error("Error message")
        logger.critical("Critical message")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete application."""
    
    def setUp(self):
        """Set up integration test environment."""
        # Create temporary config file
        self.temp_config = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        config_data = {
            "api": {"api_key": "test_key"},
            "ui": {"theme": "darkly"},
            "default_city": "Seattle, US"
        }
        json.dump(config_data, self.temp_config)
        self.temp_config.close()
    
    def tearDown(self):
        """Clean up integration test environment."""
        if os.path.exists(self.temp_config.name):
            os.unlink(self.temp_config.name)
    
    @patch('src.services.weather_api.WeatherAPIService')
    def test_end_to_end_weather_loading(self, mock_api_service):
        """Test end-to-end weather data loading process."""
        # Mock API responses
        mock_api_instance = Mock()
        mock_api_service.return_value = mock_api_instance
        
        # Mock geocoding response
        mock_api_instance.geocode_location.return_value = [{
            "name": "Seattle",
            "lat": 47.6062,
            "lon": -122.3321,
            "country": "US"
        }]
        
        # Mock weather response
        mock_api_instance.get_current_weather.return_value = {
            "main": {"temp": 15.0, "feels_like": 16.0, "humidity": 70, "pressure": 1010},
            "weather": [{"description": "Cloudy", "icon": "04d"}],
            "wind": {"speed": 3.0, "deg": 200},
            "visibility": 8000,
            "name": "Seattle",
            "sys": {"country": "US"},
            "dt": 1640995200,
            "clouds": {"all": 75}
        }
        
        # Mock forecast response
        mock_api_instance.get_extended_forecast.return_value = {
            "list": []  # Simplified for testing
        }
        
        # Mock air quality response
        mock_api_instance.get_air_pollution.return_value = {
            "list": [{
                "main": {"aqi": 2},
                "components": {"pm2_5": 10.0, "pm10": 15.0, "no2": 5.0, "o3": 50.0}
            }]
        }
        
        # Create core instance
        with patch('src.core.weather_core.config_manager') as mock_config:
            mock_config.api_key = "test_key"
            core = WeatherDashboardCore()
        
        # Set up callbacks
        status_updates = []
        data_updates = []
        
        core.set_status_callback(lambda msg: status_updates.append(msg))
        core.set_data_update_callback(lambda: data_updates.append(True))
        
        # Load weather data (this will run in a thread, so we need to wait)
        import time
        core.load_weather_data("Seattle")
        time.sleep(0.1)  # Give thread time to execute
        
        # Verify API was called
        mock_api_instance.geocode_location.assert_called()
        mock_api_instance.get_current_weather.assert_called()


# Performance tests
class TestPerformance(unittest.TestCase):
    """Performance tests for the application."""
    
    def test_config_loading_performance(self):
        """Test configuration loading performance."""
        import time
        
        start_time = time.time()
        
        # Create and load configuration multiple times
        for _ in range(10):
            config_manager = ConfigurationManager()
        
        elapsed_time = time.time() - start_time
        
        # Configuration loading should be fast (less than 1 second for 10 loads)
        self.assertLess(elapsed_time, 1.0)
    
    def test_data_model_creation_performance(self):
        """Test data model creation performance."""
        import time
        
        api_response = {
            "main": {"temp": 20.5, "feels_like": 22.0, "humidity": 65, "pressure": 1013},
            "weather": [{"description": "Clear Sky", "icon": "01d"}],
            "wind": {"speed": 3.5, "deg": 180},
            "visibility": 10000,
            "name": "Test City",
            "sys": {"country": "US"},
            "dt": 1640995200,
            "clouds": {"all": 20}
        }
        
        start_time = time.time()
        
        # Create weather data objects multiple times
        for _ in range(1000):
            weather_data = WeatherData.from_api_response(api_response)
        
        elapsed_time = time.time() - start_time
        
        # Should be able to create 1000 objects in less than 0.1 seconds
        self.assertLess(elapsed_time, 0.1)


# Test utilities and fixtures
class WeatherTestUtils:
    """Utility functions for weather dashboard testing."""
    
    @staticmethod
    def create_mock_weather_response() -> Dict[str, Any]:
        """Create a mock weather API response."""
        return {
            "main": {
                "temp": 20.5,
                "feels_like": 22.0,
                "humidity": 65,
                "pressure": 1013
            },
            "weather": [{"description": "Clear Sky", "icon": "01d"}],
            "wind": {"speed": 3.5, "deg": 180},
            "visibility": 10000,
            "name": "Test City",
            "sys": {"country": "US"},
            "dt": 1640995200,
            "clouds": {"all": 20}
        }
    
    @staticmethod
    def create_mock_forecast_response() -> Dict[str, Any]:
        """Create a mock forecast API response."""
        return {
            "list": [
                {
                    "dt": 1640995200,
                    "main": {"temp": 18.0, "humidity": 70},
                    "weather": [{"description": "Cloudy", "icon": "04d"}],
                    "wind": {"speed": 2.5}
                }
            ]
        }
    
    @staticmethod
    def create_mock_air_quality_response() -> Dict[str, Any]:
        """Create a mock air quality API response."""
        return {
            "list": [{
                "main": {"aqi": 2},
                "components": {
                    "pm2_5": 10.0,
                    "pm10": 15.0,
                    "no2": 5.0,
                    "o3": 50.0
                }
            }]
        }


if __name__ == '__main__':
    # Run tests with detailed output
    unittest.main(verbosity=2)
