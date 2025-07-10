import os
import re
import psycopg2
from sqlalchemy import create_engine
from app.db.models import Base
from app.config import settings
from urllib.parse import urlparse, unquote

# Parse DATABASE_URL using urllib.parse to handle URL encoding
DATABASE_URL = settings.DATABASE_URL
parsed_url = urlparse(DATABASE_URL)

# Extract components and decode URL-encoded parts
user = unquote(parsed_url.username)
password = unquote(parsed_url.password)
host = parsed_url.hostname
port = parsed_url.port
dbname = parsed_url.path.lstrip('/')

print(f"DEBUG: Parsed connection - user: {user}, host: {host}, port: {port}, dbname: {dbname}")

# Connect to default 'postgres' database to create the target database
conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
conn.autocommit = True
cur = conn.cursor()
cur.execute(f"SELECT 1 FROM pg_database WHERE datname = '{dbname}'")
exists = cur.fetchone()
if not exists:
    cur.execute(f'CREATE DATABASE "{dbname}"')
    print(f"Database '{dbname}' created.")
else:
    print(f"Database '{dbname}' already exists.")
cur.close()
conn.close()

# Now create tables using SQLAlchemy
# If SQLAlchemy expects '+psycopg2', add it for the engine
alchemy_url = DATABASE_URL if '+psycopg2' in DATABASE_URL else DATABASE_URL.replace('postgresql://', 'postgresql+psycopg2://')
engine = create_engine(alchemy_url)
Base.metadata.create_all(bind=engine)
print("All tables created.") 