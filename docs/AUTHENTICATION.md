# Authentication Setup Guide

This guide explains how to set up and use the authentication system in the Hospital Information System.

## Overview

The system uses JWT (JSON Web Token) based authentication with the following features:
- Secure login/logout functionality
- Token-based authentication with automatic refresh
- Protected routes in the frontend
- Role-based access (Admin, Staff, User)

## Backend Setup

### 1. Install Dependencies

First, install the required packages:

```bash
cd backend
pip install -r requirements.txt
```

This will install:
- `djangorestframework-simplejwt` - JWT authentication
- `rest_framework` - Django REST Framework
- Other dependencies

### 2. Run Migrations

Apply the database migrations to create necessary tables including `auth_user`:

```bash
python manage.py migrate
```

### 3. Create Test Users

Three scripts are provided to manage users:

#### Option A: Create All Test Users at Once

```bash
python create_test_users.py
```

This creates 5 test users:

| Username      | Password     | Role          | Description          |
|---------------|-------------|---------------|----------------------|
| admin         | admin123    | Admin         | Full system access   |
| doctor1       | doctor123   | Staff         | Doctor account       |
| nurse1        | nurse123    | Staff         | Nurse account        |
| receptionist  | reception123| User          | Front desk           |
| pharmacist    | pharma123   | User          | Pharmacy staff       |

#### Option B: Add Individual User

```bash
# Add regular user
python add_user.py username password

# Add admin user
python add_user.py username password --admin

# Examples:
python add_user.py testdoctor doc123
python add_user.py superadmin admin456 --admin
```

#### Option C: List All Users

```bash
python list_users.py
```

### 4. Start the Backend Server

```bash
python manage.py runserver
```

The backend will run on `http://localhost:8000`

## Frontend Setup

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Start the Frontend

```bash
npm start
```

The frontend will run on `http://localhost:3000` and automatically redirect to login page.

## Usage

### Login Process

1. Navigate to `http://localhost:3000`
2. You'll be redirected to `/login` if not authenticated
3. Enter credentials (use one of the test users above)
4. On successful login, you'll be redirected to the dashboard

### Logout

Click the "Logout" button in the top-right navbar to sign out.

### Protected Routes

All routes except `/login` are protected and require authentication:
- `/` - Dashboard
- `/opd` - OPD Queue
- `/beds` - Bed Management
- `/admissions` - Admissions
- `/inventory` - Inventory
- `/inter-hospital` - Inter-Hospital Transfer

## API Endpoints

### Authentication Endpoints

- `POST /api/auth/login/` - Login and get JWT tokens
  ```json
  {
    "username": "admin",
    "password": "admin123"
  }
  ```
  
- `POST /api/auth/logout/` - Logout (requires authentication)
  ```json
  {
    "refresh": "refresh_token_here"
  }
  ```

- `GET /api/auth/profile/` - Get current user profile (requires authentication)

- `POST /api/auth/token/refresh/` - Refresh access token
  ```json
  {
    "refresh": "refresh_token_here"
  }
  ```

## Token Management

### Token Storage

Tokens are stored in browser's `localStorage`:
- `access_token` - Short-lived token (1 hour)
- `refresh_token` - Long-lived token (7 days)
- `user` - User information

### Automatic Token Refresh

The frontend automatically:
1. Attaches access token to all API requests
2. Intercepts 401 responses
3. Attempts to refresh the token
4. Retries the original request
5. Redirects to login if refresh fails

## Security Features

1. **JWT Authentication** - Stateless, secure token-based auth
2. **Token Blacklisting** - Tokens are blacklisted on logout
3. **Token Rotation** - New refresh token on each refresh
4. **CORS Protection** - Only localhost:3000 allowed
5. **HTTPS Headers** - Bearer token in Authorization header
6. **Protected Routes** - Frontend route guards
7. **Backend Permissions** - Default authentication required

## Troubleshooting

### "Invalid username or password" Error

- Check if user exists: `python list_users.py`
- Verify credentials are correct
- Ensure migrations are applied: `python manage.py migrate`

### Token Expired Issues

- Tokens automatically refresh
- If issues persist, clear localStorage and login again
- Check backend is running and accessible

### CORS Errors

- Ensure backend allows `http://localhost:3000`
- Check `CORS_ALLOWED_ORIGINS` in settings.py
- Restart backend server after settings changes

### Database Connection Issues

- Verify database is running
- Check `.env` file configuration
- Run `python test_db_connection.py`

## Development Tips

### Testing Authentication

1. Use browser DevTools > Application > Local Storage to inspect tokens
2. Use Network tab to see Authorization headers
3. Use `list_users.py` to verify users in database

### Creating New Users Programmatically

```python
from django.contrib.auth.models import User

user = User.objects.create_user(
    username='newuser',
    password='password123',
    email='user@hospital.com',
    first_name='First',
    last_name='Last',
    is_staff=False,
    is_superuser=False
)
```

### Django Admin Access

Admin users can access Django admin panel:
```
http://localhost:8000/admin/
```

Use the `admin` / `admin123` credentials.

## Next Steps

1. ✅ Basic authentication implemented
2. 🔲 Add user registration (if needed)
3. 🔲 Implement role-based permissions
4. 🔲 Add password reset functionality
5. 🔲 Add user profile management
6. 🔲 Implement activity logging

## File Structure

```
backend/
├── apps/
│   └── authentication/
│       ├── __init__.py
│       ├── views.py          # Login, logout, profile endpoints
│       └── urls.py           # Authentication routes
├── create_test_users.py      # Create all test users
├── add_user.py              # Add single user
├── list_users.py            # List all users
└── hospital_ops/
    ├── settings.py          # JWT configuration
    └── urls.py              # Include auth routes

frontend/
├── src/
│   ├── components/
│   │   ├── PrivateRoute/
│   │   │   └── PrivateRoute.js  # Route protection
│   │   └── Navbar/
│   │       └── Navbar.js        # Logout button
│   ├── pages/
│   │   └── Login/
│   │       ├── Login.js         # Login page
│   │       └── Login.css        # Login styles
│   ├── services/
│   │   └── api.js              # Auth API & interceptors
│   └── App.js                  # Route configuration
```

## Support

For issues or questions, check:
1. Backend console for errors
2. Browser console for frontend errors
3. Network tab for API call failures
4. Django admin for user management
