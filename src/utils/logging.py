"""
Professional logging system for the weather dashboard application.

This module provides structured logging with different levels, formatters,
and output handlers for development and production environments.
"""

import os
import sys
import logging
import time
from pathlib import Path
from typing import Any, Optional, Dict
from datetime import datetime


class ColoredFormatter(logging.Formatter):
    """Custom formatter with color support for console output."""
    
    # Color codes
    COLORS = {
        'DEBUG': '\033[36m',     # Cyan
        'INFO': '\033[32m',      # Green
        'WARNING': '\033[33m',   # Yellow
        'ERROR': '\033[31m',     # Red
        'CRITICAL': '\033[35m',  # Magenta
        'RESET': '\033[0m'       # Reset
    }
    
    def format(self, record: logging.LogRecord) -> str:
        """Format the log record with colors."""
        # Add timestamp
        record.asctime = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        
        # Create colored level name
        level_color = self.COLORS.get(record.levelname, self.COLORS['RESET'])
        colored_level = f"{level_color}{record.levelname:8}{self.COLORS['RESET']}"
        
        # Format the message
        formatted = (
            f"{record.asctime} | "
            f"{colored_level} | "
            f"{record.name}:{record.funcName}:{record.lineno} | "
            f"{record.getMessage()}"
        )
        
        # Add exception info if present
        if record.exc_info:
            formatted += f"\n{self.formatException(record.exc_info)}"
        
        return formatted


class WeatherLogger:
    """Professional logging system implementation."""
    
    def __init__(self, name: str = "weather_dashboard", log_level: str = "INFO", log_to_file: bool = True) -> None:
        """Initialize the logging system."""
        self.name = name
        self.log_level = log_level.upper()
        self.log_to_file = log_to_file
        self.logger = logging.getLogger(name)
        self._setup_logger()
    
    def _setup_logger(self) -> None:
        """Set up the logger with appropriate handlers and formatters."""
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
        
        self.logger.setLevel(getattr(logging, self.log_level))
        
        # Console handler with colored output
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(getattr(logging, self.log_level))
        console_formatter = ColoredFormatter()
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handlers for persistent logging
        if self.log_to_file:
            log_dir = Path("logs")
            log_dir.mkdir(exist_ok=True)
            
            # Main log file
            file_handler = logging.FileHandler(log_dir / "weather_dashboard.log")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                '%(asctime)s | %(levelname)-8s | %(name)s:%(funcName)s:%(lineno)d | %(message)s'
            )
            file_handler.setFormatter(file_formatter)
            self.logger.addHandler(file_handler)
            
            # Error-only log file
            error_handler = logging.FileHandler(log_dir / "errors.log")
            error_handler.setLevel(logging.ERROR)
            error_handler.setFormatter(file_formatter)
            self.logger.addHandler(error_handler)
    
    def debug(self, message: str, **kwargs: Any) -> None:
        """Log a debug message."""
        extra_info = f" | {kwargs}" if kwargs else ""
        self.logger.debug(f"{message}{extra_info}")
    
    def info(self, message: str, **kwargs: Any) -> None:
        """Log an info message."""
        extra_info = f" | {kwargs}" if kwargs else ""
        self.logger.info(f"{message}{extra_info}")
    
    def warning(self, message: str, **kwargs: Any) -> None:
        """Log a warning message."""
        extra_info = f" | {kwargs}" if kwargs else ""
        self.logger.warning(f"{message}{extra_info}")
    
    def error(self, message: str, **kwargs: Any) -> None:
        """Log an error message."""
        extra_info = f" | {kwargs}" if kwargs else ""
        self.logger.error(f"{message}{extra_info}")
    
    def critical(self, message: str, **kwargs: Any) -> None:
        """Log a critical message."""
        extra_info = f" | {kwargs}" if kwargs else ""
        self.logger.critical(f"{message}{extra_info}")
    
    def exception(self, message: str, **kwargs: Any) -> None:
        """Log an exception with traceback."""
        extra_info = f" | {kwargs}" if kwargs else ""
        self.logger.exception(f"{message}{extra_info}")
    
    def bind(self, **kwargs: Any) -> "WeatherLogger":
        """Create a new logger instance with bound context."""
        bound_name = f"{self.name}.{'.'.join(f'{k}={v}' for k, v in kwargs.items())}"
        return WeatherLogger(bound_name, self.log_level, self.log_to_file)


class APILogger:
    """Specialized logger for API interactions."""
    
    def __init__(self, base_logger: Optional[WeatherLogger] = None) -> None:
        """Initialize with base logger."""
        self.logger = base_logger or WeatherLogger("weather_dashboard.api")
    
    def log_request(self, method: str, url: str, params: Optional[dict] = None) -> None:
        """Log an API request."""
        params_str = f" with params: {params}" if params else ""
        self.logger.info(f"API Request: {method} {url}{params_str}")
    
    def log_response(self, status_code: int, response_time: float, url: str) -> None:
        """Log an API response."""
        level_func = self.logger.info if 200 <= status_code < 300 else self.logger.warning
        level_func(f"API Response: {status_code} ({response_time:.2f}ms) {url}")
    
    def log_error(self, error: Exception, url: str, context: Optional[dict] = None) -> None:
        """Log an API error."""
        context_str = f" | Context: {context}" if context else ""
        self.logger.error(f"API Error: {error} for {url}{context_str}")


