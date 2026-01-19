"""
Unified Inventory Prediction System
====================================
Combines both inventory models:
1. Stock Depletion Model - Based on historical usage patterns
2. Disease Demand Model - Based on current patient admissions

Data is pulled AUTOMATICALLY from the database - no manual input required!
"""

import joblib
import numpy as np
import warnings
from datetime import datetime, timedelta
from django.db.models import Sum, Avg, Count, StdDev, Max
from django.db.models.functions import TruncDate
from django.utils import timezone
import os

# Suppress sklearn feature name warnings (models work fine with numpy arrays)
warnings.filterwarnings('ignore', message='X does not have valid feature names')

# Path to saved models
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'models')


# =============================================================================
# DISEASE TO MEDICINE MAPPING
# =============================================================================
DISEASE_MEDICINE_MAP = {
    'Respiratory Infection': {
        'medicines': ['Azithromycin 250mg', 'Amoxicillin 250mg', 'Salbutamol Inhaler', 
                      'Paracetamol 500mg', 'Cough Syrup'],
        'avg_qty_per_patient': [6, 10, 1, 10, 1],
    },
    'Fever/Viral': {
        'medicines': ['Paracetamol 500mg', 'Ibuprofen 400mg', 'ORS Packets', 
                      'Vitamin C', 'Antihistamine'],
        'avg_qty_per_patient': [15, 6, 5, 10, 5],
    },
    'Diabetes': {
        'medicines': ['Metformin 500mg', 'Insulin Glargine', 'Glipizide', 
                      'Glucometer Strips', 'Syringes 5ml'],
        'avg_qty_per_patient': [60, 2, 30, 50, 30],
    },
    'Hypertension': {
        'medicines': ['Amlodipine 5mg', 'Losartan 50mg', 'Atenolol 50mg', 
                      'Aspirin 100mg', 'Diuretics'],
        'avg_qty_per_patient': [30, 30, 30, 30, 15],
    },
    'Cardiac': {
        'medicines': ['Aspirin 100mg', 'Atorvastatin 10mg', 'Clopidogrel', 
                      'Nitroglycerin', 'Beta Blockers'],
        'avg_qty_per_patient': [30, 30, 30, 10, 30],
    },
    'Gastric/Ulcer': {
        'medicines': ['Omeprazole 20mg', 'Pantoprazole 40mg', 'Ranitidine 150mg', 
                      'Antacid Syrup', 'Sucralfate'],
        'avg_qty_per_patient': [14, 14, 14, 2, 28],
    },
    'Infection/Bacterial': {
        'medicines': ['Ciprofloxacin 500mg', 'Ceftriaxone 1g', 'Amoxicillin 250mg', 
                      'Metronidazole', 'Paracetamol 500mg'],
        'avg_qty_per_patient': [14, 7, 21, 21, 14],
    },
    'Pain/Injury': {
        'medicines': ['Tramadol 50mg', 'Diclofenac 50mg', 'Paracetamol 500mg', 
                      'Muscle Relaxant', 'Bandages'],
        'avg_qty_per_patient': [10, 14, 14, 10, 5],
    },
    'Allergy': {
        'medicines': ['Antihistamine', 'Prednisolone', 'Hydrocortisone Cream', 
                      'Calamine Lotion', 'Eye Drops'],
        'avg_qty_per_patient': [10, 7, 1, 1, 1],
    },
    'Pregnancy/Obstetric': {
        'medicines': ['Folic Acid', 'Iron Supplements', 'Calcium', 
                      'Prenatal Vitamins', 'Ondansetron 4mg'],
        'avg_qty_per_patient': [30, 30, 30, 30, 10],
    }
}


