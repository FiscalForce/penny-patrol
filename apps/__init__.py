from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from authlib.integrations.flask_client import OAuth


db = SQLAlchemy()
migrate = Migrate()
mail = Mail()
# oauth = OAuth()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)

    # oauth.init_app(app)

    # blueprints
    from apps.groups.routes import groups
    app.register_blueprint(groups)

    from apps.auth.routes import auth
    app.register_blueprint(auth)


    @app.route('/')
    def test():
        return 'Hello, World!'

    return app