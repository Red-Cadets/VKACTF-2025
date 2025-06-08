from flask import Blueprint, render_template, request, redirect, url_for, make_response
from .models import User
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import timedelta, datetime
from config.config import Config
import re

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        name = request.form['name']
        login = request.form['login']
        password = request.form['password']

        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[\W_]).{8,}$'
        if not re.match(pattern, password):
            return "Password must be at least 8 characters long and include uppercase, lowercase, number, and special character."

        exists = User.query.filter_by(login=login).first()
        if exists:
           return "User with this login already exists"

        new_user = User(name=name, login=login, password_hash=generate_password_hash(password))

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('auth.login'))
    
    return render_template('register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        login = request.form['login']
        password = request.form['password']

        user = User.query.filter_by(login=login).first()    
        if user and check_password_hash(user.password_hash, password):

            payload = {
                'user_id': user.id,
                'exp': datetime.utcnow() + Config.JWT_EXPIRATION_DELTA
            }


            token = jwt.encode(payload, Config.SECRET_KEY, algorithm='HS256')
            response = make_response(redirect(url_for('routes.vote')))
            response.set_cookie('session_id', token, max_age=86400, httponly=True, samesite='Lax')
                                    
            return response
        
        return "Invalid login or password"
        

    return render_template('login.html')


@auth_bp.route('/logout')
def logout():
    response = make_response(redirect(url_for('auth.login')))
    response.set_cookie("session_id", '', expires=0)
    return response

    


def init_auth(app):
    app.register_blueprint(auth_bp)