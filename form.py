from wtforms import FileField, StringField, PasswordField, TextAreaField, EmailField, SubmitField, RadioField
from wtforms.validators import DataRequired, Length, InputRequired, Email, ValidationError
from flask_wtf import FlaskForm
from model import UserData

class LoginForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()], name='email')
    password = PasswordField("Password", validators=[DataRequired(), Length(4, 22)], name="pass")
    login = SubmitField("Login")
    

class SignUpForm(FlaskForm):
    username = StringField('Username', name='username')
    email = EmailField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(4, 22)], name='pass')
    repassword = PasswordField("Re-type Passowrd", validators=[DataRequired(), Length(4, 22)])
    signup = SubmitField("Sign Up")


    def validate_email(email):

        existing_email = UserData.query.filter_by(email= email.data).first()

        if existing_email:
            raise ValidationError("Account with this Email already Exist!!")
        
class BlogDataForm(FlaskForm):
    title = StringField('Title', name='title', validators=[DataRequired(), Length(4, 22)])
    content = TextAreaField('Content', name='content', validators=[DataRequired(), Length(10, 255)])
    blog_thumbnail = FileField('Blog Thumbnail')
    create = SubmitField('Create')
    category = RadioField('Choose a category:', validators=[InputRequired(message=None)],
                          choices=[ ('Backend', 'Backend'), ('Frontend', 'Frontend'),
('Blockchain', 'Blockchain'), ('Cybersecurity', 'Cybersecurity')] )


class UserForm(FlaskForm):
    username = StringField('Change Username')
    bio = TextAreaField('Change Bio')
    profile_pic = FileField('Profile Pic')


class RequestResetForm(FlaskForm):
    email = EmailField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')


    def validate_email(self, email):
        user= UserData.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError('There is no account with that email. You must register first.')
        


class ResetPasswordForm(FlaskForm):
    password = PasswordField("Password", validators=[DataRequired(), Length(4, 22)], name='pass')
    repassword = PasswordField("Re-type Passowrd", validators=[DataRequired(), Length(4, 22)])
    submit = SubmitField("Reset Password")
    