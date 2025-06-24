# 🌦️ Advanced Weather Intelligence Platform

## JTC Tech Pathway Capstone Project

A sophisticated weather dashboard application featuring clean architecture, modern UX/UI design, and comprehensive weather monitoring capabilities with clear separation of concerns.

---

## 🚀 Features

### 🎨 Modern User Interface

- **Professional Design**: Clean, modern interface with 18+ themes
- **Responsive Layout**: Adaptive design for different screen sizes
- **Interactive Components**: Modern cards, gauges, and progress indicators
- **Smooth Animations**: Professional transitions and loading effects

### 🏗️ Clean Architecture

- **Separation of Concerns**: Clear boundaries between UI, business logic, and services
- **Modular Design**: Well-organized codebase with focused responsibilities
- **Main Coordinator**: `src/main.py` serves as the application entry point and coordinator
- **Layered Structure**: Core business logic, UI components, and external services are properly separated

### 📊 Advanced Weather Data

- **Real-time Weather**: Current conditions with comprehensive metrics
- **7-Day Forecasts**: Detailed daily forecasts with weather icons
- **Air Quality Monitoring**: AQI indicators with detailed pollutant data
- **Interactive Gauges**: Temperature, humidity, pressure, wind speed displays

### 📈 Advanced Tabular Components (Capstone Features)

- **Historical Data Tables**: Sortable, filterable weather history with advanced search
- **Location Comparison**: Multi-location weather comparison with ranking systems
- **Analytics Dashboard**: Statistical analysis, trends, and performance metrics
- **Data Export**: CSV/JSON export capabilities for research and analysis
- **Advanced Filtering**: Date ranges, conditions, and custom criteria filtering
- **Data Management**: Import/Export tools, data validation, and quality controls

---

## 🏗️ Architecture Overview

The application follows a clean, layered architecture with clear separation of concerns:

### Main Entry Point

- **`src/main.py`**: Application coordinator that manages the interaction between UI and business logic layers

### Project Structure

```text
src/
├── main.py                 # Main application coordinator
├── core/
│   └── weather_core.py     # Business logic layer
├── services/
│   └── weather_api.py      # External API integration
├── ui/
│   ├── dashboard_ui.py     # Main user interface with tabular integration
│   ├── advanced_dashboard.py # Advanced dashboard with tabular components
│   ├── tabular_components.py # Advanced data tables (sorting, filtering, export)
│   ├── weather_displays.py # Weather-specific displays
│   └── modern_components.py # Reusable UI components
├── models/
│   └── weather_models.py   # Data models and validation
├── config/
│   └── app_config.py       # Configuration management
└── utils/
    └── helpers.py          # Utility functions
```

```text
├── src/                          # Main source code
│   ├── ui/                       # User interface components
│   │   ├── modern_components.py  # Advanced UI widgets
│   │   ├── dashboard_ui.py       # Main dashboard interface with tabular integration
│   │   ├── tabular_components.py # Advanced data tables (sortable, filterable, exportable)
│   │   └── weather_displays.py   # Weather visualization components
│   ├── models/                   # Data models
│   │   └── weather_models.py     # Weather data structures
│   ├── services/                 # External services
│   │   └── weather_api.py        # OpenWeatherMap API integration
│   ├── core/                     # Business logic
│   │   └── weather_core.py       # Core weather processing
│   ├── config/                   # Configuration
│   │   └── config.py             # Application settings
│   └── utils/                    # Utilities
│       └── ml_predictions.py     # Machine learning features
├── tests/                        # Test suite
├── launcher.py                   # Application launcher
└── requirements.txt             # Python dependencies
```

### **Technical Stack**

- **Python 3.8+**: Core programming language
- **ttkbootstrap**: Modern UI framework with 18+ themes
- **tkinter**: Base GUI framework
- **requests**: HTTP client for API calls
- **scikit-learn**: Machine learning capabilities
- **matplotlib**: Data visualization and charts
- **numpy/pandas**: Data processing and analysis

