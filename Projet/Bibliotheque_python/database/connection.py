import psycopg
from config import DB_CONFIG

def get_connection():
    """
    Ouvre une connexion PostgreSQL.
    """
    return psycopg.connect(**DB_CONFIG)
