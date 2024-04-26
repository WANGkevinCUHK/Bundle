from flask import Blueprint, request, jsonify
from models.friendship import Friendship
from models.user import User
from utils.auth import auth_required
from bson import ObjectId

friendship_bp = Blueprint('friendship', __name__, url_prefix='/friendship')


@friendship_bp.route('/request/<user_id>', methods=['POST'])
@auth_required
def send_request(current_user, user_id):
    user = User.objects(id=ObjectId(user_id)).first()
    if not user:
        return jsonify({"message": "User not found"}), 404

    if current_user == user:
        return jsonify({"message": "You can't add yourself as a friend"}), 400

    if Friendship.objects(user1=current_user, user2=user).first() or Friendship.objects(user1=user,
                                                                                        user2=current_user).first():
        return jsonify({"message": "Friendship already exists or pending"}), 400

    friendship = Friendship(user1=current_user, user2=user)
    friendship.save()

    return jsonify({"message": "Friendship request sent"}), 201


@friendship_bp.route('/accept/<friendship_id>', methods=['POST'])
@auth_required
def accept_request(current_user, friendship_id):
    friendship = Friendship.objects(id=ObjectId(friendship_id)).first()
    if not friendship:
        return jsonify({"message": "Friendship not found"}), 404

    if friendship.user2 != current_user:
        return jsonify({"message": "You are not authorized to accept this request"}), 403

    friendship.status = 'accepted'
    friendship.save()

    current_user.friends.append(friendship.user1)
    current_user.save()

    friendship.user1.friends.append(current_user)
    friendship.user1.save()

    return jsonify({"message": "Friendship request accepted"}), 200


@friendship_bp.route('/', methods=['GET'])
@auth_required
def get_friends(current_user):
    friends = current_user.friends
    return jsonify([friend.to_json() for friend in friends]), 200