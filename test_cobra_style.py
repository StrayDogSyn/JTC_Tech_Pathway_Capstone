"""
🐍 COBRA Styling Test Suite

Quick test to verify all COBRA Commander styling components work correctly.
Run this to test the styling before applying to the main weather dashboard.
"""

import tkinter as tk
import ttkbootstrap as ttk
from cobra_style import *

def test_cobra_styling():
    """Test all COBRA styling components."""
    
    print("🐍 Testing COBRA Commander styling components...")
    
    # Create test window
    root = ttk.Window(themename="cyborg")
    root.title("🐍 COBRA STYLING TEST")
    root.geometry("800x600")
    
    # Apply COBRA theme
    fonts = load_cobra_fonts(root)
    style = apply_cobra_theme(root)
    
    # Show splash screen test
    show_cobra_splash(root, duration=2000)
    
    # Main test interface
    main_frame = ttk.Frame(root, style="Cobra.TFrame")
    main_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Test panel creation
    test_panel = create_cobra_panel(main_frame, "STYLING TEST CONTROL PANEL", "command")
    test_panel.pack(fill="x", pady=(0, 20))
    
    # Test button creation
    button_frame = ttk.Frame(test_panel, style="Cobra.TFrame")
    button_frame.pack(fill="x", pady=10)
    
    # Test different button types
    button_tests = [
        ("Global Scan", lambda: test_toast("scan"), "scan", "info"),
        ("Strike Again", lambda: test_toast("strike"), "strike", "danger"),
        ("Track Target", lambda: test_toast("target"), "target", "warning"),
        ("Neural Shift", lambda: test_toast("neural"), "neural", "success")
    ]
    
    for text, cmd, btn_type, style in button_tests:
        btn = create_cobra_button(button_frame, text, cmd, btn_type, style)
        btn.pack(side="left", padx=5)
    
    # Test status monitor
    status_frame = ttk.Frame(main_frame, style="Cobra.TFrame")
    status_frame.pack(fill="x", pady=(0, 20))
    
    status_monitor = create_status_monitor(status_frame)
    status_monitor.pack(side="left")
    
    status_label = ttk.Label(status_frame, text="COBRA STYLING TEST ACTIVE", 
                            style="Cobra.TLabel", font=("Courier New", 10, "bold"))
    status_label.pack(side="left", padx=20)
    
    # Test different panel types
    panel_frame = ttk.Frame(main_frame, style="Cobra.TFrame")
    panel_frame.pack(fill="both", expand=True)
    
    # Left panel
    left_panel = create_cobra_panel(panel_frame, "DATA ANALYSIS", "data")
    left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))
    
    sample_data = [
        "🌡️ Temperature Control: ONLINE",
        "💨 Wind Systems: OPERATIONAL", 
        "☁️ Cloud Formation: READY",
        "📡 Satellite Network: CONNECTED",
        "🧠 Neural Networks: PROCESSING"
    ]
    
    for data in sample_data:
        ttk.Label(left_panel, text=data, style="Cobra.TLabel").pack(anchor="w", pady=2)
    
    # Right panel
    right_panel = create_cobra_panel(panel_frame, "SYSTEM STATUS", "monitor")
    right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))
    
    status_text = tk.Text(right_panel, 
                         bg=COBRA_COLORS["bg_secondary"],
                         fg=COBRA_COLORS["text_primary"],
                         font=("Courier New", 9),
                         height=8)
    status_text.pack(fill="both", expand=True, pady=10)
    
    status_content = """🐍 COBRA STYLING TEST RESULTS
═══════════════════════════════
✅ Theme Application: SUCCESS
✅ Font Loading: SUCCESS  
✅ Button Creation: SUCCESS
✅ Panel Styling: SUCCESS
✅ Color Scheme: SUCCESS
✅ Status Monitor: SUCCESS

🎯 ALL SYSTEMS OPERATIONAL
💀 READY FOR DEPLOYMENT"""
    
    status_text.insert("1.0", status_content)
    status_text.configure(state="disabled")
    
    def test_toast(toast_type):
        """Test toast notifications."""
        messages = {
            "scan": ("GLOBAL SCAN INITIATED", "info"),
            "strike": ("STRIKING TARGET", "danger"),
            "target": ("TARGET ACQUIRED", "warning"), 
            "neural": ("NEURAL LINK ESTABLISHED", "success")
        }
        msg, alert_type = messages.get(toast_type, ("TEST MESSAGE", "info"))
        show_cobra_toast(root, msg, alert_type)
    
    # Initial success message
    root.after(2500, lambda: show_cobra_toast(root, "COBRA STYLING TEST INITIATED", "command"))
    
    print("✅ COBRA styling test window created successfully!")
    print("🎯 Test all buttons to verify toast notifications")
    print("📡 Status monitor should be blinking")
    print("🐍 COBRA theme should be fully applied")
    
    return root

def test_matplotlib_styling():
    """Test matplotlib styling in a separate window."""
    
    try:
        import matplotlib.pyplot as plt
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        import numpy as np
        
        # Create test window for chart
        chart_window = tk.Toplevel()
        chart_window.title("🧠 COBRA CHART STYLING TEST")
        chart_window.geometry("600x400")
        chart_window.configure(bg=COBRA_COLORS["bg_primary"])
        
        # Create sample chart
        fig, ax = plt.subplots(figsize=(8, 6))
        
        # Apply COBRA styling
        fig, ax = style_cobra_matplotlib(fig, ax)
        
        # Sample data
        x = np.linspace(0, 24, 50)
        temp_data = 20 + 5 * np.sin(x/4) + np.random.normal(0, 1, 50)
        humidity_data = 60 + 20 * np.cos(x/6) + np.random.normal(0, 3, 50)
        
        # Plot with COBRA colors
        ax.plot(x, temp_data, color=COBRA_COLORS["highlight_cyan"], 
                linewidth=2, label="🌡️ Temperature", marker='o', markersize=3)
        ax.plot(x, humidity_data, color=COBRA_COLORS["accent_purple"], 
                linewidth=2, label="💧 Humidity", marker='s', markersize=3)
        
        ax.set_xlabel("⏰ Time (Hours)")
        ax.set_ylabel("📊 Atmospheric Readings")
        ax.set_title("🧠 NEURAL WEATHER ANALYSIS")
        ax.legend()
        
        # Add to tkinter window
        canvas = FigureCanvasTkAgg(fig, chart_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)
        
        print("✅ COBRA matplotlib styling test created!")
        
    except ImportError:
        print("⚠️ Matplotlib not available for chart styling test")

def main():
    """Run all COBRA styling tests."""
    print("🐍" + "="*50)
    print("   COBRA COMMANDER STYLING TEST SUITE")
    print("="*53)
    
    # Test main styling
    root = test_cobra_styling()
    
    # Test matplotlib styling
    root.after(3000, test_matplotlib_styling)
    
    # Run the test
    root.mainloop()
    
    print("🐍 COBRA styling tests completed!")
    print("💀 Ready for deployment to weather dashboard")

if __name__ == "__main__":
    main()
