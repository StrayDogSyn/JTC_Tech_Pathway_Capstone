#!/usr/bin/env python3
"""
Minimal test to capture the exact error.
"""

import sys
import os
import traceback

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Importing ttkbootstrap...")
    import ttkbootstrap as ttk
    print("✅ ttkbootstrap imported")
    
    print("Creating test window...")
    root = ttk.Window(title="Test", themename="darkly", size=(400, 300))
    root.withdraw()  # Hide the window
    print("✅ Test window created")
    
    print("Importing ModernCard...")
    from ui.modern_components import ModernCard
    print("✅ ModernCard imported")
    
    print("Creating ModernCard...")
    card = ModernCard(root, title="Test Card")
    print("✅ ModernCard created")
    
    print("Destroying window...")
    root.destroy()
    print("✅ Test completed successfully")
    
except Exception as e:
    print(f"❌ Error occurred: {e}")
    print("\nFull traceback:")
    traceback.print_exc()
