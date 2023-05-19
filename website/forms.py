from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FileField, Phone
from wtforms.validators import DataRequired, Email, Length, ValidationError
from website.models import User
from wtforms import ValidationError 
from wtforms import phonenumbers

class RegistrationForm(FlaskForm):
    familyname = StringField('familyname', validators=[DataRequired(), Length(min=3, max=20)])
    firstname = StringField('firstname', validators=[DataRequired(), Length(min=3, max=20)])
    adress = StringField('adress', validators=[DataRequired(), Length(min=3, max=20)])
    phone = StringField('phone', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password1 = PasswordField('Password1', validators=[DataRequired()])
    
    submit = SubmitField('Register')

    def validate_familyname(self, familyname):
        familyname = familyname.query.filter_by(familyname=familyname.data).first()
        if familyname:
            raise ValidationError('That familyname is already taken. Please choose a different one.')
    def validate_firstname(self, firstname):
        firstname = firstname.query.filter_by(firstname=firstname.data).first()
        if firstname:
            raise ValidationError('That firstname is already taken. Please choose a different one.')


    def validate_email(self, email):
        familyname = familyname.query.filter_by(email=email.data).first()
        if familyname:
            raise ValidationError('That email is already taken. Please choose a different one.')
    def validate_phone(self, phone):
        if len(phone.data) > 10:
            raise ValidationError('Invalid phone number.')
        try:
            input_number = phonenumbers.parse(phone.data)
            if not (phonenumbers.is_valid_number(input_number)):
                raise ValidationError('Invalid phone number.')
        except:
            input_number = phonenumbers.parse("+1"+phone.data)
            if not (phonenumbers.is_valid_number(input_number)):   
                raise ValidationError('Invalid phone number.')
                
class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    password1 = PasswordField('password1', validators=[DataRequired()])
    submit = SubmitField('Login')

class UploadForm(FlaskForm):
    document = FileField('Select a document', validators=[DataRequired()])
    submit = SubmitField('Upload')

class VerifyForm(FlaskForm):
    document = FileField('Select a document', validators=[DataRequired()])
    submit = SubmitField('Verify')
