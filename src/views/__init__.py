"""
Views package for the Weather Dashboard application.

This package contains the view classes that implement the MVC pattern,
handling UI concerns and presentation logic while remaining decoupled
from business logic.
"""

from .weather_view import WeatherView
from .main_view import MainView

__all__ = ['WeatherView', 'MainView']
