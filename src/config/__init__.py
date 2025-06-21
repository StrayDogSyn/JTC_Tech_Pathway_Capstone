"""
Configuration management module.

This module provides configuration loading and validation for the weather dashboard.
"""

from .config import ApplicationConfiguration, ConfigurationManager, APP_CONFIG, setup_environment

__all__ = ['ApplicationConfiguration', 'ConfigurationManager', 'APP_CONFIG', 'setup_environment']
