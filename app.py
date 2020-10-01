#!flask/bin/python
from app import create_app
from app.models import User

app = create_app()
app.app_context().push()
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User}
