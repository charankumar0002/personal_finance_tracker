#!/usr/bin/env python3
"""
PostgreSQL Setup Script for Personal Finance Tracker
This script helps you configure your PostgreSQL database connection.
"""

import os
import getpass
from pathlib import Path

def create_env_file():
    """Create .env file with PostgreSQL configuration"""
    
    print("=== PostgreSQL Database Setup ===")
    print("Please provide your PostgreSQL connection details:")
    
    # Get database connection details
    db_user = input("Database username (default: postgres): ").strip() or "postgres"
    db_password = getpass.getpass("Database password: ").strip()
    db_host = input("Database host (default: localhost): ").strip() or "localhost"
    db_port = input("Database port (default: 5432): ").strip() or "5432"
    db_name = input("Database name (default: personal_finance_db): ").strip() or "personal_finance_db"
    
    # Generate a random secret key
    import secrets
    secret_key = secrets.token_urlsafe(32)
    
    # Create .env file content
    env_content = f"""# Database Configuration
DATABASE_URL=postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}

# Security
SECRET_KEY={secret_key}

# Debug mode
DEBUG=True
"""
    
    # Write .env file
    env_path = Path(__file__).parent / ".env"
    with open(env_path, "w") as f:
        f.write(env_content)
    
    print(f"\n✅ Environment file created at: {env_path}")
    print("📝 Please review and update the .env file if needed.")
    
    return True

def test_connection():
    """Test the database connection"""
    try:
        from app.config import settings
        from app.db.session import engine
        from sqlalchemy import text  # Add this import
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))  # Use text() for raw SQL
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_database():
    """Create database and tables"""
    try:
        import app.db.create_db_and_tables
        print("✅ Database and tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Failed to create database/tables: {e}")
        return False

def main():
    print("🚀 Setting up PostgreSQL for Personal Finance Tracker")
    print()
    
    # Step 1: Create .env file
    if create_env_file():
        print("\n" + "="*50)
        
        # Step 2: Create database and tables
        print("Creating database and tables...")
        if create_database():
            print("\n" + "="*50)
            
            # Step 3: Test connection
            print("Testing database connection...")
            if test_connection():
                print("\n🎉 Setup completed successfully!")
                print("\nNext steps:")
                print("1. Start the backend server: python -m uvicorn app.main:app --reload")
                print("2. Access the API documentation at: http://localhost:8000/docs")
            else:
                print("\n⚠️  Setup completed with warnings. Please check the database configuration.")
        else:
            print("\n❌ Setup failed. Please check your PostgreSQL configuration.")
            print("\nTroubleshooting tips:")
            print("1. Make sure PostgreSQL is running")
            print("2. Verify your username and password")
            print("3. Check if the database port is correct (default: 5432)")
            print("4. Ensure the database user has permission to create databases")

if __name__ == "__main__":
    main() 