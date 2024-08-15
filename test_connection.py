from sqlalchemy import create_engine

# Replace with your actual URL
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/belajarpython"

# Create an engine
engine = create_engine(DATABASE_URL)

try:
    # Attempt to connect
    with engine.connect() as connection:
        print("Connection successful!")
except Exception as e:
    print(f"Error: {e}")


