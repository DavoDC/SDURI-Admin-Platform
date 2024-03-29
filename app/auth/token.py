
from app import app
from itsdangerous import URLSafeTimedSerializer



def generate_confirmation_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])


def confirm_token(token, expiration=24 * 3600):
    """Return email from token"""
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    try:
        email = serializer.loads(
                                 token,
                                 salt=app.config['SECURITY_PASSWORD_SALT'],
                                 max_age=expiration
                                 )
    except:
        return False
    return email
