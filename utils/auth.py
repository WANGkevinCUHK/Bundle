import jwt
from flask import request, jsonify
from models.user import User
from functools import wraps
from config import Config

def generate_token(email):
    token = jwt.encode({"email": email}, Config.SECRET_KEY, algorithm="HS256")
    return token

def auth_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        if not token:
            return jsonify({"message": "Token is missing"}), 401
        try:
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.objects(email=data['email']).first()
        except:
            return jsonify({"message": "Token is invalid"}), 401
        return f(current_user, *args, **kwargs)
    return decorated