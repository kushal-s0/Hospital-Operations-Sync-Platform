-- Migration SQL for Payment Transactions Table
-- Database: hospital_management
-- Created: For Razorpay Payment Integration

USE hospital_management;

-- Create payment_transactions table
CREATE TABLE IF NOT EXISTS payment_transactions (
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
    
    -- Foreign key constraint
    FOREIGN KEY (bill_id) REFERENCES billing(bill_id) ON DELETE CASCADE,
    
    -- Indexes for better query performance
    INDEX idx_bill_id (bill_id),
    INDEX idx_razorpay_order_id (razorpay_order_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Add comment to table
ALTER TABLE payment_transactions COMMENT = 'Stores Razorpay payment transaction details for billing';

-- Add comments to columns
ALTER TABLE payment_transactions
    MODIFY COLUMN id INT AUTO_INCREMENT PRIMARY KEY COMMENT 'Primary key',
    MODIFY COLUMN bill_id INT NOT NULL COMMENT 'Reference to billing table',
    MODIFY COLUMN razorpay_order_id VARCHAR(100) NOT NULL UNIQUE COMMENT 'Razorpay order ID',
    MODIFY COLUMN razorpay_payment_id VARCHAR(100) NULL COMMENT 'Razorpay payment ID after successful payment',
    MODIFY COLUMN razorpay_signature VARCHAR(255) NULL COMMENT 'Payment signature for verification',
    MODIFY COLUMN amount DECIMAL(10, 2) NOT NULL COMMENT 'Payment amount in INR',
    MODIFY COLUMN currency VARCHAR(10) DEFAULT 'INR' COMMENT 'Payment currency',
    MODIFY COLUMN status VARCHAR(20) NOT NULL DEFAULT 'created' COMMENT 'Payment status: created, authorized, captured, failed, refunded',
    MODIFY COLUMN payment_method VARCHAR(50) NULL COMMENT 'Payment method used: card, netbanking, upi, etc.',
    MODIFY COLUMN error_code VARCHAR(50) NULL COMMENT 'Error code if payment failed',
    MODIFY COLUMN error_description TEXT NULL COMMENT 'Error description if payment failed',
    MODIFY COLUMN created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP COMMENT 'Transaction creation timestamp',
    MODIFY COLUMN updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT 'Last update timestamp';

-- Verify table creation
SELECT 
    'Payment Transactions table created successfully!' AS message,
    COUNT(*) AS record_count
FROM payment_transactions;

-- Display table structure
DESCRIBE payment_transactions;
