# Razorpay Payment Integration Guide

## Overview
This guide provides complete setup instructions for Razorpay payment integration in the Hospital Management System's Receptionist Billing section.

## Features Implemented

### 1. **Payment Transaction Model**
- Stores complete payment transaction details
- Tracks Razorpay order ID, payment ID, and signature
- Records payment status, method, and error information
- Maintains audit trail with timestamps

### 2. **Backend API Endpoints**

#### a) Create Payment Order
- **Endpoint:** `POST /api/payments/create_order/`
- **Purpose:** Creates a Razorpay order for a pending bill
- **Request Body:**
  ```json
  {
    "bill_id": 123
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "data": {
      "order_id": "order_xxxx",
      "amount": 50000,
      "currency": "INR",
      "bill_id": 123,
      "key": "rzp_test_xxxx"
    }
  }
  ```

#### b) Verify Payment
- **Endpoint:** `POST /api/payments/verify_payment/`
- **Purpose:** Verifies payment signature and updates billing status
- **Request Body:**
  ```json
  {
    "razorpay_order_id": "order_xxxx",
    "razorpay_payment_id": "pay_xxxx",
    "razorpay_signature": "signature_xxxx"
  }
  ```
- **Response:**
  ```json
  {
    "status": "success",
    "message": "Payment verified successfully",
    "data": {
      "bill_id": 123,
      "payment_id": "pay_xxxx",
      "status": "paid"
    }
  }
  ```

#### c) Transaction History
- **Endpoint:** `GET /api/payments/transaction_history/`
- **Query Params:** `?bill_id=123` (optional)
- **Purpose:** Retrieves payment transaction history

#### d) Webhook Handler
- **Endpoint:** `POST /api/payments/handle_webhook/`
- **Purpose:** Handles Razorpay webhook events

### 3. **Frontend Integration**
- Razorpay Checkout integration in billing tab
- Real-time payment processing
- Payment verification and status updates
- User-friendly error handling

### 4. **Database Schema**

The `payment_transactions` table stores:
- Transaction details (order ID, payment ID, signature)
- Amount and currency
- Payment status and method
- Error information (if any)
- Timestamps for audit trail

---

## Setup Instructions

### Step 1: Create Database Table

Run the SQL migration to create the `payment_transactions` table:

```bash
# Navigate to backend directory
cd backend

# Run the SQL file in MySQL
mysql -u root -p hospital_management < create_payment_transactions_table.sql
```

