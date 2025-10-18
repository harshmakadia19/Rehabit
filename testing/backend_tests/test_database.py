"""
Database Tests for Rehabit
Tests database operations and data integrity
Author: Rishi Nalam
"""
import pytest
import sys
import os
from datetime import datetime, timedelta
import sqlite3

# Add backend to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../backend'))

# Database path (adjust based on your setup)
DB_PATH = os.path.join(os.path.dirname(__file__), '../../backend/rehabit.db')


class TestDatabaseConnection:
    """Test database connectivity"""
    
    def test_database_exists(self):
        """Test that database file exists"""
        assert os.path.exists(DB_PATH), "Database file not found"
        print(f"✅ Database found at: {DB_PATH}")
    
    def test_database_connection(self):
        """Test database connection"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        conn.close()
        assert result[0] == 1
        print("✅ Database connection successful")


class TestDatabaseSchema:
    """Test database schema"""
    
    def test_users_table_exists(self):
        """Test users table exists with correct schema"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        result = cursor.fetchone()
        assert result is not None, "Users table not found"
        
        # Check table schema
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        assert 'id' in column_names
        assert 'name' in column_names
        assert 'email' in column_names
        assert 'created_at' in column_names
        
        conn.close()
        print("✅ Users table schema is correct")
    
    def test_activities_table_exists(self):
        """Test activities table exists with correct schema"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activities'")
        result = cursor.fetchone()
        assert result is not None, "Activities table not found"
        
        # Check table schema
        cursor.execute("PRAGMA table_info(activities)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        assert 'id' in column_names
        assert 'user_id' in column_names
        assert 'activity_type' in column_names
        assert 'duration' in column_names
        assert 'productivity_score' in column_names
        assert 'timestamp' in column_names
        
        conn.close()
        print("✅ Activities table schema is correct")


class TestUserOperations:
    """Test user CRUD operations"""
    
    def test_insert_user(self):
        """Test inserting a new user"""
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        test_email = f"test_{datetime.now().timestamp()}@rehabit.com"
        cursor.execute(
            "INSERT INTO users (name, email, created_at) VALUES (?, ?, ?)",
            ("Test User", test_email, datetime.now().isoformat())
        )
        conn.commit()
        user_id = cursor.lastrowid
        
        # Verify insertion
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        user = cursor.fetchone()
        conn.close()
        
        assert user is not None
        assert user[1] == "Test User"
        assert user[2] == test_email
        print(f"✅ User inserted with ID: {user_id}")


if __name__ == "__main__":
    print("\n���️  Running Rehabit Database Tests\n")
    pytest.main([__file__, "-v", "--tb=short"])
