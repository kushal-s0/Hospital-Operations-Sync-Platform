"""
Script to add expiry_date and unit_price columns to inventory_items table using raw SQL
"""
import os
import sys
import django

# Setup Django
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection

def add_columns():
    """Add expiry_date and unit_price columns to inventory_items table"""
    
    with connection.cursor() as cursor:
        print("Connected to database successfully!")
        
        # Check if columns already exist
        cursor.execute("DESCRIBE inventory_items")
        columns = [col[0] for col in cursor.fetchall()]
        print(f"\nCurrent columns: {', '.join(columns)}")
        
        # Add unit_price column if not exists
        if 'unit_price' not in columns:
            print("\n➤ Adding unit_price column...")
            try:
                cursor.execute("""
                    ALTER TABLE inventory_items
                    ADD COLUMN unit_price DECIMAL(10,2) NULL
                """)
                print("✓ unit_price column added successfully!")
            except Exception as e:
                print(f"✗ Error adding unit_price: {e}")
        else:
            print("\n✓ unit_price column already exists")
        
        # Add expiry_date column if not exists
        if 'expiry_date' not in columns:
            print("\n➤ Adding expiry_date column...")
            try:
                cursor.execute("""
                    ALTER TABLE inventory_items
                    ADD COLUMN expiry_date DATE NULL
                """)
                print("✓ expiry_date column added successfully!")
            except Exception as e:
                print(f"✗ Error adding expiry_date: {e}")
        else:
            print("\n✓ expiry_date column already exists")
        
        # Update some sample data
        print("\n➤ Updating sample data with expiry dates and prices...")
        
        try:
            cursor.execute("""
                UPDATE inventory_items 
                SET expiry_date = '2026-12-31', unit_price = 5.50 
                WHERE category = 'Medicine' AND expiry_date IS NULL 
                LIMIT 3
            """)
            print(f"✓ Updated {cursor.rowcount} Medicine items")
        except Exception as e:
            print(f"Note: {e}")
        
        try:
            cursor.execute("""
                UPDATE inventory_items 
                SET expiry_date = '2027-06-30', unit_price = 15.00 
                WHERE category = 'Consumable' AND expiry_date IS NULL 
                LIMIT 3
            """)
            print(f"✓ Updated {cursor.rowcount} Consumable items")
        except Exception as e:
            print(f"Note: {e}")
        
        try:
            cursor.execute("""
                UPDATE inventory_items 
                SET unit_price = 250.00 
                WHERE category = 'Equipment' AND unit_price IS NULL 
                LIMIT 2
            """)
            print(f"✓ Updated {cursor.rowcount} Equipment items")
        except Exception as e:
            print(f"Note: {e}")
        
        # Verify changes
        print("\n" + "="*60)
        print("➤ Verifying table structure...")
        cursor.execute("DESCRIBE inventory_items")
        print("\nUpdated columns:")
        for col in cursor.fetchall():
            print(f"  • {col[0]:<20} {col[1]:<20} {col[2]}")
        
        print("\n" + "="*60)
        print("➤ Sample inventory data:")
        cursor.execute("""
            SELECT item_id, item_name, category, unit_price, expiry_date 
            FROM inventory_items 
            LIMIT 5
        """)
        for row in cursor.fetchall():
            price = f"${row[3]:.2f}" if row[3] else "N/A"
            expiry = row[4] if row[4] else "No expiry"
            print(f"  ID:{row[0]:3} | {row[1]:<25} | {row[2]:<12} | {price:<8} | {expiry}")
        
        print("\n" + "="*60)
        print("✓ All changes completed successfully!")
        print("\nYou can now:")
        print("  1. Restart the Django server")
        print("  2. Refresh the frontend to see expiry dates")

if __name__ == '__main__':
    try:
        add_columns()
    except Exception as e:
        print(f"\n✗ Error: {e}")
        import traceback
        traceback.print_exc()
