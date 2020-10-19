from app import db
from app.models import User
import os
from datetime import date
#import subprocess

# Variables intialization
a = "flask db init"
b = "flask db migrate"
c = "flask db upgrade"

# Removing any previous migrations folder and database file for flexibility
if (os.system("rm -r migrations")):
    pass
if (os.system("rm *.db")):
    pass

# Initialization of database 
commands = [a, b, c]
for command in commands:
    os.system(command)

# The following myusers dictionary format is: 
# "email":["name", "password", "confirmed", "registered_on", "role"]
myusers = {"student1@students.com":["student1", "st", True, date.today(), "Student"], 
    "super1@supers.com":["supervisor1", "s", True, date.today(), "Supervisor"], 
    "admin1@admins.com":["admin1", "a", True, date.today(), "Administrator"]}

# Inserting users in to database from myusers (above)
for email, details in myusers.items():
    u = User(name=details[0],
             email=email,
             password=details[1],
             confirmed=details[2],
             registered_on=details[3],
             role=details[4])
    db.session.add(u)
    db.session.commit()

# Migrating and upgrading database after insertion 
commands_2 = [b, c]
for command in commands_2:
    os.system(command)





