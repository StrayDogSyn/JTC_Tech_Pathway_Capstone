"""
Custom exceptions and error handling for the weather dashboard application.

This module provides specialized exception classes and error handling utilities
for different components of the weather application.
"""

from typing import Optional, Dict, Any, Callable
from src.utils.logging import get_logger

logger = get_logger()


class WeatherDashboardError(Exception):
    """Base exception class for weather dashboard errors."""
    
    def __init__(self, message: str, error_code: Optional[str] = None, context: Optional[Dict[str, Any]] = None):
        """Initialize the exception."""
        super().__init__(message)
        self.message = message
        self.error_code = error_code
        self.context = context or {}
        
        # Log the error automatically
        logger.error(f"Weather Dashboard Error: {message}", 
                    error_code=error_code, context=context)


class APIError(WeatherDashboardError):
    """Exception for API-related errors."""
    
    def __init__(self, message: str, status_code: Optional[int] = None, 
                 url: Optional[str] = None, response_data: Optional[Dict] = None):
        """Initialize API error."""
        context = {
            "status_code": status_code,
            "url": url,
            "response_data": response_data
        }
        super().__init__(message, "API_ERROR", context)
        self.status_code = status_code
        self.url = url
        self.response_data = response_data


class ConfigurationError(WeatherDashboardError):
    """Exception for configuration-related errors."""
    
    def __init__(self, message: str, setting_name: Optional[str] = None, 
                 setting_value: Optional[Any] = None):
        """Initialize configuration error."""
        context = {
            "setting_name": setting_name,
            "setting_value": setting_value
        }
        super().__init__(message, "CONFIG_ERROR", context)
        self.setting_name = setting_name
        self.setting_value = setting_value


class DataValidationError(WeatherDashboardError):
    """Exception for data validation errors."""
    
    def __init__(self, message: str, field_name: Optional[str] = None, 
                 field_value: Optional[Any] = None, validation_rule: Optional[str] = None):
        """Initialize data validation error."""
        context = {
            "field_name": field_name,
            "field_value": field_value,
            "validation_rule": validation_rule
        }
        super().__init__(message, "VALIDATION_ERROR", context)
        self.field_name = field_name
        self.field_value = field_value
        self.validation_rule = validation_rule


# Alias for compatibility
ValidationError = DataValidationError


class WeatherAPIError(APIError):
    """Exception for weather API specific errors."""
    pass


class UIError(WeatherDashboardError):
    """Exception for UI-related errors."""
    
    def __init__(self, message: str, component_name: Optional[str] = None, 
                 user_action: Optional[str] = None):
        """Initialize UI error."""
        context = {
            "component_name": component_name,
            "user_action": user_action
        }
        super().__init__(message, "UI_ERROR", context)
        self.component_name = component_name
        self.user_action = user_action


class NetworkError(WeatherDashboardError):
    """Exception for network-related errors."""
    
    def __init__(self, message: str, timeout: Optional[bool] = None, 
                 connection_error: Optional[bool] = None, url: Optional[str] = None):
        """Initialize network error."""
        context = {
            "timeout": timeout,
            "connection_error": connection_error,
            "url": url
        }
        super().__init__(message, "NETWORK_ERROR", context)
        self.timeout = timeout
        self.connection_error = connection_error
        self.url = url


class DataProcessingError(WeatherDashboardError):
    """Exception for data processing errors."""
    
    def __init__(self, message: str, operation: Optional[str] = None, 
                 data_type: Optional[str] = None):
        """Initialize data processing error."""
        context = {
            "operation": operation,
            "data_type": data_type
        }
        super().__init__(message, "DATA_PROCESSING_ERROR", context)
        self.operation = operation
        self.data_type = data_type


# Error handling decorators and utilities

def handle_api_errors(func):
    """Decorator to handle API-related errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if "timeout" in str(e).lower():
                raise NetworkError(f"API request timed out: {e}", timeout=True)
            elif "connection" in str(e).lower():
                raise NetworkError(f"Connection error: {e}", connection_error=True)
            elif hasattr(e, 'response') and getattr(e, 'response', None):
                response = getattr(e, 'response')
                raise APIError(
                    f"API error: {e}", 
                    status_code=getattr(response, 'status_code', None),
                    url=getattr(response, 'url', None)
                )
            else:
                raise APIError(f"Unexpected API error: {e}")
    return wrapper


def handle_config_errors(func):
    """Decorator to handle configuration errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as e:
            raise ConfigurationError(f"Missing configuration setting: {e}", setting_name=str(e))
        except ValueError as e:
            raise ConfigurationError(f"Invalid configuration value: {e}")
        except Exception as e:
            raise ConfigurationError(f"Configuration error: {e}")
    return wrapper


