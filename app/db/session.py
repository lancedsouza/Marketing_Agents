from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker



DATABASE_URL = "sqlite:///./recruit_ai.db"  
engine= create_engine("sqlite:///./recruit_ai.db", connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()