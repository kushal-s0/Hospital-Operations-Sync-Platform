from django.contrib import admin
from .models import InventoryCategory, InventoryItem, InventoryTransaction

@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'sku', 'item_type', 'current_stock', 'minimum_stock', 'is_low_stock']
    list_filter = ['item_type', 'category']
    search_fields = ['name', 'sku']

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction_type', 'quantity', 'performed_by', 'created_at']
    list_filter = ['transaction_type', 'created_at']
