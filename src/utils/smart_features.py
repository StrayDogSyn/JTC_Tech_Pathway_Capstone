"""
Smart weather features: predictions, trend detection, and activity suggestions.

This module implements AI-like features for weather analysis and recommendations.
"""

import random
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass

from ..utils.logging import get_logger
from ..utils.data_storage import storage

logger = get_logger()


@dataclass
class WeatherPrediction:
    """Data class for weather predictions."""
    predicted_temp: float
    confidence: float
    reasoning: str
    prediction_date: datetime
    actual_temp: Optional[float] = None
    accuracy: Optional[float] = None


@dataclass
class TrendAnalysis:
    """Data class for trend analysis results."""
    direction: str  # "rising", "falling", "stable"
    strength: str   # "weak", "moderate", "strong"
    change_rate: float
    confidence: float
    strength_multiplier: float = 1.0


class WeatherPredictor:
    """Simple weather prediction engine."""
    
    def __init__(self):
        """Initialize the predictor."""
        self.predictions_history = []
        
    def predict_tomorrow_temperature(self, current_temp: float, city: str) -> WeatherPrediction:
        """Predict tomorrow's temperature based on recent trends."""
        # Get recent weather history
        history = storage.get_weather_history(7)
        
        if len(history) < 2:
            # Not enough data for trend analysis
            predicted_temp = current_temp + random.uniform(-3, 3)
            confidence = 0.4
            reasoning = "Limited historical data - using baseline prediction"
        else:
            # Analyze recent temperature trend
            recent_temps = [record['temperature'] for record in history[:5]]
            trend_analysis = self._analyze_temperature_trend(recent_temps)
            
            # Simple prediction logic based on trend
            if trend_analysis.direction == "rising":
                temp_change = random.uniform(1, 4) * trend_analysis.strength_multiplier
                predicted_temp = current_temp + temp_change
                confidence = min(0.8, 0.5 + trend_analysis.confidence * 0.3)
                reasoning = f"Rising temperature trend detected (strength: {trend_analysis.strength})"
            elif trend_analysis.direction == "falling":
                temp_change = random.uniform(1, 4) * trend_analysis.strength_multiplier
                predicted_temp = current_temp - temp_change
                confidence = min(0.8, 0.5 + trend_analysis.confidence * 0.3)
                reasoning = f"Falling temperature trend detected (strength: {trend_analysis.strength})"
            else:
                # Stable trend
                predicted_temp = current_temp + random.uniform(-2, 2)
                confidence = 0.6
                reasoning = "Stable temperature pattern - expecting minor variation"
        
        # Add seasonal and random factors
        predicted_temp = self._apply_seasonal_adjustment(predicted_temp)
        predicted_temp = round(predicted_temp, 1)
        confidence = round(confidence, 2)
        
        prediction = WeatherPrediction(
            predicted_temp=predicted_temp,
            confidence=confidence,
            reasoning=reasoning,
            prediction_date=datetime.now() + timedelta(days=1)
        )
        
        # Save prediction for accuracy tracking
        prediction_data = {
            'city': city,
            'predicted_temp': predicted_temp,
            'confidence': confidence,
            'reasoning': reasoning,
            'prediction_for_date': (datetime.now() + timedelta(days=1)).isoformat(),
            'current_temp': current_temp
        }
        storage.save_prediction(prediction_data)
        
        logger.info(f"Temperature prediction for {city}: {predicted_temp}°C (confidence: {confidence})")
        return prediction
    
    def _analyze_temperature_trend(self, temperatures: List[float]) -> TrendAnalysis:
        """Analyze temperature trend from recent data."""
        if len(temperatures) < 2:
            return TrendAnalysis("stable", "weak", 0.0, 0.0)
        
        # Calculate trend using simple linear regression approach
        changes = []
        for i in range(1, len(temperatures)):
            changes.append(temperatures[i-1] - temperatures[i])  # Recent first
        
        avg_change = sum(changes) / len(changes)
        
        # Determine trend direction
        if avg_change > 1:
            direction = "rising"
        elif avg_change < -1:
            direction = "falling"
        else:
            direction = "stable"
        
        # Determine trend strength
        abs_change = abs(avg_change)
        if abs_change > 3:
            strength = "strong"
            strength_multiplier = 1.0
        elif abs_change > 1.5:
            strength = "moderate"
            strength_multiplier = 0.7
        else:
            strength = "weak"
            strength_multiplier = 0.4
        
        # Calculate confidence based on consistency
        consistency = self._calculate_trend_consistency(changes)
        
        analysis = TrendAnalysis(
            direction=direction,
            strength=strength,
            change_rate=avg_change,
            confidence=consistency,
            strength_multiplier=strength_multiplier
        )
        
        return analysis
    
    def _calculate_trend_consistency(self, changes: List[float]) -> float:
        """Calculate how consistent the trend is."""
        if not changes:
            return 0.0
        
        # Check if most changes are in the same direction
        positive_changes = sum(1 for x in changes if x > 0)
        negative_changes = sum(1 for x in changes if x < 0)
        total_changes = len(changes)
        
        consistency = max(positive_changes, negative_changes) / total_changes
        return consistency
    
    def _apply_seasonal_adjustment(self, temp: float) -> float:
        """Apply simple seasonal adjustment."""
        current_month = datetime.now().month
        
        # Simple seasonal factors (Northern Hemisphere)
        if current_month in [12, 1, 2]:  # Winter
            temp += random.uniform(-1, 0.5)
        elif current_month in [6, 7, 8]:  # Summer
            temp += random.uniform(-0.5, 1)
        elif current_month in [3, 4, 5]:  # Spring
            temp += random.uniform(0, 1.5)
        else:  # Fall
            temp += random.uniform(-1.5, 0)
        
        return temp
    
    def calculate_prediction_accuracy(self) -> Dict[str, float]:
        """Calculate accuracy of past predictions."""
        predictions = storage.load_predictions()
        
        if not predictions:
            return {'accuracy': 0.0, 'total_predictions': 0}
        
        # For demo purposes, simulate accuracy checking
        # In a real app, you'd compare with actual weather data
        total_predictions = len(predictions)
        accurate_predictions = 0
        
        for prediction in predictions:
            # Simulate accuracy based on confidence
            confidence = prediction.get('confidence', 0.5)
            if random.random() < confidence:
                accurate_predictions += 1
        
        accuracy = accurate_predictions / total_predictions if total_predictions > 0 else 0.0
        
        return {
            'accuracy': round(accuracy * 100, 1),
            'total_predictions': total_predictions,
            'accurate_predictions': accurate_predictions
        }


