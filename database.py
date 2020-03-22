from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine

#bisogna ancora creare la sessione

engine = create_engine('sqlite:///testdb.db') #non so che path bisogna usare

Base= declarative_base()

class User(Base):
    __tablename__='user'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    surname=Column(String)
    email=Column(String)
    Password=Column(String)

### utenti che si registrano, bisogna implemantare la divisione tra common e admin

class employee(Base):

    #Personal
    _tablename_ = 'employee'
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

class Role(Base):
    __tablename__='role'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    description=Column(string)


employee_softskill=table('employee_softskill',
                         Base.metadata,
                         Column('employee',Integer,ForeignKey(employee.id)),
                         Column('softskill',Integer,ForeignKey(softskills.id)),
                         Column('grade',Integer))
#tabella intermedia che collega many to many employees e softskills

employee_hardskill=table('employee_hardskill',Base.metadata,
                         Column('employee',Integer,ForeignKey(employee.id)),
                         Column('hardskill',Integer,ForeignKey(hardskills.id)),
                         Column('grade',Integer))
#tabella che collega many to many employees e hardskills 

softskill_role=table('softskill_role',Base.metadata,
                     Column('softskill',Integer,ForeignKey(softskills.id)),
                     Column('role',Integer,ForeignKey(role.id)),
                     Column('grade_request',Integer))

hardskill_role=table('hardskill_role',Base.metadata,
                     Column('hardskill',Integer,ForeignKey(hardskills.id)),
                     Column('role',Integer,ForeignKey(role.id)),
                     Column('grade_request',Integer))

class Soft_skill(Base):
    __tablename__='softskills'
    id=Column(Integer,primary_key=True)
    description=Column(String)
    employee = Relationship('Employee',secondary=employee_softskill,backref=backref('softskills'))
    role=Relationship('Role',secondary=softskill_role,backref=backref('softskills'))

class Hard_skill(Base):
    __tablename__='hardskills'
    id=Column(Integer,primary_key=True)
    description=Column(String)
    employee= Relationship ('Employee',secondary=employee_hardskill,backref=backref('hardskills'))
    role = Relationship('Role', secondary=hardskill_role, backref=backref('hardskills'))

class education(Base):
    _tablename_ = 'education'
    id = Column(Integer, primary_key=True)
    employee_id=Column(Integer,ForeignKey(employee.id))
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
# tabella che collega many to many employees e project


class trainings(Base):
    _tablename_ = 'trainings'
    id = Column(Integer, primary_key=True)
    Training = Column(String)
    Starting_Date = Column(String)
    Ending_Date = Column(String)
    Skill_Acquired = Column(String)
    employee = Relationship('employee', secondary=employee_trainings, backref=backref('trainings'))


class assessment(Base):
    _tablename_ = 'assessment'
    id = Column(Integer, primary_key=True)
    Assessment = Column(String)
    Date = Column(String)
    Made_By = Column(String)
    employee = Relationship('employee', secondary=employee_assessment, backref=backref('assessment'))


class projects(Base):
    _tablename_ = 'projects'
    id = Column(Integer, primary_key=True)
    Project = Column(String)
    Starting_Date = Column(String)
    Ending_Date = Column(String)
    employee = Relationship('employee', secondary=employee_projects, backref=backref('projects'))

project_roleinaproject=table('project_role',Base.metadata,
                             Column('project',Integer,ForeignKey(projects.id)),
                             Column('roleinproject',Integer,ForeignKey(roleinproject.id)),
                             Column('numberofpeople',Integer))

class RoleinProject(Base):
    __tablename__='roleinproject'
    id=Column(Integer,primary_key=True)
    name=Column(String)
    description=Column(String)
    project=Relationship('project',secondary=project_roleinaproject,backref=backref('roleinproject'))

Base.metadata.create_all(engine)



    





