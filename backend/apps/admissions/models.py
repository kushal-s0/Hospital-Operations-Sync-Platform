from django.db import models
from apps.patients.models import Patient
from apps.beds.models import Bed


class Admission(models.Model):
    """Model representing a patient admission."""
    
    STATUS_CHOICES = [
        ('admitted', 'Admitted'),
        ('discharged', 'Discharged'),
        ('transferred', 'Transferred'),
    ]
    
    ADMISSION_TYPE_CHOICES = [
        ('emergency', 'Emergency'),
        ('planned', 'Planned'),
        ('transfer', 'Transfer'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='admissions')
    bed = models.ForeignKey(Bed, on_delete=models.SET_NULL, null=True, related_name='admissions')
    admission_type = models.CharField(max_length=20, choices=ADMISSION_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='admitted')
    admission_date = models.DateTimeField(auto_now_add=True)
    discharge_date = models.DateTimeField(null=True, blank=True)
    diagnosis = models.TextField()
    treating_doctor = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-admission_date']
    
    def __str__(self):
        return f"Admission #{self.id} - {self.patient}"


class AdmissionRule(models.Model):
    """Model for rule-based admission workflow."""
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    condition = models.TextField(help_text="Rule condition in JSON format")
    recommended_bed_type = models.CharField(max_length=50)
    recommended_department = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority']
    
    def __str__(self):
        return self.name
