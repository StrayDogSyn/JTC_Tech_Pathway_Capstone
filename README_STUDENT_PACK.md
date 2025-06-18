# 🎓 Student Pack Weather Dashboard

A comprehensive weather application showcasing all **OpenWeatherMap Student Pack** features. This project demonstrates advanced weather data integration with a modern GUI interface, perfect for educational use and learning weather API development.

## 🌟 Student Pack Features Implemented

### 📊 Current & Forecast Data
- **Rate Limits**: 3,000 API calls/minute, 100,000,000 calls/month
- **Current Weather API**: Real-time weather conditions
- **Hourly Forecast**: 4 days (96 hours) of detailed predictions
- **Daily Forecast**: 16 days of extended weather forecasts

### 🌍 Weather Maps
- **15 Weather Layers** including:
  - Temperature maps (current, forecast, historical)
  - Precipitation radar and forecasts
  - Wind speed and direction
  - Cloud coverage and satellite imagery
  - Atmospheric pressure systems

### 🌬️ Air Pollution API
- Real-time Air Quality Index (AQI)
- Detailed pollutant breakdown (CO, NO, NO2, O3, SO2, PM2.5, PM10, NH3)
- 5-day air quality forecasts
- Historical air pollution data

### 📍 Geocoding API
- City name to coordinates conversion
- Reverse geocoding (coordinates to location)
- Support for multiple location formats
- International location support

### 📚 Historical Data
- **1 Year Archive**: Access to historical weather data
- **50,000 calls/day** for historical requests
- Weather history analysis
- Climate pattern research

### 📈 Advanced Analytics
- **Statistical Weather Data API**: Advanced weather statistics
- **Accumulated Parameters**: Temperature and precipitation accumulation
- Historical trend analysis
- Research-grade data quality

## 🚀 Quick Start

### Prerequisites
- Python 3.7+
- OpenWeatherMap API key with Student Pack access

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd JTC_Tech_Pathway_Capstone
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   Create a `.env` file in the project root:
   ```env
   OPENWEATHER_API_KEY=your_api_key_here
   OPENWEATHER_API_KEY_BACKUP=your_backup_key_here
   DEFAULT_CITY=New York
   TEMPERATURE_UNITS=metric
   ```

### Running the Applications

#### 🖥️ GUI Application (Recommended)
```bash
python student_pack_gui_fixed.py
```

#### 📊 Feature Demo
```bash
python student_pack_demo.py
```

#### 🧪 API Testing
```bash
python test_subscription.py
```

## 📱 Applications Overview

### 1. Student Pack GUI (`student_pack_gui_fixed.py`)
Modern graphical interface featuring:
- **Current Weather Tab**: Real-time conditions with detailed metrics
- **Air Quality Tab**: AQI monitoring and pollutant breakdown
- **Weather Maps Tab**: Interactive maps with 15 different layers
- **Location Search**: Geocoding with international support
- **Responsive Design**: Modern, professional interface

### 2. Enhanced Weather API (`enhanced_weather_api.py`)
Comprehensive API wrapper providing:
- All Student Pack endpoints
- Error handling and fallbacks
- Rate limit management
- Data formatting utilities
- Statistical analysis tools

### 3. Student Pack Demo (`student_pack_demo.py`)
Command-line demonstration of:
- All available Student Pack features
- API capability testing
- Feature showcase with examples
- Performance and rate limit information

### 4. Configuration Management (`config.py`)
Centralized configuration for:
- API keys and endpoints
- Student Pack subscription details
- Rate limits and feature flags
- Security validation

## 🎯 Student Pack Benefits

### 💰 Cost
- **FREE** for educational use
- No monthly fees for students
- Full feature access included

### ⚡ Performance
- **3,000 calls/minute** - High-frequency requests
- **100,000,000 calls/month** - Massive monthly allowance
- **50,000 historical calls/day** - Extensive research capability

### 📊 Data Access
- **1 year historical archive** - Climate research
- **15 weather map layers** - Comprehensive visualization
- **Real-time air quality** - Environmental monitoring
- **Extended forecasts** - Long-term planning

### 🔬 Research Features
- Statistical weather analysis
- Accumulated parameter calculations
- Historical trend analysis
- Climate pattern research

## 🛠️ Technical Implementation

### Architecture
```
📦 Student Pack Weather Dashboard
├── 🎨 Presentation Layer
│   ├── student_pack_gui_fixed.py     # Modern GUI interface
│   └── student_pack_demo.py          # CLI demonstration
├── 🔌 API Layer
│   ├── enhanced_weather_api.py       # Comprehensive API wrapper
│   └── weather_api.py                # Basic weather API
├── ⚙️ Configuration
│   └── config.py                     # Centralized configuration
└── 🧪 Testing
    └── test_subscription.py          # API testing and validation
```

