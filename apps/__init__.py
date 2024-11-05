from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    mail.init_app(app)

    # blueprints
    from apps.groups.routes import groups
    app.register_blueprint(groups)

    from apps.account.routes import account
    app.register_blueprint(account)


    @app.route('/')
    def test():
        return 'Hello, World!'

    return app