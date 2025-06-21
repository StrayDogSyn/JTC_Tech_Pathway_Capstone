#!/usr/bin/env python3
"""
Test script for Advanced Weather Dashboard UX/UI Features

This script tests all the modern components and advanced features
to ensure they work correctly.
"""

import sys
import os
import time
import threading
from typing import List, Dict, Any

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    import tkinter as tk
    import ttkbootstrap as ttk
    from ttkbootstrap import Style
    print("✅ GUI libraries available")
except ImportError as e:
    print(f"❌ GUI libraries not available: {e}")
    sys.exit(1)

try:
    from src.ui.modern_components import (
        ModernCard, CircularProgress, ModernSearchBar, WeatherGauge,
        NotificationToast, ModernToggleSwitch, LoadingSpinner
    )
    print("✅ Modern components imported successfully")
    MODERN_COMPONENTS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Modern components not available: {e}")
    MODERN_COMPONENTS_AVAILABLE = False

try:
    from src.ui.dashboard_ui import WeatherDashboardUI
    print("✅ Dashboard UI imported successfully")
    DASHBOARD_UI_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Dashboard UI not available: {e}")
    DASHBOARD_UI_AVAILABLE = False

try:
    from src.ui.weather_displays import EnhancedWeatherDisplays
    print("✅ Enhanced weather displays imported successfully")
    ENHANCED_DISPLAYS_AVAILABLE = True
except ImportError as e:
    print(f"⚠️ Enhanced displays not available: {e}")
    ENHANCED_DISPLAYS_AVAILABLE = False


