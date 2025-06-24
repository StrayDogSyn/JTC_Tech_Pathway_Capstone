"""
Glassmorphic UI components for modern, translucent design.

This module provides glassmorphic design components with frosted glass effects,
transparency, blur simulation, and subtle borders.
"""

import tkinter as tk
import ttkbootstrap as ttk
from tkinter import Canvas
from typing import Optional, Callable, Dict, Any, List, Tuple
import math
import colorsys


class GlassmorphicStyle:
    """Glassmorphic design system with color schemes and effects."""
      # Glassmorphic color palettes (tkinter compatible)
    GLASS_COLORS = {
        "light": {
            "background": "#f0f0f3",
            "glass_bg": "#ffffff",
            "glass_border": "#e0e0e0",
            "text_primary": "#2c3e50",
            "text_secondary": "#7f8c8d",
            "accent": "#3498db",
            "shadow": "#d0d0d0"
        },
        "dark": {
            "background": "#1a1a2e",
            "glass_bg": "#2a2a3e",
            "glass_border": "#3a3a4e", 
            "text_primary": "#ffffff",
            "text_secondary": "#b0b0b0",
            "accent": "#64b5f6",
            "shadow": "#0a0a1e"
        },
        "aurora": {
            "background": "#0f0f23",
            "glass_bg": "#1f1f33",
            "glass_border": "#2f2f43",
            "text_primary": "#ffffff",
            "text_secondary": "#a0a0a0",
            "accent": "#64b5f6",
            "shadow": "#05051a"
        }
    }
    
    @classmethod
    def get_gradient_colors(cls, base_color: str, steps: int = 5) -> List[str]:
        """Generate gradient colors for glassmorphic effects."""
        # Convert hex to RGB
        r, g, b = tuple(int(base_color.lstrip('#')[i:i+2], 16) for i in (0, 2, 4))
        
        colors = []
        for i in range(steps):
            alpha = int(255 * (0.1 + 0.8 * i / (steps - 1)))
            colors.append(f"#{r:02x}{g:02x}{b:02x}{alpha:02x}")
        
        return colors
    
    @classmethod
    def create_blur_effect(cls, canvas: Canvas, x: int, y: int, width: int, height: int, 
                          base_color: str = "#ffffff", alpha: float = 0.1, blur_radius: int = 3):
        """Simulate blur effect using layered rectangles with varying opacity."""
        for i in range(blur_radius):
            current_alpha = alpha * (1 - i / blur_radius)
            alpha_hex = format(int(255 * current_alpha), '02x')
            color = f"{base_color}{alpha_hex}"
            
            canvas.create_rectangle(
                x - i, y - i, x + width + i, y + height + i,
                fill=color, outline="", tags="blur_effect"
            )


