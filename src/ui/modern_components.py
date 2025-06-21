"""
Modern UI components with advanced UX features.

This module provides enhanced UI components with animations, gradients,
and modern design elements for the weather dashboard.
"""

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import Canvas
from typing import Optional, Callable, Dict, Any, List
import math
from datetime import datetime, timedelta
import threading
import time


class AnimatedWidget:
    """Base class for animated widgets."""
    
    def __init__(self):
        self.animations = []
        self.animation_running = False
    
    def start_animation(self, duration: float = 1.0, easing: str = "ease_out"):
        """Start widget animation."""
        if self.animation_running:
            return
        
        self.animation_running = True
        threading.Thread(target=self._animate, args=(duration, easing), daemon=True).start()
    
    def _animate(self, duration: float, easing: str):
        """Animation worker thread."""
        steps = 60  # 60 FPS
        step_time = duration / steps
        
        for i in range(steps + 1):
            progress = i / steps
            if easing == "ease_out":
                progress = 1 - (1 - progress) ** 3
            elif easing == "ease_in":
                progress = progress ** 3
            elif easing == "ease_in_out":
                progress = 3 * progress**2 - 2 * progress**3
            
            self._update_animation(progress)
            time.sleep(step_time)
        
        self.animation_running = False
    
    def _update_animation(self, progress: float):
        """Override in subclasses."""
        pass


class ModernCard(ttk.Frame, AnimatedWidget):
    """Modern card component with shadow and hover effects."""
    
    def __init__(self, parent, title: str = "", **kwargs):
        # Comprehensive filtering of unsupported parameters
        # These might be passed from old code or user error
        unsupported_params = {
            'subtitle', 'elevation', 'shadow', 'rounded', 'card_style',
            'border_width', 'border_color', 'background_color',
            'hover_color', 'click_color'
        }
        
        # Filter kwargs to only include valid ttk.Frame parameters
        valid_frame_params = {
            'borderwidth', 'relief', 'padding', 'width', 'height', 
            'takefocus', 'cursor', 'style', 'class'
        }
        
        # Keep only valid parameters or those that don't conflict
        filtered_kwargs = {}
        for key, value in kwargs.items():
            if key not in unsupported_params:
                if key in valid_frame_params or not key.startswith('_'):
                    filtered_kwargs[key] = value
        
        # Initialize parent classes with filtered parameters
        try:
            ttk.Frame.__init__(self, parent, **filtered_kwargs)
        except tk.TclError as e:
            # If there's still an error, try with minimal parameters
            print(f"Warning: ModernCard parameter error: {e}")
            ttk.Frame.__init__(self, parent)
        
        AnimatedWidget.__init__(self)        
        # Store title and initialize other attributes
        self.title = title
        self.hover_scale = 1.0
        self.target_scale = 1.0
        
        # Debug: Log any filtered parameters
        if any(param in kwargs for param in unsupported_params):
            filtered_params = [param for param in unsupported_params if param in kwargs]
            print(f"ModernCard: Filtered unsupported parameters: {filtered_params}")
        
        self._setup_card()
        self._bind_hover_events()
    
    def _setup_card(self):
        """Set up the card layout."""
        # Configure grid weights
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
          # Title section
        if self.title:
            self.title_frame = ttk.Frame(self, style="Secondary.TFrame")
            self.title_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=(2, 0))
            
            title_label = ttk.Label(
                self.title_frame,
                text=self.title,
                font=('Segoe UI', 14, 'bold'),
                anchor="center"
            )
            title_label.pack(pady=8)
        
        # Content area
        self.content_frame = ttk.Frame(self)
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=2, pady=(0, 2))
        self.content_frame.grid_rowconfigure(0, weight=1)
        self.content_frame.grid_columnconfigure(0, weight=1)
    
    def _bind_hover_events(self):
        """Bind hover events for modern interaction."""
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        
        # Bind to all child widgets
        def bind_recursive(widget):
            widget.bind("<Enter>", self._on_enter)
            widget.bind("<Leave>", self._on_leave)
            for child in widget.winfo_children():
                bind_recursive(child)
        
        self.after(100, lambda: bind_recursive(self))
    
    def _on_enter(self, event):
        """Handle mouse enter."""
        self.target_scale = 1.02
        if not self.animation_running:
            self.start_animation(0.2, "ease_out")
    
    def _on_leave(self, event):
        """Handle mouse leave."""
        self.target_scale = 1.0
        if not self.animation_running:
            self.start_animation(0.2, "ease_out")
    
    def _update_animation(self, progress: float):
        """Update hover animation."""
        current_scale = self.hover_scale + (self.target_scale - self.hover_scale) * progress
        self.hover_scale = current_scale
        
        # Update styling to simulate scaling
        relief = "solid" if self.hover_scale > 1.0 else "flat"
        try:
            self.configure(relief=relief, borderwidth=1 if relief == "solid" else 0)
        except:
            pass
    
    def get_content_frame(self) -> ttk.Frame:
        """Get the content frame for adding widgets."""
        return self.content_frame


