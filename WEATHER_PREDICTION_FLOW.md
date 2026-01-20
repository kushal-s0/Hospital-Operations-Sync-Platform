# Weather & AQI-Based Medicine Prediction Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    WEATHER & AQI PREDICTION SYSTEM                      │
│                         (Rule-Based Approach)                            │
└─────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────┐
│                          STEP 1: DATA COLLECTION                         │
└─────────────────────────────────────────────────────────────────────────┘

  ┌──────────────────┐          ┌──────────────────┐
  │  OpenWeatherMap  │          │   Hospital DB    │
  │      API         │          │   (Location)     │
  └────────┬─────────┘          └────────┬─────────┘
           │                              │
           ├─> Weather Data               │
           │   • Temperature: 32°C        │
           │   • Humidity: 78%            │
           │   • Description: "light rain"│
           │                              │
           ├─> AQI Data                   │
           │   • AQI: 165                 │
           │   • PM2.5: 85                │
           │   • Quality: "Unhealthy"     │
           │                              │
           └──────────────┬───────────────┘
                          ▼
                  ┌───────────────┐
                  │  Cache (1hr)  │
                  │  or Mock Data │
                  └───────┬───────┘
                          │
                          ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                   STEP 2: RULE-BASED DISEASE MAPPING                    │
└─────────────────────────────────────────────────────────────────────────┘

     Input Conditions                  Rules Applied                Disease Predictions
  ┌─────────────────┐           ┌────────────────────┐         ┌───────────────────┐
  │ AQI: 165        │──────────▶│ IF AQI > 150 THEN  │────────▶│ • Respiratory     │
  │ (Unhealthy)     │           │ TRIGGER: High AQI  │         │   Infection       │
  └─────────────────┘           │ DISEASES: [...]    │         │ • Asthma          │
                                │ MULTIPLIER: 1.5x   │         │ • COPD            │
                                └────────────────────┘         └───────────────────┘

  ┌─────────────────┐           ┌────────────────────┐         ┌───────────────────┐
  │ Temp: 32°C      │──────────▶│ IF Temp > 35°C     │────────▶│ No trigger        │
  │ (Normal)        │           │ TRIGGER: Hot       │         │ (below threshold) │
  └─────────────────┘           └────────────────────┘         └───────────────────┘

  ┌─────────────────┐           ┌────────────────────┐         ┌───────────────────┐
  │ Humidity: 78%   │──────────▶│ IF Humidity < 80%  │────────▶│ No trigger        │
  │ (Normal)        │           │ TRIGGER: High Hum  │         │ (below threshold) │
  └─────────────────┘           └────────────────────┘         └───────────────────┘

  ┌─────────────────┐           ┌────────────────────┐         ┌───────────────────┐
  │ Weather: Rain   │──────────▶│ IF "rain" in desc  │────────▶│ • Dengue          │
  │                 │           │ TRIGGER: Monsoon   │         │ • Malaria         │
  └─────────────────┘           │ MULTIPLIER: 1.35x  │         │ • Fever/Viral     │
                                └────────────────────┘         └───────────────────┘

                                          ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                 STEP 3: MEDICINE DEMAND CALCULATION                      │
└─────────────────────────────────────────────────────────────────────────┘

    Disease Predictions              DISEASE_MEDICINE_MAP           Medicine Demand
  ┌───────────────────┐            ┌──────────────────┐         ┌─────────────────┐
  │ Respiratory       │───────────▶│ Respiratory →    │────────▶│ Azithromycin    │
  │ Infection         │            │ • Azithromycin   │         │ Base: 6         │
  │ (Multiplier: 1.5x)│            │ • Amoxicillin    │         │ Adjusted: 9     │
  └───────────────────┘            │ Qty: 6, 8        │         │                 │
                                   └──────────────────┘         │ Amoxicillin     │
                                                                │ Base: 8         │
                                                                │ Adjusted: 12    │
                                                                └─────────────────┘

  ┌───────────────────┐            ┌──────────────────┐         ┌─────────────────┐
  │ Asthma            │───────────▶│ Asthma →         │────────▶│ Salbutamol      │
  │ (Multiplier: 1.5x)│            │ • Salbutamol     │         │ Inhaler         │
  └───────────────────┘            │ • Prednisolone   │         │ Base: 2         │
                                   │ Qty: 2, 5        │         │ Adjusted: 3     │
                                   └──────────────────┘         │                 │
                                                                │ Prednisolone    │
                                                                │ Base: 5         │
                                                                │ Adjusted: 8     │
                                                                └─────────────────┘

  ┌───────────────────┐            ┌──────────────────┐         ┌─────────────────┐
  │ Dengue            │───────────▶│ Dengue →         │────────▶│ Paracetamol     │
  │ (Multiplier:1.35x)│            │ • Paracetamol    │         │ 500mg           │
  └───────────────────┘            │ Qty: 25          │         │ Base: 25        │
                                   └──────────────────┘         │ Adjusted: 34    │
                                                                └─────────────────┘

                                          ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                        STEP 4: API RESPONSE                             │
