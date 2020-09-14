import os, subprocess 
from app import db
from app.models import User
import datetime

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
# "email":["name", "password", "confirmed", "registered_on", "role", "confrimed_on", "password_reset_token"]
myusers = {"student1@students.com":["student1","st", False, datetime.date.today(), "",None,None], 
          "super1@supers.com":["supervisor1", "s", False, datetime.date.today(), "Supervisor", None, None], 
          "admin1@admins.com":["admin1", "a", True, datetime.date.today(), "Administrator", None, None]}

# Inserting users in to database from myusers (above)
for email, details in myusers.items():
  # u = User()
  # u.set_user_email(email)
  # u.set_user_name(details[0])
  # u.set_user_password(details[1])
  # u.set_user_role(details[2])
  u = User(details[0], email, details[1], details[2], details[3], details[4], details[5], details[6])
  db.session.add(u)
  db.session.commit()

# Migrating and upgrading database after insertion 
commands_2 = [b, c]
for command in commands_2:
  os.system(command)





