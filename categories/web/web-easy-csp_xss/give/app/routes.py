import os
from flask import render_template, Blueprint, request, redirect, url_for, make_response, flash
from functools import wraps
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from config.config import Config
from .models import Pool
from . import db
import random
import redis

port = int(os.environ.get("REDIS_PORT"))

redis_client = redis.Redis(
                    host='web-m-hawk-redis', 
                    port=port, 
                    db=0, 
                    decode_responses=True
                )

queue_key = os.environ.get("REDIS_QUEUE_KEY")  

routes_bp = Blueprint('routes', __name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('session_id')
        if not token:
            return redirect(url_for('auth.login'))

        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=['HS256'])
            request.current_user_id = payload['user_id']

        except InvalidTokenError:
            response = make_response(redirect(url_for('auth.login')))
            response.set_cookie('session_id', '', expires=0)
            return response
        
        except ExpiredSignatureError:
            response = make_response(redirect(url_for('auth.login')))
            response.set_cookie('session_id', '', expires=0)
            return response

        return f(*args, **kwargs)
    return decorated_function



@routes_bp.route('/', methods=["GET"])
def index():
    return render_template('index.html')


@routes_bp.route('/vote', methods=["GET", "POST"])
@login_required
def vote():

    if request.method == 'GET':
        active_pools = Pool.query.filter_by(is_active=True).all()
        user_id = request.current_user_id
        return render_template('vote.html', user_id=user_id, pools=active_pools)

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        options = request.form.getlist('options[]')

        if len(title) > 100:
            return "Too long title"


        options_json = {
            "options": [
                {"id": idx + 1, "text": option}
                for idx, option in enumerate(options)
            ]
        }

        new_pool = Pool(
            title=title,
            description=description,
            options_json=options_json,
            creator_id=request.current_user_id,
            is_active=True
        )

        try:
            db.session.add(new_pool)
            db.session.commit()

            redis_client.lpush(queue_key, str(new_pool.uuid))
        except Exception as e:
            db.session.rollback()
            flash('Error for create vote', 'error')

        return redirect(url_for('routes.vote'))


@routes_bp.route('/vote/<string:pool_uuid>', methods=["GET"])
def vote_detail(pool_uuid):
    pool = Pool.query.get_or_404(pool_uuid)

    points = sorted([random.randint(0, 100) for _ in range(2)])
    points = [0] + points + [100]
    progress_values = [points[i+1] - points[i] for i in range(3)]
    progress_values = [round(value / 5) * 5 for value in progress_values]
    
    return render_template('vote_detail.html', pool=pool, progress_values=progress_values)


@routes_bp.app_context_processor
def inject_user():
    token = request.cookies.get('session_id')
    user_id = None
    if token:
        try:
            payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            user_id = payload['user_id']
        except (InvalidTokenError, ExpiredSignatureError):
            pass
    return dict(current_user_id=user_id)



def page_not_found(error):
    path = request.path
    return f"{path} not found"

def init_routes(app):
    app.register_blueprint(routes_bp)
    app.errorhandler(404)(page_not_found)

@routes_bp.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] = "script-src 'self'; style-src 'self' https://fonts.googleapis.com https://unpkg.com 'unsafe-inline'; font-src https://fonts.gstatic.com;"
    return resp