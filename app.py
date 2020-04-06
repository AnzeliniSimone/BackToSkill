from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime
from random import random, randint

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hakunamatata'


# db=SQLAlchemy(app)
# login_manager=LoginManager()
# login_manager.init_app(app)

class SoftSkill:
    def  __init__(self, name, description):
        self.name=name
        self.description=description

class HardSkill:
    def  __init__(self, name, description):
        self.name=name
        self.description=description

class Project:
    def __init__(self, start, end, name, description):
        self.start=start
        self.end=end
        self.name=name
        self.description=description

@app.route('/')
@app.route('/welcome')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

# needed?
@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/layout')
def layout():
    return render_template('layout.html')


@app.route('/skills/<kind>')
def skill(kind):
    skills_list=[]

    if kind == "soft":
        skills_list = [SoftSkill("ss1", "una skill"), SoftSkill("ss2","due skill")]
    elif kind == "technical":
        skills_list = [HardSkill("hs1","una hard skill"), HardSkill("hs2", "due hard skill")]

    return render_template('skills.html', skills=skills_list, skill_type=kind)


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/employees')
def employees():
    return render_template('employees.html')


@app.route('/jobs')
def jobs():
    return render_template('jobs.html')


@app.route('/trainings')
def trainings():
    return render_template('trainings.html')


@app.route('/projects/<period>')
def projects(period):
    projects_list=[]
    for i in range(20):
        projects_list.append(Project(datetime.date(2019,1,1), datetime.date(randint(2019,2021),i%12 + 1,i+1), "Project "+ str(i), "A project"))

    to_pass = []
    for project in projects_list:
        if period=="past" and project.end<datetime.date.today():
            to_pass.append(project)
        elif period=="current" and project.end>datetime.date.today():
            to_pass.append(project)
        elif period=="all":
            to_pass=projects_list

    to_pass.sort(key=lambda x: x.start)
    return render_template('projects.html', projects=to_pass, period=period)


if __name__ == '__main__':
    app.run(debug=True)
