from django.db import models
# Import models from authentication to use the MySQL-mapped versions
from apps.authentication.models import InventoryItem, InventoryUsage


# Re-export for backwards compatibility
__all__ = ['InventoryItem', 'InventoryUsage', 'InventoryCategory', 'InventoryTransaction']


class InventoryCategory(models.Model):
    """Model representing inventory category (local model for additional categorization)."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Inventory Categories"
    
    def __str__(self):
        return self.name


class InventoryTransaction(models.Model):
    """Model for tracking inventory transactions (local model for detailed tracking)."""
    
    TRANSACTION_TYPE_CHOICES = [
        ('in', 'Stock In'),
        ('out', 'Stock Out'),
        ('adjustment', 'Adjustment'),
    ]
    
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPE_CHOICES)
    quantity = models.IntegerField()
    reference = models.CharField(max_length=100, blank=True, help_text="Admission ID or PO number")
    notes = models.TextField(blank=True)
    performed_by = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.transaction_type} - {self.item.item_name} ({self.quantity})"
