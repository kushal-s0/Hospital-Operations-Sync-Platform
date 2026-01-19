from django.db import models


class Hospital(models.Model):
    """Model representing a hospital in the network."""
    
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    address = models.TextField()
    city = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    api_endpoint = models.URLField(blank=True, help_text="API endpoint for capacity data")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name


class CapacitySnapshot(models.Model):
    """Model for storing anonymized capacity snapshots for city dashboard."""
    
    hospital = models.ForeignKey(Hospital, on_delete=models.CASCADE, related_name='capacity_snapshots')
    total_beds = models.IntegerField()
    available_beds = models.IntegerField()
    icu_beds_total = models.IntegerField(default=0)
    icu_beds_available = models.IntegerField(default=0)
    emergency_load = models.IntegerField(default=0, help_text="Current emergency patients")
    opd_load = models.IntegerField(default=0, help_text="Current OPD queue length")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']
        get_latest_by = 'timestamp'
    
    def __str__(self):
        return f"{self.hospital.name} - {self.timestamp}"
