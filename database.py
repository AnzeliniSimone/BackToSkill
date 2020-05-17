from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_, or_, and_
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
    project = db.Column(db.Integer, db.ForeignKey('project.id'))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.id).encode("utf-8").decode("utf-8")
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')


class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    employee = db.relationship("Employee")
    skill = db.relationship("Skill", secondary="role_skill")

    def get_employee_assigned(self):
        return Employee.query.filter(Employee.role == self.id).all()


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
    state_in_company = db.Column(db.String)
    education_level = db.Column(db.String)
    language_certificate = db.Column(db.String)

    def get_job(self):
        return get_role_by_id(self.role).name

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

    def get_skills_required(self):
        skills = get_skills_required_by_role_in_project(self.id)
        grades=[]
        for s in skills:
            grades.append(get_grade_of_skill_required_by_role_in_project(self.id, s.id))
        return skills,grades


class Training(db.Model):
    __tablename__ = 'training'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    starting_Date = db.Column(db.Date)
    ending_Date = db.Column(db.Date)
    hours = db.Column(db.Integer)
    skill = db.relationship("Skill", secondary="training_skill")
    employee = db.relationship("Employee", secondary="employee_training")
    closed = db.Column(db.Boolean)

    def get_skill_improvements_list(self):
        skills=[]
        for s in self.skill:
            skills.append(s.name)
        return skills


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

def get_gradeofskill_of_a_role(role_id,skill_id):
    role_skill= Role_Skill.query.filter(Role_Skill.role_id==role_id,Role_Skill.skill_id==skill_id).first()
    return role_skill.grade_required



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
    ss=Skill.query.filter(or_(Skill.type=="soft",Skill.type=="Soft")).all()
    ss.sort(key=lambda x: x.name)
    return ss

# CHANGED!!!!
# Returns a list of all the hardskills
def get_hard_skills():
    hs=Skill.query.filter(or_(Skill.type=="hard", Skill.type=="Hard")).all()
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
    roles.sort(key=lambda x: x.id)
    return roles


# Returns a list of all the trainings
def get_trainings():
    trainings=Training.query.all()
    trainings.sort(key=lambda x: x.name)
    return trainings

def get_past_trainings():
    past_tra = Training.query.filter(Training.ending_Date < datetime.date.today()).all()
    return past_tra
def get_current_trainings():
    current_tra= Training.query.filter(Training.ending_Date>=datetime.date.today()).all()
    return current_tra


# Returns a list of all the employees involved in a given project (identified by the id passed)
def get_employees_in_project(prj_id):
    links=Project_Role.query.filter(Project_Role.prj_id == prj_id).all()
    emp_ids=[]
    for l in links:
        if l.emp_id:
            emp_ids.append(l.emp_id)
    employees = Employee.query.filter(Employee.id.in_(emp_ids)).all()
    return employees


def get_roles_in_projects_by_id(role_id):
    return Role_in_project.query.filter(Role_in_project.id == role_id).first()


def get_employees_in_project_with_roles(prj_id):
    emps = get_employees_in_project(prj_id)
    tortn = []
    for emp in emps:
        link = Project_Role.query.filter(Project_Role.prj_id==prj_id, Project_Role.emp_id==emp.id).first()
        role = get_roles_in_projects_by_id(link.role_id)
        tortn.append(tuple([emp,role]))
    return tortn


def get_not_used_roles_in_proj(prj_id):
    roles_used = get_project_by_id(prj_id).role_in_project
    ids=[]
    for r in roles_used:
        ids.append(r.id)
    not_used_roles = Role_in_project.query.filter(Role_in_project.id.notin_(ids)).all()
    return not_used_roles


def get_free_roles_in_project(prj_id):
    links=Project_Role.query.filter(Project_Role.prj_id==prj_id, Project_Role.emp_id==None).all()
    roles=[]
    for l in links:
        roles.append(l.role_in_project)
    return roles


# Returns a list of all the employees involved in a given training (identified by the id passed)
def get_employees_in_training(train_id):
    links = Employee_Training.query.filter(Employee_Training.train_id == train_id).all()
    emp_ids = []
    for l in links:
        if l.emp_id:
            emp_ids.append(l.emp_id)
    employees = Employee.query.filter(Employee.id.in_(emp_ids)).all()
    return employees

