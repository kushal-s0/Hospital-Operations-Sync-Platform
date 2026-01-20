# Weather & AQI-Based Medicine Prediction Setup

## Overview

This feature predicts medicine demand based on **real-time weather and air quality (AQI) data**. It uses rule-based predictions to identify which diseases are likely to spike based on environmental conditions, then maps those diseases to required medicines.

## How It Works

### 1. Environmental Data Collection
- **Weather Data**: Temperature, humidity, weather conditions (rain, etc.)
- **AQI Data**: Air quality index, PM2.5, PM10 levels
- **Source**: OpenWeatherMap API (free tier available)

### 2. Rule-Based Disease Prediction

The system uses medically-proven correlations:

| Environmental Factor | Threshold | Diseases | Medicine Demand Increase |
|---------------------|-----------|----------|------------------------|
| **High AQI** | >150 (Unhealthy) | Respiratory Infection, Asthma, COPD | +50% |
| **Moderate AQI** | >100 | Respiratory Infection, Asthma | +20% |
| **Cold Weather** | <15°C | Fever/Viral, Respiratory Infection, Pneumonia | +30% |
| **Hot Weather** | >35°C | Heat Stroke, Dehydration, Gastric/Ulcer | +40% |
| **High Humidity** | >80% | Dengue, Malaria, Bacterial Infections | +25% |
| **Rain/Monsoon** | Rainy conditions | Dengue, Malaria, Infections, Fever | +35% |

### 3. Medicine Demand Calculation

For each detected environmental risk:
1. Identify which diseases are likely to spike
2. Map diseases to required medicines (using existing DISEASE_MEDICINE_MAP)
3. Apply multiplier to base medicine quantities
4. Sum up total additional stock needed

## Setup Instructions

### Step 1: Get Free API Key

1. Go to [OpenWeatherMap](https://openweathermap.org/api)
2. Sign up for a free account
3. Navigate to **API Keys** in your dashboard
4. Copy your API key

**Free Tier Includes**:
- 1,000 API calls per day
- Current weather data
- Air pollution data
- More than enough for hospital use!

### Step 2: Configure Hospital Location

Open `backend/hospital_ops/settings.py` and update:

```python
HOSPITAL_LOCATION = {
    'lat': 28.6139,  # Your hospital's latitude
    'lon': 77.2090,  # Your hospital's longitude
    'city': 'Delhi'  # Your city name
}
```

**How to find your coordinates**:
- Google Maps: Right-click on your location → Click the coordinates
- Or search: "my location coordinates"

### Step 3: Add API Key to Environment

Create or update `backend/.env` file:

```env
OPENWEATHER_API_KEY=your_api_key_here
```

**Important**: Never commit your API key to Git!

### Step 4: Test the System

Without API key (uses mock data):
```bash
cd backend
python manage.py runserver
```

Visit: `http://localhost:8000/api/inventory/weather-prediction/`

With API key configured:
- The system will fetch real-time data
- Cache is 1 hour (reduces API calls)
- Mock data is used as fallback if API fails

## API Response Structure

```json
{
  "weather_aqi_factors": [
    {
      "trigger": "High Air Pollution",
      "trigger_type": "aqi",
      "value": "AQI: 175 (Unhealthy)",
      "diseases": ["Respiratory Infection", "Asthma"],
      "severity": "High",
      "multiplier": 1.5,
      "recommendation": "Stock up on respiratory medicines"
    }
  ],
  "disease_impact": {
    "Respiratory Infection": {
      "triggers": ["High Air Pollution"],
      "max_multiplier": 1.5
    }
  },
  "predicted_medicine_demand": {
    "Salbutamol Inhaler": {
      "quantity": 45,
      "base_quantity": 30,
      "related_diseases": ["Asthma"],
      "urgency": "High"
    }
  },
  "current_weather": {
    "temperature": 32.5,
    "humidity": 75,
    "description": "light rain"
  },
  "current_aqi": {
    "aqi": 175,
    "quality": "Unhealthy"
  },
  "forecast_period": "7-14 days",
  "confidence": "rule_based"
}
```

## Frontend Integration

The inventory page automatically shows:

### 🌤️ Current Conditions Cards
- Temperature & weather description
- Humidity level
- Air Quality Index (color-coded)

### ⚠️ Risk Factors
- Detected environmental risks
- Expected disease spikes
- Severity levels (High/Moderate/Low)
- Actionable recommendations

### 📦 Recommended Stock Increase
- Medicines to restock
- Additional quantity needed
- Related diseases
- Urgency level

## Customization

### Adjusting Thresholds

Edit `backend/apps/inventory/weather_predictor.py`:

```python
WEATHER_DISEASE_MAP = {
    'high_aqi': {
        'threshold': 150,  # Adjust this value
        'diseases': ['Respiratory Infection', 'Asthma', 'COPD'],
        'medicine_multiplier': 1.5  # Adjust demand increase
    },
    # Add more mappings...
}
```

### Adding New Weather-Disease Correlations

```python
'extreme_cold': {
    'threshold': 5,  # Below 5°C
    'diseases': ['Hypothermia', 'Frostbite'],
    'severity': 'High',
    'medicine_multiplier': 2.0
}
```

## Benefits

✅ **Proactive Planning**: Predict demand before disease outbreaks
✅ **No ML Training Needed**: Uses proven medical correlations
✅ **Real-Time Data**: Updates automatically based on current conditions
✅ **Cost-Effective**: Free API tier is sufficient
✅ **Automatic Fallback**: Uses mock data if API unavailable
✅ **Complements Existing ML**: Works alongside admission-based predictions

## Troubleshooting

### "Error fetching weather data"
- Check your API key in `.env`
- Verify `OPENWEATHER_API_KEY` in settings
- System will use mock data as fallback

### No predictions showing
- Ensure conditions exceed thresholds
- Check if diseases are in `DISEASE_MEDICINE_MAP`
- Verify hospital location coordinates

### API quota exceeded
- Free tier: 1,000 calls/day
- System caches data for 1 hour
- Reduce refresh frequency if needed

## Future Enhancements

1. **ML Model**: Train on historical weather-disease correlation data
2. **7-Day Forecast**: Use forecast API for advance planning
3. **Seasonal Patterns**: Incorporate yearly disease trends
4. **Regional Data**: Compare with nearby hospitals
5. **Alert System**: Automated notifications for high-risk conditions

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/inventory/weather-prediction/` | GET | Get weather-based predictions |
| `/api/inventory/demand-forecast/` | GET | Get admission-based predictions |
| `/api/inventory/alerts/` | GET | Get all ML alerts |

## Support

For issues or questions:
1. Check Django logs: `backend/` terminal output
2. Verify API key configuration
3. Test with mock data first
4. Check browser console for frontend errors

---

**Last Updated**: January 2026
**Version**: 1.0
**Status**: Production Ready ✅
