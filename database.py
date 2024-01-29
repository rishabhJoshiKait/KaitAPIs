from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_Database='postgresql://fleets_user:Op70FKpyG246EhwLuf5ynqIwZlJlbnyt@dpg-cmrlhmi1hbls73fpqv20-a.oregon-postgres.render.com/fleets?sslmode=require&sslrootcert=/path/to/root.crt&sslkey=/path/to/client.key&sslcert=/path/to/client.crt'
# URL_Database='mysql+pymysql://root:rishabh123@localhost:3306/fleetrez1'
engine = create_engine(URL_Database,  pool_pre_ping=True, pool_recycle=200000)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# postgres://root:G4D4d4WnyMtF8qLccw8SHMIUBXOkWFcx@dpg-cktj48lk4k9c73amu200-a.oregon-postgres.render.com/fleetrez_db