# Returns a list of all the projects in which is involved a given employee (identified by the id passed)
def get_projects_of_employee(emp_id):
    employee = Employee.query.filter(Employee.id == emp_id).first()
    link = employee.project_role
    projects=[]
    for prj in link:
        projects.append(get_project_by_id(prj.prj_id))
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
    evaluation=None
    if project:
        evaluation = project.evaluation
    return evaluation


def get_available_employees_in_period(start, end):
    # gets the list of the projects active in the period beginning with date 'start' and ending with date 'end'
    projects_in_period = Project.query.filter(or_(and_(Project.starting_date < start, start < Project.ending_date), and_(Project.starting_date < end, end < Project.ending_date), and_((start <= Project.starting_date), (end >= Project.ending_date)))).all()
    # takes out the ids of the projects
    prj_ids=[]
    for prj in projects_in_period:
        prj_ids.append(prj.id)
    # and gets the instances of the association class between project and role, which contains info about the employees working on those projects
    links = Project_Role.query.filter(Project_Role.prj_id.in_(prj_ids)).all()
    # cycling on the list got, it takes the ids of the employees working on one of the projects held in the period selected
    # they will be considered as nonavailable, as they are working on something else in the time span considered
    nonavailable_emp_ids = []
    for link in links:
        if link.emp_id:
            nonavailable_emp_ids.append(link.emp_id)
    # gets the employees which are not in the list of nonavailables and returns the list of them
    availables = Employee.query.filter(Employee.id.notin_(nonavailable_emp_ids)).all()
    return availables


def get_suitable_emp_for_role(role_id, employee_list):
    return matching_algorithm(role_id, employee_list, False)


def get_suitable_emp_for_job(role_id):
    return matching_algorithm(role_id, get_employees(), True)


def get_employees_with_evaluation(prj_id):
    links = Project_Role.query.filter(Project_Role.prj_id==prj_id).all()
    emp_eva=[]
    for l in links:
        tup = []
        tup.append(get_employee_by_id(l.emp_id))
        tup.append(str(get_evaluation_by_proj_emp_role(prj_id,l.emp_id,l.role_in_project.id)))
        emp_eva.append(tuple(tup))
    return emp_eva


# TODO: RISCRIVERE
def get_number_of_skills():
    descending = Skill.query.order_by(Skill.id.desc())
    return descending.first().id


def get_suitable_emp_for_job(role_id):
    return matching_algorithm(role_id, get_employees(), True)
# // SETTERS \\

def add_skill(name, skill_type, desc):
    skill = Skill(name=name, description=desc, type=skill_type)
    db.session.add(skill)
    db.session.commit()
    return skill


def edit_skill(id, type, desc):
    skill = Skill.query.filter(Skill.id == id).first()
    skill.type = type
    skill.description = desc
    db.session.commit()
    return skill


def delete_skill(skill):
    links_employee = Employee_Skill.query.filter(Employee_Skill.skill_id==skill).delete()
    links_job = Role_Skill.query.filter(Role_Skill.skill_id==skill).delete()
    links_roles = Role_in_project_Skill.query.filter(Role_in_project_Skill.skill_id==skill).delete()
    links_trainings = Training_Skill.query.filter(Training_Skill.skill_id==skill).delete()
    skill = Skill.query.filter(Skill.id==skill).delete()
    db.session.commit()
    return "Skill deleted"


def set_grade_of_skill_of_employee(grade, emp_id, skill_id):
    increase_grade_of_skill_of_employee(grade, emp_id, skill_id)


def increase_grade_of_skill_of_employee(points_to_add, emp_id, skill_id):
    emp_skill = Employee_Skill.query.filter(Employee_Skill.emp_id == emp_id, Employee_Skill.skill_id == skill_id).first()
    if emp_skill:
        emp_skill.grade += points_to_add
        if emp_skill.grade > 10:
            emp_skill.grade = 10
    else:
        emp_skill = Employee_Skill(emp_id=emp_id, skill_id=skill_id, grade=points_to_add)
        db.session.add(emp_skill)
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
    return prj_role


def remove_role_from_project(prj_id, role_id):
    prj_role = Project_Role.query.filter(Project_Role.role_id==role_id, Project_Role.prj_id==prj_id).delete(synchronize_session='fetch')


def add_role_todb(name, description):
    role=Role(name=name,description=description)
    db.session.add(role)
    db.session.commit()
    return "done"


def remove_employee_from_project(prj_id, role_id):
    prj_role = Project_Role.query.filter(Project_Role.role_id == role_id, Project_Role.prj_id == prj_id).first()
    prj_role.emp_id = None
    db.session.commit()
    return prj_role


