# cobra_style.py
"""
🐍 COBRA COMMANDER WEATHER DOMINATOR - Complete Styling Arsenal

Provides the ultimate styling utilities for the Cobra Commander Weather Dominator GUI.
Transform any mundane weather app into a weapon of meteorological mass destruction!

Features:
- COBRA-themed color schemes with sci-fi villain aesthetics  
- Neon button arsenal with military-style icons
- Atmospheric control panels with glowing effects
- Neural network chart styling for global domination
- Animated status indicators and toast notifications
- Complete UI transformation framework

Author: COBRA Engineering Division
Date: 2025-06-17  
Classification: TOP SECRET - Global Weather Domination
License: For Educational Use & World Conquest Only
"""

import tkinter as tk
from tkinter import font, Canvas
import ttkbootstrap as ttk
from ttkbootstrap.constants import INFO, DANGER, WARNING, SUCCESS, PRIMARY
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import time
import os
from datetime import datetime

# === [ COBRA COLOR COMMAND PROTOCOL ] ===
COBRA_COLORS = {
    "bg_primary": "#0d1b2a",      # Deep Navy Command Center
    "bg_secondary": "#1e2a3a",    # Panel Background  
    "bg_tertiary": "#000000",     # Pure Black Void
    "highlight_cyan": "#00ffff",  # Neon Cyber Blue
    "highlight_red": "#ff0033",   # Blood Red Alert
    "accent_purple": "#8e44ad",   # Electric Purple
    "accent_green": "#00ff41",    # Matrix Green
    "text_primary": "#ffffff",    # Pure White Commands
    "text_secondary": "#cccccc",  # Muted Silver
    "warning_amber": "#ffa500",   # Amber Warning
    "success_lime": "#32cd32",    # Success Lime
}

# === [ COBRA COMMAND THEME CONFIGURATION ] ===
COBRA_THEME_CONFIG = {
    "cyborg": {
        "primary": COBRA_COLORS["highlight_cyan"],
        "secondary": COBRA_COLORS["accent_purple"], 
        "success": COBRA_COLORS["success_lime"],
        "info": COBRA_COLORS["highlight_cyan"],
        "warning": COBRA_COLORS["warning_amber"],
        "danger": COBRA_COLORS["highlight_red"],
        "light": COBRA_COLORS["text_secondary"],
        "dark": COBRA_COLORS["bg_primary"]
    }
}

# === [ ADVANCED FONT ARSENAL ] ===
def load_cobra_fonts(root: tk.Tk):
    """Load and configure COBRA command fonts for maximum intimidation."""
    try:
        # Configure default fonts with sci-fi styling
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Segoe UI", size=11, weight="normal")
        
        # Create custom font families for different UI elements
        cobra_fonts = {
            "command": font.Font(family="Consolas", size=12, weight="bold"),
            "panel": font.Font(family="Segoe UI", size=10, weight="normal"), 
            "title": font.Font(family="Segoe UI", size=14, weight="bold"),
            "status": font.Font(family="Courier New", size=9, weight="normal"),
            "alert": font.Font(family="Arial Black", size=11, weight="bold")
        }
        return cobra_fonts
    except Exception as e:
        print(f"⚠️ COBRA Font loading error: {e}")
        return None

# === [ NEON WEAPON BUTTON FACTORY ] ===
def create_cobra_button(parent, text: str, command=None, button_type: str = "scan", style: str = "info"):
    """Create themed COBRA command buttons with military iconography."""
    
    # Button icon mapping for different functions
    button_icons = {
        "scan": "🛰️",       # Global Weather Scan
        "strike": "⚔️",     # Refresh/Strike Again  
        "neural": "🧠",     # Neural Shift (Theme Toggle)
        "target": "💀",     # Track Target (Search)
        "dominate": "🌪️",  # Weather Domination
        "control": "🎛️",   # Atmospheric Control
        "monitor": "📡",    # Live Monitoring
        "engage": "⚡",     # Engage Systems
    }
    
    icon = button_icons.get(button_type, "🔧")
    button_text = f"{icon} {text}"
    
    btn = ttk.Button(
        parent,
        text=button_text,
        style=f"{style}.TButton"  # Use style instead of bootstyle
    )
    
    # Only set command if it's provided
    if command is not None:
        btn.configure(command=command)
    
    # Add hover effects for intimidation factor
    def on_enter(e):
        btn.configure(cursor="target")
        
    def on_leave(e):
        btn.configure(cursor="")
        
    btn.bind("<Enter>", on_enter)
    btn.bind("<Leave>", on_leave)
    
    return btn

