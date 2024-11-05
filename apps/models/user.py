from apps import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(225))
    name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<email {self.email}>"