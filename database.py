from flask_sqlalchemy import SQLAlchemy
import datetime
from random import randint

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    admin = db.Column(db.Boolean)


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    employee = db.relationship("Employee")
    skill = db.relationship("Skill", secondary="role_skill")


class Employee(db.Model):
    __tablename__ = 'employee'
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(100), nullable=False, default='')
    cv = db.Column(db.String) #eventually we can put a link to the Curriculum Vitae file
    name = db.Column(db.String)
    surname = db.Column(db.String)
    email = db.Column(db.String)
    telephone = db.Column(db.String)
    date_of_birth = db.Column(db.Date)
    date_of_assumption = db.Column(db.Date)
    living_place = db.Column(db.String)
    driving_licence = db.Column(db.Boolean) #I would say we only specify whether he/she has it or not, so true or false
    role = db.Column(db.Integer, db.ForeignKey('role.id'))
    skill = db.relationship("Skill", secondary="employee_skill")
    training = db.relationship("Training", secondary="employee_training")
    project_role = db.relationship("Project_Role")
#   To ADD
# state_in_company = db.Column(db.String)
# education_level = db.Column(db.String)
# AGGIUNGERE CLASSE LANGUAGE CERTIFICATE


class Skill(db.Model):
    __tablename__ = 'skill'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    type = db.Column(db.String) #HAS TO BE "Soft" OR "Hard", no other options
    employee = db.relationship("Employee", secondary="employee_skill")
    training = db.relationship("Training", secondary="training_skill")
    role_in_project = db.relationship('Role_in_project', secondary="role_in_project_skill")
    role = db.relationship("Role", secondary="role_skill")


class Project(db.Model):
    __tablename__ = 'project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    starting_date = db.Column(db.Date)
    ending_date = db.Column(db.Date)
    role_in_project = db.relationship("Role_in_project", secondary="project_role")
    supervisor = db.Column(db.Integer, db.ForeignKey('employee.id'))


class Role_in_project(db.Model):
    __tablename__ = 'role_in_project'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    project = db.relationship("Project", secondary="project_role")
    skill = db.relationship("Skill", secondary="role_in_project_skill")


class Training(db.Model):
    __tablename__ = 'training'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    starting_Date = db.Column(db.Date)
    ending_Date = db.Column(db.Date)
    hours = db.Column(db.Integer)
    skill = db.relationship("Skill", secondary="training_skill")
    employee = db.relationship("Employee", secondary="employee_training")


class Employee_Skill(db.Model):
    __tablename__ = 'employee_skill'
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    grade = db.Column(db.Integer)
    employee = db.relationship("Employee", backref='employee_skill')
    skill = db.relationship("Skill", backref='employee_skill')


class Project_Role(db.Model):
    __tablename__ = 'project_role'
    role_id = db.Column(db.Integer, db.ForeignKey('role_in_project.id'), primary_key=True)
    prj_id = db.Column(db.Integer, db.ForeignKey('project.id'), primary_key=True)
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'))
    evaluation = db.Column(db.String)
    role_in_project = db.relationship("Role_in_project", backref='project_role')
    project = db.relationship("Project", backref='project_role')