def edit_project_basic_info(prj_id, name, description, start, end, supervisor):
    project = get_project_by_id(prj_id)
    project.name = name
    project.description = description
    project.starting_date = start
    project.ending_date = end
    project.supervisor = supervisor
    db.session.commit()
    return project


def add_employee_to_project(prj_id, role_id, emp_id):
    prj_role = Project_Role.query.filter(Project_Role.prj_id==prj_id, Project_Role.role_id==role_id).first()
    prj_role.emp_id = emp_id
    db.session.commit()
    return prj_role

def add_skill_to_training(train_id,skill_id,grade):
    skill_train=Training_Skill(train_id=train_id,skill_id=skill_id,points=grade)
    db.session.add(skill_train)
    db.session.commit()

def add_training_to_db(name,start,end,hours):
    training=Training(name=name,starting_Date=start,ending_Date=end,hours=hours)
    db.session.add(training)
    db.session.commit()
    just_added=Training.query.filter(Training.name==name).first()
    return just_added.id

def get_trainings_by_id(id):
    tra=Training.query.filter(Training.id==id).first()
    return tra

def get_skill_in_training_with_points(id):
    link=Training_Skill.query.filter(Training_Skill.train_id==id).all()
    skill_ids=[]
    for l in link:
        if l.skill_id:
            skill_ids.append(l.skill_id)
    skills = Skill.query.filter(Skill.id.in_(skill_ids)).all()
    array=[]
    for skill in skills:
        points = get_pointsassigned_by_training_to_skill(id,skill.id)
        array.append(tuple([skill,points]))
    return array

def edit_training_info(id,name,start,end,hours):
    training=get_trainings_by_id(id)
    training.name=name
    training.starting_Date=start
    training.ending_Date=end
    training.hours=hours
    db.session.commit()
    return training

def add_employee_to_training(id,emp_id):
    link=Employee_Training.query.filter(Employee_Training.train_id==id).all()
    new_link =Employee_Training(train_id=id,emp_id=emp_id)
    db.session.add(new_link)
    db.session.commit()


def add_evaluation_to_employee_in_project(prj_id, emp_id, ev):
    prj_role = Project_Role.query.filter(Project_Role.prj_id==prj_id, Project_Role.emp_id==emp_id).first()
    if prj_role:
        prj_role.evaluation = ev
    db.session.commit()
    return prj_role


def delete_training(tra_id):
    links =Training_Skill.query.filter(Training_Skill.train_id==tra_id).delete(synchronize_session='fetch')
    prj = Training.query.filter(Training.id == tra_id).delete(synchronize_session='fetch')
    emp=Employee_Training.query.filter(Employee_Training.train_id==tra_id).delete(synchronize_session='fetch')
    db.session.commit()
    return "Training deleted"

def delete_skill_from_training(tra_id,skill):
    tra_skill= Training_Skill.query.filter(Training_Skill.train_id == tra_id, Training_Skill.skill_id == skill).delete(synchronize_session='fetch')
    db.session.commit()
    return "done"


def delete_employee_from_training(tra_id,emp):
    tra_emp= Employee_Training.query.filter(Employee_Training.train_id == tra_id, Employee_Training.emp_id == emp).delete(synchronize_session='fetch')
    db.session.commit()
    return "done"

def delete_project(prj_id):
    links = Project_Role.query.filter(Project_Role.prj_id==prj_id).delete(synchronize_session='fetch')
    prj = Project.query.filter(Project.id == prj_id).delete(synchronize_session='fetch')
    db.session.commit()
    return "Project deleted"


def create_role_in_project(name, description):
    role = Role_in_project(name=name, description=description)
    db.session.add(role)
    db.session.commit()
    return role


