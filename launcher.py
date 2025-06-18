#!/usr/bin/env python3
"""
🌤️ Weather Dashboard Launcher
Launch any of the three weather dashboard applications

Usage:
    python launcher.py [app_choice]
    
Where app_choice is:
    1 or complete    - Complete Weather Dashboard (main application)
    2 or cobra       - COBRA Commander Styled Weather App (demo)
    test            - Run test suite
"""

import sys
import os
import subprocess
from pathlib import Path

def show_banner():
    """Display the application banner."""
    banner = """
🌤️ ================================================ 🌤️
    JTC Tech Pathway Capstone - Weather Dashboard
🌤️ ================================================ 🌤️

Available Applications:

1. 🌟 Complete Weather Dashboard (MAIN APPLICATION)
   └─ Comprehensive weather monitoring solution
   └─ Machine learning predictions
   └─ Advanced visualizations & forecasts
   └─ Modern UI with multiple themes
   └─ All-in-one integrated features

2. 🐍 COBRA Commander Weather App (DEMO)
   └─ Sci-fi villain themed styling demo
   └─ COBRA Commander inspired interface
   └─ Demonstrates custom styling system
   └─ Showcase for styling framework

🧪 Test Suite
   └─ Verify all dependencies
   └─ Check API configuration
   └─ Validate functionality

"""
    print(banner)

def get_user_choice():
    """Get user's application choice."""
    while True:
        choice = input("Select an application (1-2) or 'test' for test suite: ").strip().lower()
        
        if choice in ['1', 'complete']:
            return 'complete'
        elif choice in ['2', 'cobra']:
            return 'cobra'
        elif choice in ['test', 't']:
            return 'test'
        elif choice in ['exit', 'quit', 'q']:
            print("👋 Goodbye!")
            sys.exit(0)
        else:
            print("❌ Invalid choice. Please enter 1, 2, or 'test'")

def run_application(app_choice):
    """Run the selected application."""
    script_dir = Path(__file__).parent
    
    apps = {
        'complete': 'complete_weather_dashboard.py',
        'cobra': 'cobra_weather_app.py',
        'test': 'test_complete_app.py'
    }
    
    if app_choice not in apps:
        print(f"❌ Unknown application choice: {app_choice}")
        return False
    
    script_path = script_dir / apps[app_choice]
    
    if not script_path.exists():
        print(f"❌ Script not found: {script_path}")
        return False
    
    print(f"🚀 Launching {apps[app_choice]}...")
    print("-" * 50)
    
    try:
        # Change to the script directory
        os.chdir(script_dir)
        
        # Run the selected script
        result = subprocess.run([sys.executable, str(script_path)], 
                              check=False, 
                              text=True)
        
        if result.returncode == 0:
            print(f"✅ {apps[app_choice]} completed successfully")
        else:
            print(f"⚠️ {apps[app_choice]} exited with code {result.returncode}")
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        return True
    except Exception as e:
        print(f"❌ Error running {apps[app_choice]}: {e}")
        return False

def check_dependencies():
    """Quick dependency check."""
    print("🔍 Checking dependencies...")
    
    required_modules = [
        'tkinter', 'ttkbootstrap', 'matplotlib', 'sklearn',
        'pandas', 'numpy', 'requests', 'dotenv', 'PIL'
    ]
    
    missing = []
    
    for module in required_modules:
        try:
            if module == 'PIL':
                import PIL
            elif module == 'sklearn':
                import sklearn
            elif module == 'dotenv':
                from dotenv import load_dotenv
            else:
                __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing dependencies: {', '.join(missing)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ All dependencies available")
        return True

def main():
    """Main launcher function."""
    show_banner()
      # Handle command line arguments
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['1', 'complete']:
            app_choice = 'complete'
        elif arg in ['2', 'cobra']:
            app_choice = 'cobra'
        elif arg in ['test', 't']:
            app_choice = 'test'
        elif arg in ['help', '-h', '--help']:
            print(__doc__)
            return
        else:
            print(f"❌ Unknown argument: {arg}")
            print("Use 'python launcher.py help' for usage information")
            return
    else:
        # Quick dependency check
        if not check_dependencies():
            print("\n🔧 Please install missing dependencies before continuing.")
            input("Press Enter to continue anyway...")
        
        app_choice = get_user_choice()
    
    # Run the selected application
    success = run_application(app_choice)
    
    if not success and app_choice != 'test':
        print("\n🔧 Troubleshooting tips:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check your .env file has a valid OpenWeatherMap API key")
        print("3. Make sure you're using Python 3.8 or higher")
        print("4. Run the test suite: python launcher.py test")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Launcher interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Launcher error: {e}")
        sys.exit(1)
