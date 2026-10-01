#-------------
# database.py
#-------------

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "postgresql+psycopg2://postgres:admin@localhost:5434/testdb"

# Création de l'engine SQLAlchemy
engine = create_engine(DATABASE_URL, echo=True)

# Création d'une factory de sessions
SessionLocal = sessionmaker(bind=engine)



