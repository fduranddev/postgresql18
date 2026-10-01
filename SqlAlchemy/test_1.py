from sqlalchemy import create_engine

db_user = "postgres"
db_password = "admin"
db_host = "127.0.0.1"
db_port = "5434"
db_name = "test_db"

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url, echo=True)