class UnifiedInventoryPredictor:
    """
    Unified prediction system that automatically pulls data from database
    and combines both prediction models.
    """
    
    def __init__(self):
        self.stock_classifier = None
        self.stock_regressor = None
        self.classifier_scaler = None
        self.regressor_scaler = None
        self.models_loaded = False
        self._load_models()
    
    def _load_models(self):
        """Load all trained models."""
        try:
            self.stock_classifier = joblib.load(
                os.path.join(MODELS_DIR, 'stock_availability_classifier.pkl')
            )
            self.stock_regressor = joblib.load(
                os.path.join(MODELS_DIR, 'stock_depletion_regressor.pkl')
            )
            # Try to load scalers if they exist
            try:
                self.classifier_scaler = joblib.load(
                    os.path.join(MODELS_DIR, 'stock_classifier_scaler.pkl')
                )
                self.regressor_scaler = joblib.load(
                    os.path.join(MODELS_DIR, 'stock_regressor_scaler.pkl')
                )
            except FileNotFoundError:
                print("[WARNING] Scalers not found, will use raw features")
            
            self.models_loaded = True
            print("[OK] All models loaded successfully")
        except FileNotFoundError as e:
            print(f"⚠️ Model not found: {e}. Will use fallback calculations.")
            self.models_loaded = False
    
    # =========================================================================
    # AUTOMATIC DATA EXTRACTION FROM DATABASE
    # =========================================================================
    
    def get_usage_stats_from_db(self, item_id):
        """
        Automatically extract usage statistics from database.
        NO MANUAL INPUT REQUIRED!
        """
        from apps.authentication.models import InventoryItem
        from apps.inventory.models import InventoryTransaction
        
        item = InventoryItem.objects.get(item_id=item_id)
        
        # Get last 30 days of usage (use timezone-aware datetimes)
        thirty_days_ago = timezone.now() - timedelta(days=30)
        seven_days_ago = timezone.now() - timedelta(days=7)
        fourteen_days_ago = timezone.now() - timedelta(days=14)
        
        # Calculate usage statistics from transactions
        # Note: transaction_type is 'out' (lowercase) in the model
        usage_queryset = InventoryTransaction.objects.filter(
            item=item,
            transaction_type='out',
            created_at__gte=thirty_days_ago
        )
        
        stats = usage_queryset.aggregate(
            total_usage=Sum('quantity'),
            avg_daily=Avg('quantity'),
            max_daily=Max('quantity'),
            std_dev=StdDev('quantity')
        )
        
        # Last 7 days usage
        last_7_days = InventoryTransaction.objects.filter(
            item=item,
            transaction_type='out',
            created_at__gte=seven_days_ago
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        # Previous 7 days usage (for trend)
        prev_7_days = InventoryTransaction.objects.filter(
            item=item,
            transaction_type='out',
            created_at__gte=fourteen_days_ago,
            created_at__lt=seven_days_ago
        ).aggregate(total=Sum('quantity'))['total'] or 0
        
        # Calculate trend
        if prev_7_days > 0:
            usage_trend = ((last_7_days - prev_7_days) / prev_7_days) * 100
        else:
            usage_trend = 0
        
        # Get category name (category is a CharField, not ForeignKey)
        category_name = item.category if item.category else 'Medicine'
        
        return {
            'quantity_available': item.quantity_available,
            'reorder_level': item.reorder_level,
            'avg_daily_usage': stats['avg_daily'] or 0,
            'usage_std': stats['std_dev'] or 0,
            'max_daily_usage': stats['max_daily'] or 0,
            'usage_last_7_days': last_7_days,
            'usage_trend': usage_trend,
            'category': category_name,
            'lead_time_days': 7  # Default lead time since model doesn't have this field
        }
    
    def get_current_admissions_from_db(self, days=7):
        """
        Automatically get current patient admissions grouped by diagnosis.
        NO MANUAL INPUT REQUIRED!
        """
        from apps.authentication.models import Admission
        
        # Use timezone-aware datetime
        cutoff_date = timezone.now() - timedelta(days=days)
        
        # Get admissions from last N days, grouped by condition_level
        # Note: MySQL schema uses 'status' as 'Active' not 'admitted', and uses 'admission_time' not 'admission_date'
        # Also, there's no 'diagnosis' field, so we'll use condition_level as proxy
        admissions = Admission.objects.filter(
            admission_time__gte=cutoff_date,
            status='Active'
        ).values('condition_level').annotate(
            count=Count('admission_id')
        )
        
        # Map condition_level to diagnosis categories for medicine prediction
        condition_to_diagnosis = {
            'Critical': 'Respiratory Infection',  # Critical patients often need respiratory support
            'High': 'Fever/Viral',
            'Medium': 'Pain/Injury',
            'Low': 'Allergy'
        }
        
        result = {}
        for a in admissions:
            diagnosis = condition_to_diagnosis.get(a['condition_level'], 'Fever/Viral')
            result[diagnosis] = result.get(diagnosis, 0) + a['count']
        
        return result
    
    def get_all_inventory_from_db(self):
        """Get all inventory items from database."""
        from apps.authentication.models import InventoryItem
        
        items = InventoryItem.objects.all()
        return {item.item_name: item.quantity_available for item in items}
    
    # =========================================================================
    # PREDICTION METHODS
    # =========================================================================
    
    def predict_stock_depletion(self, item_id=None, item_data=None):
        """
        Predict when an item will run out of stock.
        
        Can work in two modes:
        1. Automatic: Pass item_id, data is fetched from database
        2. Manual: Pass item_data dict directly (for testing/override)
        """
        # Get data from database if item_id provided
        if item_id and not item_data:
            item_data = self.get_usage_stats_from_db(item_id)
        
        # Calculate derived features
        reorder_level = max(item_data['reorder_level'], 1)
        avg_usage = max(item_data['avg_daily_usage'], 0.001)
        
        stock_ratio = item_data['quantity_available'] / reorder_level
        usage_volatility = item_data['usage_std'] / avg_usage
        
        # Category encoding
        category_map = {'Consumable': 0, 'Equipment': 1, 'Medicine': 2}
        category_encoded = category_map.get(item_data['category'], 2)
        
        # If models are loaded, use ML predictions
        if self.models_loaded and self.stock_classifier and self.stock_regressor:
            # Prepare features
            features = np.array([[
                item_data['quantity_available'],
                item_data['reorder_level'],
                item_data['avg_daily_usage'],
                item_data['usage_std'],
                item_data['max_daily_usage'],
                item_data['usage_last_7_days'],
                item_data['usage_trend'],
                stock_ratio,
                usage_volatility,
                category_encoded,
                item_data['lead_time_days']
            ]])
            
            # Predict using ML models
            try:
                is_at_risk = self.stock_classifier.predict(features)[0]
                probability = self.stock_classifier.predict_proba(features)[0][1]
                days_until_stockout = max(0, self.stock_regressor.predict(features)[0])
            except Exception as e:
                print(f"ML prediction failed, using fallback: {e}")
                # Fallback calculation
                days_until_stockout = item_data['quantity_available'] / avg_usage if avg_usage > 0 else 999
                is_at_risk = days_until_stockout < item_data['lead_time_days']
                probability = min(1.0, item_data['lead_time_days'] / max(days_until_stockout, 0.1))
        else:
            # Fallback: Simple calculation when models aren't available
            days_until_stockout = item_data['quantity_available'] / avg_usage if avg_usage > 0 else 999
            is_at_risk = days_until_stockout < item_data['lead_time_days'] or stock_ratio < 1
            probability = min(1.0, item_data['lead_time_days'] / max(days_until_stockout, 0.1))
        
        return {
            'prediction_type': 'usage_based',
            'at_risk': bool(is_at_risk),
            'stockout_probability': round(float(probability), 3),
            'days_until_stockout': round(float(days_until_stockout), 1),
            'recommendation': 'REORDER NOW' if is_at_risk else 'Stock OK'
        }
    
    def predict_disease_demand(self, admissions=None):
        """
        Predict medicine demand based on patient admissions.
        
        Can work in two modes:
        1. Automatic: No params, fetches from database
        2. Manual: Pass admissions dict (for testing/override)
        """
        # Get from database if not provided
        if admissions is None:
            admissions = self.get_current_admissions_from_db()
        
        # Calculate demand using disease-medicine mapping
        demand = {}
        for disease, count in admissions.items():
            if disease in DISEASE_MEDICINE_MAP:
                mapping = DISEASE_MEDICINE_MAP[disease]
                for med, qty in zip(mapping['medicines'], mapping['avg_qty_per_patient']):
                    demand[med] = demand.get(med, 0) + (count * qty)
        
        return {
            'prediction_type': 'disease_based',
            'current_admissions': admissions,
            'total_patients': sum(admissions.values()),
            'predicted_demand': dict(sorted(demand.items(), key=lambda x: x[1], reverse=True))
        }
    
    # =========================================================================
    # UNIFIED PREDICTION - COMBINES BOTH MODELS
    # =========================================================================
    
    def get_unified_prediction(self, item_id=None, item_name=None):
        """
        Get combined prediction from BOTH models.
        
        Returns:
        - Usage-based stockout prediction (Model 2)
        - Disease-based demand prediction (Model 3)
        - Combined risk assessment
        - Final recommendation
        """
        from apps.authentication.models import InventoryItem
        
        # Get item
        if item_id:
            item = InventoryItem.objects.get(item_id=item_id)
        elif item_name:
            item = InventoryItem.objects.get(item_name__icontains=item_name)
        else:
            raise ValueError("Provide item_id or item_name")
        
        # === Model 2: Usage-Based Prediction ===
        usage_prediction = self.predict_stock_depletion(item_id=item.item_id)
        
        # === Model 3: Disease-Based Prediction ===
        disease_prediction = self.predict_disease_demand()
        disease_demand = disease_prediction['predicted_demand'].get(item.item_name, 0)
        
        # === Combined Analysis ===
        current_stock = item.quantity_available
        
        # Days of stock based on disease demand
        if disease_demand > 0:
            days_based_on_disease = (current_stock / disease_demand) * 7  # Weekly demand
        else:
            days_based_on_disease = 999
        
        # Combined risk score (average of both predictions)
        usage_risk = usage_prediction['stockout_probability']
        disease_risk = 1.0 if days_based_on_disease < 7 else (7 / days_based_on_disease) if days_based_on_disease < 14 else 0.2
        combined_risk = (usage_risk + disease_risk) / 2
        
        # Determine final recommendation
        if combined_risk > 0.7:
            final_recommendation = 'CRITICAL: Reorder immediately'
            urgency = 'HIGH'
        elif combined_risk > 0.4:
            final_recommendation = 'WARNING: Plan to reorder soon'
            urgency = 'MEDIUM'
        else:
            final_recommendation = 'OK: Stock levels adequate'
            urgency = 'LOW'
        
        # Get category name (it's a CharField, not ForeignKey)
        category_name = item.category if item.category else 'Unknown'
        
        return {
            'item': {
                'id': item.item_id,
                'name': item.item_name,
                'category': category_name,
                'current_stock': current_stock,
                'reorder_level': item.reorder_level
            },
            'usage_based_prediction': {
                'days_until_stockout': usage_prediction['days_until_stockout'],
                'stockout_probability': usage_prediction['stockout_probability'],
                'based_on': 'Historical usage patterns (last 30 days)'
            },
            'disease_based_prediction': {
                'expected_demand_this_week': disease_demand,
                'days_of_stock': round(days_based_on_disease, 1),
                'based_on': f"Current admissions ({disease_prediction['total_patients']} patients)"
            },
            'combined_analysis': {
                'combined_risk_score': round(combined_risk, 3),
                'urgency': urgency,
                'recommendation': final_recommendation
            }
        }
    
    def get_all_alerts(self):
        """
        Scan entire inventory and return all items needing attention.
        Fully automatic - pulls all data from database.
        """
        from apps.authentication.models import InventoryItem
        
        alerts = []
        
        for item in InventoryItem.objects.all():
            try:
                prediction = self.get_unified_prediction(item_id=item.item_id)
                
                if prediction['combined_analysis']['urgency'] in ['HIGH', 'MEDIUM']:
                    # Get category name (it's a CharField, not ForeignKey)
                    category_name = item.category if item.category else 'Unknown'
                    
                    alerts.append({
                        'item_id': item.item_id,
                        'item_name': item.item_name,
                        'category': category_name,
                        'current_stock': item.quantity_available,
                        'urgency': prediction['combined_analysis']['urgency'],
                        'combined_risk': prediction['combined_analysis']['combined_risk_score'],
                        'usage_days_left': prediction['usage_based_prediction']['days_until_stockout'],
                        'disease_demand': prediction['disease_based_prediction']['expected_demand_this_week'],
                        'recommendation': prediction['combined_analysis']['recommendation']
                    })
            except Exception as e:
                print(f"Error processing {item.name}: {e}")
                continue
        
        # Sort by risk score (highest first)
        alerts.sort(key=lambda x: x['combined_risk'], reverse=True)
        
        return {
            'total_items_scanned': InventoryItem.objects.count(),
            'items_needing_attention': len(alerts),
            'high_priority': len([a for a in alerts if a['urgency'] == 'HIGH']),
            'medium_priority': len([a for a in alerts if a['urgency'] == 'MEDIUM']),
            'alerts': alerts
        }


# =============================================================================
# DJANGO VIEW FUNCTIONS
# =============================================================================

def get_predictor():
    """Get singleton predictor instance."""
    if not hasattr(get_predictor, '_instance'):
        get_predictor._instance = UnifiedInventoryPredictor()
    return get_predictor._instance
