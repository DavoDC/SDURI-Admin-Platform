# Controller.py
from app import app
from app import db
from app.models import Preference
from app.models import Project
from app.models import Student
from app.models import User

class Controller():

    # CREATE
    @staticmethod
    def create_project(projectID: int, m_sup: str, c_sup: str, faculty: str, school: str, title: str, description: str, skills: str, keywords: str, email: str, campus: str, length: int, total: int, place: str):
        '''
        Adds a project to the database
        '''

        return

    # READ

    # UPDATE

    # DELETE