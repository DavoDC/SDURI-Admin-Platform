# Controller.py
from app import app, db
from app.models import User, Student, Project, Preference

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