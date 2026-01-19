"""
Simple MySQL Connection Test (Without Django)
Tests direct connection to MySQL database
"""

import sys

try:
    import MySQLdb
    DRIVER = 'MySQLdb'
except ImportError:
    try:
        import pymysql
        pymysql.install_as_MySQLdb()
        DRIVER = 'pymysql'
    except ImportError:
        print("❌ ERROR: No MySQL driver found!")
        print("\nPlease install one of the following:")
        print("  pip install mysqlclient")
        print("  OR")
        print("  pip install pymysql")
        sys.exit(1)

from decouple import config


def test_mysql_connection():
    """Test direct MySQL connection"""
    
    print("=" * 60)
    print("DIRECT MYSQL CONNECTION TEST")
    print("=" * 60)
    print(f"Using driver: {DRIVER}\n")
    
    # Get credentials from .env
    db_config = {
        'host': config('DB_HOST', default='localhost'),
        'port': int(config('DB_PORT', default='3306')),
        'user': config('DB_USER', default='root'),
        'password': config('DB_PASSWORD', default=''),
        'database': config('DB_NAME', default='hospital_ops_db'),
    }
    
    print("📋 Connection Parameters:")
    print(f"  Host: {db_config['host']}")
    print(f"  Port: {db_config['port']}")
    print(f"  User: {db_config['user']}")
    print(f"  Database: {db_config['database']}")
    
    print("\n🔌 Testing connection...")
    
    try:
        # Test connection without database first
        print("  Step 1: Testing server connection...")
        conn = MySQLdb.connect(
            host=db_config['host'],
            port=db_config['port'],
            user=db_config['user'],
            password=db_config['password']
        )
        cursor = conn.cursor()
        
        # Get MySQL version
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        print(f"  ✅ Connected to MySQL Server!")
        print(f"  MySQL Version: {version}")
        
        # Check if database exists
        print(f"\n  Step 2: Checking if database '{db_config['database']}' exists...")
        cursor.execute("SHOW DATABASES")
        databases = [db[0] for db in cursor.fetchall()]
        
        if db_config['database'] in databases:
            print(f"  ✅ Database '{db_config['database']}' exists!")
        else:
            print(f"  ⚠️  Database '{db_config['database']}' does not exist!")
            print(f"\n  Creating database '{db_config['database']}'...")
            cursor.execute(f"CREATE DATABASE {db_config['database']} CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci")
            print(f"  ✅ Database created successfully!")
        
        cursor.close()
        conn.close()
        
        # Test connection to specific database
        print(f"\n  Step 3: Testing connection to database '{db_config['database']}'...")
        conn = MySQLdb.connect(**db_config)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        if result[0] == 1:
            print(f"  ✅ Successfully connected to database!")
            
            # Show tables
            cursor.execute("SHOW TABLES")
            tables = cursor.fetchall()
            
            print(f"\n📊 Database Info:")
            print(f"  Total tables: {len(tables)}")
            
            if tables:
                print("  Tables:")
                for table in tables:
                    print(f"    - {table[0]}")
            else:
                print("  No tables found (new database)")
        
        cursor.close()
        conn.close()
        
        print("\n✅ SUCCESS: All connection tests passed!")
        print("\n" + "=" * 60)
        return True
        
    except MySQLdb.Error as e:
        print(f"\n❌ ERROR: Connection failed!")
        print(f"  Error Code: {e.args[0]}")
        print(f"  Error Message: {e.args[1]}")
        
        print("\n💡 Troubleshooting Tips:")
        print("  1. Check if MySQL server is running")
        print("     Windows: Check Services (services.msc)")
        print("     MySQL service should be 'Running'")
        print("\n  2. Verify credentials in .env file:")
        print(f"     DB_USER={db_config['user']}")
        print(f"     DB_PASSWORD=<your_password>")
        print(f"     DB_HOST={db_config['host']}")
        print(f"     DB_PORT={db_config['port']}")
        print("\n  3. Common error solutions:")
        print("     - Error 1045: Wrong username or password")
        print("     - Error 2003: Can't connect to server (check if MySQL is running)")
        print("     - Error 1049: Unknown database (will be created automatically)")
        
        print("\n" + "=" * 60)
        return False
    
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {type(e).__name__}")
        print(f"  {str(e)}")
        print("\n" + "=" * 60)
        return False


if __name__ == '__main__':
    print("\n🏥 Hospital Operations System - Simple MySQL Test\n")
    
    success = test_mysql_connection()
    
    if success:
        print("\n🎉 MySQL connection successful!")
        print("\nNext steps:")
        print("  1. Run Django migrations: python manage.py migrate")
        print("  2. Test with Django: python test_db_connection.py")
    else:
        print("\n⚠️  Please fix the issues above before proceeding.")
        sys.exit(1)