---

## 🚀 **Quick Start**

### **Installation**

1. **Clone the repository**:

   ```bash
   git clone <repository-url>
   cd JTC_Tech_Pathway_Capstone
   ```

1. **Create virtual environment**:

   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   source .venv/bin/activate  # Linux/Mac
   ```

1. **Install dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

1. **Set up environment variables**:

   ```bash
   cp .env.example .env
   # Edit .env file with your OpenWeatherMap API key
   ```

### **Running the Application**

#### **🚀 Main Application (Recommended)**

Use the launcher for dependency checking and guided startup:

```bash
python launcher.py
```

#### **📊 Advanced Dashboard (Capstone Features)**

Launch the advanced dashboard with tabular components:

```bash
python launch_advanced_dashboard.py
```

Features:

- **🌦️ Live Dashboard**: Real-time weather with search functionality
- **📈 Historical Data**: Sortable weather history tables with filtering
- **🌍 Comparisons**: Multi-location and time period analysis
- **📊 Analytics**: Statistical analysis and trend visualization
- **🗂️ Data Management**: Import/Export and data quality tools

#### **🎯 Direct Launch**

Launch the main application directly:

```bash
python src/main.py
```

#### **🧪 Test Suite**

```bash
python -m pytest tests/
```

---

## 🎮 **Usage**

### **Main Dashboard**

1. **Launch** the application using any of the launchers above
2. **Search** for locations using the modern search bar
3. **Explore** weather data through interactive cards and gauges
4. **Customize** themes and settings via the sidebar
5. **Monitor** air quality and forecasts in real-time

### **Advanced Features**

- **Theme Selection**: Choose from 18+ professional themes
- **Auto-refresh**: Configure automatic weather updates
- **Notifications**: Receive weather alerts and updates
- **Data Export**: Export weather data for analysis
- **Settings**: Customize temperature units and preferences

---

## 🎨 **Modern UI Components**

### **Available Components**

- **ModernCard**: Styled container with headers and content areas
- **CircularProgress**: Animated progress indicators for metrics
- **ModernSearchBar**: Enhanced search with suggestions
- **WeatherGauge**: Circular gauges for weather data
- **NotificationToast**: Pop-up notifications for user feedback
- **ModernToggleSwitch**: Stylish toggle switches for settings
- **LoadingSpinner**: Animated loading indicators

### **Theme System**

- **18+ Themes Available**: cosmo, flatly, litera, minty, darkly, cyborg, etc.
- **Real-time Theme Switching**: Change themes without restarting
- **Custom Styling**: Professional color schemes and fonts
- **Responsive Design**: Adapts to different screen sizes

---

## 🧪 **Testing**

### **Automated Testing**

```bash
python -m pytest tests/
```

**Current Test Results**: Comprehensive test suite available

### **Manual Testing**

```bash
python src/main.py
```

The main application provides comprehensive weather monitoring capabilities with a modern, clean interface.

---

## 📖 **API Configuration**

### **OpenWeatherMap API**

1. Sign up at [OpenWeatherMap](https://openweathermap.org/api)
2. Get your free API key
3. Add to `.env` file:

   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   ```

### **API Features Used**

- **Current Weather**: Real-time weather data
- **5-Day Forecast**: Extended weather predictions
- **Air Quality**: AQI and pollutant monitoring
- **Geocoding**: Location search and suggestions

---

## 🔧 **Development**

### **Project Status**

- ✅ **Core Architecture**: Complete and stable
- ✅ **Modern UI Components**: Implemented and functional
- ✅ **Enhanced Dashboard**: Working with advanced features
- ✅ **Testing Suite**: Comprehensive test coverage
- ✅ **Documentation**: Complete user and developer docs
- ✅ **Windows Compatibility**: Fully tested and optimized

### **Contributing**

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the test suite
5. Submit a pull request

### **Development Tools**

