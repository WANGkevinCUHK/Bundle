from flask import request, render_template, redirect, url_for, session
from ..models.user import User
from ..models.friendship import Friendship
from ..utils.forms import AddFriendForm
from . import friend_bp, db

@friend_bp.route('/', methods=['GET'])
def get_friends():
    user_id = session['user_id']
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    friendships = Friendship.query.filter((Friendship.user_id == user_id) | (Friendship.friend_id == user_id)).paginate(page, per_page, error_out=False)
    friends = []
    for friendship in friendships.items:
        if friendship.user_id == user_id:
            friends.append(User.query.get(friendship.friend_id))
        else:
            friends.append(User.query.get(friendship.user_id))
    return render_template('friend_list.html', friends=friends, friendships=friendships)

@friend_bp.route('/', methods=['POST'])
def add_friend():
    form = AddFriendForm()
    if form.validate_on_submit():
        friend_email = form.email.data
        friend = User.query.filter_by(email=friend_email).first()
        if friend:
            user_id = session['user_id']
            friendship = Friendship(user_id=user_id, friend_id=friend.id)
            db.session.add(friendship)
            db.session.commit()
            return redirect(url_for('friend.get_friends'))
    return render_template('add_friend.html', form=form)