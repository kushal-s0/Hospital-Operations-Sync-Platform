"""
Script to create payment_transactions table using Django database connection
Run this if MySQL command-line client is not available
"""

import os
import django
import sys

# Setup Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

# SQL to create payment_transactions table
CREATE_TABLE_SQL = """
CREATE TABLE IF NOT EXISTS payment_transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT NOT NULL,
    razorpay_order_id VARCHAR(100) NOT NULL UNIQUE,
    razorpay_payment_id VARCHAR(100) NULL,
    razorpay_signature VARCHAR(255) NULL,
    amount DECIMAL(10, 2) NOT NULL,
    currency VARCHAR(10) DEFAULT 'INR',
    status VARCHAR(20) NOT NULL DEFAULT 'created',
    payment_method VARCHAR(50) NULL,
    error_code VARCHAR(50) NULL,
    error_description TEXT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    
    FOREIGN KEY (bill_id) REFERENCES billing(bill_id) ON DELETE CASCADE,
    INDEX idx_bill_id (bill_id),
    INDEX idx_razorpay_order_id (razorpay_order_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
"""

def create_payment_table():
    """Create payment_transactions table"""
    try:
        with connection.cursor() as cursor:
            print("Creating payment_transactions table...")
            cursor.execute(CREATE_TABLE_SQL)
            print("✓ Table created successfully!")
            
            # Verify table creation
            cursor.execute("SHOW TABLES LIKE 'payment_transactions';")
            result = cursor.fetchone()
            
            if result:
                print("✓ Table verified: payment_transactions exists")
                
                # Show table structure
                cursor.execute("DESCRIBE payment_transactions;")
                columns = cursor.fetchall()
                
                print("\nTable Structure:")
                print("-" * 80)
                for col in columns:
                    print(f"  {col[0]:<25} {col[1]:<20} {col[2]:<10}")
                print("-" * 80)
            else:
                print("✗ Table verification failed")
                return False
                
        return True
        
    except Exception as e:
        print(f"✗ Error creating table: {str(e)}")
        return False

if __name__ == "__main__":
    print("=" * 80)
    print("Payment Transactions Table Creation Script")
    print("=" * 80)
    print()
    
    success = create_payment_table()
    
    print()
    if success:
        print("=" * 80)
        print("SUCCESS! payment_transactions table is ready")
        print("=" * 80)
        print()
        print("Next steps:")
        print("1. pip install razorpay")
        print("2. python manage.py makemigrations payments")
        print("3. python manage.py migrate")
        print("4. python manage.py runserver")
    else:
        print("=" * 80)
        print("FAILED! Please check the error above and try again")
        print("=" * 80)
