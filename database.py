from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import psycopg2

URL_Database='postgresql://kai_api_ckgg_user:Y4h8sZYtz6kl9z73VR2t5dKQEngW1bx4@dpg-cksihupqhc9c73d3rdh0-a.singapore-postgres.render.com/kai_api_ckgg'
# URL_Database='mysql+pymysql://root:rishabh123@localhost:3306/fleetrez1'
engine = create_engine(URL_Database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
