"""
Add test inventory data for ML predictions - FIXED VERSION
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.inventory.models import InventoryCategory, InventoryTransaction
from apps.authentication.models import InventoryItem
from django.utils import timezone
from datetime import timedelta
import random

print("Adding test inventory data...")

# Create categories (local model for organization)
categories_data = [
    ('Medicine', 'Pharmaceutical products'),
    ('Consumable', 'Medical consumables'),
    ('Equipment', 'Medical equipment'),
]

categories = {}
for name, desc in categories_data:
    cat, created = InventoryCategory.objects.get_or_create(
        name=name,
        defaults={'description': desc}
    )
    categories[name] = cat
    if created:
        print(f"Created category: {name}")

# Create inventory items using MySQL schema fields
items_data = [
    ('Paracetamol 500mg', 'Medicine', 500, 100),
    ('Surgical Gloves (L)', 'Consumable', 50, 100),
    ('IV Cannula 20G', 'Consumable', 200, 150),
    ('Amoxicillin 250mg', 'Medicine', 30, 50),
    ('Oxygen Mask', 'Equipment', 75, 30),
    ('Surgical Sutures', 'Equipment', 15, 25),
    ('Metformin 500mg', 'Medicine', 80, 100),
    ('Azithromycin 250mg', 'Medicine', 25, 40),
    ('Bandages', 'Consumable', 300, 100),
    ('Syringes 5ml', 'Consumable', 150, 200),
]

# Get next item ID
max_item = InventoryItem.objects.order_by('-item_id').first()
item_id = max_item.item_id + 1 if max_item else 1

for name, cat_name, stock, min_stock in items_data:
    try:
        item, created = InventoryItem.objects.get_or_create(
            item_id=item_id,
            defaults={
                'item_name': name,
                'category': cat_name,
                'quantity_available': stock,
                'reorder_level': min_stock,
                'supplier': 'Medical Supplies Inc.',
            }
        )
        if created:
            item_id += 1
            print(f"Created item: {name} (Stock: {stock})")
        else:
            print(f"Item already exists: {name}")
    except Exception as e:
        print(f"Error creating item {name}: {e}")

# Add some transaction history for better predictions
print("\nAdding transaction history...")
items = InventoryItem.objects.all()
transaction_count = 0

for item in items:
    # Add some OUT transactions over the last 30 days
    for days_ago in range(1, 31):
        if random.random() > 0.3:  # 70% chance of transaction each day
            try:
                qty = random.randint(5, 20)
                trans, created = InventoryTransaction.objects.get_or_create(
                    item=item,
                    transaction_type='out',
                    quantity=qty,
                    reference=f'AUTO-{item.item_id}-{days_ago}',
                    defaults={
                        'notes': f'Auto-generated usage for testing',
                        'performed_by': 'System',
                    }
                )
                if created:
                    transaction_count += 1
            except Exception as e:
                print(f"Error creating transaction: {e}")

print(f"Created {transaction_count} transactions")

print("\n=== Inventory Summary ===")
print(f"Categories: {InventoryCategory.objects.count()}")
print(f"Items: {InventoryItem.objects.count()}")
print(f"Transactions: {InventoryTransaction.objects.count()}")

# Show low stock items
from django.db.models import F
low_stock = InventoryItem.objects.filter(quantity_available__lte=F('reorder_level'))
print(f"\nLow stock items: {low_stock.count()}")
for item in low_stock:
    print(f"  - {item.item_name}: {item.quantity_available}/{item.reorder_level}")

print("\nDone! Now try the inventory predictions.")
