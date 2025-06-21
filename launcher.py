#!/usr/bin/env python3
"""
🌤️ Weather Dashboard Launcher
Launch the weather dashboard application

Usage:
    python launcher.py
"""

import sys
import os
import subprocess
from pathlib import Path


def show_banner():
    """Display application banner."""
    banner = """
🌦️ Weather Dashboard - Clean Architecture
==========================================

Entry Point: src/main.py
Architecture: Clean separation of concerns
- UI Layer: Presentation components
- Core Layer: Business logic
- Services: External API interactions
- Models: Data structures
- Config: Application configuration

"""
    print(banner)


def check_dependencies():
    """Quick check for essential dependencies."""
    print("🔍 Checking essential dependencies...")
    
    required_modules = ['tkinter', 'ttkbootstrap', 'requests']
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing.append(module)
    
    if missing:
        print(f"❌ Missing critical dependencies: {', '.join(missing)}")
        print("💡 Run: pip install -r requirements.txt")
        return False
    else:
        print("✅ Essential dependencies available")
        return True


def run_main_application():
    """Run the main weather dashboard application."""
    script_dir = Path(__file__).parent
    main_script = script_dir / "src" / "main.py"
    
    if not main_script.exists():
        print(f"❌ Main script not found: {main_script}")
        return False
    
    print("🚀 Launching Weather Dashboard...")
    print("-" * 50)
    
    try:
        # Change to the script directory
        os.chdir(script_dir)
        
        # Run the main application
        result = subprocess.run([sys.executable, str(main_script)], 
                              check=False, 
                              text=True)
        
        if result.returncode == 0:
            print("✅ Application completed successfully")
        else:
            print(f"⚠️ Application exited with code {result.returncode}")
        
        return result.returncode == 0
        
    except KeyboardInterrupt:
        print("\n🛑 Application interrupted by user")
        return True
    except Exception as e:
        print(f"❌ Error running application: {e}")
        return False


def main():
    """Main launcher function."""
    show_banner()
    
    # Check dependencies
    if not check_dependencies():
        print("\n🔧 Please install missing dependencies before continuing.")
        response = input("Continue anyway? (y/N): ").strip().lower()
        if response not in ['y', 'yes']:
            return
    
    # Run the main application
    success = run_main_application()
    
    if not success:
        print("\n🔧 Troubleshooting tips:")
        print("1. Ensure dependencies are installed: pip install -r requirements.txt")
        print("2. Check your .env file has a valid OpenWeatherMap API key")
        print("3. Make sure you're using Python 3.8 or higher")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Launcher interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Launcher error: {e}")
        sys.exit(1)
