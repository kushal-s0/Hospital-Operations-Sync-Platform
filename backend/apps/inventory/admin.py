from django.contrib import admin
from apps.authentication.models import InventoryItem
from .models import InventoryCategory, InventoryTransaction

@admin.register(InventoryCategory)
class InventoryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['item_id', 'item_name', 'category', 'quantity_available', 'reorder_level', 'supplier']
    list_filter = ['category']
    search_fields = ['item_name']

@admin.register(InventoryTransaction)
class InventoryTransactionAdmin(admin.ModelAdmin):
    list_display = ['item', 'transaction_type', 'quantity', 'performed_by', 'created_at']
    list_filter = ['transaction_type', 'created_at']
