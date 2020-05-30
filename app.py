from flask import Flask, request, session, render_template, redirect, url_for
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
import datetime
from datetime import datetime as dt
from flask_wtf import Form, FlaskForm
from wtforms import StringField, SubmitField, DateField, SelectField, FileField, validators
from wtforms.validators import DataRequired, InputRequired
import os, sys

from database import *
from flask_bcrypt import Bcrypt

UPLOAD_FOLDER = 'static/images/profile'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nksndfkvnfjkvn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
track_modifications = app.config.setdefault('SQLALCHEMY_TRACK_MODIFICATIONS', False)
bcrypt=Bcrypt(app)
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

#            /// ROUTES \\\
#            Here we define the routes used to get to the html pages and the functions performing the actions needed to retrieve
#            the correct data from the db

# I will subdivide the routes based on their "macro page"

# //LOGIN AND USER MANAGEMENT\\

### LOGIN MANAGER SETTINGS ###
@login_manager.user_loader
def load_user(user_id):
    return get_user_by_id(user_id)


### LOGIN PAGE ###
@app.route('/login', methods=['GET', 'POST'])
def login():
    # Manage login procedure
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


### LOGOUT PROCEDURE ROUTE ###
@app.route('/logout', methods=['POST'])
def logout():
    if request.method=="POST":
        logout_user()
    return redirect("/home")


### USERS MANAGEMENT PAGE ###
@app.route('/users', methods=['GET', 'POST'])
@login_required
def users():
    # Returns a list of all the users, divided into admins and common users

    if request.method=='POST':
        # Same method of the project page to handle the various forms
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
            prj = request.form.get("projectResponsible")
            if password == confirm_password:
                if permission == "True":
                    user = create_user(name, surname, mail, bcrypt.generate_password_hash(password).encode('utf-8'), prj, True)
                else:
                    user = create_user(name, surname, mail, bcrypt.generate_password_hash(password).encode('utf-8'), prj, False)

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
    prjs = get_projects()
    return render_template("users.html", admins=admins, users=normal_users, projects = prjs)


# //MAIN PAGES (first dropdown menu)\\

### HOME PAGE ###
@app.route('/')
@app.route('/home')
@app.route('/index')
def index():
    return render_template('index.html')

### GUIDE PAGE ###
@app.route('/guide')
def guide():
    return render_template('guide.html')

### ABOUT US PAGE ###
@app.route('/about')
def about():
    return render_template('about.html')

### FREQUENTLY ASKED QUESTIONS PAGE ###
@app.route('/faq')
def faq():
    return render_template('FAQ.html')

### TEAM MEMBERS PAGE ###
@app.route('/team')
def team():
    return render_template('team.html')


# //SKILLS PAGES (second dropdown menu)\\

@app.route("/skills", methods=['GET','POST'])
@app.route('/skills/<kind>')
@login_required
def skills(kind="soft"):
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

###EMPLOYEES GRID###
@app.route('/employees',methods=["GET","POST"])
@login_required
def employees():
    search=""
    roles=get_roles()
    if request.method == 'POST':
        search = request.form['search']
        #Search
        if search!="":
            employees=[]
            for employee in get_employees():
                if search in employee.name or search in employee.surname:
                    employees.append(employee)

        else:
            employees = get_employees()
    else:
        employees = get_employees()
    return render_template('employees.html', employees=employees,search=search,roles=roles)


###CLASS FLASK FORM FOR ADD NEW EMPLOYEE###
class EmployeeForm(FlaskForm):
    # Personal
    name = StringField('Name:', [validators.DataRequired()])
    surname = StringField('Surname:', validators=[DataRequired()])
    # photo = FileField('Image File')
    birthday = DateField('Birthday:', format='%Y-%m-%d', validators=[DataRequired()])
    living_place = StringField('Address:', validators=[DataRequired()])
    phone = StringField('Phone Number:', validators=[DataRequired()])
    email = StringField('E-mail:', validators=[DataRequired()])
    driving_licence = SelectField(u'Driving Licence:', choices=[(True, 'YES'), (False, 'NO')],
                                  validators=[InputRequired()], coerce=lambda x: x == 'True')
    date_of_assumption = DateField('Hiring Date:', format='%Y-%m-%d')

    role = SelectField(u'Role:', coerce=int)
    # Education
    state_in_company = SelectField(u'State in the Company:',
                                   choices=[('active', 'ACTIVE'), ('layoffs', 'LAYOFFS'), ('holidays', 'HOLIDAYS')],
                                   validators=[InputRequired()])
    education_level = StringField('Level of Education')
    language_certificate = StringField('Language Certifications')
    submit = SubmitField('Save')
