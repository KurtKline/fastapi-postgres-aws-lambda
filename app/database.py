from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# user = os.environ["DB_USER"]
# password = os.environ["DB_PASS"]
# host = os.environ["DB_HOST"]
# port = os.environ["DB_PORT"]
# database = os.environ["DB_NAME"]

# SQLALCHEMY_DATABASE_URL = f"mysql://{user}:{password}@{host}:{port}/{database}"
# SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://dev:dev@127.0.0.1:3306/fitness"
SQLALCHEMY_DATABASE_URL = "sqlite:///dev-sqlite-database.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://zhzpvzruoasfks:2956c6212623be97d7cbef514ca7d387050dd799083ecd1b0d60254a020d53f3@ec2-34-230-198-12.compute-1.amazonaws.com:5432/d46uj9ac9lcdab"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
