from flask import Blueprint, request, jsonify, url_for, render_template
from werkzeug.security import generate_password_hash
from datetime import datetime
from apps.models.user import User
from apps import db
from apps.account.utils import generate_token, confirm_token
from apps.utils import send_email
account = Blueprint('account', __name__, url_prefix='/account', template_folder='templates')


@account.route('/sign_up', methods=['POST'])
def add_user():
    payload = request.json
    username = payload.get('username')
    password = payload.get('password')
    email = payload.get('email')
    name = payload.get('name')
    if not username or not password or not email or not name:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # check for existing username
    if User.query.filter_by(username=username).first():
        return jsonify({'message': "username already exists"}), 400
    # check for exisiting email
    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already Exists"}),400
    
    # Hash the password
    hash_password = generate_password_hash(password, salt_length=16)
    
    user = User(username=username,
                email=email,
                password=hash_password,
                name=name,
                created_at=datetime.now()
                )
    db.session.add(user)
    db.session.commit()

    # send email verification
    token = generate_token(email)
    print(token)
    confirm_url = url_for("account.confirm_email", token=token, _external=True)
    print(confirm_url)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    print(html)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)

    return jsonify({"message": "Success"}), 201


@account.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    email = confirm_token(token)

    if email is None:
        return jsonify({"message": "Invalid or expire token"}), 400
    
    user = User.query.filter_by(email=email).first()
    if user is None:
        return jsonify({"message": "Email does not exist"}), 404
    
    if user.is_confirmed:
        return jsonify({"message": "Email already confirmed"}), 400
    
    user.is_confirmed = True
    user.confirmed_on = datetime.now()
    # db.session.add(user)
    db.session.commit()
    return jsonify({"message": "Email confirmed successfully"}), 200