**Or manually execute:**
```sql
USE hospital_management;

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
    
    FOREIGN KEY (bill_id) REFERENCES billing(bill_id) ON DELETE CASCADE,
    INDEX idx_bill_id (bill_id),
    INDEX idx_razorpay_order_id (razorpay_order_id),
    INDEX idx_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Step 2: Verify Environment Variables

Your `.env` file already contains the Razorpay credentials:

```env
RAZORPAY_PUBLIC_KEY=rzp_test_S6EZlI0Lzafb4J
RAZORPAY_SECRET_KEY=6jW2khcl70fj7UrUOVaVsIFT
```

### Step 3: Install Backend Dependencies

The `razorpay` Python package should already be installed. If not:

```bash
cd backend
pip install razorpay
```

### Step 4: Run Migrations

Apply Django migrations for the new payment app:

```bash
cd backend
python manage.py makemigrations payments
python manage.py migrate
```

### Step 5: Start Backend Server

```bash
cd backend
python manage.py runserver
```

### Step 6: Start Frontend Server

```bash
cd frontend
npm start
```

---

## Testing the Payment Flow

### Test Mode Credentials
You're using Razorpay Test Mode. Use these test cards:

#### Successful Payment
- **Card Number:** 4111 1111 1111 1111
- **CVV:** Any 3 digits
- **Expiry:** Any future date
- **Name:** Any name

#### Failed Payment
- **Card Number:** 4111 1111 1111 1112
- **CVV:** Any 3 digits
- **Expiry:** Any future date

### Testing Steps

1. **Login as Receptionist**
   - Navigate to the receptionist login
   - Login with your receptionist credentials

2. **Navigate to Billing Tab**
   - Click on "Billing" in the sidebar
   - You'll see a list of all bills with their statuses

3. **Identify Pending Bills**
   - Look for bills with "Pending" status
   - These will have a "Pay Bill" button

4. **Initiate Payment**
   - Click "Pay Bill" button for a pending bill
   - Razorpay checkout modal will open

5. **Complete Payment**
   - Enter test card details (see above)
   - Click "Pay Now"
   - Payment will be processed

6. **Verify Success**
   - On successful payment, you'll see a success message
   - Bill status will update to "Paid"
   - Billing list will refresh automatically

### What Happens Behind the Scenes

1. **Order Creation:**
   - Frontend calls `/api/payments/create_order/`
   - Backend creates a Razorpay order
   - Order details saved in `payment_transactions` table

2. **Payment Processing:**
   - Razorpay Checkout modal opens
   - User enters payment details
   - Razorpay processes payment

3. **Payment Verification:**
   - On success, Razorpay returns payment details
   - Frontend calls `/api/payments/verify_payment/`
   - Backend verifies signature using HMAC-SHA256
   - If valid, updates billing status to "Paid"
   - Updates `payment_transactions` with payment ID and signature

4. **Database Updates:**
   - `billing` table: `payment_status` → 'Paid'
   - `payment_transactions` table: `status` → 'captured'

---

## Database Schema Reference

### payment_transactions Table

| Column | Type | Description |
|--------|------|-------------|
| id | INT | Primary key (auto-increment) |
| bill_id | INT | Foreign key to billing table |
| razorpay_order_id | VARCHAR(100) | Razorpay order ID (unique) |
| razorpay_payment_id | VARCHAR(100) | Razorpay payment ID (after payment) |
| razorpay_signature | VARCHAR(255) | Payment signature for verification |
| amount | DECIMAL(10,2) | Payment amount in INR |
| currency | VARCHAR(10) | Currency code (default: INR) |
| status | VARCHAR(20) | Payment status (created, captured, failed, etc.) |
| payment_method | VARCHAR(50) | Payment method (card, upi, netbanking, etc.) |
| error_code | VARCHAR(50) | Error code if payment failed |
| error_description | TEXT | Error description if payment failed |
| created_at | TIMESTAMP | Transaction creation time |
| updated_at | TIMESTAMP | Last update time |

### Status Values
- **created:** Order created, payment not initiated
- **authorized:** Payment authorized but not captured
- **captured:** Payment successfully completed
- **failed:** Payment failed
- **refunded:** Payment refunded

---

## API Endpoints Summary

| Endpoint | Method | Purpose | Auth Required |
|----------|--------|---------|---------------|
| `/api/payments/create_order/` | POST | Create Razorpay order | Yes |
| `/api/payments/verify_payment/` | POST | Verify payment signature | Yes |
| `/api/payments/transaction_history/` | GET | Get transaction history | Yes |
| `/api/payments/handle_webhook/` | POST | Handle Razorpay webhooks | No |

---

## Security Features

1. **Signature Verification:** All payments verified using HMAC-SHA256
2. **HTTPS Required:** Use HTTPS in production
3. **Authentication:** All endpoints require JWT authentication
4. **Database Constraints:** Foreign keys and unique constraints
5. **Error Handling:** Comprehensive error handling and logging

---

## Production Checklist

Before going live:

1. **Switch to Live Keys:**
   - Get live Razorpay keys from dashboard
   - Update `.env` file with live keys

2. **Configure Webhook:**
   - Set webhook URL in Razorpay dashboard
   - Add `RAZORPAY_WEBHOOK_SECRET` to `.env`

3. **Enable HTTPS:**
   - Use SSL certificate
   - Update CORS settings

4. **Test Thoroughly:**
   - Test all payment scenarios
   - Test webhook handling
   - Test error cases

5. **Monitor Transactions:**
   - Set up logging
   - Monitor payment_transactions table
   - Set up alerts for failed payments

---

## Troubleshooting

### Payment Not Initiating
- Check browser console for errors
- Verify Razorpay script is loaded
- Check API endpoint connectivity

### Payment Verification Failed
- Check Razorpay secret key
- Verify signature calculation
- Check network connectivity

### Database Errors
- Verify table exists
- Check foreign key constraints
- Verify bill_id exists in billing table

### Frontend Issues
- Clear browser cache
- Check React dev tools for errors
- Verify API client configuration

---

## Support

For Razorpay-specific issues:
- **Documentation:** https://razorpay.com/docs/
- **Test Cards:** https://razorpay.com/docs/payments/payments/test-card-details/
- **Support:** https://razorpay.com/support/

---

## Summary

✅ **Payment Transactions Table** created with comprehensive schema
✅ **Backend API** with order creation and verification
✅ **Frontend Integration** with Razorpay Checkout
✅ **Automatic Status Updates** after successful payment
✅ **Error Handling** for failed payments
✅ **Transaction History** tracking

The system is now ready for testing payments in the Receptionist Billing section!
