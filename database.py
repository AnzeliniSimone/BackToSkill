from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import Table
from sqlalchemy.orm import backref

engine = create_engine('sqlite:///BackToSkill.db')


Base = declarative_base()



class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String)
    Password = Column(String)


### utenti che si registrano, bisogna implemantare la divisione tra common e admin

class Employee(Base):
    # Personal
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    Photo = ''  # links to be added
    Name_and_Surname = Column(String)
    Email = Column(String)
    Telephone_Number = Column(String)
    Date_of_Birth = Column(String)
    Living_Place = Column(String)
    Drive_Licence = Column(String)
    Superior = Column(String)
    Healthy_State = Column(String)
    State_in_the_company = Column(String)

class Soft_skill(Base):
    __tablename__ = 'softskills'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    employee = relationship(Employee, secondary='employee_softskill', backref=backref('softskills'))
    role = relationship('Role', secondary='softskill_role', backref=backref('softskills'))


class Role(Base):
    __tablename__ = 'role'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

class Hard_skill(Base):
    __tablename__ = 'hardskills'
    id = Column(Integer, primary_key=True)
    description = Column(String)
    employee = relationship('Employee', secondary='employee_hardskill', backref=backref('hardskills'))
    role = relationship('Role', secondary='hardskill_role', backref=backref('hardskills'))


class education(Base):
    __tablename__ = 'education'
    id = Column(Integer, primary_key=True)
    Degree = Column(String)
    Language_Certification = Column(String)
    Course_Certification = Column(String)

class trainings(Base):
    __tablename__ = 'trainings'
    id = Column(Integer, primary_key=True)
    Training = Column(String)
    Starting_Date = Column(String)
    Ending_Date = Column(String)
    Skill_Acquired = Column(String)
    employee = relationship('employee', secondary='employee_trainings', backref=backref('trainings'))


class assessment(Base):
    __tablename__ = 'assessment'
    id = Column(Integer, primary_key=True)
    Assessment = Column(String)
    Date = Column(String)
    Made_By = Column(String)
    employee = relationship('employee', secondary='employee_assessment', backref=backref('assessment'))


class projects(Base):
    __tablename__ = 'projects'
    id = Column(Integer, primary_key=True)
    Project = Column(String)
    Starting_Date = Column(String)
    Ending_Date = Column(String)
    employee = relationship('employee', secondary='employee_projects', backref=backref('projects'))





class roleinaproject(Base):
    __tablename__ = 'roleinaproject'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    project = relationship('project', secondary='project_roleinaproject', backref=backref('roleinaproject'))


employee_softskill = Table('employee_softskill',
                           Base.metadata,
                           Column('employee', Integer, ForeignKey(Employee.id)),
                           Column('softskill', Integer, ForeignKey(Soft_skill.id)),
                           Column('grade', Integer))
# tabella intermedia che collega many to many employees e softskills

employee_hardskill = Table('employee_hardskill', Base.metadata,
                           Column('employee', Integer, ForeignKey(Employee.id)),
                           Column('hardskill', Integer, ForeignKey(Hard_skill.id)),
                           Column('grade', Integer))
# tabella che collega many to many employees e hardskills

softskill_role = Table('softskill_role', Base.metadata,
                       Column('softskill', Integer, ForeignKey(Soft_skill.id)),
                       Column('role', Integer, ForeignKey(Role.id)),
                       Column('grade_request', Integer))

hardskill_role = Table('hardskill_role', Base.metadata,
                       Column('hardskill', Integer, ForeignKey(Hard_skill.id)),
                       Column('role', Integer, ForeignKey(Role.id)),
                       Column('grade_request', Integer))




employee_trainings = Table('employee_trainings', Base.metadata,
                           Column('employee', Integer, ForeignKey(Employee.id)),
                           Column('trainings', Integer, ForeignKey(trainings.id))
                           )
# tabella che collega many to many employees e trainings
project_roleinaproject = Table('project_role', Base.metadata,
                               Column('project', Integer, ForeignKey(projects.id)),
                               Column('roleinproject', Integer, ForeignKey(roleinaproject.id)),
                               Column('numberofpeople', Integer))

employee_assessment = Table('employee_assessment', Base.metadata,
                            Column('employee', Integer, ForeignKey(Employee.id)),
                            Column('assessment', Integer, ForeignKey(assessment.id))
                            )
# tabella che collega many to many employees e assessment


employee_projects = Table('employee_projects', Base.metadata,
                          Column('employee', Integer, ForeignKey(Employee.id)),
                          Column('projects', Integer, ForeignKey(projects.id)),
                          )


# tabella che collega many to many employees e project


Base.metadata.create_all(engine)

    




