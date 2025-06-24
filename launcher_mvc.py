#!/usr/bin/env python3
"""
Enhanced Weather Dashboard Launcher with MVC Architecture

This launcher provides multiple ways to start the Weather Dashboard application
with the new Model-View-Controller architecture, ensuring proper separation
of concerns and improved maintainability.
"""

import sys
import os
import argparse
import logging
from pathlib import Path

# Add the project root and src to Python path
project_root = Path(__file__).parent
src_path = project_root / "src"
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(src_path))

try:
    # Import MVC application
    from src.main import main as run_mvc_app
    
    # Import legacy application for compatibility
    from src.main_mvc import main as run_legacy_app
    
    # Import configuration
    from src.config.config import APP_CONFIG
    
except ImportError as e:
    print(f"Error importing application modules: {e}")
    print("Please ensure you're running from the correct directory.")
    sys.exit(1)


def setup_logging(verbose: bool = False) -> None:
    """Setup logging configuration."""
    level = logging.DEBUG if verbose else logging.INFO
    
    # Ensure logs directory exists
    logs_dir = project_root / "logs"
    logs_dir.mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(logs_dir / 'launcher.log', mode='a', encoding='utf-8')
        ]
    )


def check_requirements() -> bool:
    """Check if all required dependencies are available."""
    required_modules = [
        'ttkbootstrap',
        'requests',
        'python-dotenv'
    ]
    
    missing_modules = []
    for module in required_modules:
        try:
            __import__(module.replace('-', '_'))
        except ImportError:
            missing_modules.append(module)
    
    if missing_modules:
        print(f"Error: Missing required modules: {', '.join(missing_modules)}")
        print("Please install them using: pip install -r requirements.txt")
        return False
    
    return True


def check_environment() -> bool:
    """Check if the environment is properly configured."""
    # Check for API key
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        print("Warning: OPENWEATHER_API_KEY environment variable not set.")
        print("Some features may not work properly.")
        print("Please set your API key in a .env file or environment variable.")
    
    # Ensure required directories exist
    required_dirs = ['logs', 'data', 'cache', 'exports']
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        dir_path.mkdir(exist_ok=True)
    
    return True


def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        description="Weather Dashboard Application Launcher",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launcher_mvc.py                    # Start with MVC architecture
  python launcher_mvc.py --legacy          # Start with legacy architecture  
  python launcher_mvc.py --verbose         # Start with verbose logging
  python launcher_mvc.py --check           # Check environment only
        """
    )
    
    parser.add_argument(
        '--legacy',
        action='store_true',
        help='Use legacy application architecture'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--check',
        action='store_true',
        help='Check environment and requirements only'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'Weather Dashboard {APP_CONFIG.get("version", "1.0.0")}'
    )
    
    args = parser.parse_args()
    
    # Setup logging
    setup_logging(args.verbose)
    logger = logging.getLogger(__name__)
    
    logger.info("Starting Weather Dashboard Launcher")
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check environment
    if not check_environment():
        sys.exit(1)
    
    if args.check:
        print("✓ All requirements and environment checks passed!")
        print("✓ Ready to run Weather Dashboard")
        return
    
    try:
        if args.legacy:
            logger.info("Starting Weather Dashboard with legacy architecture")
            print("🌦️  Starting Weather Dashboard (Legacy Mode)...")
            run_legacy_app()
        else:
            logger.info("Starting Weather Dashboard with MVC architecture")
            print("🌦️  Starting Weather Dashboard (MVC Mode)...")
            run_mvc_app()
            
    except KeyboardInterrupt:
        print("\n👋 Weather Dashboard stopped by user")
        logger.info("Application interrupted by user")
        
    except Exception as e:
        print(f"❌ Error starting Weather Dashboard: {e}")
        logger.error(f"Application startup error: {e}", exc_info=True)
        
        # Try to show error in GUI if possible
        try:
            import tkinter as tk
            from tkinter import messagebox
            
            root = tk.Tk()
            root.withdraw()  # Hide the root window
            
            messagebox.showerror(
                "Startup Error",
                f"Failed to start Weather Dashboard:\n\n{e}\n\n"
                f"Check the logs for more details."
            )
            
        except Exception:
            pass  # GUI error display failed, error already printed
        
        sys.exit(1)
    
    finally:
        logger.info("Weather Dashboard Launcher finished")


if __name__ == "__main__":
    main()
