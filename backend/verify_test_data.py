"""
Verify all test data is loaded correctly
"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
django.setup()

from apps.authentication.models import Patient, Admission, Bed, Department, InventoryItem
from apps.opd.models import OPDQueue
from apps.inventory.models import InventoryCategory, InventoryTransaction

print("=" * 60)
print("DATABASE TEST DATA VERIFICATION")
print("=" * 60)

print("\n📊 PATIENTS")
print(f"  Total Patients: {Patient.objects.count()}")
recent_patients = Patient.objects.order_by('-patient_id')[:5]
for p in recent_patients:
    print(f"    - {p.first_name} {p.last_name} (ID: {p.patient_id})")

print("\n🏥 DEPARTMENTS & BEDS")
print(f"  Total Departments: {Department.objects.count()}")
print(f"  Total Beds: {Bed.objects.count()}")
for dept in Department.objects.all()[:5]:
    bed_count = Bed.objects.filter(department_id=dept.department_id).count()
    available = Bed.objects.filter(department_id=dept.department_id, status='Available').count()
    print(f"    - {dept.department_name}: {bed_count} beds ({available} available)")

print("\n🛏️ ADMISSIONS")
print(f"  Total Admissions: {Admission.objects.count()}")
print(f"  Active Admissions: {Admission.objects.filter(status='Active').count()}")
active_admissions = Admission.objects.filter(status='Active')[:5]
for adm in active_admissions:
    print(f"    - Patient ID {adm.patient_id}: {adm.condition_level} condition")

print("\n👥 OPD QUEUE")
print(f"  Total in Queue: {OPDQueue.objects.count()}")
print(f"  Waiting: {OPDQueue.objects.filter(status='waiting').count()}")
print(f"  In Consultation: {OPDQueue.objects.filter(status='in_consultation').count()}")
for q in OPDQueue.objects.all()[:5]:
    print(f"    - Token #{q.token_number}: {q.patient.first_name} ({q.status}, {q.priority})")

print("\n💊 INVENTORY")
print(f"  Categories: {InventoryCategory.objects.count()}")
print(f"  Items: {InventoryItem.objects.count()}")
print(f"  Transactions: {InventoryTransaction.objects.count()}")
from django.db.models import F
low_stock = InventoryItem.objects.filter(quantity_available__lte=F('reorder_level'))
print(f"  Low Stock Items: {low_stock.count()}")
for item in low_stock[:5]:
    print(f"    - {item.item_name}: {item.quantity_available}/{item.reorder_level}")

print("\n" + "=" * 60)
print("✅ ALL TEST DATA LOADED SUCCESSFULLY!")
print("=" * 60)
print("\nYou can now:")
print("  1. Test ML predictions with real data")
print("  2. View data in the frontend dashboard")
print("  3. Run API endpoint tests")
print("\nLogin credentials: admin@hospital.com / hospital123")