└─────────────────────────────────────────────────────────────────────────┘

{
  "weather_aqi_factors": [
    {
      "trigger": "High Air Pollution",
      "value": "AQI: 165 (Unhealthy)",
      "diseases": ["Respiratory Infection", "Asthma", "COPD"],
      "severity": "High",
      "multiplier": 1.5,
      "recommendation": "Stock up on respiratory medicines"
    },
    {
      "trigger": "Rainy/Monsoon Conditions",
      "value": "Light Rain",
      "diseases": ["Dengue", "Malaria", "Fever/Viral"],
      "severity": "Moderate",
      "multiplier": 1.35,
      "recommendation": "Increase anti-malarial medicines"
    }
  ],
  "predicted_medicine_demand": {
    "Azithromycin": {
      "quantity": 9,
      "base_quantity": 6,
      "related_diseases": ["Respiratory Infection"],
      "urgency": "High"
    },
    "Salbutamol Inhaler": {
      "quantity": 3,
      "base_quantity": 2,
      "related_diseases": ["Asthma"],
      "urgency": "High"
    },
    "Paracetamol 500mg": {
      "quantity": 34,
      "base_quantity": 25,
      "related_diseases": ["Dengue", "Fever/Viral"],
      "urgency": "Moderate"
    }
  },
  "current_weather": { ... },
  "current_aqi": { ... }
}

                                          ▼

┌─────────────────────────────────────────────────────────────────────────┐
│                     STEP 5: FRONTEND DISPLAY                            │
└─────────────────────────────────────────────────────────────────────────┘

  ╔═══════════════════════════════════════════════════════════════════════╗
  ║           🌤️ Weather & AQI-Based Forecast                            ║
  ║     Real-time environmental data for Delhi                            ║
  ╠═══════════════════════════════════════════════════════════════════════╣
  ║                                                                       ║
  ║  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐          ║
  ║  │ 🌡️ 32°C     │  │ 💧 78%       │  │ 💨 AQI: 165      │          ║
  ║  │ Light Rain   │  │ Humidity     │  │ Unhealthy (RED)  │          ║
  ║  └──────────────┘  └──────────────┘  └──────────────────┘          ║
  ║                                                                       ║
  ║  ⚠️ Disease Risk Factors Detected                                    ║
  ║  ┌─────────────────────────────────────────────────────────┐        ║
  ║  │ 🔴 HIGH: High Air Pollution (AQI: 165)                  │        ║
  ║  │ Expected: Respiratory Infection, Asthma, COPD           │        ║
  ║  │ 💡 Stock up on respiratory medicines                    │        ║
  ║  │ Demand increase: 50%                                     │        ║
  ║  └─────────────────────────────────────────────────────────┘        ║
  ║  ┌─────────────────────────────────────────────────────────┐        ║
  ║  │ 🟠 MODERATE: Rainy/Monsoon Conditions                   │        ║
  ║  │ Expected: Dengue, Malaria, Fever/Viral                  │        ║
  ║  │ 💡 Increase anti-malarial medicines                     │        ║
  ║  │ Demand increase: 35%                                     │        ║
  ║  └─────────────────────────────────────────────────────────┘        ║
  ║                                                                       ║
  ║  📦 Recommended Stock Increase                                       ║
  ║  ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐      ║
  ║  │ Paracetamol     │ │ Azithromycin    │ │ Salbutamol      │      ║
  ║  │ 500mg           │ │                 │ │ Inhaler         │      ║
  ║  │ 🔴 HIGH         │ │ 🔴 HIGH         │ │ 🔴 HIGH         │      ║
  ║  │ +34 units       │ │ +9 units        │ │ +3 units        │      ║
  ║  │ Dengue, Fever   │ │ Respiratory     │ │ Asthma          │      ║
  ║  └─────────────────┘ └─────────────────┘ └─────────────────┘      ║
  ║                                                                       ║
  ║  🔄 Last updated: 2026-01-20 14:30    📅 Forecast: 7-14 days       ║
  ╚═══════════════════════════════════════════════════════════════════════╝

