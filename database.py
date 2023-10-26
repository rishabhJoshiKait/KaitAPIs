from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_Database='postgresql://root:dPbtiKHQAltVPinKlHrx4tMYhcYlAc4t@dpg-ckt62jo168ec73efttj0-a.oregon-postgres.render.com/fleet_data'
# URL_Database='mysql+pymysql://root:rishabh123@localhost:3306/fleetrez1'
engine = create_engine(URL_Database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# postgres://root:dPbtiKHQAltVPinKlHrx4tMYhcYlAc4t@dpg-ckt62jo168ec73efttj0-a.oregon-postgres.render.com/fleet_data
