"""
Weather and AQI-based disease prediction (Rule-based)
Integrates with external APIs to forecast disease spikes
"""

import requests
from datetime import datetime, timedelta
from django.core.cache import cache
from django.conf import settings

# Disease to Weather/AQI mapping (based on medical research)
WEATHER_DISEASE_MAP = {
    'high_aqi': {
        'threshold': 150,  # AQI > 150 (Unhealthy)
        'diseases': ['Respiratory Infection', 'Asthma', 'COPD'],
        'severity': 'High',
        'medicine_multiplier': 1.5
    },
    'moderate_aqi': {
        'threshold': 100,  # AQI > 100 (Unhealthy for sensitive groups)
        'diseases': ['Respiratory Infection', 'Asthma'],
        'severity': 'Moderate',
        'medicine_multiplier': 1.2
    },
    'cold_weather': {
        'threshold': 15,  # Temp < 15°C
        'diseases': ['Fever/Viral', 'Respiratory Infection', 'Pneumonia'],
        'severity': 'Moderate',
        'medicine_multiplier': 1.3
    },
    'hot_weather': {
        'threshold': 35,  # Temp > 35°C
        'diseases': ['Heat Stroke', 'Dehydration', 'Gastric/Ulcer'],
        'severity': 'Moderate',
        'medicine_multiplier': 1.4
    },
    'high_humidity': {
        'threshold': 80,  # Humidity > 80%
        'diseases': ['Dengue', 'Malaria', 'Infection/Bacterial'],
        'severity': 'Low',
        'medicine_multiplier': 1.25
    },
    'monsoon': {
        'keywords': ['rain', 'drizzle', 'thunderstorm'],
        'diseases': ['Dengue', 'Malaria', 'Infection/Bacterial', 'Fever/Viral'],
        'severity': 'Moderate',
        'medicine_multiplier': 1.35
    }
}

