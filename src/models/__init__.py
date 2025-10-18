from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, scoped_session

engine = create_engine("mysql+pymysql://root@localhost:3307/merkait?charset=utf8mb4")

connection = engine.connect()

Base = declarative_base()
Base.metadata.bind = engine



SessionLocal = scoped_session(sessionmaker(bind=engine))
session = SessionLocal()


session = SessionLocal()