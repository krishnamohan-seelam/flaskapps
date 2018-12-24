import flask
from . import app
from .forms import UserForm

@app.route('/')
def index():
    user = {'username': 'Geetha'}
    posts = [
        {
            'author': {'username': 'Krishna'},
            'body': 'Beautiful day in Hyderabad!'
        },
        {
            'author': {'username': 'Swathi'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return flask.render_template('index.html',user =user,title='Home',posts=posts),200

@app.route('/login',methods =['GET','POST'])
def login():
    userform = UserForm(flask.request.form)
    return flask.render_template('login.html',form =userform)