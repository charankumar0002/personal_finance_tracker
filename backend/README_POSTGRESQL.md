# PostgreSQL Setup for Personal Finance Tracker

This guide will help you set up PostgreSQL for your personal finance tracker application.

## Prerequisites

1. **PostgreSQL installed and running**
   - Make sure PostgreSQL is installed on your system
   - The PostgreSQL service should be running
   - Default port is 5432

2. **Python dependencies installed**
   ```bash
   pip install -r requirements.txt
   ```

## Quick Setup

Run the automated setup script:

```bash
cd backend
python setup_postgres.py
```

This script will:
1. Prompt you for PostgreSQL connection details
2. Create a `.env` file with your configuration
3. Test the database connection
4. Create the database and tables

## Manual Setup

If you prefer to set up manually:

### 1. Create a `.env` file in the `backend` directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@localhost:5432/personal_finance_db

# Security
SECRET_KEY=your-secret-key-here-change-this-in-production

# Debug mode
DEBUG=True
```

### 2. Update the DATABASE_URL with your PostgreSQL details:

- `username`: Your PostgreSQL username (default: postgres)
- `password`: Your PostgreSQL password
- `localhost`: Database host (default: localhost)
- `5432`: Database port (default: 5432)
- `personal_finance_db`: Database name

### 3. Create the database and tables:

```bash
cd backend
python -c "from app.db.create_db_and_tables import *"
```

## Testing the Setup

### 1. Test database connection:

```bash
python -c "from app.db.session import engine; print('Connection successful!' if engine.connect() else 'Connection failed!')"
```

### 2. Start the backend server:

```bash
python -m uvicorn app.main:app --reload
```

### 3. Access the API documentation:

Open your browser and go to: http://localhost:8000/docs

## Troubleshooting

### Common Issues:

1. **Connection refused**
   - Make sure PostgreSQL is running
   - Check if the port is correct (default: 5432)

2. **Authentication failed**
   - Verify your username and password
   - Check if the user has permission to create databases

3. **Database does not exist**
   - The setup script should create it automatically
   - Make sure your user has permission to create databases

### PostgreSQL Commands:

```bash
# Connect to PostgreSQL
psql -U postgres

# List databases
\l

# Create database manually (if needed)
CREATE DATABASE personal_finance_db;

# Connect to your database
\c personal_finance_db

# List tables
\dt
```

## Database Schema

The application will create the following tables:
- Users (for authentication)
- Accounts (bank accounts, credit cards, etc.)
- Transactions (income and expenses)
- Categories (for organizing transactions)

## Security Notes

- Change the `SECRET_KEY` in production
- Use strong passwords for your PostgreSQL user
- Consider using environment variables for sensitive data
- Never commit the `.env` file to version control

## Next Steps

After successful setup:
1. Start the backend server
2. Set up the frontend (if not already done)
3. Begin using the personal finance tracker application 