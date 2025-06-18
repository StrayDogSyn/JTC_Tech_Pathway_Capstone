# 🌤️ OpenWeatherMap Free Tier - Weather Dashboard

> **Justice Through Code ⚖ Capstone Project**

A modern weather application showcasing OpenWeatherMap's free tier capabilities
with a clean, efficient design.

## 🌟 Features

- **Real-time Weather Data** - Current conditions with comprehensive metrics
- **5-Day Weather Forecast** - 3-hour interval forecasts for 5 days
- **Air Quality Monitoring** - Real-time pollution data and health recommendations
- **Interactive Weather Maps** - Multiple weather layer visualizations
- **Advanced Geocoding** - Location search and coordinate conversion
- **Modern GUI** - Dark-themed, responsive interface with tabbed layout

## 🚀 Quick Start

### Prerequisites

- Python 3.7 or higher
- OpenWeatherMap API key (free tier)

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
     OPENWEATHER_API_KEY_BACKUP=your_backup_key_here
     ```

5. **Run the application:**

   ```bash
   python unified_weather_dashboard.py
   ```

## 📋 Project Structure

```text
JTC_Tech_Pathway_Capstone/
├── unified_weather_dashboard.py    # 🎯 Main application
├── test_unified_app.py            # Test suite
├── requirements.txt               # Dependencies
├── .env                          # Configuration (create this)
├── .env.example                  # Configuration template
├── README.md                     # This file
├── LICENSE                       # License information
└── SECURITY.md                   # Security guidelines
```

## 🧪 Testing

Validate that everything is working correctly:

```bash
python test_unified_app.py
```

The test suite validates:

- ✅ Required dependencies
- ✅ API key configuration  
- ✅ Application components
- ✅ Data classes and methods

## 🎯 Usage Guide

### Launch the Application

Run the unified dashboard to access all features in one interface:

```bash
python unified_weather_dashboard.py
```

### Main Features

#### Current Weather Tab

- Real-time weather conditions
- Temperature, humidity, pressure, wind data
- UV index, visibility, and sunrise/sunset times

#### Forecast Tab

- 5-day/3-hour detailed forecast
- Temperature trends and precipitation probability
- Weather conditions and cloud coverage

#### Air Quality Tab

- Real-time pollution monitoring
- Detailed pollutant breakdown (PM2.5, PM10, CO, NO2, SO2, O3, NH3)
- Health recommendations based on AQI

#### Weather Maps Tab

- Interactive weather visualization
- Multiple map layer types (temperature, precipitation, pressure, wind, clouds)
- Real-time weather patterns

#### Historical Data Tab

- ⚠️ Note: Historical data requires a paid subscription
- Shows upgrade information for One Call API 3.0

#### Analytics Tab

- Weather data visualization
- Forecast analysis and trends
- Statistical summaries

#### API Info Tab

- Subscription details and limits
- API usage monitoring
- Technical documentation

## 🔧 Configuration

### Environment Variables

Configure in your `.env` file:

```env
# Primary API key (required)
OPENWEATHER_API_KEY=your_primary_api_key

# Backup API key (optional, for redundancy)  
OPENWEATHER_API_KEY_BACKUP=your_backup_api_key
```

### Free Tier Benefits

- **Rate Limits**: 60 calls/minute, 1,000,000 calls/month
- **Current Weather**: Real-time weather data for any location
- **5-Day Forecast**: Weather predictions with 3-hour intervals
- **Air Quality**: Pollution monitoring and health recommendations
- **Weather Maps**: Visual weather data overlays
- **Geocoding**: Location search and coordinate conversion

### Paid Features (Not Available)

- ❌ **Historical Data**: Requires One Call API 3.0 subscription
- ❌ **16-Day Forecast**: Extended forecasts require paid plan
- ❌ **Hourly Forecast**: 48+ hour hourly data requires paid plan

## 📚 API Endpoints

The application utilizes these free tier endpoints:

- **Current Weather**: `/data/2.5/weather`
- **5-Day Forecast**: `/data/2.5/forecast`
- **Air Pollution**: `/data/2.5/air_pollution`
- **Geocoding**: `/geo/1.0/direct`
- **Weather Maps**: `/map/{layer}/{z}/{x}/{y}.png`

## 🛠️ Dependencies

- **requests** (>=2.28.0) - HTTP library for API calls
- **python-dotenv** (>=1.0.0) - Environment variable management
- **tkinter** - GUI framework (included with Python)

## 🔍 Troubleshooting

### Common Issues

#### "API key not found" error

- Ensure your `.env` file exists in the project root
- Verify your API key is correct and active
- Check the variable name is `OPENWEATHER_API_KEY`

#### "401 Unauthorized" error

- Verify your API key is valid and active
- Check if you're trying to access paid features (like historical data)
- Ensure you haven't exceeded rate limits

#### "Location not found" error

- Try different location formats (city name, coordinates)
- Use more specific location names
- Check spelling and verify the location exists

#### Network connectivity issues

- Check your internet connection
- Verify firewall settings allow API requests
- Try using the backup API key if configured

### Getting Help

If you encounter issues:

1. Run the test suite: `python test_unified_app.py`
2. Check console output for detailed error messages
3. Verify your API key and internet connection
4. Ensure all dependencies are installed correctly

## 📈 Upgrade Options

To access additional features like historical data and extended forecasts:

- **One Call API 3.0**: $3/month for extended forecasts and historical data
- **Professional Plan**: $40/month for advanced features and higher limits
- **Enterprise Plan**: Custom pricing for high-volume usage

Visit [OpenWeatherMap Pricing](https://openweathermap.org/price) for more details.

## 📄 License

This project is for educational use only. Please ensure you comply with
OpenWeatherMap's terms of service and API usage guidelines.

## 🙏 Acknowledgments

- **OpenWeatherMap** - For providing the comprehensive weather API
- **Justice Through Code** - For supporting this capstone project
- **Python Community** - For excellent libraries and frameworks

---

🎓 A Justice Through Code Capstone Project showcasing modern weather data integration
