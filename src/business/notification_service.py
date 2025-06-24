"""
Notification Service for the Weather Dashboard application.

This service handles all notification-related business logic, providing
a centralized way to manage user notifications and alerts.
"""

from typing import List, Dict, Any, Optional, Callable
from datetime import datetime, timedelta
from enum import Enum
import threading
import time

from ..utils.logging import get_logger


logger = get_logger()


class NotificationLevel(Enum):
    """Notification severity levels."""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    SUCCESS = "success"


class Notification:
    """Represents a notification message."""
    
    def __init__(self, title: str, message: str, level: NotificationLevel = NotificationLevel.INFO,
                 timestamp: Optional[datetime] = None, auto_dismiss: bool = True,
                 dismiss_after: int = 5000):
        """
        Initialize a notification.
        
        Args:
            title: Notification title
            message: Notification message
            level: Notification level
            timestamp: When notification was created
            auto_dismiss: Whether to auto-dismiss
            dismiss_after: Time in milliseconds to auto-dismiss
        """
        self.title = title
        self.message = message
        self.level = level
        self.timestamp = timestamp or datetime.now()
        self.auto_dismiss = auto_dismiss
        self.dismiss_after = dismiss_after
        self.id = f"{self.timestamp.isoformat()}_{hash(title + message)}"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert notification to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'message': self.message,
            'level': self.level.value,
            'timestamp': self.timestamp.isoformat(),
            'auto_dismiss': self.auto_dismiss,
            'dismiss_after': self.dismiss_after
        }


