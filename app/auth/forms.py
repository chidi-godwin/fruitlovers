from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField,ValidationError
from wtforms.validators import DataRequired, Email, Length, EqualTo
from app.models import User


class RegisterForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(
        'Enter a valid email address')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=13)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm_Password', validators=[EqualTo('password', 'password doesn\'t match')])
    submit = SubmitField('submit')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('submit')