```

## System Architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                         FRONTEND (React)                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Inventory.js                                                 │  │
│  │  • fetchWeatherPrediction()                                   │  │
│  │  • Display current conditions                                 │  │
│  │  • Show risk factors                                          │  │
│  │  • Render medicine recommendations                            │  │
│  └────────────────────────────┬─────────────────────────────────┘  │
└─────────────────────────────────┼──────────────────────────────────┘
                                  │ HTTP GET Request
                                  ▼
┌────────────────────────────────────────────────────────────────────┐
│                         BACKEND (Django)                            │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  views.py - get_weather_based_prediction()                   │  │
│  │  • Handle HTTP request                                        │  │
│  │  • Call weather predictor                                     │  │
│  │  • Return JSON response                                       │  │
│  └────────────────────────────┬─────────────────────────────────┘  │
│                                ▼                                    │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  weather_predictor.py - WeatherAQIPredictor                  │  │
│  │  • get_weather_data()                                         │  │
│  │  • get_aqi_data()                                            │  │
│  │  • predict_disease_spikes()                                  │  │
│  │  • predict_medicine_demand()                                 │  │
│  └────────────┬────────────────────────────┬───────────────────┘  │
└─────────────────┼──────────────────────────┼──────────────────────┘
                  │                           │
          API Call│                           │ Database Query
                  ▼                           ▼
    ┌──────────────────────┐    ┌──────────────────────────┐
    │  OpenWeatherMap API  │    │  DISEASE_MEDICINE_MAP    │
    │  • Weather Data      │    │  (from ml_predictor.py)  │
    │  • AQI Data          │    │  • Disease → Medicine    │
    │  • Cache: 1 hour     │    │  • Base quantities       │
    └──────────────────────┘    └──────────────────────────┘
```

## Data Flow Timeline

```
Time: 0ms     Frontend page loads
              └─> fetchWeatherPrediction() called

Time: 10ms    Backend receives GET /api/inventory/weather-prediction/
              └─> get_weather_predictor() instantiated

Time: 20ms    Check cache for weather data
              ├─> Cache HIT → Return cached data (1 hour TTL)
              └─> Cache MISS → Call OpenWeatherMap API

Time: 150ms   API returns weather + AQI data
              └─> Store in cache

Time: 160ms   Apply rule-based disease mapping
              ├─> Check AQI threshold
              ├─> Check temperature threshold
              ├─> Check humidity threshold
              └─> Check weather conditions

Time: 170ms   For each triggered rule:
              ├─> Get related diseases
              ├─> Look up DISEASE_MEDICINE_MAP
              ├─> Apply multiplier
              └─> Calculate adjusted quantities

Time: 180ms   Build response JSON
              └─> Include weather, AQI, predictions

Time: 200ms   Return response to frontend

Time: 220ms   Frontend renders:
              ├─> Current conditions cards
              ├─> Risk factor alerts
              └─> Medicine demand grid

Total: ~220ms from request to display
```

## Key Design Decisions

1. **Rule-Based vs ML**: Chose rules for immediate deployment
2. **Caching**: 1-hour TTL reduces API calls, improves performance
3. **Mock Data**: Fallback ensures system never breaks
4. **Integration**: Uses existing DISEASE_MEDICINE_MAP
5. **UI First**: Visual design prioritizes actionable insights