### END CLASS FLASK FORM FOR ADD NEW EMPLOYEE###


### EMPLOYEE PERSONAL PAGE ###
@app.route('/employee/<int:id>')
@login_required
def employee(id):
    message = request.args.get("message")
    employee = get_employee_by_id(id)
    trainings = get_trainings_of_employee(id)
    projects = get_projects_of_employee(id)
    past_projects, past_supervisors = get_past_projects()
    current_projects, current_supervisors = get_current_projects()
    skills = get_skills_of_employee(id)
    roles = get_roles()
    list_hard = []
    list_soft = []
    past_emp_pjs = []
    current_emp_pjs = []
    evaluations = []

    # Employee Skills
    for skill in skills:
        score = get_gradeofskill_by_emp_skill(id, skill.id)
        if skill.type.lower() == 'hard':
            list_hard.append((skill, score))
        elif skill.type.lower() == 'soft':
            list_soft.append((skill, score))
    # Employee Projects
    for project in projects:
        if project in past_projects:
            for tupla in employee.project_role:
                role_id = tupla.role_id
                evaluations = get_evaluation_by_proj_emp_role(project.id, employee.id, role_id)
            past_emp_pjs.append((project, evaluations))
        elif project in current_projects:
            current_emp_pjs.append(project)

    return render_template('employee.html', employee=employee, trainings=trainings, projects=projects,
                           list_hard=list_hard, list_soft=list_soft, past_emp_pjs=past_emp_pjs,
                           current_emp_pjs=current_emp_pjs, message=message, roles=roles)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


### NEW EMPLOYEE PAGE ###
@app.route('/add_employee', methods=['GET', 'POST'])
@login_required
def new_employee():
    employee = None
    form = EmployeeForm()
    form.role.choices = [(role.id, role.name) for role in get_roles()]
    skills = get_skills()

    # POST
    if form.validate_on_submit():
        ###Flask Form###
        # Personal
        first_name = form.name.data
        last_name = form.surname.data
        birthday = form.birthday.data
        phone = form.phone.data
        email = form.email.data
        driving_licence = form.driving_licence.data
        living_place = form.living_place.data
        date_of_assumption = form.date_of_assumption.data
        state_in_company = form.state_in_company.data
        role = form.role.data
        # Education
        education_level = form.education_level.data
        language_certificate = form.language_certificate.data

        # Create instance of Employee
        employee = Employee(name=first_name, surname=last_name, date_of_birth=birthday, telephone=phone, email=email,
                            driving_licence=driving_licence, living_place=living_place,
                            date_of_assumption=date_of_assumption, state_in_company=state_in_company, role=role,
                            education_level=education_level, language_certificate=language_certificate)

        # Add new employee to db
        set_employee(employee)

        # Upload Image
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename) and file.filename != '':
                filename = "image_profile_" + str(employee.id) + ".jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                employee.photo = filename

            else:
                employee.photo = "default.png"
        update_employee(employee)
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

        # Delete
        delete_all_grade_of_skill_of_employee(employee.id)  # delete all skills

        # Delete all duplicate from the dic list
        seen = set()
        dic = [(a, b) for a, b in dic if not (a in seen or seen.add(a))]

        # Add the skills of the employee into db
        for y in dic:
            set_grade_of_skill_of_employee(y[1], employee.id, y[0])
            # Once saved employee information in db return the employee.html page
        return redirect(url_for('employee', id=employee.id, message=""))  # Message neet to show popup save

    return render_template('newemployee.html', employee=employee, form=form, skills=skills)


