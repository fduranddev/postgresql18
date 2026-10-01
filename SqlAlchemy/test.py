from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Product, Warehouse, Stock

db_user = "postgres"
db_password = "admin"
db_host = "127.0.0.1"
db_port = "5432"
db_name = "test_alchemy"

db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"

engine = create_engine(db_url)

try:
        
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    chaussure = Product(name='Chaussure',description="Une belle paire de chaussure", price="20.99")
    session.add(chaussure)
    session.commit()

    chaussure.price = 30.99
    session.commit()
    

except Exception as ex:
    print(ex)
