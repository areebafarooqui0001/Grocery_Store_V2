from flask import request, current_app as app
import jwt
from flask_restful import abort
from functools import wraps
from datetime import datetime, timedelta

def get_token(user_id, user_role):
    payload = {
        'user_id': user_id,
        'roles': user_role,
        'exp': datetime.utcnow() + timedelta(hours=6)
    }
    token = jwt.encode(payload, app.config['SECRET_KEY'])
    return token
     

def role_required(allowed_roles):
    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = request.headers.get('Authentication-Token')
            # print(token)
            if not token:
                abort(401, message='Token is not passed')
            try:
                data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
                
                roles = data.get('roles', [])  
                roles_set = set(roles)
                if not roles_set.intersection(set(allowed_roles)):
                    abort(403, message='Access denied')
            except (jwt.ExpiredSignatureError, jwt.DecodeError):
                abort(401, message='Token is invalid')
            return f(*args, **kwargs)
        return decorated
    return decorator

def get_curr_user_id(token):
    token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    return token_data.get('user_id')

def get_curr_user_role(token):
    token_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
    return token_data.get('roles')[0]