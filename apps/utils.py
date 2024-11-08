from flask_mail import Message
from flask import current_app
from apps import mail

def send_email(to, subject, template):
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)


# def register_google():
#     google = oauth.register(
#         name='google',
#         client_id=current_app.config['GOOGLE_CLIENT_ID'],
#         client_secret=current_app.config['GOOGLE_CLIENT_SECRET'],
#         server_metadata_url='https://accounts.google.com/.well-known/openid-configuration',
#         client_kwargs={'scope': 'openid email profile'},
#     )

#     return google