class NotificationService:
    """
    Service for managing application notifications.
    
    This service provides a centralized way to create, manage, and deliver
    notifications throughout the application while maintaining separation
    of concerns.
    """
    
    def __init__(self):
        """Initialize the notification service."""
        logger.info("Initializing Notification Service")
        
        self._notifications: List[Notification] = []
        self._notification_handlers: List[Callable[[Notification], None]] = []
        self._max_notifications = 10
        self._cleanup_thread: Optional[threading.Thread] = None
        self._running = True
        
        # Start cleanup thread
        self._start_cleanup_thread()
        
        logger.info("Notification Service initialized")
    
    def add_notification_handler(self, handler: Callable[[Notification], None]) -> None:
        """
        Add a notification handler.
        
        Args:
            handler: Function to handle notifications
        """
        self._notification_handlers.append(handler)
        logger.debug("Notification handler added")
    
    def remove_notification_handler(self, handler: Callable[[Notification], None]) -> None:
        """
        Remove a notification handler.
        
        Args:
            handler: Function to remove
        """
        if handler in self._notification_handlers:
            self._notification_handlers.remove(handler)
            logger.debug("Notification handler removed")
    
    def notify_info(self, title: str, message: str, auto_dismiss: bool = True) -> str:
        """
        Create an info notification.
        
        Args:
            title: Notification title
            message: Notification message
            auto_dismiss: Whether to auto-dismiss
            
        Returns:
            Notification ID
        """
        return self._create_notification(title, message, NotificationLevel.INFO, auto_dismiss)
    
    def notify_warning(self, title: str, message: str, auto_dismiss: bool = True) -> str:
        """
        Create a warning notification.
        
        Args:
            title: Notification title
            message: Notification message
            auto_dismiss: Whether to auto-dismiss
            
        Returns:
            Notification ID
        """
        return self._create_notification(title, message, NotificationLevel.WARNING, auto_dismiss)
    
    def notify_error(self, title: str, message: str, auto_dismiss: bool = False) -> str:
        """
        Create an error notification.
        
        Args:
            title: Notification title
            message: Notification message
            auto_dismiss: Whether to auto-dismiss (default False for errors)
            
        Returns:
            Notification ID
        """
        return self._create_notification(title, message, NotificationLevel.ERROR, auto_dismiss)
    
    def notify_success(self, title: str, message: str, auto_dismiss: bool = True) -> str:
        """
        Create a success notification.
        
        Args:
            title: Notification title
            message: Notification message
            auto_dismiss: Whether to auto-dismiss
            
        Returns:
            Notification ID
        """
        return self._create_notification(title, message, NotificationLevel.SUCCESS, auto_dismiss)
    
    def notify_weather_alert(self, weather_condition: str, severity: str, message: str) -> str:
        """
        Create a weather-specific alert.
        
        Args:
            weather_condition: Type of weather condition
            severity: Severity level
            message: Alert message
            
        Returns:
            Notification ID
        """
        title = f"Weather Alert: {weather_condition}"
        
        # Determine notification level based on severity
        if severity.lower() in ['severe', 'extreme']:
            level = NotificationLevel.ERROR
        elif severity.lower() in ['moderate', 'warning']:
            level = NotificationLevel.WARNING
        else:
            level = NotificationLevel.INFO
        
        return self._create_notification(title, message, level, auto_dismiss=False)
    
    def dismiss_notification(self, notification_id: str) -> bool:
        """
        Dismiss a notification by ID.
        
        Args:
            notification_id: ID of notification to dismiss
            
        Returns:
            True if notification was found and dismissed
        """
        for i, notification in enumerate(self._notifications):
            if notification.id == notification_id:
                self._notifications.pop(i)
                logger.debug(f"Notification dismissed: {notification_id}")
                return True
        
        logger.warning(f"Notification not found for dismissal: {notification_id}")
        return False
    
    def clear_all_notifications(self) -> None:
        """Clear all notifications."""
        count = len(self._notifications)
        self._notifications.clear()
        logger.info(f"Cleared {count} notifications")
    
    def get_notifications(self) -> List[Dict[str, Any]]:
        """
        Get all current notifications.
        
        Returns:
            List of notification dictionaries
        """
        return [notification.to_dict() for notification in self._notifications]
    
    def get_notification_count(self) -> int:
        """Get the number of active notifications."""
        return len(self._notifications)
    
    def has_unread_errors(self) -> bool:
        """Check if there are any unread error notifications."""
        return any(n.level == NotificationLevel.ERROR for n in self._notifications)
    
    def stop(self) -> None:
        """Stop the notification service."""
        self._running = False
        if self._cleanup_thread and self._cleanup_thread.is_alive():
            self._cleanup_thread.join()
        logger.info("Notification Service stopped")
    
    # Private methods
    def _create_notification(self, title: str, message: str, level: NotificationLevel,
                           auto_dismiss: bool = True) -> str:
        """Create and deliver a notification."""
        notification = Notification(title, message, level, auto_dismiss=auto_dismiss)
        
        # Add to notifications list
        self._notifications.append(notification)
        
        # Remove old notifications if we exceed the limit
        if len(self._notifications) > self._max_notifications:
            self._notifications.pop(0)
        
        # Deliver to handlers
        self._deliver_notification(notification)
        
        logger.info(f"Notification created: {level.value} - {title}")
        return notification.id
    
    def _deliver_notification(self, notification: Notification) -> None:
        """Deliver notification to all handlers."""
        for handler in self._notification_handlers:
            try:
                handler(notification)
            except Exception as e:
                logger.error(f"Error in notification handler: {e}")
    
    def _start_cleanup_thread(self) -> None:
        """Start background thread for cleaning up expired notifications."""
        def cleanup_expired():
            while self._running:
                try:
                    current_time = datetime.now()
                    expired_notifications = []
                    
                    for notification in self._notifications:
                        if (notification.auto_dismiss and
                            current_time - notification.timestamp > timedelta(milliseconds=notification.dismiss_after)):
                            expired_notifications.append(notification)
                    
                    # Remove expired notifications
                    for notification in expired_notifications:
                        self._notifications.remove(notification)
                        logger.debug(f"Auto-dismissed notification: {notification.id}")
                    
                    time.sleep(1)  # Check every second
                except Exception as e:
                    logger.error(f"Error in notification cleanup thread: {e}")
        
        self._cleanup_thread = threading.Thread(target=cleanup_expired, daemon=True)
        self._cleanup_thread.start()
        logger.debug("Notification cleanup thread started")
