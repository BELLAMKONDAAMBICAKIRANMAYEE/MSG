
# import os
# from typing import Annotated
# from dotenv import load_dotenv
# from sqlalchemy import create_engine
# from sqlalchemy.orm import DeclarativeBase, sessionmaker
# from sqlalchemy.orm import Session

# # from app.database import SessionLocal

# load_dotenv()


# class Base(DeclarativeBase):
#     pass


# DATABASE_URL = os.getenv("DATABASE_URL")

# if not DATABASE_URL:
#     raise RuntimeError("DATABASE_URL is missing from .env")

# engine = create_engine(
#     DATABASE_URL,
#     pool_pre_ping=True,
# )

# SessionLocal = sessionmaker(
#     bind=engine,
#     autoflush=False,
#     expire_on_commit=False,
# )


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# database.py

import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Read database configuration from environment variables
DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.environ["DB_USER"],
    password=os.environ["DB_PASSWORD"],
    host=os.environ["DB_HOST"],
    port=int(os.getenv("DB_PORT", "3306")),
    database=os.environ["DB_NAME"],
)

# Aiven's CA certificate file
ca_path = os.getenv("DB_CA_CERT", "ca.pem")
ca_file = Path(ca_path)

connect_args = {}
if ca_file.is_file():
    connect_args["ssl"] = {"ca": str(ca_file)}

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=1800,
    connect_args=connect_args,
)

LocalSession = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)

class Base(DeclarativeBase):
    pass

def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()

