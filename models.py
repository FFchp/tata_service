from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from database import Base

class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True, index=True, autoincrement = True)
    username = Column(String)
    email = Column(String)
    password = Column(String)
    permission = Column(String)

class billet(Base):
    __tablename__ = 'billet'
    no = Column(Integer, index = True, autoincrement = True)
    billet_no = Column(Integer, primary_key=True, autoincrement = True)
    timestamp = Column(DateTime)
    file_name = Column(String)
    id = Column(Integer, ForeignKey('user.id'))
