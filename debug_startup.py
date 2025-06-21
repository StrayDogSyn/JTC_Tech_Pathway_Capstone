"""
Test the weather dashboard startup to identify the exact error.
"""
print("Starting test...")

try:
    print("Step 1: Importing modules...")
    import sys
    import os
    sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))
    
    print("Step 2: Testing ttkbootstrap...")
    import ttkbootstrap as ttk
    
    print("Step 3: Testing window creation...")
    root = ttk.Window(title="Weather Dashboard", themename="darkly", size=(1400, 900))
    
    print("Step 4: Testing ModernCard import...")
    from ui.modern_components import ModernCard
    
    print("Step 5: Testing ModernCard creation...")
    test_card = ModernCard(root, title="Test Card")
    
    print("Step 6: Testing dashboard UI import...")
    from ui.dashboard_ui import WeatherDashboardUI
    
    print("✅ All imports successful!")
    
    print("Step 7: Testing dashboard creation...")
    # Destroy the test window first
    root.destroy()
    
    # Create the actual dashboard
    dashboard = WeatherDashboardUI()
    
    print("✅ Dashboard created successfully!")
    print("Step 8: Destroying dashboard...")
    dashboard.destroy()
    
    print("✅ Test completed successfully!")

except Exception as e:
    print(f"❌ Error at step: {e}")
    import traceback
    traceback.print_exc()
