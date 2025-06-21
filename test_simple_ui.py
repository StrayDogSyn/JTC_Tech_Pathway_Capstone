#!/usr/bin/env python3
"""
Simple test to isolate the UI error.
"""

import sys
import os

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_basic_imports():
    """Test basic imports."""
    print("Testing basic imports...")
    try:
        import ttkbootstrap as ttk
        print("✅ ttkbootstrap imported successfully")
    except ImportError as e:
        print(f"❌ ttkbootstrap import failed: {e}")
        return False
    
    try:
        from ui.modern_components import ModernCard
        print("✅ ModernCard imported successfully")
    except ImportError as e:
        print(f"❌ ModernCard import failed: {e}")
        return False
    
    return True

def test_moderncard_creation():
    """Test ModernCard creation."""
    print("\nTesting ModernCard creation...")
    try:
        import ttkbootstrap as ttk
        from ui.modern_components import ModernCard
        
        # Create a test window
        root = ttk.Window("Test", "darkly", (400, 300))
        root.withdraw()  # Hide the window
        
        # Test ModernCard with only title parameter
        card = ModernCard(root, title="Test Card")
        print("✅ ModernCard created successfully with title only")
        
        # Try with additional kwargs
        card2 = ModernCard(root, title="Test Card", padding=10)
        print("✅ ModernCard created successfully with kwargs")
        
        root.destroy()
        return True
        
    except Exception as e:
        print(f"❌ ModernCard creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_ui_import():
    """Test dashboard UI import."""
    print("\nTesting dashboard UI import...")
    try:
        from ui.dashboard_ui import WeatherDashboardUI
        print("✅ WeatherDashboardUI imported successfully")
        return True
    except Exception as e:
        print(f"❌ WeatherDashboardUI import failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_dashboard_ui_creation():
    """Test dashboard UI creation."""
    print("\nTesting dashboard UI creation...")
    try:
        from ui.dashboard_ui import WeatherDashboardUI
        
        # Create with minimal parameters
        ui = WeatherDashboardUI()
        print("✅ WeatherDashboardUI created successfully")
        
        ui.destroy()
        return True
        
    except Exception as e:
        print(f"❌ WeatherDashboardUI creation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests."""
    print("🧪 Running UI Component Tests")
    print("=" * 40)
    
    tests = [
        test_basic_imports,
        test_moderncard_creation,
        test_dashboard_ui_import,
        test_dashboard_ui_creation
    ]
    
    for test in tests:
        try:
            if not test():
                print(f"\n❌ Test failed: {test.__name__}")
                return
        except Exception as e:
            print(f"\n❌ Test error in {test.__name__}: {e}")
            import traceback
            traceback.print_exc()
            return
    
    print("\n✅ All tests passed!")

if __name__ == "__main__":
    main()
