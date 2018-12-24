from flask_wtf import FlaskForm
from wtforms.validators import DataRequired
from wtforms import StringField, PasswordField,SubmitField

class UserForm(FlaskForm):
    username = StringField('What is your name?', validators=[DataRequired()])
    password=PasswordField('Password Please',validators=[DataRequired()])
    login = SubmitField('login')