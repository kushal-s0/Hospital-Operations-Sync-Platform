"""
Profit/Loss Prediction System for Receptionist Dashboard
=========================================================
Uses pre-trained ML models to predict profit/loss based on 
financial transaction patterns and historical data.
"""

import joblib
import numpy as np
import warnings
from datetime import datetime, timedelta
from django.db import connection
import os

# Suppress sklearn warnings
warnings.filterwarnings('ignore', message='X does not have valid feature names')

# Path to saved models
MODELS_DIR = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'models')


class ProfitLossPredictor:
    """
    Predicts profit/loss areas using pre-trained ML models.
    Extracts features from financial_transactions table.
    """
    
    def __init__(self):
        self.profit_model = None
        self.loss_area_model = None
        self.models_loaded = False
        self._load_models()
    
    def _load_models(self):
        """Load pre-trained models from disk."""
        try:
            profit_model_path = os.path.join(MODELS_DIR, 'profit_model.pkl')
            loss_model_path = os.path.join(MODELS_DIR, 'loss_area_model.pkl')
            
            self.profit_model = joblib.load(profit_model_path)
            self.loss_area_model = joblib.load(loss_model_path)
            self.models_loaded = True
            print("[OK] Profit/Loss models loaded successfully")
        except FileNotFoundError as e:
            print(f"[WARNING] Model not found: {e}. Will use fallback calculations.")
            self.models_loaded = False
    
    def extract_features_from_db(self):
        """
        Extract financial features from database for prediction.
        
        Features extracted:
        - Total income and expenses
        - Number of transactions
        - Income/expense ratio
        - Average transaction amount
        - Transaction volatility
        - Recent trends (7, 14, 30 days)
        """
        cursor = connection.cursor()
        
        try:
            # Get transaction statistics
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN transaction_type='INCOME' THEN amount ELSE 0 END), 0) as total_income,
                    COALESCE(SUM(CASE WHEN transaction_type='EXPENSE' THEN amount ELSE 0 END), 0) as total_expense,
                    COUNT(CASE WHEN transaction_type='INCOME' THEN 1 END) as income_count,
                    COUNT(CASE WHEN transaction_type='EXPENSE' THEN 1 END) as expense_count,
                    COUNT(*) as total_count,
                    AVG(amount) as avg_amount,
                    STDDEV(amount) as stddev_amount
                FROM financial_transactions
            """)
            overall_stats = cursor.fetchone()
            
            # Get 7-day trend
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN transaction_type='INCOME' THEN amount ELSE 0 END), 0) as income_7d,
                    COALESCE(SUM(CASE WHEN transaction_type='EXPENSE' THEN amount ELSE 0 END), 0) as expense_7d
                FROM financial_transactions
                WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            """)
            trend_7d = cursor.fetchone()
            
            # Get 30-day trend
            cursor.execute("""
                SELECT 
                    COALESCE(SUM(CASE WHEN transaction_type='INCOME' THEN amount ELSE 0 END), 0) as income_30d,
                    COALESCE(SUM(CASE WHEN transaction_type='EXPENSE' THEN amount ELSE 0 END), 0) as expense_30d
                FROM financial_transactions
                WHERE transaction_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            """)
            trend_30d = cursor.fetchone()
            
            # Get billing statistics
            cursor.execute("""
                SELECT 
                    COUNT(CASE WHEN payment_status='Paid' THEN 1 END) as paid_bills,
                    COUNT(CASE WHEN payment_status='Pending' THEN 1 END) as pending_bills,
                    COUNT(CASE WHEN payment_status='Failed' THEN 1 END) as failed_bills,
                    COALESCE(SUM(CASE WHEN payment_status='Paid' THEN amount ELSE 0 END), 0) as paid_amount
                FROM billing
            """)
            billing_stats = cursor.fetchone()
            
            # Extract individual features
            total_income = float(overall_stats[0]) if overall_stats else 0.0
            total_expense = float(overall_stats[1]) if overall_stats else 0.0
            income_count = overall_stats[2] if overall_stats else 0
            expense_count = overall_stats[3] if overall_stats else 0
            total_count = overall_stats[4] if overall_stats else 1
            avg_amount = float(overall_stats[5]) if overall_stats and overall_stats[5] else 0.0
            stddev_amount = float(overall_stats[6]) if overall_stats and overall_stats[6] else 0.0
            
            income_7d = float(trend_7d[0]) if trend_7d else 0.0
            expense_7d = float(trend_7d[1]) if trend_7d else 0.0
            
            income_30d = float(trend_30d[0]) if trend_30d else 0.0
            expense_30d = float(trend_30d[1]) if trend_30d else 0.0
            
            paid_bills = billing_stats[0] if billing_stats else 0
            pending_bills = billing_stats[1] if billing_stats else 0
            failed_bills = billing_stats[2] if billing_stats else 0
            paid_amount = float(billing_stats[3]) if billing_stats else 0.0
            
            # Calculate derived features
            current_profit = total_income - total_expense
            income_to_expense_ratio = total_income / max(total_expense, 1)
            expense_percentage = (total_expense / max(total_income, 1)) * 100
            
            profit_7d = income_7d - expense_7d
            profit_30d = income_30d - expense_30d
            
            transaction_diversity = income_count + expense_count if (income_count + expense_count) > 0 else 1
            expense_frequency = expense_count / max(total_count, 1)
            
            bill_collection_rate = paid_bills / max((paid_bills + pending_bills + failed_bills), 1) * 100
            failed_rate = failed_bills / max((paid_bills + pending_bills + failed_bills), 1) * 100
            
            # Feature vector for model
            features = np.array([
                total_income,           # 0: Total income so far
                total_expense,          # 1: Total expenses so far
                current_profit,         # 2: Current profit
                income_to_expense_ratio,# 3: Income to expense ratio
                expense_percentage,     # 4: Expense as % of income
                income_7d,              # 5: 7-day income
                expense_7d,             # 6: 7-day expense
                profit_7d,              # 7: 7-day profit
                income_30d,             # 8: 30-day income
                expense_30d,            # 9: 30-day expense
                profit_30d,             # 10: 30-day profit
                avg_amount,             # 11: Average transaction amount
                stddev_amount,          # 12: Transaction volatility
                transaction_diversity,  # 13: Total transaction count
                expense_frequency,      # 14: Expense frequency
                bill_collection_rate,   # 15: Bill collection rate
                failed_rate,            # 16: Failed bill rate
                paid_amount,            # 17: Paid billing amount
            ]).reshape(1, -1)
            
            return features, {
                'current_profit': current_profit,
                'total_income': total_income,
                'total_expense': total_expense,
                'income_7d': income_7d,
                'expense_7d': expense_7d,
                'profit_7d': profit_7d,
                'income_30d': income_30d,
                'expense_30d': expense_30d,
                'profit_30d': profit_30d,
                'collection_rate': bill_collection_rate,
            }
        
        except Exception as e:
            print(f"[ERROR] Error extracting features: {e}")
            # Return zero features if error
            return np.zeros((1, 18)), {
                'current_profit': 0.0,
                'total_income': 0.0,
                'total_expense': 0.0,
            }
    
    def predict_profit_loss(self):
        """
        Predict profit/loss using ML models.
        
        Returns:
        dict: {
            'predicted_profit': float,
            'profit_confidence': float,
            'loss_area': str,
            'loss_confidence': float,
            'recommendations': list,
            'metrics': dict
        }
        """
        features, metrics = self.extract_features_from_db()
        
        result = {
            'predicted_profit': metrics['current_profit'],
            'profit_confidence': 0.0,
            'loss_area': 'Normal',
            'loss_confidence': 0.0,
            'recommendations': [],
            'metrics': metrics,
        }
        
        try:
            if not self.models_loaded:
                # Fallback: Use current profit/loss without ML prediction
                result['recommendations'] = self._generate_fallback_recommendations(metrics)
                return result
            
            # Predict profit using profit model
            profit_prediction = self.profit_model.predict(features)[0]
            result['predicted_profit'] = float(profit_prediction)
            
            # Get confidence from profit model (if it has predict_proba)
            try:
                profit_proba = self.profit_model.predict_proba(features)
                result['profit_confidence'] = float(np.max(profit_proba))
            except AttributeError:
                # Model doesn't have predict_proba
                result['profit_confidence'] = 0.85
            
            # Predict loss area using loss model
            loss_prediction = self.loss_area_model.predict(features)[0]
            loss_areas = ['Normal', 'Inventory Loss', 'Staff Costs', 'Operational', 'Other']
            
            # Map prediction to loss area
            if isinstance(loss_prediction, (int, np.integer)):
                if 0 <= loss_prediction < len(loss_areas):
                    result['loss_area'] = loss_areas[int(loss_prediction)]
            else:
                result['loss_area'] = str(loss_prediction)
            
            # Get confidence from loss model
            try:
                loss_proba = self.loss_area_model.predict_proba(features)
                result['loss_confidence'] = float(np.max(loss_proba))
            except AttributeError:
                result['loss_confidence'] = 0.75
            
            # Generate recommendations
            result['recommendations'] = self._generate_recommendations(
                result['predicted_profit'],
                metrics,
                result['loss_area']
            )
            
        except Exception as e:
            print(f"[WARNING] Error in ML prediction: {e}. Using fallback values.")
            result['recommendations'] = self._generate_fallback_recommendations(metrics)
        
        return result
    
    def _generate_recommendations(self, predicted_profit, metrics, loss_area):
        """Generate business recommendations based on predictions."""
        recommendations = []
        
        current_profit = metrics['current_profit']
        total_income = metrics['total_income']
        total_expense = metrics['total_expense']
        collection_rate = metrics['collection_rate']
        
        # Profit-based recommendations
        if predicted_profit < 0:
            recommendations.append("⚠️ Negative profit predicted - urgent cost review needed")
        elif predicted_profit > 0 and predicted_profit < current_profit * 0.5:
            recommendations.append("📊 Profit trending down - monitor expenses closely")
        
        # Expense-based recommendations
        if total_expense > total_income * 0.8:
            recommendations.append("💰 High expense ratio - consider cost optimization")
        
        # Collection rate recommendations
        if collection_rate < 70:
            recommendations.append("📝 Low bill collection rate - improve follow-up process")
        
        # Loss area specific recommendations
        if loss_area == 'Inventory Loss':
            recommendations.append("📦 Watch inventory management - potential stock loss detected")
        elif loss_area == 'Staff Costs':
            recommendations.append("👥 Review staffing efficiency and payroll optimization")
        elif loss_area == 'Operational':
            recommendations.append("🔧 Operational costs increasing - review operations")
        
        # Positive recommendations
        if predicted_profit > current_profit * 1.1:
            recommendations.append("✅ Profit growth trajectory positive - maintain current strategy")
        
        return recommendations if recommendations else ["✓ Operations normal - continue monitoring"]
    
    def _generate_fallback_recommendations(self, metrics):
        """Generate basic recommendations without ML models."""
        recommendations = []
        
        current_profit = metrics['current_profit']
        total_income = metrics['total_income']
        total_expense = metrics['total_expense']
        
        if current_profit < 0:
            recommendations.append("⚠️ Current operations show negative profit")
        elif current_profit < total_income * 0.2:
            recommendations.append("💰 Profit margin is low - review expenses")
        else:
            recommendations.append("✅ Profit margin is healthy")
        
        if total_expense > total_income * 0.7:
            recommendations.append("📊 Expense ratio is high - optimize operations")
        
        return recommendations


# Global predictor instance
_predictor_instance = None


def get_profit_loss_predictions():
    """Get singleton instance of predictor and return predictions."""
    global _predictor_instance
    
    if _predictor_instance is None:
        _predictor_instance = ProfitLossPredictor()
    
    try:
        return _predictor_instance.predict_profit_loss()
    except Exception as e:
        print(f"[ERROR] Exception in predict_profit_loss: {e}")
        # Return fallback predictions if models fail
        return {
            'predicted_profit': 0.0,
            'profit_confidence': 0.0,
            'loss_area': 'Unable to predict',
            'loss_confidence': 0.0,
            'recommendations': ['Model prediction unavailable - using fallback data'],
            'metrics': {},
        }
