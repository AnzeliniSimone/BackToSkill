from flask import Flask
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

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
    project = db.relationship('Projects', secondary=project_roleinaproject, backref=db.backref('roleinaproject'))

<<<<<<< Updated upstream
=======
def fill_table():

    employee1 = Employee(id=0,name_and_surname='Francesco De Zorzi',telephone_number='857384839')
    employee2 = Employee(id=1, name_and_surname='Francesco Del Frabbro', telephone_number='75763893')
    employee3 = Employee(id=2, name_and_surname='Giulia Ioannone', telephone_number='938723642')
    employee4 = Employee(id=3, name_and_surname='Otabek Razakkov', telephone_number='428764728')
    employee5 = Employee(id=4, name_and_surname='Matteo Piovesan', telephone_number='0872637123')

    db.session.add(employee1)
    db.session.add(employee2)
    db.session.add(employee3)
    db.session.add(employee4)
    db.session.add(employee5)

    project1 = Projects(id=0,project='create a new product',starting_date='04/05/2019',ending_date='02/05/2020',employee=[employee1,employee2,employee4])
    project2 = Projects(id=1, project='analyze the balace sheet', starting_date='12/10/2019', ending_date='23/03/2019', employee=[employee5, employee2, employee1])
    project3 = Projects(id=2, project='reorginize the production line ', starting_date='12/05/2020', ending_date='22/08/2020', employee=[employee5, employee3])
    project4 = Projects(id=3, project='hire new workers ', starting_date='16/02/2019', ending_date='17/09/2019', employee=[employee1])

    db.session.add(project1)
    db.session.add(project2)
    db.session.add(project3)
    db.session.add(project4)

    rolep1 = Roleinaproject(id=0,name='Manager',project=[project1,project2,project3,project4])
    rolep2 = Roleinaproject(id=1, name='Normal employee', project=[project1, project2, project4])
    rolep3 = Roleinaproject(id=2, name='Hr', project=[project1, project2, project3])
    rolep4 = Roleinaproject(id=3, name='the thinker', project=[project2, project3, project4])
    rolep5 = Roleinaproject(id=4, name='The one that do nothing', project=[project1, project3, project4])

    db.session.add(rolep1)
    db.session.add(rolep2)
    db.session.add(rolep3)
    db.session.add(rolep4)
    db.session.add(rolep5)







>>>>>>> Stashed changes
