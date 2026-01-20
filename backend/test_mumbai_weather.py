"""
Test script for Weather & AQI prediction with real Mumbai API
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.inventory.weather_predictor import get_weather_predictor

def test_mumbai_weather():
    print("\n" + "="*60)
    print("TESTING REAL API WITH MUMBAI WEATHER DATA")
    print("="*60 + "\n")
    
    # Get predictor instance
    predictor = get_weather_predictor()
    
    print("📍 Location: Mumbai, Maharashtra")
    print("🔑 API: OpenWeatherMap (Real-time data)\n")
    
    # Get current weather
    print("🌤️ CURRENT WEATHER CONDITIONS")
    print("-" * 40)
    try:
        weather = predictor.get_weather_data()
        print(f"Temperature:     {weather['temperature']}°C")
        print(f"Feels Like:      {weather['feels_like']}°C")
        print(f"Description:     {weather['description'].title()}")
        print(f"Humidity:        {weather['humidity']}%")
        print(f"Wind Speed:      {weather['wind_speed']} m/s")
        print(f"Pressure:        {weather['pressure']} hPa")
    except Exception as e:
        print(f"❌ Weather API Error: {e}")
        return
    
    # Get AQI data
    print("\n💨 AIR QUALITY INDEX")
    print("-" * 40)
    try:
        aqi = predictor.get_aqi_data()
        print(f"AQI:             {aqi['aqi']}")
        print(f"Quality:         {aqi['quality']}")
        print(f"PM2.5:           {aqi['pm2_5']:.1f} μg/m³")
        print(f"PM10:            {aqi['pm10']:.1f} μg/m³")
    except Exception as e:
        print(f"❌ AQI API Error: {e}")
        return
    
    # Get predictions
    print("\n🔮 DISEASE & MEDICINE PREDICTIONS")
    print("-" * 40)
    try:
        result = predictor.predict_medicine_demand()
        
        if result['weather_aqi_factors']:
            print(f"\n⚠️ Risk Factors Detected: {len(result['weather_aqi_factors'])}\n")
            
            for i, factor in enumerate(result['weather_aqi_factors'], 1):
                print(f"{i}. {factor['trigger']}")
                print(f"   Value:        {factor['value']}")
                print(f"   Severity:     {factor['severity']}")
                print(f"   Diseases:     {', '.join(factor['diseases'])}")
                print(f"   Multiplier:   {factor['multiplier']}x")
                print(f"   💡 {factor['recommendation']}")
                print()
        else:
            print("✅ No significant environmental risk factors detected")
            print("   Current conditions are favorable for normal operations\n")
        
        # Medicine demand
        if result['predicted_medicine_demand']:
            print("\n📦 RECOMMENDED MEDICINE STOCK INCREASE")
            print("-" * 40)
            
            medicines = sorted(
                result['predicted_medicine_demand'].items(),
                key=lambda x: x[1]['quantity'],
                reverse=True
            )
            
            for medicine, data in medicines[:10]:  # Top 10
                print(f"\n{medicine}")
                print(f"  Additional Stock: {data['quantity']} units")
                print(f"  Base Quantity:    {data['base_quantity']} units")
                print(f"  Increase:         {data['quantity'] - data['base_quantity']} units")
                print(f"  Urgency:          {data['urgency']}")
                print(f"  Related to:       {', '.join(data['related_diseases'])}")
        
        print("\n" + "="*60)
        print("✅ REAL-TIME API TEST SUCCESSFUL!")
        print("="*60 + "\n")
        print(f"📅 Forecast Period: {result['forecast_period']}")
        print(f"🔄 Data updates every hour (cached)")
        
    except Exception as e:
        print(f"❌ Prediction Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_mumbai_weather()