###DELETE EMPLOYEE###
@app.route('/delete_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_employee_page(id):
    print("DELETE: " + str(id))
    delete_employee(id)
    return redirect(url_for("employees"))


@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "0"
    r.headers['Cache-Control'] = 'public, max-age=0'
    return r


###EDIT EMPLOYEE###
@app.route('/edit_employee/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_employee(id):
    form = EmployeeForm()
    skills = get_skills()  # get all the skills in db
    form.role.choices = [(role.id, role.name) for role in get_roles()]
    # GET
    if request.method == 'GET':
        employee = get_employee_by_id(id)
        # Flask Form
        form.name.data = employee.name
        form.surname.data = employee.surname
        form.birthday.data = employee.date_of_birth
        form.phone.data = employee.telephone
        form.email.data = employee.email
        form.driving_licence.data = employee.driving_licence
        form.living_place.data = employee.living_place
        form.date_of_assumption.data = employee.date_of_assumption
        form.state_in_company.data = employee.state_in_company
        form.role.data = employee.role
        form.education_level.data = employee.education_level
        form.language_certificate.data = employee.language_certificate
        # get the skills of the employee in db
        employee_skills = get_skills_of_employee(employee.id)
        # get the grades of the skills of the employee in db
        dic = []
        for employee_skill in employee_skills:
            grade = get_gradeofskill_by_emp_skill(id, employee_skill.id)
            dic.append((employee_skill.id, employee_skill.name, grade))
    # POST
    else:
        # Flask Form
        first_name = form.name.data
        last_name = form.surname.data
        birthday = form.birthday.data
        phone = form.phone.data
        email = form.email.data
        driving_licence = form.driving_licence.data
        living_place = form.living_place.data
        date_of_assumption = form.date_of_assumption.data
        state_in_company = form.state_in_company.data
        role = form.role.data
        language_certificate = form.language_certificate.data
        education_level = form.education_level.data

        # Create instance of Employee
        employee = Employee(id=id, name=first_name, surname=last_name, date_of_birth=birthday, telephone=phone,
                            email=email, driving_licence=driving_licence, living_place=living_place,
                            date_of_assumption=date_of_assumption, state_in_company=state_in_company, role=role,
                            education_level=education_level, language_certificate=language_certificate)

        # Update the employee data into db

        # Upload Image
        if 'file' in request.files:
            file = request.files['file']
            if file and allowed_file(file.filename) and file.filename != '':
                filename = "image_profile_" + str(employee.id) + ".jpg"
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                employee.photo = filename
            else:
                photo = get_employee_by_id(id).photo
                employee.photo = photo

        update_employee(employee)

        # Skills
        number = request.form["number"]
        number = int(number)
        dic = []
        employee_skills = get_skills_of_employee(employee.id)
        for x in range(number):
            skill_index = "skill" + str(x)
            skill = request.form.get(skill_index)
            if skill != None:
                skill_id = request.form[skill_index]  # Parametro form (ex. skill0=adaptability)
                score_index = "score" + str(x)
                score = request.form[score_index]
                dic.append((skill_id, score))

        # Delete all skills
        delete_all_grade_of_skill_of_employee(employee.id)

        # Delete all duplicate from the list dic
        seen = set()
        dic = [(a, b) for a, b in dic if not (a in seen or seen.add(a))]
        # Add the skills of the employee into db
        for skill in dic:
            set_grade_of_skill_of_employee(skill[1], employee.id, skill[0])  # insert all new skills
        # Once saved employee information in db return the employee.html page
        return redirect(url_for('employee', id=employee.id, message="Save"))  # Message neet to show popup save

    return render_template('edit_employee.html', employee=employee, form=form, employee_skills=employee_skills,
                           skills=skills, dic=dic)


# //JOBS PAGES (fourth dropdown menu)\\

### JOBS LIST PAGE ###
@app.route('/jobs',methods=['POST'])
@app.route('/jobs')
@login_required
def jobs():
    if request.method == 'POST':
        # create a new job

        # get values from the inputs of the form in job.html
        job_name = str(request.form.get('role'))
        job_description = str(request.form.get('Jdescription'))
        id_job = add_role_todb(job_name, job_description)

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
    employee_list=get_employees()

    open=[]
    closed=[]
    for job in roles:
        if job.employee:
            closed.append(job)
        else:
             open.append(job)

    return render_template('jobs.html',softskill=soft_skill,hardskill=hard_skill,role=roles,open=open,closed=closed,employee=employee_list,job_skill=job_skill)


### SINGLE JOB PAGE ###
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

        elif action =="assignEmployees":
            empl_id = request.form.get('AssignEmployee')
            update_employee_job(id,empl_id)

        elif action == "deleteJob":
            deleted = delete_role(id)
            return redirect(url_for('jobs'))

        elif action == "removeEmployee":
            emp_id = request.form.get("employeeToRemove")
            remove_employee_from_job(id, emp_id)

    skill = get_skills_required_by_role(id)
    # get the grades of the skills of the employee in db
    dic = []
    for i in skill:
        grade = get_gradeofskill_required_for_a_job(id, i.id)
        dic.append((i.id,i.name, grade))
    role=get_role_by_id(id)
    all_skills=get_skills()
    skill_id=get_skill_id_of_a_role(id)
    var1,var2,var3=get_suitable_emp_for_job(id)
    empl=True
    if role.employee:
        empl=False

    return render_template('job.html', role=role, skill=skill, grade =skill_id, var1=var1, var2=var2, var3=var3, empl=empl, all_skill=all_skills, dic=dic)


# //TRAININGS PAGES (fifth dropdown)\\

### TRAININGS LIST PAGE ###
@app.route('/trainings',methods=['POST'])
@app.route('/trainings/<period>')
@login_required
def trainings(period="all"):
    if request.method=="POST":
         tra_name=str(request.form.get('traName'))
         tra_hours=request.form.get('traHours')
         tra_start_date = request.form.get('traStartingDate')
         tra_start_date = datetime.datetime.strptime(str(tra_start_date), '%Y-%m-%d').date()
         # if there's a value inside the prjEndingDate it is converted into datetime, otherwise is set to none
         tra_end_date = request.form.get('traEndingDate')
         if tra_end_date:
             tra_end_date = datetime.datetime.strptime(str(tra_end_date), '%Y-%m-%d').date()
         else:
             tra_end_date = None

         training1=add_training_to_db(tra_name,tra_start_date,tra_end_date,tra_hours)

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

         for y in dic:
             add_skill_to_training(training1, y[0], y[1])

         return redirect(url_for('training',id=training1))


    skills=get_skills()
    if period == "past":
         trainings_list = get_past_trainings()
    elif period == "current":
         trainings_list = get_current_trainings()
    else:
         trainings_list= get_trainings()

    trainings_list.sort(key=lambda x: x.starting_Date, reverse=True)
    ranges=[1,2,3,4,5,6,7,8,9,10]

    return render_template('trainings.html',skills=skills,trainings_list=trainings_list,range=ranges)


### SINGLE TRAINING PAGE ###
@app.route('/training/<int:id>', methods=['GET','POST'])
@login_required
def training(id):
    if request.method=='POST':
        action=str(request.form.get('actionToPerform'))
        if action == "editTrainingInfo":
            tra_name=str(request.form.get('traName'))
            tra_hours=request.form.get('traHours')
            tra_start_date = request.form.get('traStart')
            tra_start_date = datetime.datetime.strptime(str(tra_start_date), '%Y-%m-%d').date()
            tra_end_date = request.form.get('traEnd')
            if tra_end_date:
                tra_end_date = datetime.datetime.strptime(str(tra_end_date), '%Y-%m-%d').date()
            else:
                tra_end_date = None
            edited_Tra=edit_training_info(id,tra_name,tra_start_date,tra_end_date,tra_hours)

        elif action=="assignEmployees":
            emp_ids = request.form.getlist("addEmployeeTraining")
            for emp_id in emp_ids:
                add_employee_to_training(id,emp_id)

        elif action=="deleteTraining":
            delete_training(id)
            return redirect('/trainings/all')

        elif action=="closeTraining":
            close_training(id)

        elif action=="deleteSkill":
            skill=request.form.get('skillToDelete')
            check_delete=delete_skill_from_training(id,skill)

        elif action=="deassignEmployee":
            emp=request.form.get('employeeToDeassign')
            check_delete=delete_employee_from_training(id,emp)

        elif action=="editSkill":
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

            delete_all_grade_of_skill_of_job(id)

            # Delete all duplicate from the list dic
            seen = set()
            dic = [(a, b) for a, b in dic if not (a in seen or seen.add(a))]
            # Add the skills of the employee into db
            for skill in dic:
                add_skill_to_training(id, skill[0], skill[1])  # insert all new skills

        return redirect(url_for('training',id=id))

    link = Training_Skill.query.filter(Training_Skill.train_id == id).all()
    skill_ids = []
    skills=[]
    for l in link:
        if l.skill_id:
            skill_ids.append(l.skill_id)
    for k in skill_ids:
        skill=get_skill_by_id(k)
        skills.append(skill)

    # get the grades of the skills of the employee in db
    dic = []
    for i in skills:
        point = get_pointsassigned_by_training_to_skill(id, i.id)
        dic.append((i.id, i.name, point))

    all_skill=get_skills()
    training=get_trainings_by_id(id)
    skill_point=get_skill_in_training_with_points(id)
    emp=get_employees_in_training(id)
    employees1=get_employees_not_in_training(id)

    return render_template('training.html',training=training,skill_point=skill_point,employees=emp,dic=dic,skills=skills,all_skill=all_skill,employees1=employees1)


# //PROJECTS PAGES (last dropdown in the navbar)\\

### PROJECTS LIST PAGE ###
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


### SINGLE PROJECT PAGE ###
@app.route('/project/<int:id>', methods=['GET', 'POST'])
@login_required
def project(id):
    if request.method == 'POST':
        # As there are many forms in the project page, they are distinguished by using an hidden input identifying the action to perform
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
                        print "An employee can't have more than one role in a project"

        # Add roles to the project
        elif action == "addRoles":
            roles = request.form.getlist("new_roles")
            for role_id in roles:
                added = add_role_to_project(id, role_id)

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

    # If not interrupted before (because of a post request with a different destination)
    # Get the project instance interested by the GET request
    prj = get_project_by_id(id)
    # get the supervisor of the project (if existent)
    supervisor = None
    if prj.supervisor:
        supervisor = get_employee_by_id(prj.supervisor)
    # get a list of all the possible employees
    all_emps = get_employees()
    # check if the project can be closed (ending date previous w.r.to the current date)
    closable = dt.today().date() > prj.ending_date
    # get info regarding the employees working on the project and those free in the project time-window
    # get also a list of the empty roles in the project
    emp_roles = get_employees_in_project_with_roles(id)
    free_roles = get_free_roles_in_project(id)
    free_employees = get_available_employees_in_period(prj.starting_date, prj.ending_date)
    empty_roles_best_employees = []
    # For every empty role in the project,
        # divide the available employees into three cathegories:
            # skilled (have all skills required with sufficient grades)
            # unskilled (have all skills required but with insufficient grades)
            # non-skilled (have a portion of the skills required)
    for fr in free_roles:
        se, ue, ne = get_suitable_emp_for_role(fr.id, free_employees)
        erbe =[fr,se,ue,ne]
        empty_roles_best_employees.append(tuple(erbe))
    # empty_roles_best_employees will be a list of tuples which contain, in order, the role entity and the 3 lists of
    # available suitable employees for that specific role
    employee_evaluations = get_employees_with_evaluation(id)
    # get list of every reamining not used role_in_project
    other_roles = get_not_used_roles_in_proj(id)
    return render_template('project.html', project=prj, employees_roles=emp_roles,\
                           free_roles_and_employees=empty_roles_best_employees,\
                           employee_evaluations=employee_evaluations, available_employees=free_employees,\
                           other_roles=other_roles, closable=closable, supervisor=supervisor, employees=all_emps)


# // ROLES IN PROJECTS PAGES \\

### EDIT ROLE PAGE ###
@app.route('/edit_role/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_role(id):
    # Gets the requested role instance and a list of all the skills
    role_in_project = get_roles_in_projects_by_id(id)
    all_skills=get_skills()

    # Edits the role's information
    if request.method=='POST':
        description = request.form.get("roleDesc")
        role_updated = edit_role_description(id, description)

        # Skills
        # number of required skills
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

        return redirect('/roles')

    # Creates a list of tuples containing the skill id, the skill name and the grade required for the role
    skills, grades = role_in_project.get_skills_required()
    dic = []
    for s, g in map(None, skills, grades):
        dic.append((s.id, s.name, g))
    return render_template('edit_role.html', role=role_in_project, all_skills=all_skills, dic=dic)


### ROLES LIST PAGE ###
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
    return render_template('roles.html', roles=roles, all_skills=skills)


if __name__ == '__main__':
    app.run(debug=True)