class WeatherAQIPredictor:
    """
    Predicts disease spikes based on weather and AQI conditions.
    Uses external APIs to get real-time environmental data.
    """
    
    def __init__(self, hospital_location=None):
        """
        Initialize predictor with hospital location.
        
        Args:
            hospital_location: dict with 'lat', 'lon', 'city'
        """
        if hospital_location is None:
            # Default hospital location (Delhi)
            self.location = {
                'lat': 28.6139,
                'lon': 77.2090,
                'city': 'Delhi'
            }
        else:
            self.location = hospital_location
    
    def get_weather_data(self):
        """
        Fetch weather data from OpenWeatherMap API.
        
        Returns:
            dict: Weather information including temperature, humidity, description
        """
        # Check cache first
        cache_key = f"weather_{self.location['city']}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        try:
            # Get API key from settings (with fallback)
            api_key = getattr(settings, 'OPENWEATHER_API_KEY', 'demo')
            
            # If no API key, return mock data
            if api_key == 'demo':
                return self._get_mock_weather()
            
            url = (
                f"http://api.openweathermap.org/data/2.5/weather?"
                f"lat={self.location['lat']}&lon={self.location['lon']}"
                f"&appid={api_key}&units=metric"
            )
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            weather = {
                'temperature': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'humidity': data['main']['humidity'],
                'description': data['weather'][0]['description'],
                'main': data['weather'][0]['main'],
                'pressure': data['main']['pressure'],
                'wind_speed': data['wind']['speed']
            }
            
            # Cache for 1 hour
            cache.set(cache_key, weather, 3600)
            return weather
            
        except Exception as e:
            print(f"Error fetching weather data: {e}")
            return self._get_mock_weather()
    
    def get_aqi_data(self):
        """
        Fetch AQI data from OpenWeatherMap Air Pollution API.
        
        Returns:
            dict: AQI information
        """
        # Check cache first
        cache_key = f"aqi_{self.location['city']}"
        cached_data = cache.get(cache_key)
        if cached_data:
            return cached_data
        
        try:
            # Get API key from settings
            api_key = getattr(settings, 'OPENWEATHER_API_KEY', 'demo')
            
            # If no API key, return mock data
            if api_key == 'demo':
                return self._get_mock_aqi()
            
            url = (
                f"http://api.openweathermap.org/data/2.5/air_pollution?"
                f"lat={self.location['lat']}&lon={self.location['lon']}"
                f"&appid={api_key}"
            )
            
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # AQI scale: 1=Good, 2=Fair, 3=Moderate, 4=Poor, 5=Very Poor
            aqi_index = data['list'][0]['main']['aqi']
            components = data['list'][0]['components']
            
            # Convert to US AQI scale (0-500)
            aqi_us = self._convert_to_us_aqi(aqi_index, components)
            
            aqi = {
                'aqi': aqi_us,
                'aqi_index': aqi_index,
                'pm2_5': components.get('pm2_5', 0),
                'pm10': components.get('pm10', 0),
                'quality': self._get_aqi_quality(aqi_us)
            }
            
            # Cache for 1 hour
            cache.set(cache_key, aqi, 3600)
            return aqi
            
        except Exception as e:
            print(f"Error fetching AQI data: {e}")
            return self._get_mock_aqi()
    
    def _convert_to_us_aqi(self, aqi_index, components):
        """Convert OpenWeatherMap AQI index to US AQI scale"""
        pm2_5 = components.get('pm2_5', 0)
        
        # Simple conversion based on PM2.5
        if pm2_5 <= 12:
            return int(pm2_5 * 4.17)  # 0-50
        elif pm2_5 <= 35.4:
            return int(50 + (pm2_5 - 12) * 2.13)  # 51-100
        elif pm2_5 <= 55.4:
            return int(100 + (pm2_5 - 35.4) * 2.5)  # 101-150
        elif pm2_5 <= 150.4:
            return int(150 + (pm2_5 - 55.4) * 0.53)  # 151-200
        else:
            return min(int(200 + (pm2_5 - 150.4) * 0.53), 500)  # 201-500
    
    def _get_aqi_quality(self, aqi):
        """Get AQI quality description"""
        if aqi <= 50:
            return 'Good'
        elif aqi <= 100:
            return 'Moderate'
        elif aqi <= 150:
            return 'Unhealthy for Sensitive Groups'
        elif aqi <= 200:
            return 'Unhealthy'
        elif aqi <= 300:
            return 'Very Unhealthy'
        else:
            return 'Hazardous'
    
    def _get_mock_weather(self):
        """Return mock weather data for demo purposes"""
        import random
        season = datetime.now().month
        
        # Simulate seasonal patterns
        if season in [12, 1, 2]:  # Winter
            temp = random.uniform(10, 20)
            humidity = random.uniform(50, 70)
            desc = 'clear sky'
        elif season in [3, 4, 5]:  # Spring
            temp = random.uniform(25, 35)
            humidity = random.uniform(40, 60)
            desc = 'few clouds'
        elif season in [6, 7, 8]:  # Monsoon
            temp = random.uniform(28, 35)
            humidity = random.uniform(70, 90)
            desc = 'light rain'
        else:  # Autumn
            temp = random.uniform(20, 30)
            humidity = random.uniform(50, 70)
            desc = 'clear sky'
        
        return {
            'temperature': round(temp, 1),
            'feels_like': round(temp + 2, 1),
            'humidity': int(humidity),
            'description': desc,
            'main': 'Clear',
            'pressure': 1013,
            'wind_speed': 3.5
        }
    
    def _get_mock_aqi(self):
        """Return mock AQI data for demo purposes"""
        import random
        aqi = random.randint(80, 180)
        
        return {
            'aqi': aqi,
            'aqi_index': 3,
            'pm2_5': aqi / 4,
            'pm10': aqi / 2,
            'quality': self._get_aqi_quality(aqi)
        }
    
    def predict_disease_spikes(self):
        """
        Predict which diseases might spike based on current weather/AQI.
        
        Returns:
            list: List of disease spike predictions with triggers
        """
        weather = self.get_weather_data()
        aqi = self.get_aqi_data()
        
        predicted_spikes = []
        
        # Check AQI levels
        if aqi['aqi'] > WEATHER_DISEASE_MAP['high_aqi']['threshold']:
            predicted_spikes.append({
                'trigger': 'High Air Pollution',
                'trigger_type': 'aqi',
                'value': f"AQI: {aqi['aqi']} ({aqi['quality']})",
                'diseases': WEATHER_DISEASE_MAP['high_aqi']['diseases'],
                'severity': WEATHER_DISEASE_MAP['high_aqi']['severity'],
                'multiplier': WEATHER_DISEASE_MAP['high_aqi']['medicine_multiplier'],
                'recommendation': 'Stock up on respiratory medicines'
            })
        elif aqi['aqi'] > WEATHER_DISEASE_MAP['moderate_aqi']['threshold']:
            predicted_spikes.append({
                'trigger': 'Moderate Air Pollution',
                'trigger_type': 'aqi',
                'value': f"AQI: {aqi['aqi']} ({aqi['quality']})",
                'diseases': WEATHER_DISEASE_MAP['moderate_aqi']['diseases'],
                'severity': WEATHER_DISEASE_MAP['moderate_aqi']['severity'],
                'multiplier': WEATHER_DISEASE_MAP['moderate_aqi']['medicine_multiplier'],
                'recommendation': 'Monitor respiratory medicine stocks'
            })
        
        # Check temperature
        if weather['temperature'] < WEATHER_DISEASE_MAP['cold_weather']['threshold']:
            predicted_spikes.append({
                'trigger': 'Cold Weather',
                'trigger_type': 'temperature',
                'value': f"{weather['temperature']}°C",
                'diseases': WEATHER_DISEASE_MAP['cold_weather']['diseases'],
                'severity': WEATHER_DISEASE_MAP['cold_weather']['severity'],
                'multiplier': WEATHER_DISEASE_MAP['cold_weather']['medicine_multiplier'],
                'recommendation': 'Increase stock of cold & flu medicines'
            })
        elif weather['temperature'] > WEATHER_DISEASE_MAP['hot_weather']['threshold']:
            predicted_spikes.append({
                'trigger': 'Hot Weather',
                'trigger_type': 'temperature',
                'value': f"{weather['temperature']}°C",
                'diseases': WEATHER_DISEASE_MAP['hot_weather']['diseases'],
                'severity': WEATHER_DISEASE_MAP['hot_weather']['severity'],
                'multiplier': WEATHER_DISEASE_MAP['hot_weather']['medicine_multiplier'],
                'recommendation': 'Stock ORS, heat stroke medications'
            })
        
        # Check humidity
        if weather['humidity'] > WEATHER_DISEASE_MAP['high_humidity']['threshold']:
            predicted_spikes.append({
                'trigger': 'High Humidity',
                'trigger_type': 'humidity',
                'value': f"{weather['humidity']}%",
                'diseases': WEATHER_DISEASE_MAP['high_humidity']['diseases'],
                'severity': WEATHER_DISEASE_MAP['high_humidity']['severity'],
                'multiplier': WEATHER_DISEASE_MAP['high_humidity']['medicine_multiplier'],
                'recommendation': 'Monitor vector-borne disease medicines'
            })
        
        # Check for rain/monsoon conditions
        desc_lower = weather['description'].lower()
        if any(keyword in desc_lower for keyword in WEATHER_DISEASE_MAP['monsoon']['keywords']):
            predicted_spikes.append({
                'trigger': 'Rainy/Monsoon Conditions',
                'trigger_type': 'weather',
                'value': weather['description'].title(),
                'diseases': WEATHER_DISEASE_MAP['monsoon']['diseases'],
                'severity': WEATHER_DISEASE_MAP['monsoon']['severity'],
                'multiplier': WEATHER_DISEASE_MAP['monsoon']['medicine_multiplier'],
                'recommendation': 'Increase anti-malarial & dengue medicines'
            })
        
        return predicted_spikes
    
    def predict_medicine_demand(self):
        """
        Predict medicine demand increases based on weather/AQI.
        Integrates with existing disease-medicine mapping.
        
        Returns:
            dict: Complete prediction with weather factors and medicine demand
        """
        from .ml_predictor import DISEASE_MEDICINE_MAP
        
        # Get disease spike predictions
        spikes = self.predict_disease_spikes()
        
        # Calculate medicine demand
        medicine_demand = {}
        disease_impact = {}
        
        for spike in spikes:
            for disease in spike['diseases']:
                # Track disease impact
                if disease not in disease_impact:
                    disease_impact[disease] = {
                        'triggers': [],
                        'max_multiplier': 1.0
                    }
                
                disease_impact[disease]['triggers'].append(spike['trigger'])
                disease_impact[disease]['max_multiplier'] = max(
                    disease_impact[disease]['max_multiplier'],
                    spike['multiplier']
                )
                
                # Map disease to medicines
                if disease in DISEASE_MEDICINE_MAP:
                    mapping = DISEASE_MEDICINE_MAP[disease]
                    for med, base_qty in zip(mapping['medicines'], mapping['avg_qty_per_patient']):
                        # Apply multiplier to base quantity
                        adjusted_qty = int(base_qty * spike['multiplier'])
                        
                        if med not in medicine_demand:
                            medicine_demand[med] = {
                                'quantity': 0,
                                'base_quantity': 0,
                                'related_diseases': [],
                                'urgency': spike['severity']
                            }
                        
                        medicine_demand[med]['quantity'] += adjusted_qty
                        medicine_demand[med]['base_quantity'] += base_qty
                        if disease not in medicine_demand[med]['related_diseases']:
                            medicine_demand[med]['related_diseases'].append(disease)
        
        return {
            'weather_aqi_factors': spikes,
            'disease_impact': disease_impact,
            'predicted_medicine_demand': medicine_demand,
            'forecast_period': '7-14 days',
            'confidence': 'rule_based',
            'last_updated': datetime.now().isoformat()
        }
    
    def get_current_conditions(self):
        """Get current weather and AQI conditions"""
        return {
            'weather': self.get_weather_data(),
            'aqi': self.get_aqi_data(),
            'location': self.location
        }


# Helper function for views
def get_weather_predictor(hospital_location=None):
    """
    Get weather predictor instance.
    
    Args:
        hospital_location: Optional dict with location info
        
    Returns:
        WeatherAQIPredictor instance
    """
    if not hospital_location:
        # Try to get from settings
        hospital_location = getattr(settings, 'HOSPITAL_LOCATION', None)
    
    return WeatherAQIPredictor(hospital_location)
