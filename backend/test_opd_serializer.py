import os
import sys
import django

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from apps.authentication.models import OPDQueue, Appointment
from apps.opd.serializers import OPDQueueSerializer
import json

print("\n" + "="*60)
print("OPD QUEUE SERIALIZER TEST")
print("="*60)

# Get all OPD queue entries
queue_entries = OPDQueue.objects.all().order_by('-id')[:5]

print(f"\nFound {queue_entries.count()} entries\n")

for entry in queue_entries:
    serializer = OPDQueueSerializer(entry)
    print(f"Token #{entry.token_number}:")
    print(json.dumps(serializer.data, indent=2, default=str))
    print("-" * 60)

