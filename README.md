# 🌤️ Complete Weather Dashboard - JTC Tech Pathway Capstone

> **Justice Through Code ⚖ Capstone Project**

A comprehensive weather application combining real-time data, machine learning predictions, and advanced visualizations using the OpenWeatherMap Student Pack API. This capstone project demonstrates the integration of multiple technologies to create a professional weather monitoring solution.

## ✨ Key Features

### 🌤️ Complete Weather Application (Recommended)

**`complete_weather_dashboard.py`** - The integrated solution combining all features:

- **Real-time Weather Data** - Current conditions with comprehensive metrics
- **Machine Learning Predictions** - 12-hour temperature forecasting using scikit-learn
- **Interactive Visualizations** - Matplotlib charts with selectable data types
- **5-Day Weather Forecast** - 3-hour interval forecasts for 5 days
- **Air Quality Monitoring** - Real-time pollution data and health recommendations
- **Interactive Weather Maps** - 12 weather layer visualizations (Student Pack)
- **Advanced Geocoding** - Location search and coordinate conversion
- **Modern GUI** - Dark-themed, responsive interface with multiple themes
- **Persistent Settings** - Theme and location preferences saved automatically

### 🔮 Additional Applications

- **Unified Weather Dashboard** (`unified_weather_dashboard.py`) - Comprehensive Student Pack showcase
- **Enhanced Weather Dashboard** (`enhanced_weather_dashboard.py`) - ML-focused implementation

### 🛠️ Technology Stack

- **Python 3.8+** with tkinter & ttkbootstrap for modern GUI
- **matplotlib** for data visualization and charting
- **scikit-learn** for machine learning predictions
- **pandas & numpy** for data analysis and manipulation
- **requests** for HTTP API communications
- **python-dotenv** for environment variable management

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- OpenWeatherMap API key (Student Pack or free tier)
- Internet connection for real-time data

### Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd JTC_Tech_Pathway_Capstone
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Get your free API key:**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Get your API key from the dashboard

4. **Configure your API key:**
   - Create a `.env` file in the project root
   - Add your OpenWeatherMap API key:
     ```env
     OPENWEATHER_API_KEY=your_api_key_here
     ```

5. **Run the complete application (Recommended):**
   ```bash
   python complete_weather_dashboard.py
   ```

### Alternative Launch Options

**Using the Launcher:**
```bash
python launcher.py
# Then select option 1 for the complete dashboard
```

**Individual Applications:**
```bash
python unified_weather_dashboard.py      # Original comprehensive dashboard
python enhanced_weather_dashboard.py     # ML-focused implementation
```

**Testing:**
```bash
python test_complete_app.py              # Comprehensive test suite
```

## � Application Features

### Complete Weather Dashboard (⭐ Recommended)

The integrated application provides four main tabs:

#### 🌤️ Current Weather & Predictions
- **Large temperature display** with feels-like temperature
- **Detailed weather metrics** (humidity, wind, pressure, clouds)
- **Machine learning predictions** for next 12 hours using scikit-learn
- **Weather description** and current conditions

#### 📊 Forecast Charts
- **Interactive matplotlib visualizations** with professional styling
- **Selectable chart types:**
  - Temperature Trend (24-hour)
  - Humidity & Pressure (dual-axis)
  - Wind Patterns
  - Precipitation Analysis
- **Real-time chart updates** based on selection
- **Dark theme integration** matching the UI

#### 🗺️ Maps & Air Quality
- **Air Quality Index** with health recommendations
- **Weather map layer selection** (temperature, precipitation, pressure, wind, clouds)
- **Direct browser integration** with OpenWeatherMap maps
- **Pollution monitoring** with detailed pollutant breakdown

#### 📈 Analytics & Historical Data
- **Historical analysis controls** with date range selection
- **Educational insights** about weather patterns
- **Student Pack feature demonstrations**
- **Seasonal pattern recognition** and trend analysis

### User Interface Features
- **Modern dark theme** with ttkbootstrap styling
- **Multiple theme options** (10+ available themes)
- **Responsive design** that adapts to window size
- **Persistent settings** that remember preferences
- **Professional status updates** and loading indicators

## 🧪 Testing & Validation

### Comprehensive Test Suite

Run the complete test suite to validate everything is working:

```bash
python test_complete_app.py
```

The test suite validates:
- ✅ Required dependencies (tkinter, ttkbootstrap, matplotlib, scikit-learn, etc.)
- ✅ API key configuration and validity
- ✅ Application components and imports
- ✅ Machine learning functionality
- ✅ Data classes and methods

### Interactive Launcher

Use the launcher for easy access to all applications:

```bash
python launcher.py
```

Features:
- Interactive menu system
- Built-in dependency checking
- Direct command-line arguments support
- Professional user interface

## 📋 Project Structure

