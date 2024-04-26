import wtforms
from models.user import User
from wtforms.validators import Email, EqualTo, Length
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message="wrong email!")])
    username = wtforms.StringField(validators=[Length(min=4,max=10,message="wrong username")])
    password = wtforms.StringField( validators=[Length(min=6,max=8,message="wrong password")])
    password_confirm = wtforms.StringField( validators=[EqualTo("password")])

    def validate_email(self, field):
        email = field.data
        user = User.query.filter_by(email = email).first()
        if user:
            raise wtforms.ValidationError(message="email taken")