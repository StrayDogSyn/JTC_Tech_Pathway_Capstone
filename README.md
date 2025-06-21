# 🌤️ Weather Dashboard - JTC Tech Pathway Capstone

A comprehensive weather monitoring application with machine learning predictions, advanced visualizations, and modern UI components.

## Features

- **Real-time Weather Data** with comprehensive metrics
- **5-Day Forecasts** with detailed 3-hour predictions  
- **Air Quality Monitoring** with AQI and pollutant data
- **Machine Learning Predictions** for temperature trends
- **Interactive Charts** and data visualizations
- **Multiple Themes** including dark mode and COBRA demo
- **Location Search** with advanced geocoding
- **Export Capabilities** for weather data and charts

## Architecture

### Project Structure

```text
src/
├── config/          # Configuration management
├── core/            # Business logic
├── models/          # Data models
├── services/        # API integrations  
├── ui/              # User interface
└── utils/           # ML predictions

Weather Dominator/   # COBRA demo files
tests/              # Test suite
```

### Design Principles

- Clean separation of concerns
- Type safety throughout
- Comprehensive error handling
- Modular and testable code

## Installation

### Prerequisites

- Python 3.8+
- OpenWeatherMap API key (free)

### Setup

1. **Clone and setup environment:**

```bash
git clone <repository-url>
cd JTC_Tech_Pathway_Capstone
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

1. **Configure API key:**

Create `.env` file:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

1. **Verify installation:**

```bash
python tests/test_complete_app.py
```

## Usage

### Quick Start

```bash
# Interactive launcher
python launcher.py

# Main application  
python complete_weather_dashboard.py

# COBRA demo
python "Weather Dominator/cobra_weather_app.py"
```

### Application Options

1. **Complete Weather Dashboard** - Full-featured main application
2. **COBRA Commander Demo** - Sci-fi themed styling showcase  
3. **Test Suite** - Verify dependencies and functionality

## Testing

Run the comprehensive test suite:

```bash
python tests/test_complete_app.py
```

Tests verify:

- Import dependencies
- API configuration
- Component functionality
- ML predictions
- COBRA styling

## Configuration

Configure through `.env` file or `settings.json`:

```json
{
    "default_city": "Your City, Country",
    "units": "metric", 
    "theme": "default",
    "auto_refresh": true
}
```

## Development

### Key Components

- **WeatherAPIService** - OpenWeatherMap integration
- **WeatherDashboardCore** - Business logic coordinator
- **WeatherPredictor** - Machine learning functionality
- **Configuration** - Settings and API key management

### Adding Features

1. Define data models in `src/models/`
2. Extend API services in `src/services/`
3. Add business logic to `src/core/`
4. Update tests in `tests/`

## Machine Learning

The application includes weather prediction capabilities:

- Temperature trend forecasting
- Humidity analysis
- Pressure change predictions
- Pattern recognition

Models use scikit-learn with dynamic training from forecast data.

## Troubleshooting

### Common Issues

**API Key Problems:**

```text
⚠️ Warning: No API key configured
```

Solution: Create `.env` file with your OpenWeatherMap API key

**Import Errors:**

```text
ModuleNotFoundError: No module named 'src'
```

Solution: Run from project root directory

**Missing Dependencies:**

```text
ModuleNotFoundError: No module named 'ttkbootstrap'
```

Solution: `pip install -r requirements.txt`

## Technology Stack

- **Python 3.8+** - Core language
- **tkinter/ttkbootstrap** - GUI framework
- **requests** - HTTP client
- **scikit-learn** - Machine learning
- **matplotlib** - Data visualization
- **python-dotenv** - Configuration

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- OpenWeatherMap for weather data API
- JTC Tech Pathway program
- Python community for excellent libraries

---

## Built for the JTC Tech Pathway Capstone Program

*Demonstrating modern Python development, clean architecture, and professional software engineering.*