def handle_ui_errors(func):
    """Decorator to handle UI-related errors."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            # Get the component name from the function or class
            component_name = getattr(func, '__qualname__', func.__name__)
            raise UIError(f"UI error in {component_name}: {e}", component_name=component_name)
    return wrapper


def safe_execute(operation, default_value=None, error_message="Operation failed"):
    """Safely execute an operation with error handling."""
    try:
        return operation()
    except Exception as e:
        logger.error(f"{error_message}: {e}")
        return default_value


class ErrorHandler:
    """Centralized error handler for the application."""
    
    def __init__(self):
        """Initialize the error handler."""
        self.error_counts = {}
        self.last_errors = []
        self.max_stored_errors = 100
    
    def handle_error(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> None:
        """Handle an error with appropriate logging and user notification."""
        error_type = type(error).__name__
        error_message = str(error)
        
        # Count errors
        self.error_counts[error_type] = self.error_counts.get(error_type, 0) + 1
        
        # Store error for debugging
        error_info = {
            "type": error_type,
            "message": error_message,
            "context": context,
            "timestamp": logger.logger.handlers[0].format(logger.logger.makeRecord(
                logger.logger.name, logger.logger.level, "", 0, "", (), None
            ))
        }
        
        self.last_errors.append(error_info)
        if len(self.last_errors) > self.max_stored_errors:
            self.last_errors.pop(0)
        
        # Log based on error type
        if isinstance(error, WeatherDashboardError):
            logger.error(f"Application Error: {error_message}", 
                        error_code=getattr(error, 'error_code', None))
        else:
            logger.exception(f"Unexpected Error: {error_message}")
    
    def get_error_summary(self) -> Dict[str, Any]:
        """Get a summary of recent errors."""
        return {
            "error_counts": self.error_counts.copy(),
            "total_errors": sum(self.error_counts.values()),
            "recent_errors": self.last_errors[-10:],  # Last 10 errors
            "most_common_error": max(self.error_counts.items(), key=lambda x: x[1])[0] if self.error_counts else None
        }
    
    def clear_errors(self) -> None:
        """Clear error history."""
        self.error_counts.clear()
        self.last_errors.clear()
        logger.info("Error history cleared")


# Global error handler instance
error_handler = ErrorHandler()


# Utility functions for common error scenarios

def validate_api_key(api_key: str) -> None:
    """Validate API key format."""
    if not api_key:
        raise ConfigurationError("API key is required", "api_key", api_key)
    
    if len(api_key) < 32:
        raise ConfigurationError("API key appears to be invalid (too short)", "api_key", api_key)
    
    if not api_key.replace('-', '').replace('_', '').isalnum():
        raise ConfigurationError("API key contains invalid characters", "api_key", api_key)


def validate_coordinates(lat: float, lon: float) -> None:
    """Validate latitude and longitude coordinates."""
    if not isinstance(lat, (int, float)) or not isinstance(lon, (int, float)):
        raise DataValidationError("Coordinates must be numeric", "coordinates", (lat, lon))
    
    if not (-90 <= lat <= 90):
        raise DataValidationError("Latitude must be between -90 and 90", "latitude", lat)
    
    if not (-180 <= lon <= 180):
        raise DataValidationError("Longitude must be between -180 and 180", "longitude", lon)


def validate_city_name(city: str) -> None:
    """Validate city name format."""
    if not city or not isinstance(city, str):
        raise DataValidationError("City name must be a non-empty string", "city", city)
    
    city = city.strip()
    if len(city) < 2:
        raise DataValidationError("City name must be at least 2 characters", "city", city)
    
    if city.isdigit():
        raise DataValidationError("City name cannot be only numbers", "city", city)


def handle_critical_error(error: Exception, shutdown_callback: Optional[Callable] = None) -> None:
    """Handle critical errors that may require application shutdown."""
    logger.critical(f"Critical error occurred: {error}")
    error_handler.handle_error(error, {"critical": True})
    
    if shutdown_callback:
        try:
            shutdown_callback()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")


# Context manager for error handling
class error_context:
    """Context manager for handling errors in specific operations."""
    
    def __init__(self, operation_name: str, reraise: bool = True, default_value=None):
        """Initialize error context."""
        self.operation_name = operation_name
        self.reraise = reraise
        self.default_value = default_value
    
    def __enter__(self):
        """Enter error context."""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit error context."""
        if exc_val:
            error_handler.handle_error(exc_val, {"operation": self.operation_name})
            
            if not self.reraise:
                logger.warning(f"Suppressing error in {self.operation_name}: {exc_val}")
                return True  # Suppress the exception
        
        return False  # Let the exception propagate


# Recovery strategies
class RecoveryStrategy:
    """Base class for error recovery strategies."""
    
    def can_recover(self, error: Exception) -> bool:
        """Check if this strategy can recover from the error."""
        return False
    
    def recover(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Any:
        """Attempt to recover from the error."""
        raise NotImplementedError


class NetworkRecoveryStrategy(RecoveryStrategy):
    """Recovery strategy for network errors."""
    
    def __init__(self, max_retries: int = 3, retry_delay: float = 1.0):
        """Initialize network recovery strategy."""
        self.max_retries = max_retries
        self.retry_delay = retry_delay
    
    def can_recover(self, error: Exception) -> bool:
        """Check if this is a recoverable network error."""
        return (isinstance(error, NetworkError) and 
                (bool(error.timeout) or bool(error.connection_error)))
    
    def recover(self, error: Exception, context: Optional[Dict[str, Any]] = None) -> Any:
        """Attempt to recover from network error."""
        import time
        
        for attempt in range(self.max_retries):
            logger.info(f"Attempting network recovery, attempt {attempt + 1}/{self.max_retries}")
            time.sleep(self.retry_delay * (attempt + 1))  # Exponential backoff
            
            try:
                # This would be implemented by the caller
                if context and 'retry_function' in context:
                    return context['retry_function']()
            except Exception as retry_error:
                if attempt == self.max_retries - 1:
                    raise retry_error
                continue
        
        raise error


# Global recovery strategies
network_recovery = NetworkRecoveryStrategy()
recovery_strategies = [network_recovery]


def attempt_recovery(error: Exception, context: Optional[Dict[str, Any]] = None) -> Any:
    """Attempt to recover from an error using available strategies."""
    for strategy in recovery_strategies:
        if strategy.can_recover(error):
            try:
                return strategy.recover(error, context)
            except Exception as recovery_error:
                logger.error(f"Recovery failed: {recovery_error}")
                continue
    
    # No recovery possible
    raise error