# === [ ATMOSPHERIC CONTROL PANELS ] ===
def create_cobra_panel(parent, title: str = "", panel_type: str = "control"):
    """Create themed control panels suitable for global weather domination."""
    
    # Panel icon mapping
    panel_icons = {
        "control": "🎛️",
        "data": "📊", 
        "forecast": "🔮",
        "monitor": "📡",
        "alert": "⚠️",
        "command": "💀"
    }
    
    icon = panel_icons.get(panel_type, "🔧")
    panel_title = f"{icon} {title}" if title else ""
    
    panel = ttk.LabelFrame(
        parent,
        text=panel_title,
        style="danger.TLabelframe",  # Use style instead of bootstyle
        padding=15
    )
    
    return panel

# === [ WEATHER DOMINATOR BACKGROUND SYSTEM ] ===
def create_cobra_background(canvas: tk.Canvas, width: int = 800, height: int = 600):
    """Generate a dynamic COBRA-themed background for the weather dominator interface."""
    try:
        # Create a gradient background using PIL
        img = Image.new('RGB', (width, height), COBRA_COLORS["bg_primary"])
        draw = ImageDraw.Draw(img)
        
        # Add subtle grid pattern for sci-fi effect
        grid_spacing = 50
        grid_color = COBRA_COLORS["accent_purple"]
        
        # Draw vertical grid lines
        for x in range(0, width, grid_spacing):
            draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
            
        # Draw horizontal grid lines  
        for y in range(0, height, grid_spacing):
            draw.line([(0, y), (width, y)], fill=grid_color, width=1)
            
        # Add some opacity for subtle effect
        img = img.filter(ImageFilter.GaussianBlur(radius=0.5))
          # Convert to PhotoImage for tkinter
        photo = ImageTk.PhotoImage(img)
        
        # Store reference to prevent garbage collection using the utility function
        photo = fix_canvas_image_reference(canvas, photo)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        
        return photo
    except Exception as e:
        print(f"⚠️ COBRA Background generation error: {e}")
        return None

# === [ NEURAL NETWORK CHART DOMINATION ] ===
def style_cobra_matplotlib(fig, ax):
    """Apply COBRA neural network styling to matplotlib charts for global domination."""
    try:
        # Set the sci-fi dark theme
        fig.patch.set_facecolor(COBRA_COLORS["bg_primary"])
        ax.set_facecolor(COBRA_COLORS["bg_secondary"])
        
        # Style the axes and labels
        ax.tick_params(colors=COBRA_COLORS["highlight_cyan"], labelsize=9)
        ax.xaxis.label.set_color(COBRA_COLORS["highlight_cyan"])
        ax.yaxis.label.set_color(COBRA_COLORS["highlight_cyan"])
        ax.title.set_color(COBRA_COLORS["highlight_red"])
        ax.title.set_fontsize(12)
        ax.title.set_fontweight('bold')
        
        # Add COBRA-style grid
        ax.grid(True, color=COBRA_COLORS["accent_purple"], linestyle='--', linewidth=0.5, alpha=0.7)
        
        # Style spines (borders)
        for spine in ax.spines.values():
            spine.set_color(COBRA_COLORS["highlight_cyan"])
            spine.set_linewidth(1.5)
            
        return fig, ax
    except Exception as e:
        print(f"⚠️ COBRA Chart styling error: {e}")
        return fig, ax

# === [ ATMOSPHERIC ALERT SYSTEM ] ===
def show_cobra_toast(root, message: str, alert_type: str = "info", duration: int = 3000):
    """Display COBRA-themed toast notifications for operational updates."""
    
    # Alert type configurations
    alert_configs = {
        "info": {"icon": "📡", "bg": COBRA_COLORS["highlight_cyan"], "fg": COBRA_COLORS["bg_primary"]},
        "success": {"icon": "✅", "bg": COBRA_COLORS["success_lime"], "fg": COBRA_COLORS["bg_primary"]},
        "warning": {"icon": "⚠️", "bg": COBRA_COLORS["warning_amber"], "fg": COBRA_COLORS["bg_primary"]},
        "danger": {"icon": "🚨", "bg": COBRA_COLORS["highlight_red"], "fg": COBRA_COLORS["text_primary"]},
        "command": {"icon": "💀", "bg": COBRA_COLORS["accent_purple"], "fg": COBRA_COLORS["text_primary"]}
    }
    
    config = alert_configs.get(alert_type, alert_configs["info"])
    toast_text = f"{config['icon']} {message}"
    
    # Create toast notification
    toast = tk.Label(
        root, 
        text=toast_text,
        font=("Segoe UI", 10, "bold"),
        background=config["bg"],
        foreground=config["fg"],
        padx=20,
        pady=10,
        relief="raised",
        borderwidth=2
    )
    
    # Position at bottom center
    toast.place(relx=0.5, rely=0.9, anchor="center")
    
    # Auto-remove after duration
    root.after(duration, lambda: toast.destroy())
    
    return toast