class UILogger:
    """Specialized logger for UI events."""
    
    def __init__(self, base_logger: Optional[WeatherLogger] = None) -> None:
        """Initialize with base logger."""
        self.logger = base_logger or WeatherLogger("weather_dashboard.ui")
    
    def log_user_action(self, action: str, details: Optional[dict] = None) -> None:
        """Log a user action."""
        details_str = f" | Details: {details}" if details else ""
        self.logger.info(f"User Action: {action}{details_str}")
    
    def log_ui_update(self, component: str, data_type: str) -> None:
        """Log a UI update."""
        self.logger.debug(f"UI Update: {component} updated with {data_type}")
    
    def log_ui_error(self, component: str, error: Exception) -> None:
        """Log a UI error."""
        self.logger.error(f"UI Error in {component}: {error}")


class PerformanceLogger:
    """Logger for performance monitoring."""
    
    def __init__(self, base_logger: Optional[WeatherLogger] = None) -> None:
        """Initialize with base logger."""
        self.logger = base_logger or WeatherLogger("weather_dashboard.performance")
    
    def log_execution_time(self, operation: str, duration: float, context: Optional[dict] = None) -> None:
        """Log execution time for an operation."""
        level_func = self.logger.warning if duration > 5.0 else self.logger.info
        context_str = f" | Context: {context}" if context else ""
        level_func(f"Operation '{operation}' took {duration:.2f}s{context_str}")
    
    def log_memory_usage(self, component: str, memory_mb: float) -> None:
        """Log memory usage."""
        self.logger.info(f"Memory usage in {component}: {memory_mb:.1f} MB")


# Global logger instances
_main_logger: Optional[WeatherLogger] = None
_api_logger: Optional[APILogger] = None
_ui_logger: Optional[UILogger] = None
_performance_logger: Optional[PerformanceLogger] = None


def get_logger() -> WeatherLogger:
    """Get the main application logger."""
    global _main_logger
    if _main_logger is None:
        _main_logger = WeatherLogger()
    return _main_logger


def get_api_logger() -> APILogger:
    """Get the API logger."""
    global _api_logger
    if _api_logger is None:
        _api_logger = APILogger()
    return _api_logger


def get_ui_logger() -> UILogger:
    """Get the UI logger."""
    global _ui_logger
    if _ui_logger is None:
        _ui_logger = UILogger()
    return _ui_logger


def get_performance_logger() -> PerformanceLogger:
    """Get the performance logger."""
    global _performance_logger
    if _performance_logger is None:
        _performance_logger = PerformanceLogger()
    return _performance_logger


# Decorator for automatic function logging
def log_function_call(logger_instance: Optional[WeatherLogger] = None):
    """Decorator to automatically log function calls."""
    def decorator(func):
        def wrapper(*args, **kwargs):
            _logger = logger_instance or get_logger()
            _logger.debug(f"Calling {func.__name__}")
            
            try:
                result = func(*args, **kwargs)
                _logger.debug(f"{func.__name__} completed successfully")
                return result
            except Exception as e:
                _logger.error(f"Error in {func.__name__}: {e}")
                raise
        
        return wrapper
    return decorator


# Context manager for performance timing
class performance_timer:
    """Context manager for timing operations."""
    
    def __init__(self, operation_name: str, logger_instance: Optional[PerformanceLogger] = None):
        """Initialize the timer."""
        self.operation_name = operation_name
        self.logger = logger_instance or get_performance_logger()
        self.start_time = None
    
    def __enter__(self):
        """Start timing."""
        self.start_time = time.time()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Stop timing and log results."""
        if self.start_time:
            duration = time.time() - self.start_time
            self.logger.log_execution_time(self.operation_name, duration)


# Structured logging helpers
def log_weather_data_update(city: str, success: bool, error: Optional[str] = None) -> None:
    """Log weather data update with structured data."""
    logger = get_logger()
    
    if success:
        logger.info(f"Weather data updated successfully for {city}")
    else:
        logger.error(f"Failed to update weather data for {city}: {error}")


def log_api_quota_usage(calls_made: int, quota_limit: int) -> None:
    """Log API quota usage."""
    logger = get_api_logger()
    percentage = (calls_made / quota_limit) * 100 if quota_limit > 0 else 0
    
    level_func = logger.logger.warning if percentage > 80 else logger.logger.info
    level_func(f"API quota usage: {calls_made}/{quota_limit} ({percentage:.1f}%)")
