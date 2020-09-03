from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, SelectField, DateField, RadioField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from app.models import User


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AddUserForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last_name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[Email(
        'Enter a valid email address')])
    phone = StringField('Phone', validators=[DataRequired(), Length(min=11, max=13)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField(
        'Confirm_Password', validators=[EqualTo('password', 'password doesn\'t match')])
    role = RadioField('Role', validators=DataRequired(), choices=[('Sales', 'Sales'), ('Admin', 'Admin')])
    submit = SubmitField('Create')

    def validate_username(self, username):

        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):

        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')

class DiscountForm(FlaskForm):
    amount_percentage = FloatField(
        'Amount/Percentage', validators=[DataRequired()])
    code_type = SelectField('Code Type', validators=[DataRequired()], choices=[
                            ('Percentage', 'Percentage'), ('Amount', 'Amount')])
    expiry_date = DateField('Expiration Date', validators=(DataRequired()))
    submit = SubmitField('Create Discount')