class CircularProgress(Canvas, AnimatedWidget):
    """Circular progress indicator with smooth animations."""
    
    def __init__(self, parent, size: int = 120, thickness: int = 8, **kwargs):
        Canvas.__init__(self, parent, width=size, height=size, highlightthickness=0, **kwargs)
        AnimatedWidget.__init__(self)
        
        self.size = size
        self.thickness = thickness
        self.progress = 0.0
        self.target_progress = 0.0
        self.center = size // 2
        self.radius = (size - thickness) // 2
        
        self._setup_progress()
    
    def _setup_progress(self):
        """Set up the progress circle."""
        # Background circle
        self.create_oval(
            self.center - self.radius,
            self.center - self.radius,
            self.center + self.radius,
            self.center + self.radius,
            outline="#E0E0E0",
            width=self.thickness,
            fill=""
        )
        
        # Progress arc
        self.progress_arc = self.create_arc(
            self.center - self.radius,
            self.center - self.radius,
            self.center + self.radius,
            self.center + self.radius,
            start=90,
            extent=0,
            outline="#4CAF50",
            width=self.thickness,
            style="arc"
        )
    
    def set_progress(self, value: float):
        """Set progress value (0.0 to 1.0) with animation."""
        self.target_progress = max(0.0, min(1.0, value))
        if not self.animation_running:
            self.start_animation(0.8, "ease_out")
    
    def _update_animation(self, progress: float):
        """Update progress animation."""
        current_progress = self.progress + (self.target_progress - self.progress) * progress
        self.progress = current_progress
        
        # Update arc extent
        extent = -360 * self.progress  # Negative for clockwise
        self.itemconfig(self.progress_arc, extent=extent)
        
        # Update color based on progress
        if self.progress < 0.3:
            color = "#FF5722"  # Red
        elif self.progress < 0.7:
            color = "#FF9800"  # Orange
        else:
            color = "#4CAF50"  # Green
        
        self.itemconfig(self.progress_arc, outline=color)


