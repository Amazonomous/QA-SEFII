from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, Regexp, Email, EqualTo, ValidationError
from markupsafe import Markup

class SignUpForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(min=4)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    password_confirmation = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

class DeviceForm(FlaskForm):
    device_dsn = StringField('Device Serial Number (found on bottom of device)', validators=[
        DataRequired(),
        Length(max=16),
        Regexp(r'^[A-Z0-9]{16}$', message='Must be 16 alphanumeric characters in uppercase')
    ],
    render_kw={'placeholder': 'Enter 16 alphanumeric letters'})

    device_location_code = SelectField('Device Building Number', choices=[
        ('', 'Select Building Number'),
        ('SEA20', 'SEA20'),
        ('SEA22', 'SEA22'),
        ('LHR16', 'LHR16'),
        ('LHR14', 'LHR14'),
        ('LHR10', 'LHR10'),
        ('SEA30', 'SEA30')
    ], validators=[DataRequired()])

    device_condition = SelectField('Device Condition', choices=[
        ('', 'Select Device Condition'),
        ('Healthy', 'Healthy'),
        ('Isolated', 'Isolated'),
        ('Unknown', 'Unknown')
    ], validators=[DataRequired()])

    device_program = SelectField('Device Program (cannot update once added!)', choices=[
        ('', 'Select Device Program'),
        ('Echo Spot', 'Echo Spot'),
        ('Echo Dot', 'Echo Dot'),
        ('Echo Show 5', 'Echo Show 5'),
        ('Echo Show 10', 'Echo Show 10')
    ], validators=[DataRequired()])

    add_button = SubmitField('Add Device')
    update_button = SubmitField('Update Device')