from django.db import models


class PaymentTransaction(models.Model):
    """
    Model to store Razorpay payment transaction details
    
    Database Schema for MySQL:
    
    CREATE TABLE payment_transactions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        bill_id INT NOT NULL,
        razorpay_order_id VARCHAR(100) NOT NULL UNIQUE,
        razorpay_payment_id VARCHAR(100) NULL,
        razorpay_signature VARCHAR(255) NULL,
        amount DECIMAL(10, 2) NOT NULL,
        currency VARCHAR(10) DEFAULT 'INR',
        status VARCHAR(20) NOT NULL DEFAULT 'created',
        payment_method VARCHAR(50) NULL,
        error_code VARCHAR(50) NULL,
        error_description TEXT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (bill_id) REFERENCES billing(bill_id) ON DELETE CASCADE,
        INDEX idx_bill_id (bill_id),
        INDEX idx_razorpay_order_id (razorpay_order_id),
        INDEX idx_status (status)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
    """
    
    STATUS_CHOICES = [
        ('created', 'Created'),
        ('authorized', 'Authorized'),
        ('captured', 'Captured'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    id = models.AutoField(primary_key=True)
    bill_id = models.IntegerField(db_index=True)
    razorpay_order_id = models.CharField(max_length=100, unique=True, db_index=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=255, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=10, default='INR')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='created', db_index=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)
    error_code = models.CharField(max_length=50, null=True, blank=True)
    error_description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payment_transactions'
        ordering = ['-created_at']
        verbose_name = 'Payment Transaction'
        verbose_name_plural = 'Payment Transactions'
    
    def __str__(self):
        return f"Payment {self.razorpay_order_id} - Bill {self.bill_id} - {self.status}"
