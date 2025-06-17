# JTC_Tech_Pathway_Capstone

My project pages for my Justice Through Code ⚖ Capstone Project

## OpenWeatherMap API Integration

This project includes integration with the OpenWeatherMap Current Weather API to fetch real-time weather data.

### Setup Instructions

1. **Get an API Key**
   - Visit [OpenWeatherMap](https://openweathermap.org/api)
   - Sign up for a free account
   - Generate an API key

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

#### Basic Weather Query

```python
from weather_api import WeatherAPI

# Initialize the API
weather = WeatherAPI()

# Get current weather for a city
weather_data = weather.get_current_weather("New York")
formatted_data = weather.format_weather_data(weather_data)

print(f"Temperature in {formatted_data['city']}: {formatted_data['temperature']}°")
```

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

- ✅ Current weather by city name
- ✅ Current weather by coordinates (lat/lon)
- ✅ Support for different temperature units (metric, imperial, kelvin)
- ✅ Formatted, readable weather data output
- ✅ Proper error handling for invalid cities/API keys
- ✅ Environment variable configuration

### File Structure

```text
├── .env.example          # Environment variables template
├── config.py            # Configuration management
├── weather_api.py       # Main weather API implementation
├── requirements.txt     # Python dependencies
└── README.md           # This file
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENWEATHER_API_KEY` | Your OpenWeatherMap API key | Required |
| `DEFAULT_CITY` | Default city for weather queries | "New York" |
| `TEMPERATURE_UNITS` | Temperature units (metric/imperial/kelvin) | "metric" |
