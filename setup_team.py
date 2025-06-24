#!/usr/bin/env python3
"""
Team setup script for the Advanced Weather Intelligence Platform.

This script helps new team members quickly set up their development environment.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def run_command(command, description, check=True):
    """Run a command and handle errors."""
    print(f"🔄 {description}...")
    try:
        if isinstance(command, str):
            result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        else:
            result = subprocess.run(command, check=check, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
        else:
            print(f"⚠️  {description} completed with warnings")
            if result.stderr:
                print(f"   Warning: {result.stderr.strip()}")
        return result
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"   Error: {e.stderr.strip() if e.stderr else str(e)}")
        return None


def check_python_version():
    """Check if Python version is 3.8 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} detected. Python 3.8+ required")
        return False


def check_git():
    """Check if git is available."""
    result = run_command("git --version", "Checking Git installation", check=False)
    return result is not None and result.returncode == 0


def setup_virtual_environment():
    """Set up Python virtual environment."""
    venv_path = Path(".venv")
    
    if venv_path.exists():
        print("✅ Virtual environment already exists")
        return True
    
    result = run_command([sys.executable, "-m", "venv", ".venv"], "Creating virtual environment")
    return result is not None


def get_activation_command():
    """Get the activation command for the current platform."""
    if os.name == 'nt':  # Windows
        return ".venv\\Scripts\\activate"
    else:  # macOS/Linux
        return "source .venv/bin/activate"


def install_dependencies():
    """Install project dependencies."""
    # Check if we're in a virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        pip_command = "pip"
    else:
        # Use virtual environment pip
        if os.name == 'nt':  # Windows
            pip_command = ".venv\\Scripts\\pip"
        else:  # macOS/Linux
            pip_command = ".venv/bin/pip"
    
    result = run_command(f"{pip_command} install -r requirements.txt", "Installing dependencies")
    return result is not None


def setup_environment_file():
    """Set up the .env file."""
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if env_file.exists():
        print("✅ .env file already exists")
        return True
    
    if env_example.exists():
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("⚠️  Remember to add your OpenWeatherMap API key to .env")
        return True
    else:
        print("❌ .env.example not found")
        return False


def check_api_key():
    """Check if API key is configured."""
    env_file = Path(".env")
    if env_file.exists():
        content = env_file.read_text()
        if "your_api_key_here" in content:
            print("⚠️  Please update your API key in .env file")
            print("   Get your free API key from: https://openweathermap.org/api")
            return False
        else:
            print("✅ API key appears to be configured")
            return True
    return False


def run_tests():
    """Run the test suite."""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        python_command = "python"
    else:
        if os.name == 'nt':  # Windows
            python_command = ".venv\\Scripts\\python"
        else:  # macOS/Linux
            python_command = ".venv/bin/python"
    
    result = run_command(f"{python_command} -m pytest tests/ -v", "Running tests", check=False)
    return result is not None and result.returncode == 0


def main():
    """Main setup routine."""
    print("🌦️  Advanced Weather Intelligence Platform - Team Setup")
    print("=" * 60)
    
    # Check prerequisites
    if not check_python_version():
        sys.exit(1)
    
    if not check_git():
        print("⚠️  Git not found. Please install Git for version control.")
    
    # Setup steps
    steps = [
        ("Setting up virtual environment", setup_virtual_environment),
        ("Setting up environment file", setup_environment_file),
        ("Installing dependencies", install_dependencies),
    ]
    
    for description, step_func in steps:
        print(f"\n📋 {description}")
        if not step_func():
            print(f"❌ Setup failed at: {description}")
            sys.exit(1)
    
    # Post-setup checks
    print(f"\n🔧 Post-setup checks")
    check_api_key()
    
    # Final instructions
    print(f"\n🎉 Setup completed successfully!")
    print(f"\n📝 Next steps:")
    print(f"   1. Activate your virtual environment: {get_activation_command()}")
    print(f"   2. Update your API key in .env file")
    print(f"   3. Run the application: python launcher.py")
    print(f"   4. Run tests: python -m pytest tests/")
    print(f"\n📚 Documentation:")
    print(f"   - README.md: Project overview and features")
    print(f"   - CONTRIBUTING.md: Development guidelines")
    print(f"   - ARCHITECTURE.md: Technical architecture")
    
    # Optional test run
    if input(f"\n🧪 Would you like to run the test suite now? (y/N): ").lower() == 'y':
        print(f"\n🧪 Running tests")
        if run_tests():
            print("✅ All tests passed!")
        else:
            print("⚠️  Some tests failed. Check the output above.")


if __name__ == "__main__":
    main()
