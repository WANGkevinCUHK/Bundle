from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo

# ...

class AddFriendForm(FlaskForm):
    email = StringField('Friend Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Add Friend')
class EventForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    submit = SubmitField('Create Event')