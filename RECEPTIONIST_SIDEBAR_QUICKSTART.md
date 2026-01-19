# Receptionist Sidebar - Quick Start Guide

## What Changed?

The receptionist menu items are now integrated into the **main left sidebar** instead of being in a separate internal sidebar. They appear **only for receptionist users**.

## How to Use

### Step 1: Login as Receptionist
```
Username: receptionist
Password: password123
```

### Step 2: View the Sidebar
After login, the left sidebar will automatically show the **"Receptionist Menu"** with 4 options:
- 📊 Dashboard
- 💳 Billing  
- 💰 Transactions
- 🏥 Treatments

### Step 3: Click on Any Option
- Each option opens a **full-page view**
- Navbar and profile/logout button remain at the top
- Click to navigate between receptionist sections

## Key Features

✅ **Role-based Menu** - Only receptionists see receptionist menu
✅ **Full Page Views** - Each section displays as a complete page
✅ **Pagination** - Billing, Transactions, and Treatments support pagination
✅ **Live Data** - Connected to backend API endpoints
✅ **Responsive** - Works on desktop and mobile

## Menu Structure

### For Receptionists:
```
Receptionist Menu
├── Dashboard
├── Billing
├── Transactions
└── Treatments
```

### For Other Staff:
```
(unchanged)
├── Dashboard
├── OPD Queue
├── Bed Management
├── Admissions
├── Inventory
└── Inter-Hospital
```

## Data Views

### Dashboard
- Total billing amount
- Paid bills count
- Pending bills count
- Failed bills count
- Total income
- Total expenses

### Billing
- List of all bills with pagination
- Payment status breakdown (Paid, Pending, Failed)
- Payment method filtering
- Sortable by date, amount, status

### Transactions
- All financial transactions
- Income vs Expense breakdown
- Reference type filtering
- Payment method tracking

### Treatments
- Treatment records
- Treatment type listing
- Cost tracking
- Date-based sorting

## Technical Notes

- All pages use the same responsive CSS styling
- API calls include error handling
- Loading states display during data fetch
- Pagination defaults to 10 items per page
- User role detected from localStorage on mount

## Troubleshooting

**Q: Why don't I see the receptionist menu?**
A: You must be logged in as a user with role "Receptionist". Check your login credentials.

**Q: Where did the old receptionist page go?**
A: The old `/receptionist` route still exists for backward compatibility, but now menu items are integrated into the sidebar.

**Q: Can I go back to the old interface?**
A: Yes - navigate to `/receptionist` directly in the URL to see the original tabbed interface.

**Q: Why is the sidebar empty sometimes?**
A: The role check happens when the sidebar mounts. If you login very quickly or there's a timing issue, try refreshing the page.

## API Endpoints Used

The receptionist dashboard uses these backend endpoints:

```
GET /api/receptionist/dashboard/
GET /api/receptionist/dashboard/billing_list/?page=1&page_size=10
GET /api/receptionist/dashboard/financial_transactions_list/?page=1&page_size=10
GET /api/receptionist/dashboard/treatments_list/?page=1&page_size=10
GET /api/receptionist/dashboard/billing_statistics/
GET /api/receptionist/dashboard/transaction_statistics/
```

All endpoints require authentication token in headers.