# returns the most suited employees (among a list passed) for a certain job (job_or_role = True) or a role in a project
# (job_or_role = False)
def matching_algorithm(role_id, employee_list, job_or_role):
    skilled_employees = []
    unskilled_employees = []
    noskill_employees = []

    skills_required = []
    if job_or_role:
        skills_required = get_skills_required_by_role(role_id)
    else:
        skills_required = get_skills_required_by_role_in_project(role_id)

    for emp in employee_list:
        employee_skills = get_employee_skill_by_id(emp.id)
        # if has_all_skills = true then the employee possesses all the skills requested
        has_all_skills = True
        for skill in skills_required:
            has_single_skill = False

            # if the skill considered at the moment is in the list of the employee's skills
            has_single_skill = skill in employee_skills
            # for emp_skill in employee_skills:
            #     if emp_skill == s:
            #         has_single_skill = True

            if has_single_skill == False:
                has_all_skills = False

        # if the employee has every skill requested
        if has_all_skills:
            tot = 0
            check = True
            for s in skills_required:
                eg = get_gradeofskill_by_emp_skill(emp.id, s.id)
                rg = get_grade_of_skill_required_by_role_in_project(role_id, s.id)
                tot += eg
                if eg<rg:
                    check = False
            # after the loop, check will be false if one (or more) of the skills possessed by the employee have a lower
            # grade than the one requested
            if check:
                # if all the skills have the right grade or higher then the employee is considered "skilled"
                skilled_employees.append(tuple([emp, tot]))
            else:
                # otherwise he is considered unskilled (but still he has all the skills required
                unskilled_employees.append(tuple([emp, tot]))
        else:
            # if the employee doesn't have all the skills required
            tot = 0
            for s in skills_required:
                tot += get_gradeofskill_by_emp_skill(emp.id, s.id)
            # appends every other employee with the total score of his skills, but only if they have at least one of the
            # skills required
            if(tot>0):
                noskill_employees.append(tuple([emp, tot]))

    #sorts the three lists by the scores of the employees (in descending order, from the one with highest value to the
    # lowest
    skilled_employees.sort(key=lambda tup: -tup[1])
    unskilled_employees.sort(key=lambda tup: -tup[1])
    noskill_employees.sort(key=lambda tup: -tup[1])

    MAX_EMPLOYEES = 15
    if len(skilled_employees) >= MAX_EMPLOYEES:
        skilled_employees=skilled_employees[:MAX_EMPLOYEES]
    if len(skilled_employees) < MAX_EMPLOYEES:
        n_unskilled = MAX_EMPLOYEES-len(skilled_employees)
        unskilled_employees=unskilled_employees[:n_unskilled]
    else:
        unskilled_employees=[]
    if len(skilled_employees)+len(unskilled_employees)<MAX_EMPLOYEES:
        n_noskill = MAX_EMPLOYEES - (len(skilled_employees)+len(unskilled_employees))
        noskill_employees=noskill_employees[:n_noskill]
    else:
        noskill_employees=[]

    # Returns the three lists, with a total max number of employees of MAX_EMPLOYEES. Note that some of the lists may
    # be empty, depending on the number of skilled and unskilled employees found
    return skilled_employees, unskilled_employees, noskill_employees


def add_role_todb(name, description=None):
    role=Role(name=name,description=description)
    db.session.add(role)
    db.session.commit()
    just_added=Role.query.order_by(Role.id.desc()).first()
    return just_added.id

def modify_role_todb(id,name, description=None,):
    role=Role(id=id,name=name,description=description)
    db.session.add(role)
    db.session.commit()
    just_added=Role.query.order_by(Role.id.desc()).first()
    return just_added.id


def add_skill_to_role(role_id,skill_id):
    skill_role=Role_Skill(role_id=role_id, skill_id=skill_id)
    db.session.add(skill_role)
    db.session.commit()
    return skill_role


def add_skill_to_role_in_project(role_id, skill_id, grade_required):
    skill_role=Role_in_project_Skill(role_id=role_id, skill_id=skill_id, grade_required=grade_required)
    db.session.add(skill_role)
    db.session.commit()
    return skill_role


def delete_role_in_project(role_id):
    links = Project_Role.query.filter(Project_Role.role_id==role_id).delete(synchronize_session='fetch')
    links = Role_in_project_Skill.query.filter(Role_in_project_Skill.role_id==role_id).delete(synchronize_session='fetch')
    links = Role_in_project.query.filter(Role_in_project.id==role_id).delete(synchronize_session='fetch')
    db.session.commit()
    return "Deleted"


def edit_role_description(role_id, desc):
    role = get_roles_in_projects_by_id(role_id)
    role.description=desc
    db.session.commit()
    return role


def remove_skills_required_from_role_in_project(role_id):
    deleted = Role_in_project_Skill.query.filter(Role_in_project_Skill.role_id==role_id).delete(synchronize_session='fetch')
    db.session.commit()
    deleted = get_roles_in_projects_by_id(role_id)
    return deleted


def add_skill_to_role(role_id,skill_id,grade):
    skill_role=Role_Skill(role_id=role_id,skill_id=skill_id,grade_required=grade)
    db.session.add(skill_role)
    db.session.commit()