class Training_Skill(db.Model):
    __tablename__ = 'training_skill'
    train_id = db.Column(db.Integer, db.ForeignKey('training.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    points = db.Column(db.Integer)
    training = db.relationship("Training", backref='training_skill')
    skill = db.relationship("Skill", backref='training_skill')


class Employee_Training(db.Model):
    __tablename__ = 'employee_training'
    emp_id = db.Column(db.Integer, db.ForeignKey('employee.id'), primary_key=True)
    train_id = db.Column(db.Integer, db.ForeignKey('training.id'), primary_key=True)
    employee = db.relationship("Employee", backref='employee_training')
    training = db.relationship("Training", backref='employee_training')


class Role_in_project_Skill(db.Model):
    __tablename__ = 'role_in_project_skill'
    role_id = db.Column(db.Integer, db.ForeignKey('role_in_project.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    grade_required = db.Column(db.Integer)
    role_in_project = db.relationship("Role_in_project", backref='role_in_project_skill')
    skill = db.relationship("Skill", backref='role_in_project_skill')


# // NEW ADDITIONS \\
class Role_Skill(db.Model):
    __tablename__ = 'role_skill'
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), primary_key=True)
    skill_id = db.Column(db.Integer, db.ForeignKey('skill.id'), primary_key=True)
    grade_required = db.Column(db.Integer)
    role = db.relationship("Role", backref='role_skill')
    skill = db.relationship("Skill", backref='role_skill')


def fill_users(db):
    emp = Employee()
    for i in range(10):
        emp = Employee(name="Emp "+str(i+1), surname="loyee", email="emp"+str(i)+"@b2s.com", date_of_birth=datetime.date(randint(1965,1998),randint(1,12),randint(1,28)), driving_licence=True)
        db.session.add(emp)
    db.session.commit()


# // GETTERS \\

# Returns a list of all the employees
def get_employees():
    employees=Employee.query.all()
    employees.sort(key=lambda x: x.name)
    return employees

def get_employee_skill_by_id(emp_id):
    employee = Employee.query.filter(Employee.id == emp_id).first()
    skills = employee.skill
    return skills

def get_employee_by_id(emp_id):
    return Employee.query.filter(Employee.id==emp_id).first()


# Returns a list of all the projects
def get_projects():
    projects=Project.query.all()
    projects.sort(key=lambda x: x.name)
    return projects


def get_projects_and_supervisors():
    projects=Project.query.all()
    projects.sort(key=lambda x: x.name)
    supervisors = []
    for prj in projects:
        if prj.supervisor:
            supervisors.append(get_employee_by_id(prj.supervisor))
    supervisors = list(dict.fromkeys(supervisors))
    return projects, supervisors


def get_role_by_id(role_id):
    return Role.query.filter(Role.id==role_id).first()


def get_skills_required_by_role(role_id):
    role = Role.query.filter(Role.id == role_id).first()
    skill_list=role.skill
    return skill_list


def get_skill_id_of_a_role(role_id):
    role=Role_Skill.query.filter(Role_Skill.role_id==role_id).all()
    return role

def get_project_by_id(prj_id):
    return Project.query.filter(Project.id==prj_id).first()

def get_employee_by_role(role_id):
    empl=Employee.query.filter(Employee.role==role_id).first()
    return empl


# Returns a list of all the past projects
def get_past_projects():
    past_prj=Project.query.filter(Project.ending_date < datetime.date.today()).all()
    supervisors = []
    for prj in past_prj:
        if prj.supervisor:
            supervisors.append(get_employee_by_id(prj.supervisor))
    supervisors = list(dict.fromkeys(supervisors))
    return past_prj, supervisors


# Returns a list of all the current projects
def get_current_projects():
    curr_prj=Project.query.filter(Project.ending_date >= datetime.date.today()).all()
    supervisors = []
    for prj in curr_prj:
        if prj.supervisor:
            supervisors.append(get_employee_by_id(prj.supervisor))
    supervisors = list(dict.fromkeys(supervisors))
    return curr_prj, supervisors


# Returns a list of all the users
def get_users():
    users=User.query.all()
    users.sort(key=lambda x: x.name)
    return users


def get_user_by_id(user_id):
    return User.query.filter(User.id==user_id).first()


def get_user_by_email(email):
    return User.query.filter(User.email==email).first()


# Returns a list of all the skills
def get_skills():
    skills=Skill.query.all()
    skills.sort(key=lambda x: x.name)
    return skills


def get_skill_by_id(skill_id):
    return Skill.query.filter(Skill.id==skill_id).first()


# Returns a list of all the softskills
def get_soft_skills():
    ss=Skill.query.filter(Skill.type=="soft" or Skill.type=="Soft").all()
    ss.sort(key=lambda x: x.name)
    return ss


# Returns a list of all the hardskills
def get_hard_skills():
    hs=Skill.query.filter(Skill.type=="hard" or Skill.type=="Hard").all()
    hs.sort(key=lambda x: x.name)
    return hs


# Returns a list of all the roles in the company
def get_roles():
    roles=Role.query.all()
    roles.sort(key=lambda x: x.name)
    return roles


# Returns a list of all the possible roles in a project
def get_roles_in_projects():
    roles=Role_in_project.query.all()
    roles.sort(key=lambda x: x.name)
    return roles


# Returns a list of all the trainings
def get_trainings():
    trainings=Training.query.all()
    trainings.sort(key=lambda x: x.name)
    return trainings


# Returns a list of all the employees involved in a given project (identified by the id passed)
def get_employees_in_project(prj_id):
    project=Project.query.filter(Project.id==prj_id).first()
    employees=project.employee
    return employees


# Returns a list of all the employees involved in a given training (identified by the id passed)
def get_employees_in_training(train_id):
    training = Training.query.filter(Training.id == train_id).first()
    employees = training.employee
    return employees


# Returns a list of all the projects in which is involved a given employee (identified by the id passed)
def get_projects_of_employee(emp_id):
    employee = Employee.query.filter(Employee.id == emp_id).first()
    projects = employee.project
    return projects


# Returns a list of all the trainings in which is involved a given employee (identified by the id passed)
def get_trainings_of_employee(emp_id):
    employee = Employee.query.filter(Employee.id == emp_id).first()
    trainings = employee.training
    return trainings


# Returns a list of all the skills of a given employee (identified by the id passed)
def get_skills_of_employee(emp_id):
    employee = Employee.query.filter(Employee.id == emp_id).first()
    skills = employee.skill
    return skills


# Returns a list of all the softskills of a given employee (identified by the id passed)
def get_softskills_of_employee(emp_id):
    employee = Employee.query.filter(Employee.id == emp_id).first()
    skills = employee.skill
    soft_skills=[]
    for s in skills:
        if s.type=="soft" or s.type=="Soft":
            soft_skills.append(s)
    return soft_skills


# Returns a list of all the hardskills of a given employee (identified by the id passed)
def get_hardskills_of_employee(emp_id):
    employee = Employee.query.filter(Employee.id == emp_id).first()
    skills = employee.skill
    hard_skills=[]
    for s in skills:
        if s.type=="hard" or s.type=="Hard":
            hard_skills.append(s)
    return hard_skills


# Returns a list of all the employees having a given skill (identified by the id passed)
def get_employees_having_a_skill(skill_id):
    skill=Skill.query.filter(Skill.id == skill_id).first()
    employees=skill.employee
    return employees


def get_gradeofskill_by_emp_skill(emp_id, skill_id):
    link=Employee_Skill.query.filter(Employee_Skill.emp_id==emp_id, Employee_Skill.skill_id==skill_id).first()
    grade=0
    if link:
        grade=link.grade
    return grade


def get_skills_required_by_role_in_project(role_id):
    role = Role_in_project.query.filter(Role_in_project.id == role_id).first()
    skills=role.skill
    return skills


def get_grade_of_skill_required_by_role_in_project(role_id, skill_id):
    link=Role_in_project_Skill.query.filter(Role_in_project_Skill.role_id==role_id, Role_in_project_Skill.skill_id==skill_id).first()
    grade=0
    if link:
        grade=link.grade_required
    return grade


def get_pointsassigned_by_training_to_skill(training_id, skill_id):
    link=Training_Skill.query.filter(Training_Skill.train_id==training_id, Training_Skill.skill_id==skill_id).first()
    points=0
    if link:
        points=link.points
    return points


def get_evaluation_by_proj_emp_role(prj_id, emp_id, role_id):
    project = Project_Role.query.filter(Project_Role.prj_id==prj_id, Project_Role.emp_id==emp_id, Project_Role.role_id==role_id).first()
    evaluation=''
    if project:
        evaluation = project.evaluation
    return evaluation


# // SETTERS \\
def set_grade_of_skill_of_employee(grade, emp_id, skill_id):
    emp_skill=Employee_Skill.query.filter(Employee_Skill.emp_id==emp_id, Employee_Skill.skill_id==skill_id).first()
    if emp_skill:
        emp_skill.grade = grade
        db.session.commit()


def increase_grade_of_skill_of_employee(points_to_add, emp_id, skill_id):
    emp_skill = Employee_Skill.query.filter(Employee_Skill.emp_id == emp_id, Employee_Skill.skill_id == skill_id).first()
    if emp_skill:
        emp_skill.grade += points_to_add
        db.session.commit()


def set_evaluation_project_employee_role(evaluation, emp_id, prj_id, role_id):
    emp_prj = Project_Role.query.filter(Project_Role.emp_id == emp_id, Project_Role.prj_id == prj_id, Project_Role.role_id==role_id).first()
    if emp_prj:
        emp_prj.evaluation = evaluation
        db.session.commit()


def set_pointsassigned_by_training_to_skill(points, training_id, skill_id):
    training_skill = Training_Skill.query.filter(Training_Skill.train_id == training_id, Training_Skill.skill_id == skill_id).first()
    if training_skill:
        training_skill.points = points
        db.session.commit()


def set_grade_skill_required_by_role_in_project(grade_required, role_id, skill_id):
    prj_skill = Role_in_project_Skill.query.filter(Role_in_project_Skill.role_id == role_id, Role_in_project_Skill.skill_id == skill_id).first()
    if prj_skill:
        prj_skill.grade_required = grade_required
        db.session.commit()


def set_role_of_employee_in_project(prj_id, emp_id, role_id):
    prj_role = Project_Role.query.filter(Project_Role.prj_id == prj_id, Project_Role.role_id == role_id).first()
    if prj_role:
        prj_role.emp_id = emp_id
        db.session.commit()


def add_project_todb(name, description=None, start=None, end=None, supervisor=None):
    prj = Project(name=name, description=description,starting_date=start,ending_date=end,supervisor=supervisor)
    db.session.add(prj)
    db.session.commit()
    just_added = Project.query.order_by(Project.id.desc()).first()
    return just_added.id


def add_role_to_project(prj_id, role_id):
    prj_role = Project_Role(role_id=role_id, prj_id=prj_id)
    db.session.add(prj_role)
    db.session.commit()

def add_role_todb(name, description=None,):
    role=Role(name=name,description=description)
    db.session.add(role)
    db.session.commit()
    just_added=Role.query.order_by(Role.id.desc()).first()
    return just_added.id


def add_skill_to_role(role_id,skill_id):
    skill_role=Role_Skill(role_id=role_id,skill_id=skill_id)
    db.session.add(skill_role)
    db.session.commit()
