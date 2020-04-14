from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime
from random import random, randint
from database1 import db,Assessment,Employee,Education,Hardskill,Projects,Role,Roleinaproject,Softskill,Trainings,User,fill_table
from database1 import employee_projects,employee_hardskill,employee_assessment,employee_softskill,employee_trainings,hardskill_role,project_roleinaproject,softskill_role


app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database1.db'
db.init_app(app)

# CAN USE THESE CLASSES TO DO SOME TRIALS, BUT THEN USE THE CLASSES FROM THE database1.py
# class SoftSkill:
#     def  __init__(self, name, description):
#         self.name=name
#         self.description=description
#
#
# class HardSkill:
#     def  __init__(self, name, description):
#         self.name=name
#         self.description=description
#
#
# class Project:
#     def __init__(self, start, end, name, description):
#         self.start=start
#         self.end=end
#         self.name=name
#         self.description=description


# /// ROUTES \\\
# Here we define the routes used to get to the html pages and the functions performing the actions needed to retrieve
# the correct data from the db

# I will subdivide the routes based on their "macro page"

@app.before_first_request
def create_all():
    db.drop_all()
    db.create_all()
    db.fill_table()
    db.session.commit()


# //MAIN PAGES (first dropdown menu)\\
@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/about')
def about():
    return render_template('about.html')


# //SKILLS PAGES (second dropdown menu)\\
@app.route('/skills/<kind>')
def skill(kind):
    # skills_list=[]
    #
    # if kind == "soft":
    #     skills_list = [SoftSkill("ss1", "una skill"), SoftSkill("ss2","due skill")]
    # elif kind == "technical":
    #     skills_list = [HardSkill("hs1","una hard skill"), HardSkill("hs2", "due hard skill")]
    #
    # return render_template('skills.html', skills=skills_list, skill_type=kind)
    return render_template('skills.html', skill_type=kind)


# //EMPLOYEES PAGES (third button of navbar)\\
@app.route('/employees')
def employees():
    return render_template('employees.html')


@app.route('/employee/<int:id>')
def employee(id):
    # Here you have to add all the conditions and the instructions to retrieve the right employee's information from
    # the db
    # Also, you will have to pass the entire employee instance to the html page (see the skill(kind) function to see
    # how to do it
    # In the employee.html you will have to take the information you have to show from the variable passed from here,
    # see skills.html to have an example
    return render_template('employee.html')


# //JOBS PAGES\\
@app.route('/jobs')
def jobs():
    return render_template('jobs.html')

# //TRAININGS PAGES (trainings dropdown)\\
@app.route('/trainings/<period>')
def trainings(period):
    # This function has to do the exact same thing of the projects one (of course retrieving the list of trainings from
    # the db, not creating it randomly
    return render_template('trainings.html')


@app.route('/training/<int:id>')
def training(id):
    # Here you have to add all the conditions and the instructions to retrieve the right training's information from
    # the db
    # Also, you will have to pass the entire training instance to the html page (see the skill(kind) function to see
    # how to do it
    # In the training.html you will have to take the information you have to show from the variable passed from here,
    # see skills.html to have an example
    return render_template('training.html')


# //PROJECTS PAGES\\
@app.route('/projects/<period>')
def projects(period):
    # for i in range(20):
    #     projects_list.append(Project(datetime.date(2019,1,1), datetime.date(randint(2019,2021),i%12 + 1,i+1), "Project "+ str(i), "A project"))

    # if period=="past":
    #     projects_list = Projects.query.filter_by(ending_date == datetime.date.today())
    # elif period=="current":
    #     projects_list = Projects.query.filter_by(Projects.ending_date > datetime.date.today())
    # else:
    projects_list = Projects.query.all()


    projects_list.sort(key=lambda x: x.starting_date)
    return render_template('projects.html', projects=projects_list, period=period)


@app.route('/project/<int:id>')
def project(id):
    # Here you have to add all the conditions and the instructions to retrieve the right project's information from the
    # db
    # Also, you will have to pass the entire project instance to the html page (see the skill(kind) function to see how
    # to do it
    # In the project.html you will have to take the information you have to show from the variable passed from here,
    # see skills.html to have an example
    return render_template('project.html')


# //LOGIN AND USER MANAGEMENT\\
@app.route('/login')
def login():
    # Here we'll have to manage the entire login procedure
    return render_template('login.html')

# Should think about adding a user page and also the functionality to add more users with different permissionss


if __name__ == '__main__':
    app.run(debug=True)