- **Type Hints**: Full type safety throughout codebase
- **Error Handling**: Comprehensive error handling and logging
- **Modular Design**: Clean separation of concerns
- **Extensible Architecture**: Easy to add new features

---

## 📋 **Requirements**

### **System Requirements**

- **Python**: 3.8 or higher
- **Operating System**: Windows 10+, macOS 10.14+, Linux Ubuntu 18.04+
- **Memory**: 512MB RAM minimum
- **Storage**: 100MB free space

### **Dependencies**

See `requirements.txt` for complete list:

- ttkbootstrap>=1.10.0
- requests>=2.25.0
- matplotlib>=3.5.0
- scikit-learn>=1.0.0
- numpy>=1.21.0
- pandas>=1.3.0

---

## 🤝 **Team Collaboration**

This project is designed for team collaboration with clean architecture and established development practices.

### **Quick Team Setup**

New team members can get started quickly:

```bash
# Clone the repository
git clone <repository-url>
cd JTC_Tech_Pathway_Capstone

# Run the team setup script
python setup_team.py
```

### **Development Guidelines**

- 📖 **Read First**: [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines
- 🏗️ **Architecture**: [ARCHITECTURE.md](ARCHITECTURE.md) for system design
- 📝 **Changes**: [CHANGELOG.md](CHANGELOG.md) for version history
- 🔒 **Security**: [SECURITY.md](SECURITY.md) for security practices

### **Project Structure**

```text
├── src/                    # Source code (modular architecture)
├── tests/                  # Test suite
├── .env.example           # Environment template
├── requirements.txt       # Dependencies
├── setup_team.py         # Team onboarding script
└── docs/                  # Documentation
```

### **Development Workflow**

1. **Setup**: Run `python setup_team.py`
2. **Branch**: Create feature branches from `main`
3. **Code**: Follow PEP 8 and add type hints
4. **Test**: Write tests and ensure they pass
5. **PR**: Submit pull requests with clear descriptions

---

## 🧹 **Maintenance & Cleanup**

### **Project Cleanup**

The project includes automated cleanup scripts to remove development artifacts:

#### **Python Script (Cross-platform)**

```bash
# Show what would be cleaned (dry run)
python cleanup.py --dry-run --verbose

# Perform actual cleanup
python cleanup.py --verbose
```

#### **PowerShell Script (Windows)**

```powershell
# Show what would be cleaned (dry run)
.\cleanup.ps1 -DryRun -Verbose

# Perform actual cleanup
.\cleanup.ps1 -Verbose
```

### **What Gets Cleaned**

- **`__pycache__`** directories (excluding `.venv`)
- **`.pyc`** compiled Python files
- **Temporary files** (`.tmp`, `.bak`, `.swp`, `.DS_Store`)
- **Runtime logs** (content cleared, files preserved)

### **Manual Cleanup**

You can also manually clean up using:

```bash
# Remove Python cache files
find . -name "__pycache__" -not -path "./.venv/*" -exec rm -rf {} +
find . -name "*.pyc" -not -path "./.venv/*" -delete

# Clear log files
> logs/weather_dashboard.log
> logs/errors.log
```

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 **Acknowledgments**

- **OpenWeatherMap**: Weather data API
- **ttkbootstrap**: Modern UI framework
- **Python Community**: Excellent libraries and tools
- **JTC Tech Pathway**: Educational program and support

---

## 📞 **Support**

For questions, issues, or feature requests:

1. Run the test suite to diagnose issues: `python -m pytest tests/`
2. Review the [Architecture Documentation](ARCHITECTURE.md)
3. Check the [Contributing Guidelines](CONTRIBUTING.md)
4. Launch the application with `python launcher.py`

---

🌟 Advanced Weather Intelligence Platform - Built with ❤️ using Python

**Status**: ✅ Ready for Team Collaboration
**Version**: 1.0 - Clean Architecture Release
**Last Updated**: June 23, 2025
