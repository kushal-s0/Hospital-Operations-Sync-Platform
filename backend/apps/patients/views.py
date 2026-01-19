from rest_framework import viewsets
from .models import Patient
from .serializers import PatientSerializer


class PatientViewSet(viewsets.ModelViewSet):
    """ViewSet for Patient CRUD operations."""
    
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
