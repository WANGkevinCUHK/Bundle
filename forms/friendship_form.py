from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email
from models.user import User

class AddFriendForm(FlaskForm):
    friend_email = StringField('Friend Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Friend')

    def validate_friend_email(self, friend_email):
        friend = User.query.filter_by(email=friend_email.data).first()
        if friend is None:
            raise ValidationError('User with this email does not exist.')