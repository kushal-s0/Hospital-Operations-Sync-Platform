from django.db import models


class Department(models.Model):
    """Model representing a hospital department."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    floor = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name


class Bed(models.Model):
    """Model representing a hospital bed."""
    
    BED_STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('reserved', 'Reserved'),
    ]
    
    BED_TYPE_CHOICES = [
        ('general', 'General'),
        ('icu', 'ICU'),
        ('private', 'Private'),
        ('semi_private', 'Semi-Private'),
        ('pediatric', 'Pediatric'),
        ('maternity', 'Maternity'),
    ]
    
    bed_number = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='beds')
    bed_type = models.CharField(max_length=20, choices=BED_TYPE_CHOICES, default='general')
    status = models.CharField(max_length=20, choices=BED_STATUS_CHOICES, default='available')
    floor = models.IntegerField()
    room_number = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['bed_number']
    
    def __str__(self):
        return f"Bed {self.bed_number} - {self.department.name}"
