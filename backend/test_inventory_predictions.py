"""
Test inventory ML prediction endpoints
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

print("Testing Inventory ML Predictions...")
print("=" * 60)

# Test 1: Get predictor
try:
    from apps.inventory.ml_predictor import get_predictor
    predictor = get_predictor()
    print("✅ Predictor loaded successfully")
    print(f"   Models loaded: {predictor.models_loaded}")
except Exception as e:
    print(f"❌ Error loading predictor: {e}")
    sys.exit(1)

# Test 2: Get all alerts
try:
    print("\n📊 Testing: Get All Alerts")
    alerts = predictor.get_all_alerts()
    print(f"✅ Total items scanned: {alerts['total_items_scanned']}")
    print(f"   Items needing attention: {alerts['items_needing_attention']}")
    print(f"   High priority: {alerts['high_priority']}")
    print(f"   Medium priority: {alerts['medium_priority']}")
    
    if alerts['alerts']:
        print("\n   Top 3 alerts:")
        for alert in alerts['alerts'][:3]:
            print(f"   - {alert['item_name']}: {alert['urgency']} priority (stock: {alert['current_stock']})")
except Exception as e:
    print(f"❌ Error getting alerts: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Get disease demand forecast
try:
    print("\n🏥 Testing: Disease Demand Forecast")
    forecast = predictor.predict_disease_demand()
    print(f"✅ Total patients: {forecast['total_patients']}")
    print(f"   Current admissions by condition:")
    for condition, count in forecast['current_admissions'].items():
        print(f"   - {condition}: {count} patients")
    
    if forecast['predicted_demand']:
        print(f"\n   Top 5 medicines needed:")
        sorted_demand = sorted(forecast['predicted_demand'].items(), key=lambda x: x[1], reverse=True)[:5]
        for med, qty in sorted_demand:
            print(f"   - {med}: {qty} units")
except Exception as e:
    print(f"❌ Error getting forecast: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Get prediction for specific item
try:
    from apps.authentication.models import InventoryItem
    first_item = InventoryItem.objects.first()
    
    if first_item:
        print(f"\n🔍 Testing: Prediction for '{first_item.item_name}'")
        prediction = predictor.get_unified_prediction(item_id=first_item.item_id)
        print(f"✅ Current stock: {prediction['item']['current_stock']}")
        print(f"   Days until stockout: {prediction['usage_based_prediction']['days_until_stockout']}")
        print(f"   Disease demand this week: {prediction['disease_based_prediction']['expected_demand_this_week']}")
        print(f"   Combined risk: {prediction['combined_analysis']['combined_risk_score']:.2f}")
        print(f"   Urgency: {prediction['combined_analysis']['urgency']}")
        print(f"   Recommendation: {prediction['combined_analysis']['recommendation']}")
except Exception as e:
    print(f"❌ Error getting item prediction: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 60)
print("✅ All tests completed!")