class ModernSearchBar(ttk.Frame):
    """Modern search bar with auto-complete and suggestions."""
    
    def __init__(self, parent, placeholder: str = "Search...", **kwargs):
        super().__init__(parent, **kwargs)
        
        self.placeholder = placeholder
        self.search_callback: Optional[Callable[[str], None]] = None
        self.suggestions_callback: Optional[Callable[[str], List[str]]] = None
        self.current_suggestions = []
        
        self._setup_search_bar()
    
    def _setup_search_bar(self):
        """Set up the search bar components."""
        # Configure grid
        self.grid_columnconfigure(0, weight=1)
          # Search frame
        search_frame = ttk.Frame(self, style="Secondary.TFrame")
        search_frame.grid(row=0, column=0, sticky="ew", padx=2, pady=2)
        search_frame.grid_columnconfigure(1, weight=1)
        
        # Search icon
        search_icon = ttk.Label(search_frame, text="🔍", font=('Segoe UI', 12))
        search_icon.grid(row=0, column=0, padx=(10, 5), pady=8)
        
        # Search entry
        self.search_var = tk.StringVar()
        self.entry = ttk.Entry(
            search_frame,
            textvariable=self.search_var,
            font=('Segoe UI', 11),
            foreground="gray"
        )
        self.entry.grid(row=0, column=1, sticky="ew", padx=(0, 5), pady=5)
          # Clear button
        self.clear_btn = ttk.Button(
            search_frame,
            text="✕",
            width=3,
            command=self._clear_search
        )
        self.clear_btn.grid(row=0, column=2, padx=(0, 5), pady=5)
        
        # Search button
        search_btn = ttk.Button(
            search_frame,
            text="Search",
            command=self._perform_search
        )
        search_btn.grid(row=0, column=3, padx=(0, 10), pady=5)
        
        # Suggestions listbox (initially hidden)
        self.suggestions_frame = ttk.Frame(self)
        self.suggestions_listbox = tk.Listbox(
            self.suggestions_frame,
            height=5,
            font=('Segoe UI', 10),
            activestyle="none",
            selectmode=tk.SINGLE
        )
        self.suggestions_listbox.pack(fill="both", expand=True)
        
        # Bind events
        self.entry.bind('<FocusIn>', self._on_focus_in)
        self.entry.bind('<FocusOut>', self._on_focus_out)
        self.entry.bind('<KeyRelease>', self._on_key_release)
        self.entry.bind('<Return>', lambda e: self._perform_search())
        self.suggestions_listbox.bind('<Double-Button-1>', self._on_suggestion_select)
        
        # Set placeholder
        self._set_placeholder()
    
    def _set_placeholder(self):
        """Set placeholder text."""
        self.entry.insert(0, self.placeholder)
        self.entry.configure(foreground="gray")
    
    def _on_focus_in(self, event):
        """Handle focus in event."""
        if self.search_var.get() == self.placeholder:
            self.entry.delete(0, tk.END)
            self.entry.configure(foreground="black")
    
    def _on_focus_out(self, event):
        """Handle focus out event."""
        if not self.search_var.get():
            self._set_placeholder()
        self._hide_suggestions()
    
    def _on_key_release(self, event):
        """Handle key release for auto-suggestions."""
        query = self.search_var.get()
        if query and query != self.placeholder and self.suggestions_callback:
            suggestions = self.suggestions_callback(query)
            self._show_suggestions(suggestions)
        else:
            self._hide_suggestions()
    
    def _show_suggestions(self, suggestions: List[str]):
        """Show suggestions dropdown."""
        if not suggestions:
            self._hide_suggestions()
            return
        
        self.current_suggestions = suggestions
        self.suggestions_listbox.delete(0, tk.END)
        for suggestion in suggestions:
            self.suggestions_listbox.insert(tk.END, suggestion)
        
        self.suggestions_frame.grid(row=1, column=0, sticky="ew", padx=2)
    
    def _hide_suggestions(self):
        """Hide suggestions dropdown."""
        self.suggestions_frame.grid_remove()
    
    def _on_suggestion_select(self, event):
        """Handle suggestion selection."""
        selection = self.suggestions_listbox.curselection()
        if selection:
            selected_text = self.suggestions_listbox.get(selection[0])
            self.search_var.set(selected_text)
            self._hide_suggestions()
            self._perform_search()
    
    def _clear_search(self):
        """Clear search field."""
        self.entry.delete(0, tk.END)
        self._hide_suggestions()
        self.entry.focus()
    
    def _perform_search(self):
        """Perform search."""
        query = self.search_var.get()
        if query and query != self.placeholder and self.search_callback:
            self.search_callback(query)
        self._hide_suggestions()
    
    def set_search_callback(self, callback: Callable[[str], None]):
        """Set search callback."""
        self.search_callback = callback
    
    def set_suggestions_callback(self, callback: Callable[[str], List[str]]):
        """Set suggestions callback."""
        self.suggestions_callback = callback


