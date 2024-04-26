from flask import Blueprint, render_template
user_bp = Blueprint("event", __name__, url_prefix="/")
from .forms import RegisterForm

# from flask import render_template, redirect, url_for, flash
# from bp import bp
# from forms.user_form import RegistrationForm, LoginForm, UpdateProfileForm
# from models.user import User
# from werkzeug.security import generate_password_hash, check_password_hash
# from flask_login import login_user, logout_user, login_required, current_user

@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        form = RegisterForm(request.form)
        if form.validate():
            return "success"
        else:
            print(form.errors)
            return "fall"

    # form = RegistrationForm()
    # if form.validate_on_submit():
    #     hashed_password = generate_password_hash(form.password.data)
    #     user = User(email=form.email.data, password=hashed_password, name=form.name.data, avatar=form.avatar.data)
    #     user.save()
    #     flash('Registration successful. Please log in.', 'success')
    #     return redirect(url_for('login'))
@controllers.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Login successful.', 'success')
            return redirect(url_for('event_list'))
        else:
            flash('Login unsuccessful. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

@controllers.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'success')
    return redirect(url_for('register'))

@controllers.route('/users/<int:id>', methods=['GET', 'PUT'])
@login_required
def user_profile(id):
    user = User.query.get_or_404(id)
    if request.method == 'PUT':
        form = UpdateProfileForm()
        if form.validate_on_submit():
            user.name = form.name.data
            user.avatar = form.avatar.data
            user.save()
            flash('Profile updated successfully.', 'success')
            return redirect(url_for('user_profile', id=user.id))
    return render_template('profile.html', user=user)