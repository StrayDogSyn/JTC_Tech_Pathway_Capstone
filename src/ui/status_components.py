"""
Status bar and notification components for the weather dashboard.

This module provides status updates, progress indicators, and notifications.
"""

import tkinter as tk
import ttkbootstrap as ttk
from typing import Optional, Dict, Any
from threading import Timer
from datetime import datetime

from ..utils.logging import get_logger


logger = get_logger()


class StatusBarComponent:
    """Enhanced status bar with progress indicators and notifications."""
    
    def __init__(self, parent: tk.Widget):
        """Initialize the status bar component."""
        self.parent = parent
        
        # Status variables
        self.status_var = tk.StringVar()
        self.status_var.set("🚀 Weather Dashboard - Ready")
        self.loading_var = tk.BooleanVar()
        
        # UI components
        self.status_frame: Optional[tk.Widget] = None
        self.status_label: Optional[tk.Label] = None
        self.progress_bar: Optional[ttk.Progressbar] = None
        self.time_label: Optional[tk.Label] = None
        
        # Timer for clearing temporary messages
        self._clear_timer: Optional[Timer] = None
        
        logger.debug("StatusBarComponent initialized")
    
    def create_ui(self) -> tk.Widget:
        """Create the status bar UI."""
        try:
            # Main status frame
            self.status_frame = ttk.Frame(self.parent, relief=tk.SUNKEN, borderwidth=1)
            
            # Status label (left side)
            self.status_label = ttk.Label(
                self.status_frame,
                textvariable=self.status_var,
                font=("Segoe UI", 9)
            )
            self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
            
            # Progress bar (center)
            self.progress_bar = ttk.Progressbar(
                self.status_frame,
                mode='indeterminate',
                length=200
            )
            # Initially hidden
            
            # Time label (right side)
            self.time_label = ttk.Label(
                self.status_frame,
                font=("Segoe UI", 9),
                foreground="gray"
            )
            self.time_label.pack(side=tk.RIGHT, padx=5, pady=2)
            
            # Start time updates
            self._update_time()
            
            logger.info("Status bar UI created successfully")
            return self.status_frame
            
        except Exception as e:
            logger.error(f"Error creating status bar UI: {e}")
            raise
    
    def _update_time(self) -> None:
        """Update the time display."""
        try:
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            if self.time_label:
                self.time_label.config(text=current_time)
            
            # Schedule next update
            self.parent.after(1000, self._update_time)
            
        except Exception as e:
            logger.error(f"Error updating time: {e}")
    
    def set_status(self, message: str, temporary: bool = False, duration: int = 5) -> None:
        """Set the status message."""
        try:
            self.status_var.set(message)
            
            # Cancel previous timer
            if self._clear_timer:
                self._clear_timer.cancel()
            
            # Set timer to clear temporary messages
            if temporary:
                self._clear_timer = Timer(duration, self._clear_temporary_status)
                self._clear_timer.start()
            
            logger.debug(f"Status set: {message} (temporary: {temporary})")
            
        except Exception as e:
            logger.error(f"Error setting status: {e}")
    
    def _clear_temporary_status(self) -> None:
        """Clear temporary status message."""
        try:
            self.status_var.set("🚀 Weather Dashboard - Ready")
        except Exception as e:
            logger.error(f"Error clearing status: {e}")
    
    def set_loading(self, loading: bool) -> None:
        """Set the loading state."""
        try:
            self.loading_var.set(loading)
            
            if loading:
                if self.progress_bar:
                    self.progress_bar.pack(side=tk.LEFT, padx=(10, 5), pady=2)
                    self.progress_bar.start(10)  # Start animation
                self.set_status("⏳ Loading...", temporary=False)
            else:
                if self.progress_bar:
                    self.progress_bar.stop()  # Stop animation
                    self.progress_bar.pack_forget()
                self.set_status("✅ Ready", temporary=True)
            
            logger.debug(f"Loading state set: {loading}")
            
        except Exception as e:
            logger.error(f"Error setting loading state: {e}")
    
    def show_success(self, message: str, duration: int = 3) -> None:
        """Show a success message."""
        try:
            self.set_status(f"✅ {message}", temporary=True, duration=duration)
        except Exception as e:
            logger.error(f"Error showing success message: {e}")
    
    def show_error(self, message: str, duration: int = 5) -> None:
        """Show an error message."""
        try:
            self.set_status(f"❌ {message}", temporary=True, duration=duration)
        except Exception as e:
            logger.error(f"Error showing error message: {e}")
    
    def show_warning(self, message: str, duration: int = 4) -> None:
        """Show a warning message."""
        try:
            self.set_status(f"⚠️ {message}", temporary=True, duration=duration)
        except Exception as e:
            logger.error(f"Error showing warning message: {e}")
    
    def show_info(self, message: str, duration: int = 3) -> None:
        """Show an info message."""
        try:
            self.set_status(f"ℹ️ {message}", temporary=True, duration=duration)
        except Exception as e:
            logger.error(f"Error showing info message: {e}")


