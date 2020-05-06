from flask import Flask, request, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import datetime
from flask_wtf import FlaskForm

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
    return render_template('index.html')


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/about')
def about():
    return render_template('about.html')


# //SKILLS PAGES (second dropdown menu)\\

@app.route('/skills', methods=['GET', 'POST'])
@app.route('/skills/<kind>')
def skills(kind="soft"):
    if request.method == 'POST':
        name = str(request.form.get('skill_name'))
        kind = request.form.get('skill_type')

        #TODO: rinominare tutte le variabili in "Soft" e "Hard"

        desc = str(request.form.get('desc'))
        add_skill(name, kind, desc)


    skills_list=[]
    if kind == "soft":
        skills_list = get_soft_skills()
    elif kind == "technical":
        skills_list = get_hard_skills()
    return render_template('skills.html', skills=skills_list, skill_type=kind)


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
@app.route('/jobs',methods=['POST'])
@app.route('/jobs')
def jobs():
    if request.method == 'POST':
        # create a new job

        # get values from the inputs of the form in job.html
        job_name = str(request.form.get('role'))
        job_description = str(request.form.get('Jdescription'))
        job_softskill_id_list = request.form.getlist('skselection')
        job_hardskill_id_list = request.form.getlist('hkselection')
        job_skill_id_list=job_hardskill_id_list+job_softskill_id_list
        id_job = add_role_todb(job_name, job_description)
       # the job is connected to the skills required for it
        for skill_id in job_skill_id_list :
           add_skill_to_role(id_job, skill_id)
        # redirecting to the page of the job created
        # Skills
        number = request.form["number"]
        number = int(number)
        dic = []
        for x in range(number):
           skill_index = "skill" + str(x)
           skill = request.form.get(skill_index)
           if skill != None:
               skill_id = request.form[skill_index]  # Parametro form (ex. skill0=adaptability)
               score_index = "score" + str(x)
               score = request.form[score_index]
               dic.append((skill_id, score))





        # Add the skills of the employee into db
        for y in dic:
           add_skill_to_role(id_job, y[0], y[1])

        return redirect(url_for('EmployeeJob', id=id_job))

    soft_skill=get_soft_skills()
    hard_skill=get_hard_skills()
    job_skill=soft_skill+hard_skill
    roles=get_roles()
    employee_list=[]

    for role in roles:
        employee_list.append(get_employee_by_role(role.id))

    open=[]
    closed=[]
    for job in roles:
        if job.employee:
            closed.append(job)
        else:
             open.append(job)



    return render_template('jobs.html',softskill=soft_skill,hardskill=hard_skill,role=roles,open=open,closed=closed,employee=employee_list,job_skill=job_skill)

@app.route('/EmployeeJob/<int:id>',methods=['GET','POST'])
@app.route('/EmployeeJob/<int:id>')
def EmployeeJob(id):
    if request.method=='POST':
        action=str(request.form.get('actionToPerform'))
        if action=="editJob":
            job_description = str(request.form.get('Jdescription'))
            update_role(id,job_description)
            number = request.form["number"]
            number = int(number)
            dic = []
            job_skills = get_skills_required_by_role(id)
            for x in range(number):
                skill_index = "skill" + str(x)
                skill = request.form.get(skill_index)
                if skill != None:
                    skill_id = request.form[skill_index]  # Parametro form (ex. skill0=adaptability)
                    score_index = "score" + str(x)
                    score = request.form[score_index]
                    dic.append((skill_id, score))

            delete_all_grade_of_skill_of_job(id)


            # Delete all duplicate from the list dic
            seen = set()
            dic = [(a, b) for a, b in dic if not (a in seen or seen.add(a))]
            # Add the skills of the employee into db
            for skill in dic:
                add_skill_to_role(id, skill[0], skill[1])  # insert all new skills
            # Once saved employee information in db return the employee.html page
            return redirect(url_for('EmployeeJob', id=id, message="Save"))  # Message neet to show popup save

        elif action =="assignEmployees":
            empl_id = request.form.get('AssignEmployee')
            update_employee(id,empl_id)
            return redirect(url_for('jobs',message="Save"))

    role=get_role_by_id(id)
    all_skills=get_skills()
    skill=get_skills_required_by_role(id)
    skill_id=get_skill_id_of_a_role(id)
    var1,var2,var3=get_suitable_emp_for_job(id)
    empl=True
    if role.employee:
        empl=False

    return render_template('EmployeeJob.html', role=role,skill=skill,grade =skill_id,var1=var1,var2=var2,var3=var3,empl=empl,all_skill=all_skills)


# //TRAININGS PAGES (trainings dropdown)\\
@app.route('/trainings/<period>')
def trainings(period="all"):
     skills=get_skills()
     if period == "past":
         trainings_list = get_past_trainings()
     elif period == "current":
         trainings_list = get_current_trainings()
     else:
         trainings_list= get_trainings()

     trainings_list.sort(key=lambda x: x.starting_Date, reverse=True)
     range=[1,2,3,4,5,6,7,8,9,10]

     return render_template('trainings.html',skills=skills,trainings_list=trainings_list,range=range)


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
@app.route('/projects', methods=['POST'])
@app.route('/projects/<period>')
def projects(period="all"):
    if request.method == 'POST':
        # create a new project

        # get values from the inputs of the form in projects.html
        prj_name = str(request.form.get('prjName'))
        prj_description = str(request.form.get('prjDescription'))
        # starting date is a required value, so there's no check on its content (it is needed to sort the list of projects when retrieved from the db
        prj_start_date = request.form.get('prjStartingDate')
        prj_start_date = datetime.datetime.strptime(str(prj_start_date), '%Y-%m-%d').date()
        # if there's a value inside the prjEndingDate it is converted into datetime, otherwise is set to none
        prj_end_date = request.form.get('prjEndingDate')
        if prj_end_date:
            prj_end_date = datetime.datetime.strptime(str(prj_end_date), '%Y-%m-%d').date()
        else:
            prj_end_date = None
        prj_supervisor = int(request.form.get('prjSupervisor'))
        # list of the ids of the roles required for the project created
        prj_roles_id_list = request.form.getlist('prjRoles')
        id_prj = add_project_todb(prj_name,prj_description,prj_start_date,prj_end_date,prj_supervisor)
        # the project is connected to the roles required for it
        for role_id in prj_roles_id_list:
            add_role_to_project(id_prj,role_id)
        # redirecting to the page of the project created
        return redirect(url_for('project', id=id_prj))

    # if the request is not a post (so it doesn't require any insert of data in the db), redirect to the list of projects requested
    if period == "past":
        projects_list, supervisors = get_past_projects()
    elif period == "current":
        projects_list, supervisors = get_current_projects()
    else:
        projects_list, supervisors = get_projects_and_supervisors()

    projects_list.sort(key=lambda x: x.starting_date, reverse=True)
    possible_roles=get_roles_in_projects()
    possible_roles.sort(key=lambda x: x.id)
    emp = get_employees()

    return render_template('projects.html', projects=projects_list, period=period, supervisors=supervisors, roles=possible_roles, employees=emp)


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


