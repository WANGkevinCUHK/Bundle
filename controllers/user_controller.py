from flask import Blueprint, request, jsonify
from models.user import User
from utils.auth import generate_token, auth_required
import bcrypt

user_bp = Blueprint('user', __name__, url_prefix='/user')


@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')

    if User.objects(email=email).first():
        return jsonify({"message": "Email already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = User(email=email, password=hashed_password.decode('utf-8'), name=name)
    user.save()

    token = generate_token(user.email)
    return jsonify({"token": token}), 201


@user_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.objects(email=email).first()
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
        return jsonify({"message": "Invalid email or password"}), 401

    token = generate_token(user.email)
    return jsonify({"token": token}), 200


@user_bp.route('/', methods=['PUT'])
@auth_required
def update_profile(current_user):
    data = request.get_json()
    name = data.get('name')

    current_user.name = name
    current_user.save()

    return jsonify(current_user.to_json()), 200