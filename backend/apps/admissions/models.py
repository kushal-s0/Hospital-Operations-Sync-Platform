from django.db import models
# Import models from authentication to use the MySQL-mapped versions
from apps.authentication.models import Patient, Bed, Admission


# Re-export for backwards compatibility
__all__ = ['Admission']


class AdmissionRule(models.Model):
    """Model for rule-based admission workflow."""
    
    CONDITION_CHOICES = [
        ('Critical', 'Critical'),
        ('High', 'High'),
        ('Medium', 'Medium'),
        ('Low', 'Low'),
    ]
    
    BED_TYPE_CHOICES = [
        ('Normal', 'Normal'),
        ('ICU', 'ICU'),
        ('Ventilator', 'Ventilator'),
        ('Emergency', 'Emergency'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    condition = models.TextField(help_text="Rule condition in JSON format")
    recommended_bed_type = models.CharField(max_length=50, choices=BED_TYPE_CHOICES)
    recommended_department = models.CharField(max_length=100)
    priority = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-priority']
    
    def __str__(self):
        return self.name
