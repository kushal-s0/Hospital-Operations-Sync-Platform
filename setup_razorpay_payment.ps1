# Razorpay Payment Integration Setup Script - PowerShell
# Hospital Management System

Write-Host "============================================" -ForegroundColor Cyan
Write-Host " Razorpay Payment Integration Setup" -ForegroundColor Cyan
Write-Host " Hospital Management System" -ForegroundColor Cyan
Write-Host "============================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Create payment_transactions table
Write-Host "Step 1: Creating payment_transactions table..." -ForegroundColor Yellow
Write-Host ""

$mysqlPath = "mysql"
$dbName = "hospital_management"
$sqlFile = "create_payment_transactions_table.sql"

# Check if MySQL is accessible
try {
    $null = & mysql --version 2>&1
} catch {
    Write-Host "ERROR: MySQL is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install MySQL or add it to your PATH" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host "Enter MySQL root password when prompted..." -ForegroundColor Green
Get-Content $sqlFile | mysql -u root -p $dbName

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "ERROR: Failed to create payment_transactions table" -ForegroundColor Red
    Write-Host "Please check your MySQL connection and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""
Write-Host "Step 2: Installing Python dependencies..." -ForegroundColor Yellow
Write-Host ""

# Check if razorpay is already installed
$razorpayInstalled = pip show razorpay 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host "Installing razorpay package..." -ForegroundColor Green
    pip install razorpay
} else {
    Write-Host "razorpay package already installed" -ForegroundColor Green
}

Write-Host ""
Write-Host "Step 3: Creating Django migrations..." -ForegroundColor Yellow
Write-Host ""

python manage.py makemigrations payments
python manage.py migrate

if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "WARNING: Migration failed. This is normal if table already exists." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "============================================" -ForegroundColor Green
Write-Host " Setup Complete!" -ForegroundColor Green
Write-Host "============================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Start backend server: python manage.py runserver" -ForegroundColor White
Write-Host "2. Start frontend server: cd ..\frontend; npm start" -ForegroundColor White
Write-Host "3. Login as receptionist" -ForegroundColor White
Write-Host "4. Navigate to Billing tab" -ForegroundColor White
Write-Host "5. Click 'Pay Bill' on any pending bill" -ForegroundColor White
Write-Host ""
Write-Host "Test Card Details (Razorpay Test Mode):" -ForegroundColor Cyan
Write-Host "- Card Number: 4111 1111 1111 1111" -ForegroundColor White
Write-Host "- CVV: Any 3 digits" -ForegroundColor White
Write-Host "- Expiry: Any future date" -ForegroundColor White
Write-Host ""
Write-Host "For more details, see RAZORPAY_PAYMENT_INTEGRATION.md" -ForegroundColor Yellow
Write-Host ""
Read-Host "Press Enter to exit"
