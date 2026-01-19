# Hospital Information System - Quick Start

## 🚀 Running the Application

### Method 1: Windows Batch File (Recommended)
**Double-click `start.bat`** in the project root folder.
- Opens 2 terminal windows (Backend + Frontend)
- Easiest method for Windows users

### Method 2: PowerShell Script
Right-click `start.ps1` → **Run with PowerShell**
- Same as Method 1 but uses PowerShell

### Method 3: Using npm (Single Terminal)
```bash
# First time only
npm install

# Run both servers in one terminal with colored output
npm start
```

### Method 4: Manual Start (Separate Terminals)

**Terminal 1 - Backend:**
```bash
cd backend
python manage.py runserver
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

## 🔐 Login Credentials

After servers start, visit **http://localhost:3000**

| Username | Password | Role |
|----------|----------|------|
| admin | admin123 | Admin (Full Access) |
| doctor1 | doctor123 | Staff |
| nurse1 | nurse123 | Staff |

## 📦 First Time Setup

Run these commands once before first use:

```bash
# Install all dependencies
npm run install:all

# Setup database and create users
npm run setup

# OR do it manually:
cd backend
pip install -r requirements.txt
python manage.py migrate
python create_test_users.py
cd ../frontend
npm install
```

## 🛠️ Available npm Commands

```bash
npm start              # Start both servers (requires npm install first)
npm run backend        # Start only backend
npm run frontend       # Start only frontend
npm run install:all    # Install all dependencies
npm run setup         # Setup database and create users
npm run check:users   # List all users in database
npm run check:login   # Test login functionality
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000/api
- **Django Admin**: http://localhost:8000/admin

## ⚠️ Troubleshooting

### Can't login?
1. Make sure both servers are running
2. Check backend is on port 8000: http://localhost:8000
3. Run: `npm run check:login` to verify

### Backend won't start?
- Check if virtual environment is activated
- Run: `cd backend && pip install -r requirements.txt`

### Frontend won't start?
- Run: `cd frontend && npm install`

### Port already in use?
- Stop other applications using ports 3000 or 8000
- Or change ports in settings

## 🛑 Stopping Servers

- Close the terminal windows, OR
- Press `Ctrl+C` in each terminal

## 📁 Project Structure

```
HIS_Rubix/
├── start.bat          # Windows batch script
├── start.ps1          # PowerShell script
├── package.json       # Root npm scripts
├── backend/           # Django backend
│   ├── manage.py
│   └── requirements.txt
└── frontend/          # React frontend
    ├── package.json
    └── src/
```

## ✅ Quick Health Check

Run this to verify everything:
```bash
npm run check:login
```

Should show:
- ✓ Admin user exists
- ✓ Authentication works!
