from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine

#bisogna ancora creare la sessione

engine = create_engine('sqlite:///testdb.db')

Base= declarative_base()

class User(Base):
    __tablename__='utenti'
    id=Column(Integer,primary_key=true)
    name=Column(String)
    surname=Column(String)
    email=Column(String)
    Password=Column(String)

### utenti che si registrano, bisogna implemantare la divisione tra common e admin

class Role(Base)
    __tablename__='ruolo'
    id=Column(Integer,primary_key=true)
    name=Column(String)
    description=Column(string)

class Project(Base)
    __tablename__='progetti'
    id=Column(Integer,primary_key=true)
    name=Column(String)
    description=Column(String)
    start=Column(String)
    end=Column(String)

class Soft_skill(Base)
    __tablename__='softskills'
    id=Column(Integer,primary_key=true)
    description=Column(String)

class Hard_skill(Base)
    __tablename__='hardskills'
    id=Column(Integer,primary_key=true)
    description=Column(String)
    
    
    kksksksk

    




