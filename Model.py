##### MODEL ######
# None=[], void list

from enum import Enum
from datetime import date  # capire come si fa


class Licence(Enum):
    B = 1
    C = 2
    NO = 3


class StateHealth(Enum):
    HEALTHY = 1
    SICK = 2


class States(Enum):
    ACTIVE = 1
    ON_HOLIDAYS = 2
    IN_LAYOFFS = 3


class SkillType(Enum):
    SOFT = 1
    TECHNICAL = 2


class Employee:
    def __init__(self, name='', surname='', email='', birthday=date, place='', licence=Licence(Enum), superior='',
                 health_state=StateHealth(Enum), role='', degree=None, certifications=None, company_state=States(Enum),
                 file='', skills=None, training_courses=None, project_works=None):
        self.name = name
        self.surname = surname
        self.email = email
        self.birthday = birthday
        self.living_place = place
        self.driving_licence = licence
        self.superior = superior
        self.health_state = health_state
        self.company_role = role
        self.degree = degree
        self.certifications = certifications
        self.company_state = company_state
        self.photo = file  # change the type of it in the default
        self.skills = skills
        self.training_courses = training_courses
        self.project_works = project_works


class Job:
    def __init__(self, title='', duration=0, starting_date=date, skill_required=None, description='', nominees=None):
        self.title = title
        self.duration = duration
        self.starting_date = starting_date
        self.skill_required = skill_required
        self.job_description = description
        self.nominees = nominees


class Skill:
    def __init__(self, skill_name='', weight=0, skill_type=SkillType(Enum)):
        self.name = skill_name
        self.weight = weight
        self.type = skill_type


class ProjectWork:
    def __init_(self, title='', beginning_date=date, ending_date=date, project_type=None, description='', skills=None,
                team=None, coordinators=None, evaluations=None, partecipants=None):
        self.title = title
        self.beginning_date = beginning_date
        self.ending_date = ending_date
        self.type = project_type
        self.project_description = description
        self.skills = skills
        self.team = team
        self.coordinators = coordinators  # Basic Users which give the evaluation
        self.partecipants = partecipants  # list of employee


class TrainingCourse:
    def __init__(self, title='', course_date=date, course_description='', obtained_skills=Skill(), training_type=None,
                 employees=None):
        self.title = title
        self.course_date = course_date
        self.description = course_description
        self.obtained_skill = obtained_skills  # nella definizione del default si può mettere come lista di skill oppure come una singola skill decidere
        self.training_type = training_type
        self.employees = employees


class User:
    def __init__(self, username='', password='', id_number=0):
        self.username = username
        self.password = password
        self.id = id_number


class HR(User):
    def __init__(self, user=User()):
        User.__init__(self, user.username, user.password, user.id)


class BasicUser(User):  # nel controler inserire il methodo valutazione
    def __init__(self, user=User(), project_works=None):
        User.__init__(self, user.username, user.password, user.id)
        self.project_works = project_works