class TrendDetector:
    """Detects weather trends and patterns."""
    
    def detect_temperature_trends(self, days: int = 7) -> Dict[str, Any]:
        """Detect temperature trends over specified period."""
        history = storage.get_weather_history(days)
        
        if len(history) < 3:
            return {
                'trend': 'insufficient_data',
                'direction': 'unknown',
                'strength': 'unknown',
                'arrow': '→',
                'description': 'Need more data for trend analysis'
            }
        
        temperatures = [record['temperature'] for record in reversed(history)]  # Chronological order
        
        # Calculate trend
        predictor = WeatherPredictor()
        trend_analysis = predictor._analyze_temperature_trend(list(reversed(temperatures)))
        
        # Map to display arrows
        arrow_map = {
            'rising': '↗️',
            'falling': '↘️',
            'stable': '→'
        }
        
        # Generate description
        descriptions = {
            ('rising', 'strong'): 'Significant warming trend detected',
            ('rising', 'moderate'): 'Moderate warming trend',
            ('rising', 'weak'): 'Slight warming tendency',
            ('falling', 'strong'): 'Significant cooling trend detected',
            ('falling', 'moderate'): 'Moderate cooling trend',
            ('falling', 'weak'): 'Slight cooling tendency',
            ('stable', 'weak'): 'Stable temperature pattern',
            ('stable', 'moderate'): 'Consistent temperature range',
            ('stable', 'strong'): 'Very stable conditions'
        }
        
        description = descriptions.get((trend_analysis.direction, trend_analysis.strength), 'Mixed pattern')
        
        return {
            'trend': trend_analysis.direction,
            'direction': trend_analysis.direction,
            'strength': trend_analysis.strength,
            'change_rate': round(trend_analysis.change_rate, 1),
            'confidence': round(trend_analysis.confidence * 100, 1),
            'arrow': arrow_map.get(trend_analysis.direction, '→'),
            'description': description
        }
    
    def detect_weather_patterns(self) -> Dict[str, Any]:
        """Detect patterns in weather conditions."""
        history = storage.get_weather_history(14)
        
        if not history:
            return {'patterns': [], 'insights': ['Need more weather data for pattern analysis']}
        
        # Analyze weather description patterns
        descriptions = [record['description'].lower() for record in history]
        
        patterns = []
        insights = []
        
        # Check for consecutive similar weather
        consecutive_count = 1
        current_weather = descriptions[0] if descriptions else ""
        
        for i in range(1, len(descriptions)):
            if descriptions[i] == current_weather:
                consecutive_count += 1
            else:
                if consecutive_count >= 3:
                    patterns.append({
                        'type': 'consecutive_weather',
                        'description': f"{consecutive_count} consecutive days of {current_weather}",
                        'strength': 'notable' if consecutive_count >= 5 else 'moderate'
                    })
                consecutive_count = 1
                current_weather = descriptions[i]
        
        # Check final sequence
        if consecutive_count >= 3:
            patterns.append({
                'type': 'consecutive_weather',
                'description': f"{consecutive_count} consecutive days of {current_weather}",
                'strength': 'notable' if consecutive_count >= 5 else 'moderate'
            })
        
        # Generate insights
        if patterns:
            insights.append(f"Detected {len(patterns)} weather patterns in the last 2 weeks")
        else:
            insights.append("Variable weather conditions - no strong patterns detected")
        
        return {
            'patterns': patterns,
            'insights': insights
        }
    
    def analyze_temperature_trend(self) -> Optional[TrendAnalysis]:
        """Analyze temperature trend and return TrendAnalysis object."""
        history = storage.get_weather_history(7)
        
        if len(history) < 3:
            return None
        
        temperatures = [record['temperature'] for record in reversed(history)]  # Chronological order
        
        # Calculate linear regression for trend
        days = list(range(len(temperatures)))
        
        # Simple linear regression
        n = len(temperatures)
        sum_x = sum(days)
        sum_y = sum(temperatures)
        sum_xy = sum(x * y for x, y in zip(days, temperatures))
        sum_x2 = sum(x ** 2 for x in days)
        
        # Calculate slope (change rate per day)
        if n * sum_x2 - sum_x ** 2 != 0:
            slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x2 - sum_x ** 2)
        else:
            slope = 0
        
        # Determine direction
        if abs(slope) < 0.5:
            direction = "stable"
        elif slope > 0:
            direction = "rising"
        else:
            direction = "falling"
        
        # Determine strength based on absolute slope
        abs_slope = abs(slope)
        if abs_slope < 0.5:
            strength = "weak"
        elif abs_slope < 1.5:
            strength = "moderate"
        else:
            strength = "strong"
        
        # Calculate confidence based on data consistency
        variance = sum((temp - sum_y/n) ** 2 for temp in temperatures) / n
        confidence = max(0.3, min(0.9, 1.0 - (variance / 100)))  # Normalize variance to confidence
        
        return TrendAnalysis(
            direction=direction,
            strength=strength,
            change_rate=slope,
            confidence=confidence
        )


