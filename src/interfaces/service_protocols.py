"""
Service protocols for the Weather Dashboard application.

These protocols define the contracts for service components, ensuring
proper abstraction and dependency inversion.
"""

from typing import Protocol, Dict, Any, Optional, List
from abc import abstractmethod


class DataStorageProtocol(Protocol):
    """Protocol for data storage services."""
    
    def save_data(self, key: str, data: Any) -> bool:
        """Save data with given key."""
        ...
    
    def load_data(self, key: str) -> Optional[Any]:
        """Load data by key."""
        ...
    
    def delete_data(self, key: str) -> bool:
        """Delete data by key."""
        ...
    
    def exists(self, key: str) -> bool:
        """Check if key exists."""
        ...
    
    def list_keys(self) -> List[str]:
        """List all available keys."""
        ...


class ConfigurationProtocol(Protocol):
    """Protocol for configuration management."""
    
    def get_setting(self, key: str, default: Any = None) -> Any:
        """Get setting value."""
        ...
    
    def set_setting(self, key: str, value: Any) -> None:
        """Set setting value."""
        ...
    
    def save_settings(self, **settings) -> bool:
        """Save multiple settings."""
        ...
    
    def load_settings(self) -> Dict[str, Any]:
        """Load all settings."""
        ...
    
    def reset_settings(self) -> bool:
        """Reset settings to defaults."""
        ...
    
    @property
    def current_city(self) -> Optional[str]:
        """Get current city setting."""
        ...
    
    @property
    def current_theme(self) -> str:
        """Get current theme setting."""
        ...


class LoggingProtocol(Protocol):
    """Protocol for logging services."""
    
    def log_info(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log info message."""
        ...
    
    def log_warning(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log warning message."""
        ...
    
    def log_error(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log error message."""
        ...
    
    def log_debug(self, message: str, extra: Optional[Dict[str, Any]] = None) -> None:
        """Log debug message."""
        ...
    
    def log_user_action(self, action: str, data: Dict[str, Any]) -> None:
        """Log user action."""
        ...


class CacheProtocol(Protocol):
    """Protocol for caching services."""
    
    def get(self, key: str) -> Optional[Any]:
        """Get cached value."""
        ...
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cached value with optional TTL."""
        ...
    
    def delete(self, key: str) -> bool:
        """Delete cached value."""
        ...
    
    def clear(self) -> None:
        """Clear all cached values."""
        ...
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        ...


class NotificationServiceProtocol(Protocol):
    """Protocol for notification services."""
    
    def send_notification(self, title: str, message: str, level: str = "info") -> bool:
        """Send notification to user."""
        ...
    
    def schedule_notification(self, title: str, message: str, delay: int) -> bool:
        """Schedule notification for later."""
        ...
    
    def clear_notifications(self) -> None:
        """Clear all pending notifications."""
        ...