# === [ LIVE MONITORING STATUS SYSTEM ] ===
def create_status_monitor(parent):
    """Create an animated status monitor with blinking red indicator."""
    
    monitor_frame = ttk.Frame(parent)
    
    # Status indicator canvas
    status_canvas = tk.Canvas(monitor_frame, width=15, height=15, bg=COBRA_COLORS["bg_primary"], highlightthickness=0)
    status_canvas.pack(side="left", padx=(0, 5))
    
    # Status label
    status_label = ttk.Label(monitor_frame, text="LIVE MONITORING", font=("Courier New", 9, "bold"))
    status_label.pack(side="left")
    
    # Blinking red dot animation
    def blink_status():
        current_color = status_canvas.itemcget("status_dot", "fill") if status_canvas.find_all() else "red"
        new_color = COBRA_COLORS["highlight_red"] if current_color != COBRA_COLORS["highlight_red"] else "#660000"
        
        status_canvas.delete("status_dot")
        status_canvas.create_oval(2, 2, 13, 13, fill=new_color, outline=new_color, tags="status_dot")
        
        # Schedule next blink
        parent.after(800, blink_status)
    
    # Start blinking animation
    blink_status()
    
    return monitor_frame

# === [ COBRA COMMAND SPLASH SCREEN ] ===
def show_cobra_splash(root, duration: int = 3000):
    """Display the COBRA Weather Dominator system initialization splash screen."""
    
    # Create splash window
    splash = tk.Toplevel(root)
    splash.title("COBRA WEATHER DOMINATOR")
    splash.geometry("500x300")
    splash.configure(bg=COBRA_COLORS["bg_primary"])
    splash.resizable(False, False)
    
    # Center on screen
    splash.geometry("+{}+{}".format(
        (splash.winfo_screenwidth() // 2) - 250,
        (splash.winfo_screenheight() // 2) - 150
    ))
    
    # Remove window decorations for full effect
    splash.overrideredirect(True)
    
    # COBRA logo and text
    logo_frame = tk.Frame(splash, bg=COBRA_COLORS["bg_primary"])
    logo_frame.pack(expand=True, fill="both", padx=20, pady=20)
    
    # Main title
    title_label = tk.Label(
        logo_frame,
        text="🐍 COBRA WEATHER DOMINATOR",
        font=("Arial Black", 18, "bold"),
        fg=COBRA_COLORS["highlight_red"],
        bg=COBRA_COLORS["bg_primary"]
    )
    title_label.pack(pady=(40, 10))
    
    # Version info
    version_label = tk.Label(
        logo_frame,
        text="Version 1.0 — GLOBAL ATMOSPHERIC CONTROL SYSTEM",
        font=("Courier New", 10),
        fg=COBRA_COLORS["highlight_cyan"],
        bg=COBRA_COLORS["bg_primary"]
    )
    version_label.pack(pady=10)
    
    # Status message
    status_label = tk.Label(
        logo_frame,
        text="⚠️ SYSTEM OVERRIDE INITIATED ⚠️",
        font=("Arial", 12, "bold"),
        fg=COBRA_COLORS["warning_amber"],
        bg=COBRA_COLORS["bg_primary"]
    )
    status_label.pack(pady=20)
    
    # Loading animation
    loading_label = tk.Label(
        logo_frame,
        text="🔄 Initializing Weather Domination Protocols...",
        font=("Segoe UI", 10),
        fg=COBRA_COLORS["text_secondary"],
        bg=COBRA_COLORS["bg_primary"]
    )
    loading_label.pack(pady=(20, 40))
    
    # Auto-close after duration
    root.after(duration, splash.destroy)
    
    return splash

# === [ COBRA THEME CONFIGURATOR ] ===
def apply_cobra_theme(root):
    """Apply the complete COBRA Commander theme to ttkbootstrap."""
    
    # Configure ttkbootstrap with cyborg theme as base
    style = ttk.Style("cyborg")
    
    # Custom COBRA style configurations
    cobra_styles = {
        # Button styles
        "Cobra.TButton": {
            "configure": {
                "foreground": COBRA_COLORS["text_primary"],
                "background": COBRA_COLORS["bg_secondary"],
                "bordercolor": COBRA_COLORS["highlight_cyan"],
                "focuscolor": COBRA_COLORS["highlight_red"],
                "font": ("Segoe UI", 10, "bold")
            },
            "map": {
                "background": [("active", COBRA_COLORS["highlight_cyan"])],
                "foreground": [("active", COBRA_COLORS["bg_primary"])]
            }
        },
        
        # Frame styles
        "Cobra.TFrame": {
            "configure": {
                "background": COBRA_COLORS["bg_primary"],
                "relief": "flat"
            }
        },
        
        # Label styles
        "Cobra.TLabel": {
            "configure": {
                "foreground": COBRA_COLORS["text_primary"],
                "background": COBRA_COLORS["bg_primary"],
                "font": ("Segoe UI", 10)
            }
        },
        
        # LabelFrame styles
        "Cobra.TLabelframe": {
            "configure": {
                "foreground": COBRA_COLORS["highlight_cyan"],
                "background": COBRA_COLORS["bg_primary"],
                "bordercolor": COBRA_COLORS["highlight_red"],
                "relief": "ridge",
                "borderwidth": 2
            }
        }
    }
    
    # Apply custom styles
    for style_name, style_config in cobra_styles.items():
        if "configure" in style_config:
            style.configure(style_name, **style_config["configure"])
        if "map" in style_config:
            style.map(style_name, **style_config["map"])
    
    # Configure root window
    root.configure(bg=COBRA_COLORS["bg_primary"])
    
    return style

# === [ WEATHER CHART ANIMATION SYSTEM ] ===
class CobraChartAnimator:
    """Animate weather charts with COBRA-style effects."""
    
    def __init__(self, canvas_widget):
        self.canvas_widget = canvas_widget
        self.animation_active = False
    
    def pulse_chart_borders(self, color=None, duration=2000):
        """Create a pulsing border effect around weather charts."""
        if not color:
            color = COBRA_COLORS["highlight_cyan"]
            
        def pulse_cycle():
            if not self.animation_active:
                return
                
            # This would be implemented to pulse chart borders
            # Implementation depends on the specific chart widget
            self.canvas_widget.after(100, pulse_cycle)
        
        self.animation_active = True
        pulse_cycle()
    
    def stop_animations(self):
        """Stop all chart animations."""
        self.animation_active = False

# === [ UTILITY FUNCTIONS ] ===
def fix_canvas_image_reference(canvas, photo):
    """Fix the image reference issue by storing it in a way tkinter can access."""
    # Store the image reference in the canvas's widget info
    if not hasattr(canvas, '_cobra_images'):
        canvas._cobra_images = []
    canvas._cobra_images.append(photo)
    return photo

def create_cobra_menu_options():
    """Create COBRA-themed menu options for world control protocol."""
    return {
        "World Control Protocol": [
            ("🛰️ Global Weather Scan", "scan_weather"),
            ("📡 Satellite Network", "satellite_view"),
            ("⚡ Atmospheric Control", "atmosphere_control"),
            ("🌪️ Storm Generator", "storm_mode"),
            ("🧠 Neural Interface", "neural_mode"),
            ("separator", None),
            ("💀 System Override", "system_override"),
            ("🔒 Security Protocols", "security_mode")
        ],
        "Domination Protocols": [
            ("🌡️ Temperature Control", "temp_control"),
            ("💨 Wind Manipulation", "wind_control"), 
            ("☁️ Cloud Formation", "cloud_control"),
            ("🌧️ Precipitation Control", "rain_control"),
            ("separator", None),
            ("🚨 Alert Systems", "alert_mode"),
            ("📊 Data Analysis", "analysis_mode")
        ]
    }

# === [ EXPORT CONFIGURATION ] ===
__all__ = [
    'COBRA_COLORS',
    'COBRA_THEME_CONFIG', 
    'load_cobra_fonts',
    'create_cobra_button',
    'create_cobra_panel',
    'create_cobra_background',
    'style_cobra_matplotlib',
    'show_cobra_toast',
    'create_status_monitor',
    'show_cobra_splash',
    'apply_cobra_theme',
    'CobraChartAnimator',
    'fix_canvas_image_reference',
    'create_cobra_menu_options'
]