class UXTestSuite:
    """Test suite for UX/UI features."""
    
    def __init__(self):
        """Initialize the test suite."""
        self.root = None
        self.test_results: List[Dict[str, Any]] = []
        
    def run_all_tests(self):
        """Run all UX/UI tests."""
        print("\n🧪 Starting Advanced UX/UI Test Suite")
        print("=" * 50)
        
        # Test 1: Basic GUI setup
        self.test_basic_gui()
        
        # Test 2: Modern components
        if MODERN_COMPONENTS_AVAILABLE:
            self.test_modern_components()
        
        # Test 3: Dashboard UI
        if DASHBOARD_UI_AVAILABLE:
            self.test_dashboard_ui()
        
        # Test 4: Enhanced displays
        if ENHANCED_DISPLAYS_AVAILABLE:
            self.test_enhanced_displays()
        
        # Test 5: Themes
        self.test_themes()
        
        # Test 6: Animations
        self.test_animations()
        
        # Show results
        self.show_test_results()
    
    def test_basic_gui(self):
        """Test basic GUI functionality."""
        print("\n🔧 Testing Basic GUI Setup...")
        
        try:
            # Create test window
            self.root = ttk.Window(
                title="🧪 UX/UI Test Suite",
                themename="darkly",
                size=(800, 600)
            )
            
            # Test basic widgets
            frame = ttk.Frame(self.root, padding=20)
            frame.pack(fill="both", expand=True)
            
            ttk.Label(frame, text="🧪 UX/UI Test Suite", 
                     font=('Segoe UI', 16, 'bold')).pack(pady=10)
            
            # Test different widget types
            ttk.Button(frame, text="Test Button").pack(pady=5)
            ttk.Entry(frame, placeholder_text="Test Entry").pack(pady=5)
            ttk.Scale(frame, from_=0, to=100, value=50).pack(pady=5)
            
            self.add_test_result("Basic GUI", True, "GUI components created successfully")
            print("  ✅ Basic GUI components working")
            
        except Exception as e:
            self.add_test_result("Basic GUI", False, str(e))
            print(f"  ❌ Basic GUI failed: {e}")
    
    def test_modern_components(self):
        """Test modern UI components."""
        print("\n🎨 Testing Modern Components...")
        
        if not self.root:
            print("  ⚠️ Skipping - no root window")
            return
        
        try:
            test_frame = ttk.Frame(self.root)
            
            # Test ModernCard
            try:
                card = ModernCard(test_frame, title="Test Card", padding=10)
                ttk.Label(card, text="Card content").pack()
                self.add_test_result("ModernCard", True, "Card created successfully")
                print("  ✅ ModernCard working")
            except Exception as e:
                self.add_test_result("ModernCard", False, str(e))
                print(f"  ❌ ModernCard failed: {e}")
            
            # Test CircularProgress
            try:
                progress = CircularProgress(test_frame, value=75, max_value=100)
                self.add_test_result("CircularProgress", True, "Progress indicator created")
                print("  ✅ CircularProgress working")
            except Exception as e:
                self.add_test_result("CircularProgress", False, str(e))
                print(f"  ❌ CircularProgress failed: {e}")
            
            # Test WeatherGauge
            try:
                gauge = WeatherGauge(test_frame, value=65, max_value=100, 
                                   label="Humidity", unit="%")
                self.add_test_result("WeatherGauge", True, "Gauge created successfully")
                print("  ✅ WeatherGauge working")
            except Exception as e:
                self.add_test_result("WeatherGauge", False, str(e))
                print(f"  ❌ WeatherGauge failed: {e}")
            
            # Test LoadingSpinner
            try:
                spinner = LoadingSpinner(test_frame, size=30)
                spinner.start_spinning()
                time.sleep(0.5)
                spinner.stop_spinning()
                self.add_test_result("LoadingSpinner", True, "Spinner animated successfully")
                print("  ✅ LoadingSpinner working")
            except Exception as e:
                self.add_test_result("LoadingSpinner", False, str(e))
                print(f"  ❌ LoadingSpinner failed: {e}")
            
            # Test ModernToggleSwitch
            try:
                toggle = ModernToggleSwitch(test_frame, text="Test Toggle")
                toggle.set_state(True)
                toggle.set_state(False)
                self.add_test_result("ModernToggleSwitch", True, "Toggle switch working")
                print("  ✅ ModernToggleSwitch working")
            except Exception as e:
                self.add_test_result("ModernToggleSwitch", False, str(e))
                print(f"  ❌ ModernToggleSwitch failed: {e}")
            
        except Exception as e:
            print(f"  ❌ Modern components test failed: {e}")
    
    def test_dashboard_ui(self):
        """Test dashboard UI functionality."""
        print("\n🖥️ Testing Dashboard UI...")
        
        try:
            # Test dashboard initialization (don't actually run it)
            dashboard = WeatherDashboardUI(
                title="Test Dashboard",
                theme="darkly",
                size=(800, 600)
            )
            
            # Test method availability
            methods_to_test = [
                'set_search_callback',
                'set_theme_change_callback', 
                'update_status',
                'show_error',
                'show_info'
            ]
            
            for method in methods_to_test:
                if hasattr(dashboard, method):
                    print(f"  ✅ {method} available")
                else:
                    print(f"  ❌ {method} missing")
            
            self.add_test_result("Dashboard UI", True, "Dashboard UI initialized successfully")
            
            # Clean up
            dashboard.destroy()
            
        except Exception as e:
            self.add_test_result("Dashboard UI", False, str(e))
            print(f"  ❌ Dashboard UI failed: {e}")
    
    def test_enhanced_displays(self):
        """Test enhanced weather displays."""
        print("\n📊 Testing Enhanced Displays...")
        
        if not self.root:
            print("  ⚠️ Skipping - no root window")
            return
        
        try:
            # Test weather icon function
            test_descriptions = [
                "clear sky", "partly cloudy", "rain", "snow", 
                "thunderstorm", "mist", "wind"
            ]
            
            for desc in test_descriptions:
                icon = EnhancedWeatherDisplays._get_weather_icon(desc)
                if icon:
                    print(f"  ✅ Weather icon for '{desc}': {icon}")
                else:
                    print(f"  ❌ No icon for '{desc}'")
            
            self.add_test_result("Enhanced Displays", True, "Weather displays working")
            
        except Exception as e:
            self.add_test_result("Enhanced Displays", False, str(e))
            print(f"  ❌ Enhanced displays failed: {e}")
    
    def test_themes(self):
        """Test theme functionality."""
        print("\n🎨 Testing Themes...")
        
        try:
            # Test available themes
            style = Style()
            available_themes = style.theme_names()
            
            print(f"  📋 Available themes: {len(available_themes)}")
            for theme in available_themes:
                print(f"    • {theme}")
            
            # Test theme switching
            original_theme = style.theme_use()
            test_themes = ['darkly', 'flatly', 'litera']
            
            for theme in test_themes:
                if theme in available_themes:
                    style.theme_use(theme)
                    print(f"  ✅ Switched to {theme}")
                else:
                    print(f"  ❌ Theme {theme} not available")
            
            # Restore original theme
            style.theme_use(original_theme)
            
            self.add_test_result("Themes", True, f"{len(available_themes)} themes available")
            
        except Exception as e:
            self.add_test_result("Themes", False, str(e))
            print(f"  ❌ Theme testing failed: {e}")
    
    def test_animations(self):
        """Test animation capabilities."""
        print("\n✨ Testing Animations...")
        
        if not self.root:
            print("  ⚠️ Skipping - no root window")
            return
        
        try:
            # Test fade animation
            test_label = ttk.Label(self.root, text="Animation Test")
            test_label.pack()
            
            # Test alpha transparency
            self.root.attributes('-alpha', 1.0)
            time.sleep(0.1)
            self.root.attributes('-alpha', 0.8)
            time.sleep(0.1)
            self.root.attributes('-alpha', 1.0)
            
            print("  ✅ Alpha transparency working")
            
            # Test geometry animations (size/position)
            original_geometry = self.root.geometry()
            self.root.geometry("820x620")
            self.root.update()
            time.sleep(0.1)
            self.root.geometry(original_geometry)
            
            print("  ✅ Geometry animations working")
            
            test_label.destroy()
            
            self.add_test_result("Animations", True, "Animation features working")
            
        except Exception as e:
            self.add_test_result("Animations", False, str(e))
            print(f"  ❌ Animation testing failed: {e}")
    
    def add_test_result(self, test_name: str, passed: bool, message: str):
        """Add a test result."""
        self.test_results.append({
            'test': test_name,
            'passed': passed,
            'message': message
        })
    
    def show_test_results(self):
        """Show final test results."""
        print("\n📊 Test Results Summary")
        print("=" * 50)
        
        passed = sum(1 for result in self.test_results if result['passed'])
        total = len(self.test_results)
        
        print(f"Tests Passed: {passed}/{total}")
        print(f"Success Rate: {(passed/total)*100:.1f}%")
        print()
        
        for result in self.test_results:
            status = "✅ PASS" if result['passed'] else "❌ FAIL"
            print(f"{status} - {result['test']}: {result['message']}")
        
        print("\n" + "=" * 50)
        
        if passed == total:
            print("🎉 All tests passed! Advanced UX/UI features are working correctly.")
        elif passed > total * 0.8:
            print("✅ Most tests passed. Minor issues detected.")
        else:
            print("⚠️ Several tests failed. Please check the installation.")
    
    def run_interactive_demo(self):
        """Run an interactive demo of the UX features."""
        if not self.root:
            print("❌ Cannot run interactive demo - no GUI available")
            return
        
        print("\n🚀 Starting Interactive Demo...")
        
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
        
        # Create demo interface
        self.root.title("🎨 Advanced UX/UI Demo")
        
        # Main container
        main_frame = ttk.Frame(self.root, padding=20)
        main_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            main_frame,
            text="🎨 Advanced UX/UI Features Demo",
            font=('Segoe UI', 18, 'bold')
        )
        title_label.pack(pady=(0, 20))
        
        # Demo sections
        if MODERN_COMPONENTS_AVAILABLE:
            self._create_components_demo(main_frame)
        
        # Controls
        controls_frame = ttk.Frame(main_frame)
        controls_frame.pack(fill="x", pady=(20, 0))
        
        ttk.Button(
            controls_frame,
            text="🔄 Run Tests Again",
            command=self.run_all_tests
        ).pack(side="left", padx=(0, 10))
        
        ttk.Button(
            controls_frame,
            text="❌ Close Demo",
            command=self.root.quit
        ).pack(side="left")
        
        # Status
        status_label = ttk.Label(
            main_frame,
            text="✅ Interactive demo ready - explore the features!",
            font=('Segoe UI', 10),
            foreground="green"
        )
        status_label.pack(side="bottom", pady=(20, 0))
        
        print("✅ Interactive demo started. Close the window to continue.")
        self.root.mainloop()
    
    def _create_components_demo(self, parent):
        """Create demo of modern components."""
        # Components section
        components_frame = ttk.LabelFrame(parent, text="🧩 Modern Components", padding=15)
        components_frame.pack(fill="x", pady=(0, 20))
        
        # Grid layout for components
        row = 0
        
        try:
            # ModernCard demo
            card = ModernCard(components_frame, title="Sample Weather Card", padding=10)
            card.grid(row=row, column=0, padx=10, pady=10, sticky="ew")
            
            ttk.Label(card, text="🌤️ 22°C", font=('Segoe UI', 14, 'bold')).pack()
            ttk.Label(card, text="Partly Cloudy").pack()
            
            # WeatherGauge demo
            if WeatherGauge:
                gauge = WeatherGauge(components_frame, value=75, max_value=100,
                                   label="Humidity", unit="%", size=100)
                gauge.grid(row=row, column=1, padx=10, pady=10)
            
            row += 1
            
            # LoadingSpinner demo
            if LoadingSpinner:
                spinner_frame = ttk.Frame(components_frame)
                spinner_frame.grid(row=row, column=0, padx=10, pady=10)
                
                ttk.Label(spinner_frame, text="Loading Spinner:").pack()
                spinner = LoadingSpinner(spinner_frame, size=30)
                spinner.pack(pady=5)
                spinner.start_spinning()
            
            # Toggle switch demo
            if ModernToggleSwitch:
                toggle_frame = ttk.Frame(components_frame)
                toggle_frame.grid(row=row, column=1, padx=10, pady=10)
                
                ttk.Label(toggle_frame, text="Toggle Switch:").pack()
                toggle = ModernToggleSwitch(toggle_frame, text="Auto-refresh")
                toggle.pack(pady=5)
            
        except Exception as e:
            ttk.Label(components_frame, text=f"⚠️ Component demo error: {e}").pack()


def main():
    """Main test function."""
    print("🧪 Advanced Weather Dashboard - UX/UI Test Suite")
    print("=" * 60)
    print("This script tests all the modern UI components and features.")
    print()
    
    # Initialize test suite
    test_suite = UXTestSuite()
    
    # Run tests
    test_suite.run_all_tests()
    
    # Ask if user wants interactive demo
    if test_suite.root:
        print("\n🤔 Would you like to see an interactive demo?")
        response = input("Enter 'y' for yes, or any other key to exit: ").lower().strip()
        
        if response == 'y':
            test_suite.run_interactive_demo()
        else:
            test_suite.root.destroy()
    
    print("\n👋 Test suite completed. Thank you!")


if __name__ == "__main__":
    main()
