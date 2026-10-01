import os


DB_CONFIG = {
    "host": os.getenv("BIB_DB_HOST", "localhost"),
    "port": int(os.getenv("BIB_DB_PORT", "5436")),
    "dbname": os.getenv("BIB_DB_NAME", "bibliotheque"),
    "user": os.getenv("BIB_DB_USER", "postgres"),
    "password": os.getenv("BIB_DB_PASSWORD", "admin"),
}
