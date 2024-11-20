import requests
from datetime import datetime
from flask import Blueprint, request, jsonify, url_for, render_template, current_app, redirect, session
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token
from apps.models.user import User
from apps import db
from apps.auth.utils import generate_token, confirm_token
from apps.utils import send_email
from apps.auth.utils import create_unique_username


auth = Blueprint('auth', __name__, url_prefix='/auth', template_folder='templates')


@auth.route('/sign_up', methods=['POST'])
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
    confirm_url = url_for("auth.confirm_email", token=token, _external=True)
    html = render_template("confirm_email.html", confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(user.email, subject, html)

    return jsonify({"message": "Success"}), 201


@auth.route('/confirm/<token>', methods=['GET'])
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

    # todo: add redirect url of login page
    redirect_url = "#"
    return render_template('verified_email.html', redirect_url=redirect_url)


# Google SSO
@auth.route('/google/login')
def google_login():
    try:
        google_discovery_url = "https://accounts.google.com/.well-known/openid-configuration"
        google_provider_cfg = requests.get(google_discovery_url).json()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = (
            f"{authorization_endpoint}?client_id={current_app.config['GOOGLE_CLIENT_ID']}"
            f"&redirect_uri={url_for('auth.google_callback', _external=True)}"
            f"&scope=openid email profile"
            f"&response_type=code"
        )
        print(request_uri)
        return redirect(request_uri)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
    

@auth.route("/google/callback")
def google_callback():
    if "error" in request.args:
        return f"Error: {request.args['error']}", 400

    code = request.args.get("code")
    google_discovery_url = "https://accounts.google.com/.well-known/openid-configuration"
    google_provider_cfg = requests.get(google_discovery_url).json()
    token_endpoint = google_provider_cfg["token_endpoint"]

    token_response = requests.post(
        token_endpoint,
        data={
            "code": code,
            "client_id": current_app.config["GOOGLE_CLIENT_ID"],
            "client_secret": current_app.config["GOOGLE_CLIENT_SECRET"],
            "redirect_uri": url_for("auth.google_callback", _external=True),
            "grant_type": "authorization_code",
        }
    )
    token_json = token_response.json()
    user_info_endpoint = google_provider_cfg["userinfo_endpoint"]
    user_info_response = requests.get(
        user_info_endpoint,
        headers={"Authorization": f"Bearer {token_json['access_token']}"}
    )
    user_info = user_info_response.json()
    
    user = User.query.filter_by(email=user_info["email"]).first()
    if not user:
        # create a unique username
        username = create_unique_username(user_info.get('given_name'))
        user = User(username=username,
                    email=user_info.get("email"),
                    name=user_info.get("name"),
                    created_at=datetime.now(),
                    is_confirmed=True,
                    confirmed_on = datetime.now(),
                    is_sso_user = True
                    )
        db.session.add(user)
        db.session.commit()



    # user = User.query.filter_by(email)
    # 101548056677760946793
    # 101548056677760946793
     # Create and return JWT token
    jwt_token = create_access_token(user_info['email'])
    return jsonify({"access_token": jwt_token, "user_info": user_info})

    return jsonify(user_info)