### Key Technologies
- **Python 3.7+**: Core programming language
- **Tkinter**: GUI framework with modern styling
- **Requests**: HTTP API communication
- **Threading**: Asynchronous data loading
- **OpenWeatherMap APIs**: Weather data source

### API Endpoints Used
- **Current Weather**: `api.openweathermap.org/data/2.5/weather`
- **One Call API 3.0**: `api.openweathermap.org/data/3.0/onecall`
- **Historical**: `api.openweathermap.org/data/3.0/onecall/timemachine`
- **Geocoding**: `api.openweathermap.org/geo/1.0`
- **Air Pollution**: `api.openweathermap.org/data/2.5/air_pollution`
- **Weather Maps**: `tile.openweathermap.org/map`
- **Statistics**: `api.openweathermap.org/data/2.5/statistics`

## 📖 Usage Examples

### Basic Weather Query
```python
from enhanced_weather_api import EnhancedWeatherAPI

weather = EnhancedWeatherAPI()

# Get current weather
current = weather.get_current_weather("New York", "US")
print(f"Temperature: {current['main']['temp']}°C")

# Get coordinates
locations = weather.geocode_city("London")
lat, lon = locations[0]['lat'], locations[0]['lon']

# Get hourly forecast (4 days)
hourly = weather.get_hourly_forecast_4days(lat, lon)
print(f"Hours available: {len(hourly['hourly'])}")
```

### Air Quality Monitoring
```python
# Get current air quality
aqi = weather.get_air_pollution_current(lat, lon)
print(f"AQI: {aqi['list'][0]['main']['aqi']}/5")

# Get air quality forecast
forecast = weather.get_air_pollution_forecast(lat, lon)
print(f"Forecast points: {len(forecast['list'])}")
```

### Historical Analysis
```python
from datetime import datetime, timedelta

# Get weather from 30 days ago
past_date = datetime.now() - timedelta(days=30)
historical = weather.get_historical_weather(lat, lon, past_date)
print(f"Historical temperature: {historical['data'][0]['temp']}°C")
```

## 🔧 Configuration Options

### Environment Variables
```env
# Required
OPENWEATHER_API_KEY=your_student_pack_api_key

# Optional
OPENWEATHER_API_KEY_BACKUP=backup_key
DEFAULT_CITY=New York
TEMPERATURE_UNITS=metric  # metric, imperial, kelvin
```

### Student Pack Settings
The application automatically configures Student Pack features:
- Rate limits: 3,000/min, 100M/month
- Historical access: 50,000/day, 1 year archive
- All premium features enabled
- Educational use license

## 🎓 Educational Value

### Learning Objectives
- **API Integration**: RESTful API consumption and management
- **GUI Development**: Modern interface design with Tkinter
- **Data Visualization**: Weather data presentation
- **Error Handling**: Robust error management
- **Configuration Management**: Environment-based configuration
- **Threading**: Asynchronous programming
- **Data Processing**: JSON parsing and formatting

### Use Cases
- **Meteorology Students**: Real-world weather data analysis
- **Computer Science**: API programming and GUI development
- **Environmental Science**: Air quality and climate research
- **Geography**: Location-based data visualization
- **Data Science**: Statistical weather analysis

## 🛡️ Security Features

### API Key Protection
- Environment variable storage
- Key validation and testing
- Backup key support
- Secure error messaging

### Rate Limit Management
- Automatic rate limiting
- Fallback mechanisms
- Usage monitoring
- Error recovery

## 📄 Previous Project Files

This project also includes the original weather application files:

### Legacy Applications
- `weather_gui.py` - Original modern GUI with basic features
- `weather_api.py` - Basic weather API implementation
- Additional example files for learning progression

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

### Documentation
- [OpenWeatherMap API Docs](https://openweathermap.org/api)
- [Student Pack Information](https://openweathermap.org/price#student)

### Getting Help
- **Email**: support@openweathermap.org
- **Issues**: Use GitHub Issues for bug reports
- **Discussions**: Use GitHub Discussions for questions

## 🌟 Acknowledgments

- **OpenWeatherMap** for providing the Student Pack program
- **Python Community** for excellent libraries and frameworks
- **Educational Institutions** supporting weather research

---

**🎓 Built for Education • 🌍 Powered by OpenWeatherMap Student Pack • 💡 Open Source**
