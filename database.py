from flask_sqlalchemy import SQLAlchemy
import datetime
from random import randint
db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)
    admin = db.Column(db.Boolean)
    # TODO: AGGIUNGERE ENCRYPTION


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    employee = db.relationship("Employee")


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100), nullable=False, default='')
    cv = db.Column(db.String) #eventually we can put a link to the Curriculum Vitae file
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    telephone = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    date_of_assumption = db.Column(db.String)
    living_place = db.Column(db.String)
    driving_licence = db.Column(db.Boolean) #I would say we only specify whether he/she has it or not, so true or false
    role = db.Column(db.Integer, db.ForeignKey('role.id'))
    skill = db.relationship("Employee_Skill", back_populates="employee")
    project = db.relationship("Employee_Project", back_populates="employee")
    training = db.relationship("Employee_Training", back_populates="employee")


class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    type = db.Column(db.String) #HAS TO BE "Soft" OR "Hard", no other options (also watch for case, so Hard is good, hard is not
    employee = db.relationship('Employee_Skill', back_populates='skill')
    training = db.relationship('Training_Skill', back_populates='skill')
    project = db.relationship('Project_Skill', back_populates='skill')


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    starting_date = db.Column(db.String)
    ending_date = db.Column(db.String)
    employee = db.relationship("Employee_Project", back_populates="project")
    skill = db.relationship("Project_Skill", back_populates="project")
    supervisor = db.Column(db.Integer, db.ForeignKey('employee.id'))


class Role_in_project(db.Model):
    __tablename__ = 'role_in_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    project_employee = db.relationship("Employee_Project")


class Training(db.Model):
    __tablename__ = 'training'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    starting_Date = db.Column(db.String)
    ending_Date = db.Column(db.String)
    hours = db.Column(db.Integer)
    skill = db.relationship("Training_Skill", back_populates="training")
    employee = db.relationship("Employee_Training", back_populates="training")


class Employee_Skill(db.Model):
    __tablename__ = 'employee_skill'
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    ss_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    grade = db.Column(db.Integer)
    employee = db.relationship("Employee", back_populates="skill")
    skill = db.relationship("Skill", back_populates="employee")


class Employee_Project(db.Model):
    __tablename__ = 'employee_project'
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    prj_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey('role_in_project.id'))
    evaluation = db.Column(db.String)
    employee = db.relationship("Employee", back_populates="project")
    project = db.relationship("Project", back_populates="employee")


class Training_Skill(db.Model):
    __tablename__ = 'training_skill'
    train_id = db.Column(db.Integer, db.ForeignKey('training.id'), primary_key=True)
    ss_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    points = db.Column(db.Integer)
    training = db.relationship("Training", back_populates="skill")
    skill = db.relationship("Skill", back_populates="training")


class Employee_Training(db.Model):
    __tablename__ = 'employee_training'
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('training.id'), primary_key=True)
    employee = db.relationship("Employee", back_populates="training")
    training = db.relationship("Training", back_populates="employee")


class Project_Skill(db.Model):
    __tablename__ = 'project_skill'
    prj_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    ss_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    grade_required = db.Column(db.Integer)
    project = db.relationship("Project", back_populates="skill")
    skill = db.relationship("Skill", back_populates="project")


def fillEmployee(db):
    emp = Employee()
    for i in range(10):
        emp = Employee(name="Emp "+str(i+1), surname="loyee", email="emp"+str(i)+"@b2s.com", date_of_birth=datetime.date(randint(1965,1998),randint(1,12),randint(1,28)), driving_licence=True)
        db.session.add(emp)
    db.session.commit()