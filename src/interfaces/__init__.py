"""
Interfaces package for the Weather Dashboard application.

This package contains protocols and abstract base classes that define
the contracts between different components of the application, ensuring
loose coupling and high cohesion in the MVC architecture.
"""

from .weather_api_protocol import WeatherAPIProtocol
from .view_protocols import (
    WeatherViewProtocol, 
    MainViewProtocol, 
    NotificationProtocol
)
from .controller_protocols import (
    WeatherControllerProtocol,
    ApplicationControllerProtocol
)
from .service_protocols import (
    DataStorageProtocol,
    ConfigurationProtocol,
    LoggingProtocol,
    CacheProtocol,
    NotificationServiceProtocol
)

__all__ = [
    'WeatherAPIProtocol',
    'WeatherViewProtocol',
    'MainViewProtocol', 
    'NotificationProtocol',
    'WeatherControllerProtocol',
    'ApplicationControllerProtocol',
    'DataStorageProtocol',
    'ConfigurationProtocol',
    'LoggingProtocol',
    'CacheProtocol',
    'NotificationServiceProtocol'
]
