from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
db = SQLAlchemy(app)

employee_softskill = db.Table('employee_softskill',
                              db.Column('employee', db.Integer, db.ForeignKey('employee.id')),
                              db.Column('softskill', db.Integer, db.ForeignKey('softskill.id')),
                              db.Column('grade', db.Integer))
# tabella intermedia che collega many to many employees e softskills

employee_hardskill = db.Table('employee_hardskill',
                              db.Column('employee', db.Integer, db.ForeignKey('employee.id')),
                              db.Column('hardskill', db.Integer, db.ForeignKey('hardskill.id')),
                              db.Column('grade', db.Integer))
# tabella che collega many to many employees e hardskills

softskill_role = db.Table('softskill_role',
                          db.Column('softskill', db.Integer, db.ForeignKey('softskill.id')),
                          db.Column('role', db.Integer, db.ForeignKey('role.id')),
                          db.Column('grade_request', db.Integer))

hardskill_role = db.Table('hardskill_role',
                          db.Column('hardskill', db.Integer, db.ForeignKey('hardskill.id')),
                          db.Column('role', db.Integer, db.ForeignKey('role.id')),
                          db.Column('grade_request', db.Integer))

employee_trainings = db.Table('employee_trainings',
                              db.Column('employee', db.Integer, db.ForeignKey('employee.id')),
                              db.Column('trainings', db.Integer, db.ForeignKey('trainings.id'))
                              )
# tabella che collega many to many employees e trainings
project_roleinaproject = db.Table('project_role',
                                  db.Column('project', db.Integer, db.ForeignKey('projects.id')),
                                  db.Column('roleinproject', db.Integer,db.ForeignKey('roleinaproject.id')),
                                  db.Column('numberofpeople', db.Integer))

employee_assessment = db.Table('employee_assessment',
                               db.Column('employee', db.Integer, db.ForeignKey('employee.id')),
                               db.Column('assessment', db.Integer, db.ForeignKey('assessment.id'))
                               )
# tabella che collega many to many employees e assessment


employee_projects = db.Table('employee_projects',
                             db.Column('employee', db.Integer, db.ForeignKey('employee.id')),
                             db.Column('projects', db.Integer, db.ForeignKey('projects.id')),
                             )


# tabella che collega many to many employees e project

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return "User('{self.name}', '{self.email}')"


### utenti che si registrano, bisogna implemantare la divisione tra common e admin

class Employee(db.Model):
    # Personal
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(20), nullable=False, default='default.jpg')
    name_and_surname = db.Column(db.String)
    email = db.Column(db.String)
    telephone_number = db.Column(db.String)
    date_of_birth = db.Column(db.String)
    living_place = db.Column(db.String)
    drive_licence = db.Column(db.String)
    superior = db.Column(db.String)
    healthy_state = db.Column(db.String)
    state_in_the_company = db.Column(db.String)


class Softskill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    employee = db.relationship('Employee', secondary=employee_softskill, backref=db.backref('softskills'))
    role = db.relationship('Role', secondary=softskill_role, backref=db.backref('softskills'))


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)


class Hardskill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String)
    employee = db.relationship('Employee', secondary=employee_hardskill, backref=db.backref('hardskills'))
    role = db.relationship('Role', secondary=hardskill_role, backref=db.backref('hardskills'))


class Education(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    degree = db.Column(db.String)
    language_certification = db.Column(db.String)
    course_certification = db.Column(db.String)


class Trainings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    training = db.Column(db.String)
    starting_Date = db.Column(db.String)
    ending_Date = db.Column(db.String)
    skill_acquired = db.Column(db.String)
    employee = db.relationship('Employee', secondary=employee_trainings, backref=db.backref('trainings'))


class Assessment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    assessment = db.Column(db.String)
    date = db.Column(db.String)
    made_by = db.Column(db.String)
    employee = db.relationship('Employee', secondary=employee_assessment, backref=db.backref('assessment'))


class Projects(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    project = db.Column(db.String)
    starting_date = db.Column(db.String)
    ending_date = db.Column(db.String)
    employee = db.relationship('Employee', secondary=employee_projects, backref=db.backref('projects'))


class Roleinaproject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    project = db.relationship('Project', secondary=project_roleinaproject, backref=db.backref('roleinaproject'))
    
db.create_all()
