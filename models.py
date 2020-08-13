from sqlalchemy import Column, Integer, String
from database import Base


class Questions(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(String(100))
    option1 = Column(String(100))
    option2 = Column(String(100))
    option3 = Column(String(100))

class Student(Base):
    __tablename__ = "student"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    marks = Column(Integer)
