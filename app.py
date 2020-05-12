from flask import Flask, request, session, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import not_, or_, and_
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import datetime
from datetime import datetime as dt
from flask_wtf import FlaskForm

from sqlalchemy import true, false

from database import *
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SECRET_KEY'] = '1234'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database_per_prove.db'
bcrypt=Bcrypt(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

# /// ROUTES \\\
# Here we define the routes used to get to the html pages and the functions performing the actions needed to retrieve
# the correct data from the db

# I will subdivide the routes based on their "macro page"

# //MAIN PAGES (first dropdown menu)\\
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/guide')
def guide():
    return render_template('guide.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/faq')
def faq():
    return render_template('FAQ.html')\


@app.route('/team')
def team():
    return render_template('team.html')


# //SKILLS PAGES (second dropdown menu)\\

@app.route("/skills", methods=['GET','POST'])
@app.route('/skills/<kind>')
@login_required
def skills(kind="soft", s=None):
    if request.method == 'POST':
        action = request.form.get("actionToPerform")
        kind="soft"
        if action == "addSkill":
            name = str(request.form.get('newSkillName'))
            kind = str(request.form.get('newSkillType'))
            desc = str(request.form.get('newSkillDescription'))
            new_skill = add_skill(name, kind, desc)
        elif action == "deleteSkill":
            skill_id = request.form.get('skillToDelete')
            kind = get_skill_by_id(skill_id).type.lower()
            deleted = delete_skill(skill_id)
        elif action == "editSkill":
            skill_id = request.form.get('skillToEdit')
            kind = request.form.get('editedSkillType')
            desc = request.form.get('editedSkillDescription')
            edited_skill = edit_skill(skill_id,kind,desc)
         #TODO: rinominare tutte le variabili in "Soft" e "Hard"
        return redirect("skills/"+kind)

    skills_list=[]
    if kind == "soft":
        skills_list = get_soft_skills()
    elif kind == "hard":
        skills_list = get_hard_skills()
    return render_template('skills.html', skills=skills_list, skill_type=kind)


# //EMPLOYEES PAGES (third button of navbar)\\
@app.route('/employees')
@login_required
def employees():
    return render_template('employees.html')


@app.route('/employee/<int:id>')
@login_required
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
@login_required
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

        return redirect(url_for('job', id=id_job))

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

@app.route('/job/<int:id>',methods=['GET','POST'])
@app.route('/job/<int:id>')
@login_required
def job(id):
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
            return redirect(url_for('job', id=id, message="Save"))  # Message neet to show popup save

        elif action =="assignEmployees":
            empl_id = request.form.get('AssignEmployee')
            update_employee(id,empl_id)
            return redirect(url_for('jobs',message="Save"))
    else:
        skill = get_skills_required_by_role(id)
        # get the grades of the skills of the employee in db
        dic = []
        for i in skill:
            grade = get_gradeofskill_of_a_role(id, i.id)
            dic.append((i.id,i.name, grade))
        role=get_role_by_id(id)
        all_skills=get_skills()
        skill_id=get_skill_id_of_a_role(id)
        var1,var2,var3=get_suitable_emp_for_job(id)
        empl=True
        if role.employee:
            empl=False

        return render_template('job.html', role=role, skill=skill, grade =skill_id, var1=var1, var2=var2, var3=var3, empl=empl, all_skill=all_skills, dic=dic)


# //TRAININGS PAGES (trainings dropdown)\\
@app.route('/trainings',methods=['POST'])
@app.route('/trainings/<period>')
@login_required
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
@login_required
def training(id):
    # Here you have to add all the conditions and the instructions to retrieve the right training's information from
    # the db
    # Also, you will have to pass the entire training instance to the html page (see the skill(kind) function to see
    # how to do it
    # In the training.html you will have to take the information you have to show from the variable passed from here,
    # see skills.html to have an example
    return render_template('training.html')


# //PROJECTS PAGES\\
@app.route('/projects', methods=['GET', 'POST'])
@app.route('/projects/<period>')
@login_required
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
        prj_supervisor = request.form.get('prjSupervisor')
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
    elif period == "all":
        projects_list, supervisors = get_projects_and_supervisors()

    projects_list.sort(key=lambda x: x.starting_date, reverse=True)
    possible_roles=get_roles_in_projects()
    possible_roles.sort(key=lambda x: x.id)
    emp = get_employees()

    return render_template('projects.html', projects=projects_list, period=period, supervisors=supervisors, roles=possible_roles, employees=emp)


@app.route('/project/<int:id>', methods=['GET', 'POST'])
@login_required
def project(id):
    if request.method == 'POST':
        action = str(request.form.get('actionToPerform'))
        # Edit project basic information
        if action == "editProjectInfo":
            prj_name = str(request.form.get('prjName'))
            prj_description = str(request.form.get('prjDesc'))
            # starting date is a required value, so there's no check on its content (it is needed to sort the list of projects when retrieved from the db
            prj_start_date = request.form.get('prjStart')
            prj_start_date = datetime.datetime.strptime(str(prj_start_date), '%Y-%m-%d').date()
            # if there's a value inside the prjEndingDate it is converted into datetime, otherwise is set to none
            prj_end_date = request.form.get('prjEnd')
            if prj_end_date:
                prj_end_date = datetime.datetime.strptime(str(prj_end_date), '%Y-%m-%d').date()
            else:
                prj_end_date = None
            supervisor = request.form.get("prjSupervisor")
            edited_proj = edit_project_basic_info(id, prj_name, prj_description, prj_start_date, prj_end_date, supervisor)

        # Assign a role to an employee
        elif action == "assignEmployees":
            free_roles = get_free_roles_in_project(id)
            for role in free_roles:
                emp_id = request.form.get("addEmployeeRole"+str(role.id))
                if emp_id:
                    emp = get_employee_by_id(emp_id)
                    if emp not in get_employees_in_project(id):
                        new_prj_role=add_employee_to_project(id, role.id, emp_id)
                    else:
                        error = "An employee can't have more than one role in a project"
                else:
                    print "No employee selected"

        # Add roles to the project
        elif action == "addRoles":
            roles = request.form.getlist("new_roles")
            for role_id in roles:
                added= add_role_to_project(id, role_id)

        # Remove roles from the project
        elif action == "deleteRole":
            role = request.form.get("roleToDelete")
            check_delete = remove_role_from_project(id, role)

        # Remove employee from a role
        elif action == "deassignRole":
            role = request.form.get("roleToDeassign")
            prj_role = remove_employee_from_project(id, role)

        elif action == "addEvaluations":
            emps = get_employees_in_project(id)
            for emp in emps:
                ev = request.form.get("evaluationEmp"+str(emp.id))
                if ev != "":
                    prj_role = add_evaluation_to_employee_in_project(id, emp.id, ev)

        elif action == "deleteProject":
            proj = request.form.get("projectToDelete")
            delProj = delete_project(id)
            return redirect(url_for('projects'))

        return redirect(url_for('project', id=id))

    prj = get_project_by_id(id)
    supervisor = None
    if prj.supervisor:
        supervisor = get_employee_by_id(prj.supervisor)
    all_emps = get_employees()
    closable = dt.today().date() > prj.ending_date
    emp_roles = get_employees_in_project_with_roles(id)
    free_roles = get_free_roles_in_project(id)
    free_employees = get_available_employees_in_period(prj.starting_date, prj.ending_date)
    empty_roles_best_employees = []
    for fr in free_roles:
        se, ue, ne = get_suitable_emp_for_role(fr.id, free_employees)
        erbe =[fr,se,ue,ne]
        empty_roles_best_employees.append(tuple(erbe))
    # empty_roles_best_employees will be a list of tuples which contain, in order, the role entity and the 3 lists of
    # available suitable employees for that specific role
    employee_evaluations = get_employees_with_evaluation(id)
    other_roles = get_not_used_roles_in_proj(id)
    return render_template('project.html', project=prj, employees_roles=emp_roles,\
                           free_roles_and_employees=empty_roles_best_employees,\
                           employee_evaluations=employee_evaluations, available_employees=free_employees,\
                           other_roles=other_roles, closable=closable, supervisor=supervisor, employees=all_emps)


@app.route('/edit_role/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    role_in_project = get_roles_in_projects_by_id(id)
    all_skills=get_skills()
    skills, grades = role_in_project.get_skills_required()
    dic=[]
    for s, g in map(None, skills, grades):
        dic.append((s.id, s.name, g))

    if request.method=='POST':
        description = request.form.get("newDescription")
        role_updated = edit_role_description(id, description)
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

        # Delete all duplicate from the list dic
        seen = set()
        dic = [(a, b) for a, b in dic if not (a in seen or seen.add(a))]
        # Delete previous requirements
        role_updated = remove_skills_required_from_role_in_project(id)
        # Update skill requirements
        for skill in dic:
            add_skill_to_role_in_project(role_updated.id, skill[0], skill[1])  # insert all new skills requirements
        return redirect(url_for('roles'))

    return render_template('edit_role.html', role=role_in_project, all_skills=all_skills, dic=dic)


@app.route('/roles', methods=['GET', 'POST'])
@login_required
def roles():
    if request.method=='POST':
        action = request.form.get("actionToPerform")

        if action == "deleteRole":
            role_id = request.form.get("roleToDelete")
            deleted = delete_role_in_project(role_id)

        elif action == "newRole":
            name = request.form.get("roleName")
            description = request.form.get("roleDescription")
            new_role = create_role_in_project(name,description)
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

            # Delete all duplicate from the list dic
            seen = set()
            dic = [(a, b) for a, b in dic if not (a in seen or seen.add(a))]
            # Add skill requirements to the role created
            for skill in dic:
                add_skill_to_role_in_project(new_role.id, skill[0], skill[1])  # insert all new skills requirements
            return redirect(url_for('roles'))

    roles = get_roles_in_projects()
    skills = get_skills()
    print skills
    return render_template('roles.html', roles=roles, all_skills=skills)


@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


# //LOGIN AND USER MANAGEMENT\\
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Here we'll have to manage the entire login procedure
    if request.method=='POST':
        email = request.form.get("userEmail")
        password = request.form.get("userPassword")
        user = get_user_by_email(email)
        if user and bcrypt.check_password_hash(user.password, password):
            if request.form.get("rememberMe"):
                login_user(user,True)
            else:
                login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Incorrect username or password", email=email)

    return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
    if request.method=="POST":
        logout_user()
    return redirect("/home")


@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    if request.method=='POST':
        action = request.form.get("actionToPerform")
        if action == "deleteUser":
            user_id = request.form.get("userToDelete")
            if user_id == current_user.id:
                logout_user()
            deleted = delete_user(user_id)
            if not current_user.is_authenticated:
                return redirect("/home")
        elif action == "editPermission":
            user_id = request.form.get("userToAdmin")
            new_admin = make_user_admin(user_id)
        elif action == "editEmail":
            user_id = current_user.id
            new_mail = request.form.get("userEmail")
            user = edit_user_email(user_id, new_mail)
        elif action == "newUser":
            name = request.form.get("userName")
            surname = request.form.get("userSurname")
            mail = request.form.get("userEmail")
            password = request.form.get("userPassword")
            confirm_password = request.form.get("userConfirmPassword")
            permission = request.form.get("userPermission")
            if password == confirm_password:
                if permission == "True":
                    user = create_user(name, surname, mail, bcrypt.generate_password_hash(password).encode('utf-8'), True)
                else:
                    user = create_user(name, surname, mail, bcrypt.generate_password_hash(password).encode('utf-8'), False)
        elif action == "changePassword":
            user_id = current_user.id
            user = get_user_by_id(user_id)
            old_password = request.form.get("oldPassword")
            if user and bcrypt.check_password_hash(user.password, old_password):
                new_password = request.form.get("newPassword")
                confirm_password = request.form.get("confirmPassword")
                if new_password == confirm_password:
                    edited = edit_user_password(user_id, bcrypt.generate_password_hash(new_password).encode('utf-8'))
                else:
                    return render_template("users.html", error_password="Confirmation is different from new password")
            else:
                return render_template("users.html", error_password="Error with your old password")

    admins = get_admins(True)
    normal_users = get_admins(False)
    return render_template("users.html", admins=admins, users=normal_users)


if __name__ == '__main__':
    app.run(debug=True)
