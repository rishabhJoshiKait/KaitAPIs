from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_Database='postgresql://kai_api_user:eJix0ZnC4ohapciIDXVpmbJDI4bnLWK1@dpg-cknasoiv7m0s73bu4psg-a.singapore-postgres.render.com/kai_api'
engine = create_engine(URL_Database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
