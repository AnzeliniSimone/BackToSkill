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
    
employee_softskill=table('employee_softskill',Base.metadata,Column('employee',Integer,ForeignKey(employee.id)),Column('softskill',Integer,ForeignKey(softskills.id)),Column('grade',Integer))
#tabella intermedia che collega many to many employees e softskills

employee_hardskill=table('employee_hardskill',Base.metadata,Column('employee',Integer,ForeignKey(employee.id)),Column('hardskill',Integer,ForeignKey(hardskills.id)),Column('grade',Integer))
#tabella che collega many to many employees e hardskills 

class Soft_skill(Base)
    __tablename__='softskills'
    id=Column(Integer,primary_key=true)
    description=Column(String)
    employee = Relationship('Employee',secondary=employee_softskill,backref=backref('softskills'))

class Hard_skill(Base)
    __tablename__='hardskills'
    id=Column(Integer,primary_key=true)
    description=Column(String)
    employee= Relationship ('Employee',secondary=employee_hardskill,backref=backref('hardskills'))
  

    