class WeatherGauge(Canvas, AnimatedWidget):
    """Modern weather gauge with animated needle."""
    
    def __init__(self, parent, size: int = 150, min_val: float = 0, max_val: float = 100, 
                 unit: str = "", title: str = "", **kwargs):
        Canvas.__init__(self, parent, width=size, height=size, highlightthickness=0, **kwargs)
        AnimatedWidget.__init__(self)
        
        self.size = size
        self.min_val = min_val
        self.max_val = max_val
        self.unit = unit
        self.title = title
        self.current_value = min_val
        self.target_value = min_val
        self.center = size // 2
        self.radius = size // 3
        
        self._setup_gauge()
    
    def _setup_gauge(self):
        """Set up the gauge display."""
        # Background arc
        self.create_arc(
            self.center - self.radius,
            self.center - self.radius,
            self.center + self.radius,
            self.center + self.radius,
            start=225,
            extent=90,
            outline="#E0E0E0",
            width=15,
            style="arc"
        )
        
        # Title
        if self.title:
            self.create_text(
                self.center,
                self.center - self.radius - 20,
                text=self.title,
                font=('Segoe UI', 12, 'bold'),
                fill="black"
            )
        
        # Value text
        self.value_text = self.create_text(
            self.center,
            self.center + 10,
            text=f"{self.current_value:.1f}{self.unit}",
            font=('Segoe UI', 16, 'bold'),
            fill="black"
        )
        
        # Needle
        self.needle = self.create_line(
            self.center,
            self.center,
            self.center,
            self.center - self.radius + 10,
            fill="red",
            width=3,
            capstyle="round"
        )
    
    def set_value(self, value: float):
        """Set gauge value with animation."""
        self.target_value = max(self.min_val, min(self.max_val, value))
        if not self.animation_running:
            self.start_animation(1.0, "ease_out")
    
    def _update_animation(self, progress: float):
        """Update gauge animation."""
        # Interpolate value
        self.current_value = self.current_value + (self.target_value - self.current_value) * progress
        
        # Update value text
        self.itemconfig(self.value_text, text=f"{self.current_value:.1f}{self.unit}")
        
        # Calculate needle angle
        value_ratio = (self.current_value - self.min_val) / (self.max_val - self.min_val)
        angle = 225 + (90 * value_ratio)  # 225° to 315°
        angle_rad = math.radians(angle)
        
        # Calculate needle end position
        needle_length = self.radius - 10
        end_x = self.center + needle_length * math.cos(angle_rad)
        end_y = self.center + needle_length * math.sin(angle_rad)
        
        # Update needle
        self.coords(self.needle, self.center, self.center, end_x, end_y)


class NotificationToast(ttk.Toplevel, AnimatedWidget):
    """Modern notification toast with auto-dismiss."""
    
    def __init__(self, parent, message: str, toast_type: str = "info", duration: float = 3.0):
        ttk.Toplevel.__init__(self, parent)
        AnimatedWidget.__init__(self)
        
        self.message = message
        self.toast_type = toast_type
        self.duration = duration
        self.alpha = 0.0
        
        self._setup_toast()
        self._position_toast()
        self._show_toast()
    
    def _setup_toast(self):
        """Set up the toast appearance."""
        # Configure window
        self.overrideredirect(True)
        self.attributes('-topmost', True)
        self.attributes('-alpha', 0.0)
        
        # Configure style based on type
        style_map = {
            "info": ("info", "ℹ️"),
            "success": ("success", "✅"),
            "warning": ("warning", "⚠️"),
            "error": ("danger", "❌")
        }
        
        bootstyle, icon = style_map.get(self.toast_type, ("info", "ℹ️"))
          # Main frame
        main_frame = ttk.Frame(self, padding=15)
        main_frame.pack(fill="both", expand=True)
        
        # Icon and message
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="x")
        
        icon_label = ttk.Label(content_frame, text=icon, font=('Segoe UI', 16))
        icon_label.pack(side="left", padx=(0, 10))
        
        message_label = ttk.Label(
            content_frame,
            text=self.message,
            font=('Segoe UI', 11),
            wraplength=300
        )
        message_label.pack(side="left", fill="x", expand=True)
          # Close button
        close_btn = ttk.Button(
            content_frame,
            text="✕",
            width=3,
            command=self._hide_toast
        )
        close_btn.pack(side="right", padx=(10, 0))
    
    def _position_toast(self):
        """Position toast in the top-right corner."""
        self.update_idletasks()
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        
        # Get screen dimensions
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Position in top-right corner
        x = screen_width - width - 20
        y = 20
        
        self.geometry(f"{width}x{height}+{x}+{y}")
    
    def _show_toast(self):
        """Show toast with fade-in animation."""
        self.start_animation(0.5, "ease_out")
        
        # Auto-dismiss after duration
        self.after(int(self.duration * 1000), self._hide_toast)
    
    def _hide_toast(self):
        """Hide toast with fade-out animation."""
        self.target_alpha = 0.0
        threading.Thread(target=self._fade_out, daemon=True).start()
    
    def _fade_out(self):
        """Fade out animation."""
        steps = 20
        step_time = 0.3 / steps
        
        for i in range(steps + 1):
            alpha = 1.0 - (i / steps)
            self.attributes('-alpha', alpha)
            time.sleep(step_time)
        
        self.destroy()
    
    def _update_animation(self, progress: float):
        """Update fade-in animation."""
        self.alpha = progress
        self.attributes('-alpha', self.alpha)


