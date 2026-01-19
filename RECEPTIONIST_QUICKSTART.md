# Receptionist Dashboard - Quick Start

## How to Access

1. **Start the application:**
   ```bash
   npm start
   ```

2. **Login as Receptionist:**
   - Go to: `http://localhost:3000/login`
   - Email: `emily.d@hospital.com`
   - Password: `reception123`

3. **View Receptionist Dashboard:**
   - Click "Receptionist" (🎤) in the left sidebar
   - Or navigate to: `http://localhost:3000/receptionist`

## Dashboard Tabs

### 📊 Dashboard Tab
Shows summary statistics:
- Total Billing Amount
- Paid Bills & Pending Bills
- Income & Expense Transactions
- Total Treatments Count

### 💳 Billing Tab
View all billing records with:
- Bill ID, Patient ID, Treatment ID
- Date, Amount, Payment Method
- Status (Paid/Pending/Failed)
- Statistics by Status & Payment Method

### 💰 Financial Transactions Tab
View all financial transactions:
- Transaction ID, Type (INCOME/EXPENSE)
- Amount, Payment Method
- Reference Type & Description
- Date information

### 🏥 Treatments Tab
Browse treatment records:
- Treatment ID, Appointment ID
- Type, Description, Cost
- Treatment Date

## Features

✅ **View-Only Interface** - Designed for data viewing, not editing
✅ **Paginated Data** - View 10 records per page with Next/Previous navigation
✅ **Quick Statistics** - See financial summaries at a glance
✅ **Responsive Design** - Works on desktop and mobile
✅ **Real Data** - Uses existing database tables (billing, financial_transactions, treatments)

## Navigation

| Element | Action |
|---------|--------|
| Tab Buttons | Switch between Dashboard, Billing, Transactions, Treatments |
| Previous/Next | Navigate through paginated records |
| Page Indicator | Shows current page and total pages |

## Created Files

### Backend
```
backend/apps/receptionist/
├── __init__.py
├── models.py
├── serializers.py
├── views.py (ReceptionistDashboardViewSet)
├── urls.py
├── admin.py
└── apps.py
```

### Frontend
```
frontend/src/pages/Receptionist/
├── ReceptionistDashboard.js
└── ReceptionistDashboard.css
```

### Configuration Updates
- `backend/hospital_ops/settings.py` - Added receptionist app
- `backend/hospital_ops/urls.py` - Added API routes
- `frontend/src/App.js` - Added route
- `frontend/src/components/Sidebar/Sidebar.js` - Added menu item

## API Endpoints

All endpoints require JWT authentication and are at `/api/receptionist/dashboard/`

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Get dashboard summary |
| GET | `/billing_list/` | Get billing records (paginated) |
| GET | `/financial_transactions_list/` | Get transactions (paginated) |
| GET | `/treatments_list/` | Get treatments (paginated) |
| GET | `/billing_statistics/` | Get billing stats by status/method |
| GET | `/transaction_statistics/` | Get transaction stats by type |

Query parameters:
- `page=1` - Page number
- `page_size=10` - Records per page

## Color Scheme

| Element | Color |
|---------|-------|
| Header | Purple gradient (#667eea to #764ba2) |
| Active Tab | #764ba2 |
| Primary Button | #667eea |
| Paid/Income | Green (#27ae60) |
| Pending | Yellow (#ffc107) |
| Failed/Expense | Red (#e74c3c) |

## Testing

1. Ensure database has data in:
   - `billing` table
   - `financial_transactions` table
   - `treatments` table

2. Create sample data if needed:
   ```bash
   python backend/create_staff_users.py
   ```

3. If data is empty, add test data:
   ```bash
   python backend/add_test_admissions_fixed.py
   ```

## Troubleshooting

**Empty Tables:**
- Run test data scripts to populate tables

**API 404 Errors:**
- Ensure settings.py includes 'apps.receptionist'
- Check urls.py includes receptionist routes

**Authentication Issues:**
- Ensure you're logged in with valid JWT token
- Check token is sent in Authorization header

**CORS Errors:**
- Frontend must be on port 3000
- Backend must be on port 8000
- Check ALLOWED_HOSTS in settings.py

## Documentation

Full guide available in: `RECEPTIONIST_DASHBOARD_GUIDE.md`

---

**Version:** 1.0
**Created:** January 19, 2026
**Status:** Ready for Use ✅
