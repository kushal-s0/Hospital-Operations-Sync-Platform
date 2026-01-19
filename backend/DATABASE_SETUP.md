# Database Setup Guide

## Overview
This guide will help you set up and test the MySQL database connection for the Hospital Operations System.

## Prerequisites

1. **MySQL Server** installed and running
   - Download from: https://dev.mysql.com/downloads/mysql/
   - For Windows: Check if MySQL service is running in Services (Win + R, type `services.msc`)

2. **Python packages** installed:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration Steps

### 1. Configure Environment Variables

Edit the `.env` file in the `backend` directory with your MySQL credentials:

```env
# Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=hospital_ops_db
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
```

**Important**: Replace `your_mysql_password` with your actual MySQL root password.

### 2. Create Database (if not exists)

Option A - Using MySQL Command Line:
```sql
mysql -u root -p
CREATE DATABASE hospital_ops_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
EXIT;
```

Option B - The test script will create it automatically if it doesn't exist.

### 3. Test Database Connection

We provide two test scripts:

#### Option 1: Simple MySQL Test (Recommended First)
Tests direct MySQL connection without Django:

```bash
cd backend
python test_mysql_simple.py
```

This will:
- ✅ Test MySQL server connection
- ✅ Check if database exists (create if needed)
- ✅ Verify credentials
- ✅ Display database information

#### Option 2: Full Django Database Test
Tests Django's database connection:

```bash
cd backend
python test_db_connection.py
```

This will:
- ✅ Test database connection through Django
- ✅ Display database configuration
- ✅ Show installed Django apps
- ✅ Check for existing tables

### 4. Run Migrations

Once the connection test passes, create database tables:

```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 5. Create Admin User

```bash
python manage.py createsuperuser
```

### 6. Start Development Server

```bash
python manage.py runserver
```

## Troubleshooting

### Common Issues

#### Error: "No module named 'MySQLdb'"
**Solution**: Install the MySQL client library
```bash
pip install mysqlclient
```

If that fails on Windows, try:
```bash
pip install pymysql
```

#### Error 1045: Access denied
**Problem**: Incorrect username or password

**Solution**: 
1. Verify your MySQL password
2. Update `DB_PASSWORD` in `.env` file
3. Try logging in with MySQL command line: `mysql -u root -p`

#### Error 2003: Can't connect to MySQL server
**Problem**: MySQL server is not running

**Solution**:
1. **Windows**: Open Services (Win + R, type `services.msc`)
2. Find "MySQL" service
3. Right-click → Start
4. Set startup type to "Automatic" if you want it to start with Windows

#### Error 1049: Unknown database
**Problem**: Database doesn't exist

**Solution**: Run `test_mysql_simple.py` which will create the database automatically, or create it manually:
```sql
CREATE DATABASE hospital_ops_db;
```

#### Import Error: No module named 'decouple'
**Solution**:
```bash
pip install python-decouple
```

## Database Switching

### Switch to SQLite (for development/testing)

Edit `.env`:
```env
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3
```

### Switch to PostgreSQL

1. Install PostgreSQL and psycopg2:
```bash
pip install psycopg2-binary
```

2. Edit `.env`:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=hospital_ops_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

## Verification Checklist

- [ ] MySQL server is running
- [ ] `.env` file configured with correct credentials
- [ ] `pip install -r requirements.txt` completed
- [ ] `test_mysql_simple.py` runs successfully
- [ ] `test_db_connection.py` runs successfully
- [ ] Migrations completed (`python manage.py migrate`)
- [ ] Admin user created (`python manage.py createsuperuser`)
- [ ] Server starts without errors (`python manage.py runserver`)

## Next Steps

After successful database setup:

1. Access admin panel: http://localhost:8000/admin
2. Start the frontend: `cd frontend && npm start`
3. Begin development!

## Support

If you encounter issues not covered here:
1. Check Django database documentation: https://docs.djangoproject.com/en/4.2/ref/databases/
2. Check MySQL documentation: https://dev.mysql.com/doc/
3. Review error messages carefully - they usually indicate the exact problem

---
Last Updated: January 2026