class ActivitySuggester:
    """Suggests activities based on weather conditions."""
    
    def __init__(self):
        """Initialize with activity databases."""
        self.activities = {
            'sunny': [
                'Go for a picnic in the park',
                'Take a nature photography walk',
                'Have a barbecue outdoors',
                'Visit a botanical garden',
                'Go hiking or cycling',
                'Play outdoor sports',
                'Wash your car',
                'Read a book outside'
            ],
            'cloudy': [
                'Visit a museum or art gallery',
                'Go shopping at outdoor markets',
                'Take a scenic drive',
                'Do some gardening',
                'Have coffee at an outdoor café',
                'Go for a leisurely walk'
            ],
            'rainy': [
                'Watch a movie marathon',
                'Try a new recipe in the kitchen',
                'Read that book you\'ve been meaning to start',
                'Organize and declutter your space',
                'Do indoor yoga or meditation',
                'Play board games or puzzles',
                'Learn something new online',
                'Have a cozy tea time'
            ],
            'snowy': [
                'Build a snowman',
                'Go skiing or snowboarding',
                'Make hot chocolate and watch the snow',
                'Take winter photography',
                'Have a warm soup meal',
                'Do indoor crafts',
                'Plan your next vacation'
            ],
            'stormy': [
                'Stay indoors and be safe',
                'Watch nature documentaries',
                'Practice mindfulness or meditation',
                'Do some indoor exercises',
                'Organize your digital photos',
                'Write in a journal',
                'Learn a new skill online'
            ]
        }
        
        self.temperature_activities = {
            'hot': [  # >25°C
                'Go swimming',
                'Enjoy ice cream or cold drinks',
                'Find shade and relax',
                'Have a water balloon fight',
                'Visit an air-conditioned mall',
                'Do early morning or evening activities'
            ],
            'warm': [  # 15-25°C
                'Perfect weather for any outdoor activity!',
                'Go for a bike ride',
                'Have a picnic',
                'Play outdoor sports',
                'Do some gardening'
            ],
            'cool': [  # 5-15°C
                'Take a brisk walk',
                'Go jogging',
                'Visit a cozy café',
                'Do some light outdoor work',
                'Layer up and enjoy the fresh air'
            ],
            'cold': [  # <5°C
                'Bundle up for a winter walk',
                'Enjoy hot beverages',
                'Do indoor activities',
                'Have a warm meal',
                'Stay cozy indoors'
            ]
        }
    
    def get_activity_suggestions(self, weather_desc: str, temperature: float, 
                               custom_activities: Optional[List[str]] = None) -> List[str]:
        """Get activity suggestions based on weather conditions."""
        suggestions = []
        
        # Weather-based suggestions
        weather_lower = weather_desc.lower()
        if 'sun' in weather_lower or 'clear' in weather_lower:
            suggestions.extend(random.sample(self.activities['sunny'], 3))
        elif 'rain' in weather_lower or 'drizzle' in weather_lower:
            suggestions.extend(random.sample(self.activities['rainy'], 3))
        elif 'snow' in weather_lower:
            suggestions.extend(random.sample(self.activities['snowy'], 3))
        elif 'storm' in weather_lower or 'thunder' in weather_lower:
            suggestions.extend(random.sample(self.activities['stormy'], 2))
        elif 'cloud' in weather_lower:
            suggestions.extend(random.sample(self.activities['cloudy'], 3))
        else:
            suggestions.extend(random.sample(self.activities['cloudy'], 2))
        
        # Temperature-based suggestions
        if temperature > 25:
            suggestions.extend(random.sample(self.temperature_activities['hot'], 2))
        elif temperature > 15:
            suggestions.extend(random.sample(self.temperature_activities['warm'], 2))
        elif temperature > 5:
            suggestions.extend(random.sample(self.temperature_activities['cool'], 2))
        else:
            suggestions.extend(random.sample(self.temperature_activities['cold'], 2))
        
        # Add custom activities if provided
        if custom_activities:
            suggestions.extend(random.sample(custom_activities, min(2, len(custom_activities))))
        
        # Remove duplicates and limit to 5-7 suggestions
        unique_suggestions = list(dict.fromkeys(suggestions))
        return unique_suggestions[:7]
    
    def get_custom_activity_lists(self) -> Dict[str, List[str]]:
        """Get predefined custom activity lists for different interests."""
        return {
            'fitness': [
                'Go for a run', 'Do outdoor yoga', 'Bike to work',
                'Try a new hiking trail', 'Do bodyweight exercises outside',
                'Play frisbee or catch'
            ],
            'creative': [
                'Sketch the landscape', 'Take artistic photos',
                'Write poetry inspired by weather', 'Do plein air painting',
                'Create weather-themed crafts', 'Design a garden layout'
            ],
            'social': [
                'Meet friends for coffee', 'Have a group picnic',
                'Organize outdoor games', 'Visit local events',
                'Host a weather-watching party', 'Go to a farmer\'s market'
            ],
            'learning': [
                'Study cloud formations', 'Learn about local weather patterns',
                'Research climate science', 'Practice weather photography',
                'Study seasonal changes', 'Learn about meteorology'
            ]
        }
    
    def get_activity_suggestions_from_dict(self, weather_data: Dict[str, Any]) -> List[str]:
        """Get activity suggestions from weather data dictionary."""
        weather_desc = weather_data.get('description', 'clear')
        temperature = weather_data.get('temperature', 20)
        return self.get_activity_suggestions(weather_desc, temperature)


# Global instances
weather_predictor = WeatherPredictor()
trend_detector = TrendDetector()
activity_suggester = ActivitySuggester()
