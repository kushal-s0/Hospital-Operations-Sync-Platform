@echo off
REM Razorpay Payment Integration Setup Script
REM Hospital Management System

echo ============================================
echo  Razorpay Payment Integration Setup
echo  Hospital Management System
echo ============================================
echo.

echo Step 1: Creating payment_transactions table...
echo.

cd backend

REM Check if MySQL is accessible
mysql --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: MySQL is not installed or not in PATH
    echo Please install MySQL or add it to your PATH
    pause
    exit /b 1
)

echo Enter MySQL root password when prompted...
mysql -u root -p hospital_management < create_payment_transactions_table.sql

if %errorlevel% neq 0 (
    echo ERROR: Failed to create payment_transactions table
    echo Please check your MySQL connection and try again
    pause
    exit /b 1
)

echo.
echo Step 2: Installing Python dependencies...
echo.

REM Check if razorpay is already installed
pip show razorpay >nul 2>&1
if %errorlevel% neq 0 (
    echo Installing razorpay package...
    pip install razorpay
) else (
    echo razorpay package already installed
)

echo.
echo Step 3: Creating Django migrations...
echo.

python manage.py makemigrations payments
python manage.py migrate

if %errorlevel% neq 0 (
    echo WARNING: Migration failed. This is normal if table already exists.
)

echo.
echo ============================================
echo  Setup Complete!
echo ============================================
echo.
echo Next Steps:
echo 1. Start backend server: python manage.py runserver
echo 2. Start frontend server: cd ../frontend ^&^& npm start
echo 3. Login as receptionist
echo 4. Navigate to Billing tab
echo 5. Click "Pay Bill" on any pending bill
echo.
echo Test Card Details (Razorpay Test Mode):
echo - Card Number: 4111 1111 1111 1111
echo - CVV: Any 3 digits
echo - Expiry: Any future date
echo.
echo For more details, see RAZORPAY_PAYMENT_INTEGRATION.md
echo.
pause
