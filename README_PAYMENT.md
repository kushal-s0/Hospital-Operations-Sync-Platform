# 💳 Razorpay Payment Integration - Complete Setup

## 🎯 Overview

This implementation adds **Razorpay payment gateway integration** to the Hospital Management System's Receptionist Billing section. Receptionists can now process payments for pending bills directly through a secure payment interface.

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [What's Included](#whats-included)
3. [Setup Instructions](#setup-instructions)
4. [Testing](#testing)
5. [Database Schema](#database-schema)
6. [API Documentation](#api-documentation)
7. [Troubleshooting](#troubleshooting)
8. [Production Deployment](#production-deployment)

---

## ⚡ Quick Start

### Run the automated setup:

```bash
# Windows
setup_razorpay_payment.bat

# OR manually follow steps below
```

### Manual Setup:

```bash
# 1. Create database table
cd backend
mysql -u root -p hospital_management < create_payment_transactions_table.sql

# 2. Install dependencies
pip install razorpay

# 3. Run migrations
python manage.py makemigrations payments
python manage.py migrate

# 4. Start backend
python manage.py runserver

# 5. Start frontend (new terminal)
cd ../frontend
npm start
```

---

## 📦 What's Included

### Backend Components

```
backend/apps/payments/
├── __init__.py           # Package init
├── admin.py              # Django admin interface
├── apps.py               # App configuration
├── models.py             # PaymentTransaction model
├── serializers.py        # API serializers
├── urls.py               # URL routing
└── views.py              # Payment API endpoints
```

### Database

- **Table:** `payment_transactions`
- **Purpose:** Stores all Razorpay transaction details
- **Relations:** Foreign key to `billing` table

### Frontend Updates

- **ReceptionistBillingTab.js** - Payment button and Razorpay integration
- **ReceptionistDashboard.js** - Same updates for billing tab

### Documentation

1. **RAZORPAY_PAYMENT_INTEGRATION.md** - Complete guide
2. **RAZORPAY_QUICK_REFERENCE.md** - Quick reference
3. **PAYMENT_ARCHITECTURE.txt** - Technical architecture
4. **IMPLEMENTATION_SUMMARY.md** - Implementation summary
5. **README_PAYMENT.md** - This file

---

## 🔧 Setup Instructions

### Step 1: Database Setup

Run the SQL migration:

```bash
cd backend
mysql -u root -p hospital_management < create_payment_transactions_table.sql
```

Verify table creation:

```sql
USE hospital_management;
DESCRIBE payment_transactions;
```

### Step 2: Install Python Dependencies

```bash
pip install razorpay
```

### Step 3: Environment Variables

Your `.env` file already contains:

```env
RAZORPAY_PUBLIC_KEY=rzp_test_YOUR_KEY_ID
RAZORPAY_SECRET_KEY=YOUR_RAZORPAY_KEY_SECRET
```

✅ No changes needed!

### Step 4: Django Migrations

```bash
python manage.py makemigrations payments
python manage.py migrate
```

### Step 5: Start Servers

```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver

# Terminal 2 - Frontend
cd frontend
npm start
```

---

## 🧪 Testing

### Test Payment Flow

1. **Login as Receptionist**
   - Navigate to http://localhost:3000
   - Login with receptionist credentials

2. **Navigate to Billing**
   - Click "Billing" in the sidebar
   - View all bills with their statuses

3. **Find Pending Bills**
   - Look for bills with "Pending" status
   - These will have a "Pay Bill" button

4. **Process Payment**
   - Click "Pay Bill"
   - Razorpay checkout modal opens

5. **Enter Test Card Details**
   - **Card Number:** 4111 1111 1111 1111
   - **CVV:** 123
   - **Expiry:** 12/25
   - **Name:** Test User

6. **Complete Payment**
   - Click "Pay"
   - Wait for success message
   - Bill status updates to "Paid"

### Test Scenarios

#### ✅ Successful Payment
Use card: **4111 1111 1111 1111**

#### ❌ Failed Payment
Use card: **4111 1111 1111 1112**

#### 🔄 Check Database
```sql
-- View payment transactions
SELECT * FROM payment_transactions ORDER BY created_at DESC LIMIT 10;

-- View updated billing
SELECT bill_id, amount, payment_status, payment_method 
FROM billing 
WHERE payment_status = 'Paid' 
ORDER BY updated_at DESC 
LIMIT 10;
```

---

## 🗄️ Database Schema

### payment_transactions Table

```sql
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
    FOREIGN KEY (bill_id) REFERENCES billing(bill_id) ON DELETE CASCADE
);
```

### Status Values

| Status | Description |
|--------|-------------|
| `created` | Order created, payment not initiated |
| `authorized` | Payment authorized but not captured |
| `captured` | Payment successfully completed ✅ |
| `failed` | Payment failed ❌ |
| `refunded` | Payment refunded |

---

## 🔌 API Documentation

### 1. Create Order

**Endpoint:** `POST /api/payments/create_order/`

**Auth:** Required (JWT)

**Request:**
```json
{
  "bill_id": 123
}
```

**Response:**
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

---

### 2. Verify Payment

**Endpoint:** `POST /api/payments/verify_payment/`

**Auth:** Required (JWT)

**Request:**
```json
{
  "razorpay_order_id": "order_xxxx",
  "razorpay_payment_id": "pay_xxxx",
  "razorpay_signature": "signature_xxxx"
}
```

**Response:**
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

---

### 3. Transaction History

**Endpoint:** `GET /api/payments/transaction_history/?bill_id=123`

**Auth:** Required (JWT)

**Response:**
```json
{
  "status": "success",
  "data": [
    {
      "id": 1,
      "bill_id": 123,
      "razorpay_order_id": "order_xxxx",
      "amount": "500.00",
      "status": "captured",
      "created_at": "2026-01-21T10:30:00Z"
    }
  ]
}
```

---

## 🐛 Troubleshooting

### Issue: Payment modal not opening

**Solutions:**
- Check browser console for errors
- Verify Razorpay script loaded: `window.Razorpay`
- Clear browser cache
- Check network tab for API calls

---

### Issue: Payment verification failed

**Solutions:**
- Check Razorpay secret key in `.env`
- Verify signature calculation
- Check backend logs
- Ensure database connection

---

### Issue: Bill status not updating

**Solutions:**
```sql
-- Check payment transaction
SELECT * FROM payment_transactions WHERE bill_id = 123;

-- Check billing status
SELECT bill_id, payment_status FROM billing WHERE bill_id = 123;

-- Manually update (if needed)
UPDATE billing SET payment_status = 'Paid' WHERE bill_id = 123;
```

---

### Issue: Database error

**Solutions:**
```sql
-- Verify table exists
SHOW TABLES LIKE 'payment_transactions';

-- Check foreign key
SHOW CREATE TABLE payment_transactions;

-- Verify bill exists
SELECT * FROM billing WHERE bill_id = 123;
```

---

## 🚀 Production Deployment

### Before Going Live:

#### 1. Switch to Live Keys

```env
# Replace in .env
RAZORPAY_PUBLIC_KEY=rzp_live_xxxxxxxxxx
RAZORPAY_SECRET_KEY=your_live_secret_key
```

#### 2. Configure Webhook

1. Go to Razorpay Dashboard
2. Settings → Webhooks
3. Add webhook URL: `https://yourdomain.com/api/payments/handle_webhook/`
4. Copy webhook secret
5. Add to `.env`:
   ```env
   RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
   ```

#### 3. Enable HTTPS

- Install SSL certificate
- Update ALLOWED_HOSTS in settings.py
- Update CORS_ALLOWED_ORIGINS

#### 4. Test Thoroughly

- [ ] Successful payment flow
- [ ] Failed payment handling
- [ ] Webhook processing
- [ ] Error scenarios
- [ ] Database updates

#### 5. Monitor

- Set up logging
- Monitor payment_transactions table
- Set up alerts for failures
- Track payment success rate

---

## 📊 Monitoring Queries

### Daily Payment Summary
```sql
SELECT 
    DATE(created_at) as date,
    COUNT(*) as total_transactions,
    SUM(CASE WHEN status = 'captured' THEN 1 ELSE 0 END) as successful,
    SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed,
    SUM(CASE WHEN status = 'captured' THEN amount ELSE 0 END) as total_amount
FROM payment_transactions
WHERE created_at >= DATE_SUB(NOW(), INTERVAL 30 DAY)
GROUP BY DATE(created_at)
ORDER BY date DESC;
```

### Failed Payments
```sql
SELECT 
    pt.bill_id,
    pt.amount,
    pt.error_code,
    pt.error_description,
    pt.created_at,
    b.patient_id
FROM payment_transactions pt
JOIN billing b ON pt.bill_id = b.bill_id
WHERE pt.status = 'failed'
ORDER BY pt.created_at DESC
LIMIT 20;
```

---

## 📞 Support & Resources

### Documentation
- **Full Guide:** [RAZORPAY_PAYMENT_INTEGRATION.md](RAZORPAY_PAYMENT_INTEGRATION.md)
- **Quick Reference:** [RAZORPAY_QUICK_REFERENCE.md](RAZORPAY_QUICK_REFERENCE.md)
- **Architecture:** [PAYMENT_ARCHITECTURE.txt](PAYMENT_ARCHITECTURE.txt)

### Razorpay Resources
- **Docs:** https://razorpay.com/docs/
- **Test Cards:** https://razorpay.com/docs/payments/payments/test-card-details/
- **API Reference:** https://razorpay.com/docs/api/
- **Support:** https://razorpay.com/support/

---

## ✅ Feature Checklist

- [x] Payment transaction model created
- [x] API endpoints implemented
- [x] Frontend Razorpay integration
- [x] Signature verification
- [x] Automatic status updates
- [x] Error handling
- [x] Transaction history
- [x] Database migrations
- [x] Documentation
- [x] Test mode configured

---

## 🎉 Success!

Your Razorpay payment integration is now complete and ready for testing!

**Next Step:** Run `setup_razorpay_payment.bat` to set up everything automatically.

---

**Version:** 1.0  
**Date:** January 21, 2026  
**Status:** ✅ Ready for Testing