def update_role(role_id,desc):
   job=Role.query.filter(Role.id==role_id).first()
   job.description=desc
   db.session.commit()
   return job


#Aggiorna gli attributi di un employee and db
def update_employee(new_employee):
    old_employee = get_employee_by_id(new_employee.id)
    old_employee.name = new_employee.name
    old_employee.surname = new_employee.surname
    old_employee.date_of_birth = new_employee.date_of_birth
    old_employee.email = new_employee.email
    old_employee.telephone = new_employee.telephone
    old_employee.living_place = new_employee.living_place
    old_employee.driving_licence = new_employee.driving_licence
    old_employee.date_of_assumption = new_employee.date_of_assumption
    old_employee.state_in_company = new_employee.state_in_company
    old_employee.role = new_employee.role
    old_employee.education_level = new_employee.education_level
    old_employee.language_certificate = new_employee.language_certificate
    old_employee.photo=new_employee.photo
    db.session.commit()


def update_employee_job(job_id, emp_id):
    emp = get_employee_by_id(emp_id)
    emp.role = job_id
    db.session.commit()
    return emp


def delete_all_grade_of_skill_of_job(job_id):
    Role_Skill.query.filter(Role_Skill.role_id == job_id).delete(synchronize_session='fetch')
    db.session.commit()


def create_user(name, surname, email, password, project, admin=False):
    user = User(name=name, surname=surname, email=email, password=password, admin=admin, project=project)
    db.session.add(user)
    db.session.commit()
    return user


def delete_user(user_id):
    deleted = User.query.filter(User.id==user_id).delete(synchronize_session='fetch')
    db.session.commit()
    return "User deleted"


def make_user_admin(user_id):
    user = get_user_by_id(user_id)
    user.admin = True
    db.session.commit()
    return user


def edit_user_password(user_id, new_password):
    user = get_user_by_id(user_id)
    user.password = new_password
    db.session.commit()
    return user


def edit_user_email(user_id, new_email):
    user = get_user_by_id(user_id)
    user.email = new_email
    db.session.commit()
    return user


def get_admins(admin):
    admins=User.query.filter(User.admin==admin).all()
    return admins


###### EMPLOYEE
#Aggiunge employee and db
def set_employee(employee):
    db.session.add(employee)
    db.session.commit()


#Cancella employee
def delete_employee(id):
    Employee_Skill.query.filter_by(emp_id=id).delete()
    Employee_Training.query.filter_by(emp_id=id).delete()
    Employee.query.filter_by(id=id).delete()
    db.session.commit()


#AGGIUNTA
def delete_all_grade_of_skill_of_employee(emp_id):
    Employee_Skill.query.filter(Employee_Skill.emp_id == emp_id).delete()
    db.session.commit()


#AGGIUNTA
def delete_grade_of_skill_of_employee(emp_id, skill_id):
    Employee_Skill.query.filter(Employee_Skill.emp_id == emp_id,Employee_Skill.skill_id == skill_id).delete()
    db.session.commit()


#AGGIUNTA
def get_grade_of_skill_of_employee(emp_id, skill_id):
    emp_skill = Employee_Skill.query.filter(Employee_Skill.emp_id == emp_id,Employee_Skill.skill_id == skill_id).first()
    return emp_skill


def delete_role(role_id):
    links = Role_Skill.query.filter(Role_Skill.role_id == role_id).delete()
    emps = Employee.query.filter(Employee.role==role_id).all()
    for e in emps:
        e.role = None
    role = Role.query.filter(Role.id == role_id).delete()
    db.session.commit()
    return "deleted"


def remove_employee_from_job(job_id, emp_id):
    emp = get_employee_by_id(emp_id)
    if emp.role == job_id:
        emp.role = None
    db.session.commit()
    return emp


def alter_db():
    result = db.session.execute("ALTER TABLE training ADD closed Boolean ")
    result = db.session.execute("ALTER TABLE user ADD project integer ")
    result = db.session.execute("ALTER TABLE user ADD FOREIGN KEY (project) REFERENCES project(id);")
    db.session.commit()
    return "done"


def close_training(trn_id):
    employees = Employee_Training.query.filter(Employee_Training.train_id==trn_id).all()
    skills = Training_Skill.query.filter(Training_Skill.train_id==trn_id).all()
    for e in employees:
        for s in skills:
            increase_grade_of_skill_of_employee(s.points, e.emp_id, s.skill_id)
    training = get_trainings_by_id(trn_id)
    training.closed = True
    db.session.commit()
    return "done"
