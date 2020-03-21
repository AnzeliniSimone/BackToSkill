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
class Employees_Personal(Base):

    #Personal
    _tablename_ = 'Employees Personal'
    id = Column(Integer, primary_key = True)
    Photo =
    Name_and_Surname = Column(String)
    Email = Column(String)
    Telephone_Number = Column(String)
    Date_of_Birth = Column(String)
    Living_Place = Column(String)
    Drive_Licence = Column(String)
    Superior = Column(String)
    Healthy_State = Column(String)
    State_in_the_company = Column(String)

class Employees_Education(Base):
    # Education
    _tablename_ = 'Employees Education'
    id = Column(Integer, primary_key=True)
    Degree = Column(String)
    Language_Certification = Column(String)
    Course_Certification = Column(String)

class Employees_Skills(Base):
    _tablename_ = 'Employees Skills'
    id = Column(Integer, primary_key=True)
    #Skills
    Soft_Skill1 = Column(Integer)
    Soft_Skill2 = Column(Integer)
    Soft_Skill3 = Column(Integer)
    Soft_Skill4 = Column(Integer)
    Soft_Skill5 = Column(Integer)

    Technical_Skill1 = Column(Integer)
    Technical_Skill2 = Column(Integer)
    Technical_Skill3 = Column(Integer)
    Technical_Skill4 = Column(Integer)
    Technical_Skill5 = Column(Integer)

class Employees_TrainingsUpcomings(Base):
    _tablename_ = 'Employees Trainings Upcoming'
    id = Column(Integer, primary_key=True)
    #Trainings Upcomings
    Training1 = Column(String)
    Date1 = Column(String)
    Training_Type1 = Column(String)
    Skill_Acquired1 = Column(String)

    Training2 = Column(String)
    Date2 = Column(String)
    Training_Type2 = Column(String)
    Skill_Acquired2 = Column(String)

    Training3 = Column(String)
    Date3 = Column(String)
    Training_Type3 = Column(String)
    Skill_Acquired3 = Column(String)

    Training4 = Column(String)
    Date4 = Column(String)
    Training_Type4 = Column(String)
    Skill_Acquired4 = Column(String)

    Training5 = Column(String)
    Date5 = Column(String)
    Training_Type5 = Column(String)
    Skill_Acquired5 = Column(String)

class Employees_TrainingsCompleted(Base):
    _tablename_ = 'Employees Trainings Completed'
    id = Column(Integer, primary_key=True)
    #Trainings Complete
    Training1 = Column(String)
    Date1 = Column(String)
    Training_Type1 = Column(String)
    Skill_Acquired1 = Column(String)

    Training2 = Column(String)
    Date2 = Column(String)
    Training_Type2 = Column(String)
    Skill_Acquired2 = Column(String)

    Training3 = Column(String)
    Date3 = Column(String)
    Training_Type3 = Column(String)
    Skill_Acquired3 = Column(String)

    Training4 = Column(String)
    Date4 = Column(String)
    Training_Type4 = Column(String)
    Skill_Acquired4 = Column(String)

    Training5 = Column(String)
    Date5 = Column(String)
    Training_Type5 = Column(String)
    Skill_Acquired5 = Column(String)

class Employees_Assessment(Base):
    _tablename_ = 'Employees Assessment'
    id = Column(Integer, primary_key=True)
    #Assessment
    Assessment1 = Column(String)
    Date1 = Column(String)
    Made_By1 = Column(String)

    Assessment2 = Column(String)
    Date2 = Column(String)
    Made_By2 = Column(String)

    Assessment3 = Column(String)
    Date3 = Column(String)
    Made_By3 = Column(String)

    Assessment4 = Column(String)
    Date4 = Column(String)
    Made_By4 = Column(String)

    Assessment5 = Column(String)
    Date5 = Column(String)
    Made_By5 = Column(String)

class Employees_Project_Upcomings(Base):
    _tablename_ = 'Employees Projects Upcoming'
    id = Column(Integer, primary_key=True)
    #Project_Works
    Project_Work1 = Column(String)
    Beginning_Date1 = Column(String)
    Ending_Date1 = Column(String)

    Project_Work2 = Column(String)
    Beginning_Date2 = Column(String)
    Ending_Date2 = Column(String)

    Project_Work3 = Column(String)
    Beginning_Date3 = Column(String)
    Ending_Date3 = Column(String)

class Employees_Project_WorkInProgress(Base):
    _tablename_ = 'Employees Projects in Progress'
    id = Column(Integer, primary_key=True)
    #Project_Works
    Project_Work1 = Column(String)
    Beginning_Date1 = Column(String)
    Ending_Date1 = Column(String)

    Project_Work2 = Column(String)
    Beginning_Date2 = Column(String)
    Ending_Date2 = Column(String)

    Project_Work3 = Column(String)
    Beginning_Date3 = Column(String)
    Ending_Date3 = Column(String)

class Employees_Project_Completed(Base):
    _tablename_ = 'Employees Projects Completed'
    id = Column(Integer, primary_key=True)
    Project_Work1 = Column(String)
    Beginning_Date1 = Column(String)
    Ending_Date1 = Column(String)

    Project_Work2 = Column(String)
    Beginning_Date2 = Column(String)
    Ending_Date2 = Column(String)

    Project_Work3 = Column(String)
    Beginning_Date3 = Column(String)
    Ending_Date3 = Column(String)


    




