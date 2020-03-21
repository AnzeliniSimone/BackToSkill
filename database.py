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
  

#---------------------------------------------------------------------------------
class employee(Base):

    #Personal
    _tablename_ = 'employees'
    id = Column(Integer, primary_key = True)
    Photo = ''  #links to be added
    Name_and_Surname = Column(String)
    Email = Column(String)
    Telephone_Number = Column(String)
    Date_of_Birth = Column(String)
    Living_Place = Column(String)
    Drive_Licence = Column(String)
    Superior = Column(String)
    Healthy_State = Column(String)
    State_in_the_company = Column(String)

class education(Base):
    _tablename_ = 'education'
    id = Column(Integer, primary_key=True)
    Degree = Column(String)
    Language_Certification = Column(String)
    Course_Certification = Column(String)



employee_trainings= table('employee_trainings',Base.metadata,
                         Column('employee',Integer,ForeignKey(employee.id)),
                         Column('trainings',Integer,ForeignKey(trainings.id))
                         )
#tabella che collega many to many employees e trainings


employee_assessment = table('employee_assessment', Base.metadata,
                            Column('employee', Integer, ForeignKey(employee.id)),
                            Column('assessment', Integer, ForeignKey(assessment.id))
                            )
# tabella che collega many to many employees e assessment


employee_projects = table('employee_projects', Base.metadata,
                          Column('employee', Integer, ForeignKey(employee.id)),
                          Column('projects', Integer, ForeignKey(projects.id)),
                          )
# tabella che collega many to many employees e projects



class trainings(Base):
    _tablename_ = 'trainings'
    id = Column(Integer, primary_key=True)
    Training = Column(String)
    Starting_Date = Column(String)
    Ending_Date = Column(String)
    Skill_Acquired = Column(String)
    employee = Relationship('employee', secondary=employee_trainings, backref=backref('trainings');


class assessment(Base):
    _tablename_ = 'assessment'
    id = Column(Integer, primary_key=True)
    Assessment = Column(String)
    Date = Column(String)
    Made_By = Column(String)
    employee = Relationship('employee', secondary=employee_assessment, backref=backref('assessment');


class projects(Base):
    _tablename_ = 'projects'
    id = Column(Integer, primary_key=True)
    Project = Column(String)
    Starting_Date = Column(String)
    Ending_Date = Column(String)
    employee = Relationship('employee', secondary=employee_projects, backref=backref('projects');



    