class ModernToggleSwitch(ttk.Frame):
    """Modern toggle switch component."""
    
    def __init__(self, parent, text: str = "", initial_state: bool = False, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.text = text
        self.toggle_state = initial_state
        self.callback: Optional[Callable[[bool], None]] = None
        
        self._setup_switch()
    
    def _setup_switch(self):
        """Set up the toggle switch."""
        # Configure grid
        self.grid_columnconfigure(1, weight=1)
        
        # Switch canvas
        self.canvas = Canvas(self, width=50, height=25, highlightthickness=0)
        self.canvas.grid(row=0, column=0, padx=(0, 10) if self.text else 0, pady=5)
        
        # Text label
        if self.text:
            self.label = ttk.Label(self, text=self.text, font=('Segoe UI', 11))
            self.label.grid(row=0, column=1, sticky="w", pady=5)
        
        # Draw switch
        self._draw_switch()
        
        # Bind click event
        self.canvas.bind("<Button-1>", self._toggle)
        if hasattr(self, 'label'):
            self.label.bind("<Button-1>", self._toggle)
    
    def _draw_switch(self):
        """Draw the switch appearance."""
        self.canvas.delete("all")
        
        # Background
        bg_color = "#4CAF50" if self.toggle_state else "#E0E0E0"
        self.canvas.create_oval(2, 2, 48, 23, fill=bg_color, outline=bg_color)
        
        # Handle
        handle_x = 35 if self.toggle_state else 15
        self.canvas.create_oval(handle_x - 8, 4, handle_x + 8, 21, fill="white", outline="#CCC")
    
    def _toggle(self, event=None):
        """Toggle switch state."""
        self.toggle_state = not self.toggle_state
        self._draw_switch()
        
        if self.callback:
            self.callback(self.toggle_state)
    
    def set_state(self, state: bool):
        """Set switch state programmatically."""
        self.toggle_state = state
        self._draw_switch()
    
    def set_callback(self, callback: Callable[[bool], None]):
        """Set toggle callback."""
        self.callback = callback


class LoadingSpinner(Canvas, AnimatedWidget):
    """Modern loading spinner with smooth rotation."""
    
    def __init__(self, parent, size: int = 40, **kwargs):
        Canvas.__init__(self, parent, width=size, height=size, highlightthickness=0, **kwargs)
        AnimatedWidget.__init__(self)
        
        self.size = size
        self.center = size // 2
        self.rotation = 0
        self.is_spinning = False
        
        self._setup_spinner()
    
    def _setup_spinner(self):
        """Set up the spinner appearance."""
        # Create dots in a circle
        self.dots = []
        num_dots = 8
        radius = self.size // 3
        
        for i in range(num_dots):
            angle = (2 * math.pi * i) / num_dots
            x = self.center + radius * math.cos(angle)
            y = self.center + radius * math.sin(angle)
            
            # Calculate opacity based on position
            opacity = 1.0 - (i / num_dots)
            color = self._opacity_to_color(opacity)
            
            dot = self.create_oval(x-3, y-3, x+3, y+3, fill=color, outline=color)
            self.dots.append((dot, angle))
    
    def _opacity_to_color(self, opacity: float) -> str:
        """Convert opacity to grayscale color."""
        value = int(255 * (1 - opacity * 0.8))
        return f"#{value:02x}{value:02x}{value:02x}"
    
    def start_spinning(self):
        """Start the spinning animation."""
        if self.is_spinning:
            return
        
        self.is_spinning = True
        self._spin()
    
    def stop_spinning(self):
        """Stop the spinning animation."""
        self.is_spinning = False
    
    def _spin(self):
        """Spin animation loop."""
        if not self.is_spinning:
            return
        
        self.rotation += 0.2
        
        # Update dot positions and colors
        for i, (dot, base_angle) in enumerate(self.dots):
            angle = base_angle + self.rotation
            x = self.center + (self.size // 3) * math.cos(angle)
            y = self.center + (self.size // 3) * math.sin(angle)
            
            # Update position
            self.coords(dot, x-3, y-3, x+3, y+3)
            
            # Update color based on rotation
            opacity = (math.sin(angle + math.pi) + 1) / 2
            color = self._opacity_to_color(opacity)
            self.itemconfig(dot, fill=color, outline=color)
        
        # Schedule next frame
        self.after(50, self._spin)