class NotificationComponent:
    """Toast-style notifications for the weather dashboard."""
    
    def __init__(self, parent: tk.Widget):
        """Initialize the notification component."""
        self.parent = parent
        self.active_notifications: Dict[str, tk.Toplevel] = {}
        
        logger.debug("NotificationComponent initialized")
    
    def show_notification(
        self, 
        title: str, 
        message: str, 
        notification_type: str = "info",
        duration: int = 5,
        position: str = "top-right"
    ) -> None:
        """Show a toast notification."""
        try:
            # Create notification window
            notification_id = f"{notification_type}_{len(self.active_notifications)}"
            
            # Create toplevel window
            notification = tk.Toplevel(self.parent)
            notification.withdraw()  # Start hidden
            
            # Configure window
            notification.overrideredirect(True)  # Remove window decorations
            notification.attributes('-topmost', True)  # Always on top
            
            # Set window properties based on type
            colors = {
                "info": {"bg": "#17a2b8", "fg": "white"},
                "success": {"bg": "#28a745", "fg": "white"},
                "warning": {"bg": "#ffc107", "fg": "black"},
                "error": {"bg": "#dc3545", "fg": "white"}
            }
            
            color_config = colors.get(notification_type, colors["info"])
            
            # Create content frame
            content_frame = tk.Frame(
                notification,
                bg=color_config["bg"],
                relief=tk.RAISED,
                borderwidth=2
            )
            content_frame.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
            
            # Title label
            title_label = tk.Label(
                content_frame,
                text=title,
                font=("Segoe UI", 10, "bold"),
                bg=color_config["bg"],
                fg=color_config["fg"],
                wraplength=300
            )
            title_label.pack(anchor=tk.W, padx=10, pady=(5, 0))
            
            # Message label
            message_label = tk.Label(
                content_frame,
                text=message,
                font=("Segoe UI", 9),
                bg=color_config["bg"],
                fg=color_config["fg"],
                wraplength=300,
                justify=tk.LEFT
            )
            message_label.pack(anchor=tk.W, padx=10, pady=(0, 5))
            
            # Close button
            close_btn = tk.Button(
                content_frame,
                text="×",
                font=("Segoe UI", 12, "bold"),
                bg=color_config["bg"],
                fg=color_config["fg"],
                bd=0,
                command=lambda: self._close_notification(notification_id)
            )
            close_btn.pack(anchor=tk.NE, padx=5, pady=5)
            
            # Position the notification
            self._position_notification(notification, position)
            
            # Show the notification
            notification.deiconify()
            
            # Store reference
            self.active_notifications[notification_id] = notification
            
            # Set timer to auto-close
            Timer(duration, lambda: self._close_notification(notification_id)).start()
            
            logger.info(f"Notification shown: {title}")
            
        except Exception as e:
            logger.error(f"Error showing notification: {e}")
    
    def _position_notification(self, notification: tk.Toplevel, position: str) -> None:
        """Position the notification window."""
        try:
            notification.update_idletasks()  # Ensure size is calculated
            
            # Get screen dimensions
            screen_width = notification.winfo_screenwidth()
            screen_height = notification.winfo_screenheight()
            
            # Get notification dimensions
            notification_width = notification.winfo_reqwidth()
            notification_height = notification.winfo_reqheight()
            
            # Calculate position based on preference
            margin = 20
            existing_count = len(self.active_notifications)
            vertical_offset = existing_count * (notification_height + 10)
            
            if position == "top-right":
                x = screen_width - notification_width - margin
                y = margin + vertical_offset
            elif position == "top-left":
                x = margin
                y = margin + vertical_offset
            elif position == "bottom-right":
                x = screen_width - notification_width - margin
                y = screen_height - notification_height - margin - vertical_offset
            elif position == "bottom-left":
                x = margin
                y = screen_height - notification_height - margin - vertical_offset
            else:  # center
                x = (screen_width - notification_width) // 2
                y = (screen_height - notification_height) // 2 + vertical_offset
            
            notification.geometry(f"+{x}+{y}")
            
        except Exception as e:
            logger.error(f"Error positioning notification: {e}")
    
    def _close_notification(self, notification_id: str) -> None:
        """Close a specific notification."""
        try:
            if notification_id in self.active_notifications:
                notification = self.active_notifications[notification_id]
                notification.destroy()
                del self.active_notifications[notification_id]
                logger.debug(f"Notification closed: {notification_id}")
                
        except Exception as e:
            logger.error(f"Error closing notification: {e}")
    
    def close_all_notifications(self) -> None:
        """Close all active notifications."""
        try:
            for notification_id in list(self.active_notifications.keys()):
                self._close_notification(notification_id)
            logger.info("All notifications closed")
            
        except Exception as e:
            logger.error(f"Error closing all notifications: {e}")
    
    def show_error(self, title: str, message: str, duration: int = 7) -> None:
        """Show an error notification."""
        self.show_notification(title, message, "error", duration)
    
    def show_success(self, title: str, message: str, duration: int = 4) -> None:
        """Show a success notification."""
        self.show_notification(title, message, "success", duration)
    
    def show_warning(self, title: str, message: str, duration: int = 5) -> None:
        """Show a warning notification."""
        self.show_notification(title, message, "warning", duration)
    
    def show_info(self, title: str, message: str, duration: int = 4) -> None:
        """Show an info notification."""
        self.show_notification(title, message, "info", duration)
