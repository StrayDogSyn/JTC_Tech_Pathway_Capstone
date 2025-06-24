# Contributing to Advanced Weather Intelligence Platform

Thank you for your interest in contributing to this project! This document provides guidelines for contributing to the Advanced Weather Intelligence Platform.

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git
- OpenWeatherMap API key (free at <https://openweathermap.org/api>)

### Initial Setup

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd JTC_Tech_Pathway_Capstone
   ```

2. **Set up Python virtual environment:**

   ```bash
   python -m venv .venv
   
   # On Windows:
   .venv\Scripts\activate
   
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment:**

   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your OpenWeatherMap API key
   OPENWEATHER_API_KEY=your_actual_api_key_here
   ```

5. **Run the application:**

   ```bash
   python launcher.py
   ```

## 🏗️ Project Structure

```text
src/
├── config/          # Configuration management
├── core/           # Business logic and core functionality
├── interfaces/     # Interface definitions and contracts
├── models/         # Data models and structures
├── services/       # External service integrations
├── ui/            # User interface components
└── utils/         # Utility functions and helpers

tests/             # Test files
```

## 🔧 Development Workflow

### Branch Naming Convention

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `hotfix/description` - Critical fixes
- `docs/description` - Documentation updates

### Commit Message Format

Use conventional commit format:

```text
type(scope): description

Examples:
feat(ui): add new weather chart component
fix(api): resolve rate limiting issue
docs(readme): update installation instructions
test(core): add unit tests for weather calculations
```

### Pull Request Process

1. Create a feature branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Update documentation if needed
5. Ensure all tests pass
6. Submit a pull request with a clear description

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m pytest

# Run specific test file
python -m pytest tests/test_weather_dashboard.py

# Run with coverage
python -m pytest --cov=src tests/
```

### Writing Tests

- Place test files in the `tests/` directory
- Use descriptive test names
- Follow the Arrange-Act-Assert pattern
- Mock external dependencies

## 📝 Code Style

### Python Style Guidelines

- Follow PEP 8
- Use type hints
- Write docstrings for classes and functions
- Keep functions small and focused
- Use meaningful variable names

### Example

```python
def calculate_wind_chill(temperature: float, wind_speed: float) -> float:
    """
    Calculate wind chill temperature.
    
    Args:
        temperature: Temperature in Celsius
        wind_speed: Wind speed in km/h
        
    Returns:
        Wind chill temperature in Celsius
    """
    # Implementation here
    pass
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Clear description** of the issue
2. **Steps to reproduce** the bug
3. **Expected behavior**
4. **Actual behavior**
5. **Environment details** (OS, Python version, etc.)
6. **Screenshots** if applicable

## 💡 Feature Requests

For new features:

1. Check if the feature already exists
2. Describe the use case
3. Explain the expected behavior
4. Consider implementation complexity

## 📚 Documentation

- Update README.md for user-facing changes
- Update ARCHITECTURE.md for structural changes
- Add inline comments for complex logic
- Keep documentation up to date

## 🔐 Security

- Never commit API keys or secrets
- Use environment variables for configuration
- Follow security best practices
- Report security issues privately

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project.

## 🤝 Code of Conduct

- Be respectful and professional
- Welcome newcomers and help them learn
- Focus on constructive feedback
- Celebrate successes and learn from failures

## 📞 Getting Help

- Check existing issues and documentation
- Ask questions in discussions
- Reach out to maintainers for guidance

---

Thank you for contributing to make this project better! 🌟
