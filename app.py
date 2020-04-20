from flask import Flask, request, session, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime

from sqlalchemy import true, false

from database import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_per_prove.db'
bcrypt=Bcrypt(app)
db.init_app(app)


# /// ROUTES \\\
# Here we define the routes used to get to the html pages and the functions performing the actions needed to retrieve
# the correct data from the db

# I will subdivide the routes based on their "macro page"

# //MAIN PAGES (first dropdown menu)\\
@app.route('/')
@app.route('/home')
def index():
    matchingAlgorithm(1)
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
    if period == "past":
        projects_list = get_past_projects()
    elif period == "current":
        projects_list = get_current_projects()
    else:
        projects_list = get_projects()

    projects_list.sort(key=lambda x: x.starting_date)
    return render_template('projects.html', projects=projects_list, period=period)


@app.route('/project/<int:id>')
def project(id):
    prj = get_project_by_id(id)
    return render_template('project.html', project=prj)


# //LOGIN AND USER MANAGEMENT\\
@app.route('/login')
def login():
    # Here we'll have to manage the entire login procedure
    return render_template('login.html')

# Should think about adding a user page and also the functionality to add more users with different permissionss

if __name__ == '__main__':
    app.run(debug=True)


skilled_employees = []
unskilled_employees = []
noskill_employees = []
def matchingAlgorithm(role):
    skill_ids = get_skills_required_by_role_in_project(role)
    employee_list = get_employees()
    for employeeeees in employee_list:
        y = employeeeees.id
        employee_skills = get_employee_skill_by_id(y)
        x = true
        for skills in skill_ids:
            z = false
            for emp_skill in employee_skills:
                if emp_skill == skills:
                    z = true
            if z == false:
                x = false
        if x == true:
            tot = 0
            check = true
            for skills in skill_ids:
                eg = get_gradeofskill_by_emp_skill(y, skills.id)
                rg = get_grade_of_skill_required_by_role_in_project(y, skills.id)
                tot += eg
                if eg<rg:
                    check = false
            if check == true:
                skilled_employees.append(tuple([employeeeees, tot]))
            else:
                unskilled_employees.append(tuple([employeeeees, tot]))
        else:
            tot = 0
            for skills in skill_ids:
                tot += get_gradeofskill_by_emp_skill(y, skills.id)
            noskill_employees.append(tuple([employeeeees, tot]))
    skilled_employees.sort(key=lambda tup: -tup[1])
    unskilled_employees.sort(key=lambda tup: -tup[1])
    noskill_employees.sort(key=lambda tup: -tup[1])
    length = len(skilled_employees)
    length2 = len(skilled_employees) + len(unskilled_employees)
    if length >= 5:
        print("First 5 employees who have every  grade of skill required:")
        print("\n", skilled_employees)
    elif length2 < 5 and length > 0:
        print(length, "employees have every grade of skill required:")
        print("\n", skilled_employees)
        print("Other options:")
        if len(unskilled_employees) > 0:
            print("\nEmployees who do not have every grade of skill required:")
            print("\n", unskilled_employees)
        print("Employees who do not have every skill required:")
        n = 0
        while length2 < 5 and noskill_employees[n][1] > 0:
            print("\n", noskill_employees[n])
            n = n+1
            length2 = length2 + 1