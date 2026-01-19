from django.db import models
from apps.authentication.models import Patient, Visit, Appointment, OPDQueue


# Re-export for backwards compatibility
__all__ = ['OPDQueue', 'OPDStatistics', 'Visit', 'Appointment']


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
