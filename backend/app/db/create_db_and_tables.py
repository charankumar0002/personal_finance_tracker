import os
import re
import psycopg2
from sqlalchemy import create_engine
from app.db.models import Base
from app.config import settings

# Parse DATABASE_URL (support both with and without '+psycopg2')
DATABASE_URL = settings.DATABASE_URL
pattern = r"postgresql(?:\+psycopg2)?://(.*?):(.*?)@(.*?):(\d+)/(.*)"
match = re.match(pattern, DATABASE_URL)
if not match:
    raise ValueError(f"DATABASE_URL is not in the expected format: {DATABASE_URL}")
user, password, host, port, dbname = match.groups()

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