class GlassmorphicFrame(ttk.Frame):
    """Glassmorphic frame with frosted glass effect."""
    
    def __init__(self, parent, style_theme: str = "dark", blur_intensity: float = 0.15, 
                 border_radius: int = 15, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.style_theme = style_theme
        self.blur_intensity = blur_intensity
        self.border_radius = border_radius
        self.colors = GlassmorphicStyle.GLASS_COLORS[style_theme]
        
        # Configure the frame appearance
        self.configure(relief="flat", borderwidth=0)
        
        # Create glassmorphic canvas overlay
        self.glass_canvas = Canvas(
            self, highlightthickness=0, relief="flat",
            bg=self.colors["background"]
        )
        self.glass_canvas.place(x=0, y=0, relwidth=1, relheight=1)
        
        # Create content frame that sits above the glass effect
        self.content_frame = ttk.Frame(self)
        self.content_frame.place(x=15, y=15, relwidth=1, relheight=1, width=-30, height=-30)
        
        # Bind resize event
        self.bind("<Configure>", self._on_resize)
        
        # Draw initial glass effect
        self.after(10, self._draw_glass_effect)
    
    def _on_resize(self, event):
        """Handle frame resize."""
        if event.widget == self:
            self.after(10, self._draw_glass_effect)
    def _draw_glass_effect(self):
        """Draw the glassmorphic effect using tkinter-compatible colors."""
        self.glass_canvas.delete("glass_effect")
        
        width = self.glass_canvas.winfo_width()
        height = self.glass_canvas.winfo_height()
        
        if width <= 1 or height <= 1:
            return
        
        # Main glass background
        self.glass_canvas.create_rectangle(
            2, 2, width - 2, height - 2,
            fill=self.colors["glass_bg"],
            outline=self.colors["glass_border"],
            width=1,
            tags="glass_effect"
        )
        
        # Add subtle gradient effect using multiple rectangles
        self._add_gradient_overlay()
        
        # Add border highlights for glass effect
        self._add_border_highlight()
    
    def _draw_rounded_rectangle(self, canvas, x1, y1, x2, y2, radius, **kwargs):
        """Draw a rounded rectangle on canvas."""
        points = []
        
        # Calculate corner coordinates
        for x, y in [(x1, y1), (x2, y1), (x2, y2), (x1, y2)]:
            points.extend([x, y])
        
        # Simple rectangle for now (tkinter doesn't support true rounded rectangles)
        return canvas.create_rectangle(x1, y1, x2, y2, **kwargs)
    def _add_gradient_overlay(self):
        """Add a subtle gradient overlay for depth using tkinter-compatible colors."""
        width = self.glass_canvas.winfo_width()
        height = self.glass_canvas.winfo_height()
        
        # Create a subtle highlight near the top
        highlight_height = height // 6
        self.glass_canvas.create_rectangle(
            3, 3, width - 3, highlight_height,
            fill=self.colors["glass_border"],
            outline="",
            tags="glass_effect"
        )
    def _add_border_highlight(self):
        """Add subtle border highlights for glassmorphic effect."""
        width = self.glass_canvas.winfo_width()
        height = self.glass_canvas.winfo_height()
        
        # Top and left highlights (lighter)
        self.glass_canvas.create_line(
            1, 1, width - 1, 1,
            fill=self.colors["glass_border"], width=1, tags="glass_effect"
        )
        self.glass_canvas.create_line(
            1, 1, 1, height - 1,
            fill=self.colors["glass_border"], width=1, tags="glass_effect"
        )
        
        # Bottom and right shadows (darker)
        self.glass_canvas.create_line(
            0, height - 1, width, height - 1,
            fill=self.colors["shadow"], width=1, tags="glass_effect"
        )
        self.glass_canvas.create_line(
            width - 1, 0, width - 1, height,
            fill=self.colors["shadow"], width=1, tags="glass_effect"
        )


class GlassmorphicCard(GlassmorphicFrame):
    """Glassmorphic card component with content area."""
    
    def __init__(self, parent, title: str = "", style_theme: str = "dark", **kwargs):
        super().__init__(parent, style_theme=style_theme, **kwargs)
        
        self.title = title
        self.content_frame = None
        
        # Create content area
        self._create_content_area()
    
    def _create_content_area(self):
        """Create the content area within the glass frame."""
        # Content frame that sits above the glass effect
        self.content_frame = ttk.Frame(self, style="Glass.TFrame")
        self.content_frame.place(x=15, y=15, relwidth=1, relheight=1, width=-30, height=-30)
        if self.title:
            # Title label with glassmorphic styling
            title_label = ttk.Label(
                self.content_frame,
                text=self.title,
                font=("Segoe UI", 14, "bold"),
                foreground=self.colors["text_primary"],
                background=self.colors["glass_bg"]
            )
            title_label.pack(anchor="w", pady=(0, 10))
    
    def add_content(self, widget):
        """Add content to the glassmorphic card."""
        if self.content_frame:
            widget.pack(in_=self.content_frame, fill="both", expand=True)


class GlassmorphicButton(tk.Button):
    """Glassmorphic button with hover effects."""
    
    def __init__(self, parent, text: str = "", command: Optional[Callable] = None,
                 style_theme: str = "dark", **kwargs):
        
        self.style_theme = style_theme
        self.colors = GlassmorphicStyle.GLASS_COLORS[style_theme]
        self.is_hovered = False
        
        # Configure button appearance
        super().__init__(
            parent,
            text=text,
            command=command if command is not None else lambda: None,
            relief="flat",
            borderwidth=0,
            bg=self.colors["glass_bg"],
            fg=self.colors["text_primary"],
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            **kwargs
        )
        
        # Bind hover events
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        self.bind("<Button-1>", self._on_click)
        self.bind("<ButtonRelease-1>", self._on_release)
    
    def _on_enter(self, event):
        """Handle mouse enter."""
        self.is_hovered = True
        self.configure(bg=self._blend_colors(self.colors["glass_bg"], "#ffffff", 0.1))
    
    def _on_leave(self, event):
        """Handle mouse leave."""
        self.is_hovered = False
        self.configure(bg=self.colors["glass_bg"])
    
    def _on_click(self, event):
        """Handle button click."""
        self.configure(bg=self._blend_colors(self.colors["glass_bg"], "#000000", 0.1))
    
    def _on_release(self, event):
        """Handle button release."""
        if self.is_hovered:
            self.configure(bg=self._blend_colors(self.colors["glass_bg"], "#ffffff", 0.1))
        else:
            self.configure(bg=self.colors["glass_bg"])
    
    def _blend_colors(self, color1: str, color2: str, factor: float) -> str:
        """Blend two colors together."""
        # Simple color blending (could be enhanced)
        return color1  # Simplified for now


class GlassmorphicSearchBar(GlassmorphicFrame):
    """Glassmorphic search bar with modern styling."""
    
    def __init__(self, parent, placeholder: str = "Search...", 
                 search_callback: Optional[Callable] = None, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.placeholder = placeholder
        self.search_callback = search_callback
        self.is_placeholder_active = True
        
        # Create content area first
        self._create_content_area()
        
        # Create search entry
        self._create_search_components()
    
    def _create_content_area(self):
        """Create the content area within the glass frame."""
        # Content frame that sits above the glass effect
        self.content_frame = ttk.Frame(self)
        self.content_frame.place(x=15, y=15, relwidth=1, relheight=1, width=-30, height=-30)
    
    def _create_search_components(self):
        """Create search bar components."""
        # Search frame
        search_frame = ttk.Frame(self.content_frame)
        search_frame.pack(fill="x", padx=10, pady=5)
        
        # Search icon (using Unicode)
        search_icon = ttk.Label(
            search_frame,
            text="🔍",
            font=("Segoe UI", 12),
            foreground=self.colors["text_secondary"]
        )
        search_icon.pack(side="left", padx=(5, 10))
        
        # Search entry
        self.search_entry = ttk.Entry(
            search_frame,
            font=("Segoe UI", 11),
            foreground=self.colors["text_secondary"]
        )
        self.search_entry.pack(side="left", fill="x", expand=True)
        
        # Set placeholder
        self.search_entry.insert(0, self.placeholder)
        
        # Bind events
        self.search_entry.bind("<FocusIn>", self._on_focus_in)
        self.search_entry.bind("<FocusOut>", self._on_focus_out)
        self.search_entry.bind("<Return>", self._on_search)
        
        # Search button
        search_btn = GlassmorphicButton(
            search_frame,
            text="Search",
            command=self._on_search,
            style_theme=self.style_theme
        )
        search_btn.pack(side="right", padx=(10, 5))
    
    def _on_focus_in(self, event):
        """Handle entry focus in."""
        if self.is_placeholder_active:
            self.search_entry.delete(0, tk.END)
            self.search_entry.configure(foreground=self.colors["text_primary"])
            self.is_placeholder_active = False
    
    def _on_focus_out(self, event):
        """Handle entry focus out."""
        if not self.search_entry.get():
            self.search_entry.insert(0, self.placeholder)
            self.search_entry.configure(foreground=self.colors["text_secondary"])
            self.is_placeholder_active = True
    
    def _on_search(self, event=None):
        """Handle search action."""
        if not self.is_placeholder_active and self.search_callback:
            query = self.search_entry.get().strip()
            if query:
                self.search_callback(query)
    
    def get_text(self) -> str:
        """Get current search text."""
        return "" if self.is_placeholder_active else self.search_entry.get()
    
    def set_text(self, text: str):
        """Set search text."""
        self.search_entry.delete(0, tk.END)
        if text:
            self.search_entry.insert(0, text)
            self.search_entry.configure(foreground=self.colors["text_primary"])
            self.is_placeholder_active = False
        else:
            self.search_entry.insert(0, self.placeholder)
            self.search_entry.configure(foreground=self.colors["text_secondary"])
            self.is_placeholder_active = True


class GlassmorphicProgressBar(GlassmorphicFrame):
    """Glassmorphic progress bar with smooth animations."""
    def __init__(self, parent, style_theme: str = "dark", **kwargs):
        super().__init__(parent, style_theme=style_theme, **kwargs)
        
        self.progress = 0.0
        self.target_progress = 0.0
        self.animation_speed = 0.05
        
        # Create content area first
        self._create_content_area()
        
        # Create progress components
        self._create_progress_bar()
        
        # Start animation loop
        self._animate_progress()
    
    def _create_content_area(self):
        """Create the content area within the glass frame."""
        # Content frame that sits above the glass effect
        self.content_frame = ttk.Frame(self)
        self.content_frame.place(x=15, y=15, relwidth=1, relheight=1, width=-30, height=-30)
    
    def _create_progress_bar(self):
        """Create progress bar components."""
        self.progress_canvas = Canvas(
            self.content_frame,
            height=20,
            highlightthickness=0,
            bg=self.colors["background"]
        )
        self.progress_canvas.pack(fill="x", padx=5, pady=5)
    
    def _animate_progress(self):
        """Animate progress bar smoothly."""
        if abs(self.progress - self.target_progress) > 0.01:
            diff = self.target_progress - self.progress
            self.progress += diff * self.animation_speed
            self._draw_progress()
        
        self.after(16, self._animate_progress)  # ~60 FPS
    
    def _draw_progress(self):
        """Draw the progress bar."""
        self.progress_canvas.delete("progress")
        
        width = self.progress_canvas.winfo_width()
        height = self.progress_canvas.winfo_height()
        
        if width <= 1:
            return
        
        # Background
        self.progress_canvas.create_rectangle(
            0, 0, width, height,
            fill=self.colors["glass_bg"],
            outline=self.colors["glass_border"],
            tags="progress"
        )
        
        # Progress fill
        fill_width = width * self.progress
        if fill_width > 0:
            # Gradient effect using multiple rectangles
            steps = int(fill_width // 2) + 1
            for i in range(steps):
                x = i * 2
                if x >= fill_width:
                    break
                    
                alpha = 0.3 + 0.4 * (i / max(steps - 1, 1))
                alpha_hex = format(int(255 * alpha), '02x')
                
                self.progress_canvas.create_rectangle(
                    x, 2, min(x + 2, fill_width), height - 2,
                    fill=f"{self.colors['accent'][:-2] if len(self.colors['accent']) > 7 else self.colors['accent']}",
                    outline="",
                    tags="progress"
                )
    
    def set_progress(self, value: float):
        """Set progress value (0.0 to 1.0)."""
        self.target_progress = max(0.0, min(1.0, value))


class GlassmorphicWeatherCard(GlassmorphicCard):
    """Specialized glassmorphic card for weather data display."""
    
    def __init__(self, parent, weather_type: str = "current", **kwargs):
        super().__init__(parent, title=weather_type.title() + " Weather", **kwargs)
        
        self.weather_type = weather_type
        self.weather_data = {}
        
        # Create weather-specific layout
        self._create_weather_layout()
    
    def _create_weather_layout(self):
        """Create weather-specific layout."""
        if self.weather_type == "current":
            self._create_current_weather_layout()
        elif self.weather_type == "forecast":
            self._create_forecast_layout()
        elif self.weather_type == "air_quality":
            self._create_air_quality_layout()
    
    def _create_current_weather_layout(self):
        """Create current weather layout."""
        # Temperature display
        self.temp_frame = ttk.Frame(self.content_frame)
        self.temp_frame.pack(fill="x", pady=(0, 10))
        
        self.temp_label = ttk.Label(
            self.temp_frame,
            text="--°",
            font=("Segoe UI", 36, "bold"),
            foreground=self.colors["text_primary"]
        )
        self.temp_label.pack(side="left")
        
        self.condition_label = ttk.Label(
            self.temp_frame,
            text="--",
            font=("Segoe UI", 12),
            foreground=self.colors["text_secondary"]
        )
        self.condition_label.pack(side="right", anchor="ne")
        
        # Details frame
        self.details_frame = ttk.Frame(self.content_frame)
        self.details_frame.pack(fill="both", expand=True)
    
    def _create_forecast_layout(self):
        """Create forecast layout."""
        # Forecast items will be added dynamically
        pass
    
    def _create_air_quality_layout(self):
        """Create air quality layout."""
        # Air quality components
        pass
    
    def update_weather_data(self, data: Dict[str, Any]):
        """Update weather data display."""
        self.weather_data = data
        
        if self.weather_type == "current" and data:
            self._update_current_weather(data)
    
    def _update_current_weather(self, data: Dict[str, Any]):
        """Update current weather display."""
        try:
            # Update temperature
            temp = data.get("main", {}).get("temp", 0)
            self.temp_label.configure(text=f"{temp:.0f}°")
            
            # Update condition
            weather = data.get("weather", [{}])
            if weather:
                condition = weather[0].get("description", "").title()
                self.condition_label.configure(text=condition)
        except Exception as e:
            print(f"Error updating weather display: {e}")
