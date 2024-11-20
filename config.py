from dotenv import load_dotenv
import os

load_dotenv() 

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "very-important")
    # JWT
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "super-secret")
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Mail Settings
    MAIL_DEFAULT_SENDER = "noreply@flask.com"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = False
    MAIL_USERNAME = os.environ.get("EMAIL_USER")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    # Google SSO
    print('GOOGLE_CLIENT_ID-->',os.environ.get("SECRET_KEY"))
    GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
    GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
    GOOGLE_DISCOVERY_URL = "https://accounts.google.com/.well-known/openid-configuration"

