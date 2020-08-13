from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = "sqlite:///./stocks.db"
# SQLALCHEMY_DATABASE_URL = "mariadb://root:@localhost/db"
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://fastapi:12345@localhost:3306/test"


engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()