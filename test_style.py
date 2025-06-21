"""
Simple test to check ttkbootstrap styling issues
"""

import tkinter as tk
import ttkbootstrap as ttk

try:
    print("Testing ttkbootstrap styling...")
    
    root = ttk.Window(
        title="Style Test",
        themename="darkly",
        size=(400, 300)
    )
    
    style = ttk.Style()
    print("Style object created successfully")
    
    # Test basic configurations
    try:
        style.configure("Temperature.TLabel", font=('Segoe UI', 48, 'bold'), foreground="#FF6B35")
        print("Temperature style configured successfully")
    except Exception as e:
        print(f"Temperature style error: {e}")
    
    try:
        style.configure("UpdateTime.TLabel", font=('Segoe UI', 9), foreground="gray")
        print("UpdateTime style configured successfully")
    except Exception as e:
        print(f"UpdateTime style error: {e}")
    
    # Create test labels
    temp_label = ttk.Label(root, text="25.5°C", style="Temperature.TLabel")
    temp_label.pack(pady=20)
    
    update_label = ttk.Label(root, text="Last update: 22:45", style="UpdateTime.TLabel")
    update_label.pack(pady=10)
    
    print("Labels created successfully")
    
    # Don't actually run the GUI, just test creation
    root.destroy()
    print("Test completed successfully!")
    
except Exception as e:
    print(f"Test failed: {e}")
    import traceback
    print(f"Traceback: {traceback.format_exc()}")
