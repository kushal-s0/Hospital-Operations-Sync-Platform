# Razorpay Payment - Quick Reference

## 🚀 Quick Start

### 1. Setup Database
```bash
cd backend
mysql -u root -p hospital_management < create_payment_transactions_table.sql
```

### 2. Install Dependencies
```bash
pip install razorpay
```

### 3. Run Migrations
```bash
python manage.py makemigrations payments
python manage.py migrate
```

### 4. Start Servers
```bash
# Backend
python manage.py runserver

# Frontend (new terminal)
cd ../frontend
npm start
```

---

## 💳 Test Payment

### Access Billing
1. Login as Receptionist
2. Navigate to "Billing" tab
3. Find a bill with "Pending" status
4. Click "Pay Bill"

### Test Card (Always Success)
- **Card:** 4111 1111 1111 1111
- **CVV:** 123
- **Expiry:** 12/25
- **Name:** Test User

---

## 📊 Database Schema

```sql
payment_transactions
├── id (PK)
├── bill_id (FK → billing.bill_id)
├── razorpay_order_id (Unique)
├── razorpay_payment_id
├── razorpay_signature
├── amount (DECIMAL)
├── status (created/captured/failed)
├── payment_method
└── timestamps
```

---

## 🔗 API Endpoints

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/payments/create_order/` | POST | Create order |
| `/api/payments/verify_payment/` | POST | Verify payment |
| `/api/payments/transaction_history/` | GET | View history |

---

## 📱 Payment Flow

```
1. User clicks "Pay Bill"
   ↓
2. Backend creates Razorpay order
   ↓
3. Razorpay Checkout opens
   ↓
4. User enters card details
   ↓
5. Payment processed
   ↓
6. Backend verifies signature
   ↓
7. Bill status → "Paid"
   ✓ Transaction saved
```

---

## ⚙️ Configuration

### Environment Variables (.env)
```env
RAZORPAY_PUBLIC_KEY=rzp_test_S6EZlI0Lzafb4J
RAZORPAY_SECRET_KEY=6jW2khcl70fj7UrUOVaVsIFT
```

### Settings (already configured)
- ✅ Payments app added to INSTALLED_APPS
- ✅ URL routing configured
- ✅ Environment variables loaded

---

## 🐛 Troubleshooting

### Payment modal not opening
- Check browser console
- Verify Razorpay script loaded
- Clear cache

### Verification failed
- Check secret key
- Verify signature calculation
- Check network

### Database error
- Verify table exists: `SHOW TABLES LIKE 'payment_transactions';`
- Check foreign key: Bill must exist in billing table

---

## 📞 Test Scenarios

### ✅ Successful Payment
Use card: 4111 1111 1111 1111

### ❌ Failed Payment
Use card: 4111 1111 1111 1112

### 🔄 Status Updates
- Before: billing.payment_status = 'Pending'
- After: billing.payment_status = 'Paid'

---

## 🎯 Key Features

✅ Secure signature verification
✅ Real-time payment processing
✅ Automatic status updates
✅ Transaction history tracking
✅ Error handling & logging
✅ Test mode integration

---

## 📝 Notes

- **Test Mode:** Currently using test keys
- **Production:** Switch to live keys before deployment
- **Webhooks:** Configure in Razorpay dashboard for production
- **HTTPS:** Required in production

---

**Full Documentation:** See `RAZORPAY_PAYMENT_INTEGRATION.md`
