"""
Database Connection Test Script
This script tests the database connection for the Hospital Operations System
"""

import os
import sys
import django
from pathlib import Path

# Add the backend directory to the Python path
backend_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(backend_dir))

# Setup Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hospital_ops.settings')
django.setup()

from django.db import connection
from django.conf import settings
from decouple import config


def test_database_connection():
    """Test database connection and display configuration"""
    
    print("=" * 60)
    print("DATABASE CONNECTION TEST")
    print("=" * 60)
    
    # Display database configuration
    db_config = settings.DATABASES['default']
    print("\n📋 Database Configuration:")
    print(f"  Engine: {db_config['ENGINE']}")
    print(f"  Name: {db_config['NAME']}")
    print(f"  User: {db_config.get('USER', 'N/A')}")
    print(f"  Host: {db_config.get('HOST', 'N/A')}")
    print(f"  Port: {db_config.get('PORT', 'N/A')}")
    
    # Test connection
    print("\n🔌 Testing database connection...")
    
    try:
        with connection.cursor() as cursor:
            # Test query
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
            if result[0] == 1:
                print("✅ SUCCESS: Database connection established!")
                
                # Get database version
                if 'mysql' in db_config['ENGINE']:
                    cursor.execute("SELECT VERSION()")
                    version = cursor.fetchone()[0]
                    print(f"  MySQL Version: {version}")
                elif 'postgresql' in db_config['ENGINE']:
                    cursor.execute("SELECT version()")
                    version = cursor.fetchone()[0]
                    print(f"  PostgreSQL Version: {version}")
                elif 'sqlite' in db_config['ENGINE']:
                    cursor.execute("SELECT sqlite_version()")
                    version = cursor.fetchone()[0]
                    print(f"  SQLite Version: {version}")
                
                # Test tables access
                print("\n📊 Checking database tables...")
                cursor.execute("""
                    SELECT COUNT(*) 
                    FROM information_schema.tables 
                    WHERE table_schema = %s
                """ if 'mysql' in db_config['ENGINE'] else """
                    SELECT COUNT(*) 
                    FROM sqlite_master 
                    WHERE type='table'
                """, [db_config['NAME']] if 'mysql' in db_config['ENGINE'] else [])
                
                table_count = cursor.fetchone()[0]
                print(f"  Total tables in database: {table_count}")
                
                if table_count == 0:
                    print("\n⚠️  WARNING: No tables found. Run migrations:")
                    print("     python manage.py makemigrations")
                    print("     python manage.py migrate")
                
                return True
                
    except Exception as e:
        print("❌ ERROR: Database connection failed!")
        print(f"  Error Type: {type(e).__name__}")
        print(f"  Error Message: {str(e)}")
        print("\n💡 Troubleshooting Tips:")
        
        if 'mysql' in db_config['ENGINE']:
            print("  1. Ensure MySQL server is running")
            print("  2. Verify database credentials in .env file")
            print("  3. Check if database exists: CREATE DATABASE hospital_ops_db;")
            print("  4. Verify user has proper permissions")
            print("  5. Install mysqlclient: pip install mysqlclient")
        elif 'postgresql' in db_config['ENGINE']:
            print("  1. Ensure PostgreSQL server is running")
            print("  2. Verify database credentials in .env file")
            print("  3. Check if database exists")
            print("  4. Install psycopg2: pip install psycopg2-binary")
        else:
            print("  1. Check database configuration in .env file")
            print("  2. Ensure database file/server is accessible")
        
        return False
    
    finally:
        print("\n" + "=" * 60)


def test_django_apps():
    """Test if Django apps are properly configured"""
    print("\n📱 Testing Django Apps Configuration...")
    
    installed_apps = settings.INSTALLED_APPS
    local_apps = [app for app in installed_apps if app.startswith('apps.')]
    
    print(f"  Total installed apps: {len(installed_apps)}")
    print(f"  Local apps: {len(local_apps)}")
    
    for app in local_apps:
        print(f"    ✓ {app}")
    
    return True


def main():
    """Main test function"""
    print("\n🏥 Hospital Operations System - Database Test\n")
    
    # Test database connection
    db_success = test_database_connection()
    
    # Test Django apps
    apps_success = test_django_apps()
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Database Connection: {'✅ PASS' if db_success else '❌ FAIL'}")
    print(f"Django Apps: {'✅ PASS' if apps_success else '❌ FAIL'}")
    print("=" * 60)
    
    if db_success:
        print("\n🎉 All tests passed! Your database is ready to use.")
        print("\nNext steps:")
        print("  1. Run migrations: python manage.py migrate")
        print("  2. Create superuser: python manage.py createsuperuser")
        print("  3. Start server: python manage.py runserver")
    else:
        print("\n⚠️  Please fix the database connection issues above.")
        sys.exit(1)


if __name__ == '__main__':
    main()
