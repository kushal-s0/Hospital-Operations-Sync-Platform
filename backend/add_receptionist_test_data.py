"""
Add test data for receptionist dashboard (SIMPLIFIED)
"""
import os
import sys
import django
from datetime import datetime, timedelta
import random

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from django.db import connection

def add_receptionist_test_data():
    """Add sample data for receptionist dashboard"""
    
    print("=" * 60)
    print("ADDING RECEPTIONIST TEST DATA")
    print("=" * 60)
    
    cursor = connection.cursor()
    
    # Get existing patients
    cursor.execute("SELECT patient_id FROM patients LIMIT 15")
    patient_ids = [row[0] for row in cursor.fetchall()]
    
    if not patient_ids:
        print(" No patients found. Cannot proceed with test data.")
        return
    
    print(f"\n Found {len(patient_ids)} patients to work with")
    
    # Get max IDs
    cursor.execute("SELECT MAX(bill_id) FROM billing")
    max_bill = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT MAX(transaction_id) FROM financial_transactions")
    max_transaction = cursor.fetchone()[0] or 0
    
    cursor.execute("SELECT hospital_id FROM hospitals LIMIT 1")
    hospital_result = cursor.fetchone()
    hospital_id = hospital_result[0] if hospital_result else 1
    
    # Add test billing records
    print("\n Adding billing records...")
    payment_methods = ['Cash', 'Card', 'Insurance']
    payment_statuses = ['Paid', 'Pending', 'Failed']
    
    for i in range(15):
        bill_id = max_bill + i + 1
        patient_id = random.choice(patient_ids)
        amount = random.randint(1000, 50000)
        method = random.choice(payment_methods)
        status = random.choice(payment_statuses)
        
        cursor.execute("""
            INSERT INTO billing (bill_id, patient_id, bill_date, amount, payment_method, payment_status)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, [bill_id, patient_id, datetime.now().date(), amount, method, status])
    
    print(f" Added 15 billing records")
    
    # Add test financial transactions
    print("\n Adding financial transactions...")
    reference_types = ['Billing', 'Inventory', 'Salary', 'Maintenance', 'Other']
    transaction_types = ['INCOME', 'EXPENSE']
    payment_types = ['Cash', 'Card', 'Insurance', 'UPI', 'Bank']
    
    for i in range(20):
        trans_id = max_transaction + i + 1
        ref_type = random.choice(reference_types)
        trans_type = random.choice(transaction_types)
        payment = random.choice(payment_types)
        amount = random.randint(5000, 100000)
        date = datetime.now() - timedelta(days=random.randint(1, 30))
        
        cursor.execute("""
            INSERT INTO financial_transactions (transaction_id, hospital_id, reference_type, transaction_type, amount, payment_method, transaction_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """, [trans_id, hospital_id, ref_type, trans_type, amount, payment, date])
    
    print(f" Added 20 financial transactions")
    
    # Commit all changes
    connection.commit()
    
    print("\n" + "=" * 60)
    print(" TEST DATA SUCCESSFULLY ADDED!")
    print("=" * 60)
    print("\n Summary:")
    print(f"   Billing Records: +15 added")
    print(f"   Financial Transactions: +20 added")
    print(f"\n Login Credentials (Receptionist):")
    print(f"   Username: receptionist")
    print(f"   Password: password123")
    print(f"\n Access Dashboard at: http://localhost:3000/receptionist")
    print("\nReload the browser to see the updated data!")

if __name__ == '__main__':
    add_receptionist_test_data()
