"""
Debug script to test API key and configuration loading
"""

import os
from dotenv import load_dotenv
import requests

# Load environment variables
load_dotenv()

# Check if .env file is loaded
print("🔍 Debugging API Configuration...")
print(f"📁 Current working directory: {os.getcwd()}")
print(f"📄 .env file exists: {os.path.exists('.env')}")

# Check environment variables
api_key = os.getenv('OPENWEATHER_API_KEY')
print(f"🔑 API Key loaded: {'✅ Yes' if api_key else '❌ No'}")
if api_key:
    print(f"🔑 API Key (first 8 chars): {api_key[:8]}...")
    print(f"🔑 API Key length: {len(api_key)}")

# Test API key with a simple request
if api_key:
    print("\n🌐 Testing API key with OpenWeatherMap...")
    test_url = f"https://api.openweathermap.org/data/2.5/weather?q=London&appid={api_key}&units=metric"
    
    try:
        response = requests.get(test_url)
        print(f"📡 Response status: {response.status_code}")
        if response.status_code == 200:
            print("✅ API key is working!")
            data = response.json()
            print(f"🏙️  Test city: {data['name']}")
            print(f"🌡️  Temperature: {data['main']['temp']}°C")
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"🔍 Response: {response.text}")
    except Exception as e:
        print(f"❌ Request failed: {e}")
else:
    print("❌ Cannot test API - no key found")
