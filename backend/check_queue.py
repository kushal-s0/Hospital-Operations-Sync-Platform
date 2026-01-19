import os, sys, django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()
from apps.opd.models import OPDQueue
from django.utils import timezone

today = timezone.now()
print(f'Today: {today.date()}')
print(f'Total queue: {OPDQueue.objects.count()}')
print(f'Waiting status: {OPDQueue.objects.filter(status="waiting").count()}')
print(f'Today filter: {OPDQueue.objects.filter(created_at__date=today.date()).count()}')
print(f'Today + waiting: {OPDQueue.objects.filter(created_at__date=today.date(), status="waiting").count()}')
print('\nQueue entries:')
for q in OPDQueue.objects.all():
    print(f'  Token {q.token_number}: status={q.status}, created={q.created_at}')