```text
JTC_Tech_Pathway_Capstone/
├── complete_weather_dashboard.py     # 🌟 Complete integrated application (RECOMMENDED)
├── unified_weather_dashboard.py     # 🌤️ Original comprehensive dashboard
├── enhanced_weather_dashboard.py    # 🔮 ML-focused implementation
├── launcher.py                      # 🚀 Interactive application launcher
├── test_complete_app.py            # 🧪 Comprehensive test suite
├── requirements.txt                # 📦 Python dependencies
├── settings.json                   # ⚙️ Persistent application settings
├── .env                           # 🔑 Configuration (create this)
├── README.md                      # 📖 This documentation
├── LICENSE                        # 📄 License information
└── SECURITY.md                    # 🔒 Security guidelines
```

## 🔧 Configuration & API Setup

### Environment Variables

Configure your API key in a `.env` file:

```env
# OpenWeatherMap API key (required)
OPENWEATHER_API_KEY=your_api_key_here
```

### OpenWeatherMap Student Pack Benefits

- **Rate Limits**: 60 calls/minute, 1,000,000 calls/month
- **Current Weather**: Real-time weather data for any location
- **5-Day Forecast**: Weather predictions with 3-hour intervals
- **Air Quality**: Pollution monitoring and health recommendations
- **Weather Maps**: 12 weather layer visualizations (all included)
- **Geocoding**: Location search and coordinate conversion
- **Historical Data**: Full historical data archive (Student Pack)
- **Advanced Analytics**: Statistical weather data access
- **Educational Support**: Extended features for learning

### API Endpoints Used

- **Current Weather**: `/data/2.5/weather`
- **5-Day Forecast**: `/data/2.5/forecast`
- **Air Pollution**: `/data/2.5/air_pollution`
- **Geocoding**: `/geo/1.0/direct`
- **Weather Maps**: `/map/{layer}/{z}/{x}/{y}.png`

## 🎓 Educational Value

### Learning Objectives Demonstrated

1. **API Integration** - Real-world service consumption with error handling
2. **Data Analysis** - Processing and visualization of weather data
3. **Machine Learning** - Predictive modeling using scikit-learn
4. **GUI Development** - Professional interface design with ttkbootstrap
5. **Software Architecture** - Modular design and code organization
6. **Testing** - Comprehensive validation and verification

### Technical Skills Showcased

- **Object-oriented programming** principles and design patterns
- **Asynchronous operations** with threading for non-blocking UI
- **Data persistence** and configuration management
- **Third-party library** integration and dependency management
- **User experience** design considerations and responsive layouts
- **Error handling** and robust application design

## �️ Dependencies

All required packages are listed in `requirements.txt`:

- **requests** (>=2.28.0) - HTTP library for API calls
- **python-dotenv** (>=1.0.0) - Environment variable management
- **ttkbootstrap** (>=1.10.1) - Modern GUI framework
- **matplotlib** (>=3.5.0) - Data visualization and charting
- **numpy** (>=1.21.0) - Numerical computing
- **pandas** (>=1.3.0) - Data analysis and manipulation
- **scikit-learn** (>=1.0.0) - Machine learning library
- **Pillow** (>=8.0.0) - Image processing capabilities

## �🔍 Troubleshooting

### Common Issues

#### "API key not found" error
- Ensure your `.env` file exists in the project root
- Verify your API key is correct and active
- Check the variable name is `OPENWEATHER_API_KEY`

#### Import or dependency errors
```bash
pip install --upgrade -r requirements.txt
```

#### "Location not found" error
- Try different location formats (city name, coordinates)
- Use more specific location names (e.g., "London, UK" instead of "London")
- Check spelling and verify the location exists

#### Chart or visualization issues
- Verify matplotlib backend compatibility
- Check system graphics drivers
- Restart application after theme changes

#### Network connectivity issues
- Check your internet connection
- Verify firewall settings allow API requests
- Ensure you haven't exceeded rate limits

### Getting Help

If you encounter issues:
1. Run the test suite: `python test_complete_app.py`
2. Check console output for detailed error messages
3. Verify your API key and internet connection
4. Ensure all dependencies are installed correctly

## 📈 Future Enhancements

### Potential Improvements
- **Weather alerts** and notifications
- **Export functionality** for charts and data
- **Database integration** for historical storage
- **Mobile-responsive** web version
- **Advanced ML models** (neural networks, ensemble methods)
- **Social sharing** features
- **Multi-location** comparison tools

## 📄 License

This project is for educational use only as part of the JTC Tech Pathway Capstone program. Please ensure you comply with OpenWeatherMap's terms of service and API usage guidelines.

**Educational Use Only** - OpenWeatherMap Student Pack Integration

## 🙏 Acknowledgments

- **OpenWeatherMap** - For providing the comprehensive weather API and Student Pack benefits
- **Justice Through Code** - For supporting this capstone project and educational journey
- **Python Community** - For excellent libraries and frameworks that made this project possible
- **Open Source Contributors** - For maintaining the libraries used in this project

---

🎓 **A Justice Through Code Capstone Project showcasing modern weather data integration, machine learning, and professional software development practices.**

*This application demonstrates the successful integration of multiple technologies to create a professional weather monitoring solution, showcasing skills in software development, data analysis, machine learning, and user interface design.*
