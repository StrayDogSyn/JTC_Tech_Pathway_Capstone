# JTC_Tech_Pathway_Capstone

My project pages for my Justice Through Code ⚖ Capstone Project

## OpenWeatherMap Developer API Integration

This project includes integration with the OpenWeatherMap Developer API subscription to fetch real-time weather data with premium features and enhanced reliability.

### 🔑 API Subscription Requirements

#### OpenWeatherMap Developer Plan Required

- **Plan**: Developer subscription ($40/month)
- **API Calls**: 60 calls/minute, 1,000,000 calls/month
- **Endpoint**: Premium endpoint (pro.openweathermap.org)
- **Features**: Current weather, 5-day forecast, weather maps, alerts
- **Support**: Email support included

#### Get Your API Key

1. Visit [OpenWeatherMap Pricing](https://openweathermap.org/price)
2. Subscribe to the Developer plan
3. Access your API key from your account dashboard
4. Use the premium endpoint: `https://pro.openweathermap.org/data/2.5`

### Setup Instructions

1. **Subscribe to Developer API**

   - Visit [OpenWeatherMap](https://openweathermap.org/price)
   - Subscribe to the Developer plan ($40/month)
   - Get your API key from the dashboard

2. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   - Copy `.env.example` to `.env`
   - Replace `your_api_key_here` with your actual OpenWeatherMap API key

   ```bash
   cp .env.example .env
   ```

4. **Update your `.env` file**

   ```env
   OPENWEATHER_API_KEY=your_actual_api_key_here
   DEFAULT_CITY=New York
   TEMPERATURE_UNITS=metric
   ```

### Usage

#### 🖥️ GUI Application (Recommended)

Run the modern weather dashboard with a beautiful graphical interface:

```bash
python weather_gui.py
```

**Features:**

- 🎨 **Modern dark theme** with gradient effects and smooth animations
- 📱 **Fully responsive design** - adapts to any window size (400x300 minimum)
- 📜 **Scrollable content** - all elements accessible regardless of viewport size
- � **Dynamic font scaling** - text sizes adjust automatically to window size
- ⚡ **Real-time updates** with threaded API calls (non-blocking UI)
- 🕒 **Live clock display** with formatted date/time
- 🌡️ **Complete weather data** - temperature, humidity, wind, pressure, visibility
- 🔍 **Instant search** with Enter key support and loading states
- 🖱️ **Mouse wheel scrolling** for easy navigation
- ⚠️ **Robust error handling** with user-friendly messages

#### 💻 Command Line Interface

```python
from weather_api import WeatherAPI

# Initialize the API
weather = WeatherAPI()

# Get current weather for a city
weather_data = weather.get_current_weather("New York")
formatted_data = weather.format_weather_data(weather_data)

print(f"Temperature in {formatted_data['city']}: {formatted_data['temperature']}°")
```

#### 🧪 Test Subscription Status

Verify your Developer API subscription is properly configured:

```bash
python test_subscription.py
```

This will validate:

- API key configuration
- Subscription plan details
- Rate limits and endpoints
- Feature availability

#### Weather by Coordinates

```python
# Get weather by latitude and longitude
weather_data = weather.get_weather_by_coordinates(40.7128, -74.0060)  # NYC coordinates
```

#### Run the Example

```bash
python weather_api.py
```

### API Features

#### ✅ Available Features (Developer Subscription)

- ✅ **Current weather by city name** - Real-time weather data
- ✅ **Current weather by coordinates** - Lat/lon support
- ✅ **5-day weather forecast** - Extended forecast data
- ✅ **Weather maps** - Visual weather overlays
- ✅ **Weather alerts** - Severe weather notifications
- ✅ **Premium API endpoints** - Enhanced reliability (pro.openweathermap.org)
- ✅ **Multiple temperature units** - Metric, imperial, kelvin support
- ✅ **Modern GUI Application** - Beautiful tkinter interface with dark theme
- ✅ **Real-time updates** - Live weather data with animations
- ✅ **Responsive design** - Scales beautifully with window resizing
- ✅ **Comprehensive error handling** - User-friendly error messages
- ✅ **Secure configuration** - Environment variable API key management

#### ❌ Not Available (Developer Subscription)

- ❌ **History API** - Historical weather data (requires higher plan)
- ❌ **Statistics API** - Weather statistics (requires higher plan)
- ❌ **Solar Radiation API** - Solar irradiance data (requires higher plan)
- ❌ **Road Risk API** - Weather-based road conditions (requires higher plan)

#### 📞 Support & Documentation

- **Technical Support**: [support@openweathermap.org](mailto:support@openweathermap.org) (Developer plan includes email support)
- **API Documentation**: [https://openweathermap.org/api](https://openweathermap.org/api)
- **Subscription Management**: [https://openweathermap.org/price#commonquestions](https://openweathermap.org/price#commonquestions)
- **Rate Limits**: 60 calls/minute, 1,000,000 calls/month

### File Structure

```text
├── .env                  # Your API keys (not in git)
├── .env.example          # Environment variables template
├── .gitignore           # Git ignore rules
├── assets/              # Project assets (empty, ready for use)
├── config.py            # Configuration management with subscription details
├── weather_api.py       # Core OpenWeatherMap API implementation
├── weather_gui.py       # Modern tkinter GUI application
├── test_subscription.py # Test script for subscription validation
├── requirements.txt     # Python dependencies
├── SECURITY.md          # Security guidelines and best practices
├── LICENSE              # Project license (The Unlicense)
└── README.md           # Complete documentation
```

### 🔒 Security

This project implements comprehensive security measures for API key protection:

- **Environment Variables**: API keys stored securely in `.env` file
- **Git Protection**: `.env` file excluded from version control
- **Key Masking**: API keys masked in logs and error messages
- **Secure Configuration**: Uses `os.getenv()` for environment variable access
- **Security Documentation**: See [SECURITY.md](./SECURITY.md) for detailed guidelines

⚠️ **Important**: Never commit real API keys to version control. Always use the `.env.example` template.

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | Your OpenWeatherMap API key | Required |
| `DEFAULT_CITY` | Default city for weather queries | "New York" |
| `TEMPERATURE_UNITS` | Temperature units (metric/imperial/kelvin) | "metric" |
