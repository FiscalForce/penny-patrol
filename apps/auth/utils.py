from itsdangerous import URLSafeTimedSerializer
from flask import current_app
from apps.models.user import User


def generate_token(email):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    return serializer.dumps(email, salt=current_app.config["SECURITY_PASSWORD_SALT"])


def confirm_token(token, expiration=3600):
    serializer = URLSafeTimedSerializer(current_app.config["SECRET_KEY"])
    try:
        email = serializer.loads(
            token, salt=current_app.config["SECURITY_PASSWORD_SALT"], max_age=expiration
        )
        return email
    except Exception:
        return False


def create_unique_username(username):
    i = 1
    while is_username_taken(username):
        username = f"{username}_{i}"
        i += 1
    return username


def is_username_taken(username):
    user = User.query.filter_by(username=username).first()
    return user is not None