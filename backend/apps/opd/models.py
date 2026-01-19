from django.db import models
from apps.authentication.models import Patient, Visit, Appointment


# Re-export for backwards compatibility
__all__ = ['OPDQueue', 'OPDStatistics', 'Visit', 'Appointment']


class OPDQueue(models.Model):
    """Model representing an OPD queue entry."""
    
    STATUS_CHOICES = [
        ('waiting', 'Waiting'),
        ('in_consultation', 'In Consultation'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('normal', 'Normal'),
        ('urgent', 'Urgent'),
        ('emergency', 'Emergency'),
    ]
    
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='opd_visits')
    token_number = models.IntegerField()
    department = models.CharField(max_length=100)
    doctor_name = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='waiting')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')
    check_in_time = models.DateTimeField(auto_now_add=True)
    consultation_start_time = models.DateTimeField(null=True, blank=True)
    consultation_end_time = models.DateTimeField(null=True, blank=True)
    estimated_wait_time = models.IntegerField(default=0, help_text="Estimated wait time in minutes")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['priority', 'check_in_time']
    
    def __str__(self):
        return f"Token #{self.token_number} - {self.patient}"


class OPDStatistics(models.Model):
    """Model for storing OPD historical statistics."""
    
    date = models.DateField()
    department = models.CharField(max_length=100)
    total_patients = models.IntegerField(default=0)
    average_wait_time = models.FloatField(default=0, help_text="Average wait time in minutes")
    average_consultation_time = models.FloatField(default=0, help_text="Average consultation time in minutes")
    peak_hour = models.IntegerField(null=True, blank=True, help_text="Hour with maximum patients (0-23)")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['date', 'department']
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.department} - {self.date}"
