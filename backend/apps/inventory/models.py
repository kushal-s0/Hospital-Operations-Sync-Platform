from django.db import models


class InventoryCategory(models.Model):
    """Model representing inventory category."""
    
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = "Inventory Categories"
    
    def __str__(self):
        return self.name


class InventoryItem(models.Model):
    """Model representing an inventory item (medicine/consumable)."""
    
    ITEM_TYPE_CHOICES = [
        ('medicine', 'Medicine'),
        ('consumable', 'Consumable'),
        ('equipment', 'Equipment'),
        ('surgical', 'Surgical Supplies'),
    ]
    
    name = models.CharField(max_length=200)
    category = models.ForeignKey(InventoryCategory, on_delete=models.CASCADE, related_name='items')
    item_type = models.CharField(max_length=20, choices=ITEM_TYPE_CHOICES)
    sku = models.CharField(max_length=50, unique=True)
    unit = models.CharField(max_length=50, help_text="e.g., tablets, ml, pieces")
    current_stock = models.IntegerField(default=0)
    minimum_stock = models.IntegerField(default=10, help_text="Low stock alert threshold")
    maximum_stock = models.IntegerField(default=1000)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date = models.DateField(null=True, blank=True)
    supplier = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=100, blank=True, help_text="Storage location")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.sku})"
    
    @property
    def is_low_stock(self):
        return self.current_stock <= self.minimum_stock


class InventoryTransaction(models.Model):
    """Model for tracking inventory usage/restocking."""
    
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
        return f"{self.transaction_type} - {self.item.name} ({self.quantity})"
