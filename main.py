import os
from flask import Flask, render_template, redirect, url_for, flash
from flask_login import FlaskLoginClient
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_session import Session
from flask_migrate import Migrate
from dotenv import load_dotenv

import datetime


load_dotenv('.env')

from os import environ
from routes import route, db, UserData, bcrypt

app = Flask(__name__, template_folder=os.path.abspath('templates'), static_folder=os.path.abspath('static'))

app.config["SECRET_KEY"] = environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///userdata.db"
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(minutes=1)
# app.config['MAIL_SERVER']
# app.config['MAIL_PORT']
# app.config['MAIL_USE_TLS']
# app.config['MAIL_DEBUG']
# app.config['MAIL_USERNAME']
# app.config['MAIL_PASSWORD']
# app.config['MAIL_DEFAULT_SENDER']
# app.config['MAIL_MAX_EMAILS']
# app.config['MAIL_SUPPRESS_SEND']
# app.config['MAIL_ASCII_ATTACHMENT']
# app.config['SESSION_TYPE'] = 'filesystem'

csrf= CSRFProtect(app)
login_manager = LoginManager() 
migrate =Migrate()
# serializer = Serializer('secret', 30)


# session = Session()

# check if directory exists
# if os.path.exists(UPLOAD_FOLDER.isalpha):
#     app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# else:
#     os.mkdir(UPLOAD_FOLDER)

UPLOAD_FOLDER = environ.get('UPLOAD_FOLDER')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

login_manager.init_app(app)
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db, render_as_batch=True)
# session.init_app(app)

with app.app_context():
    db.create_all() 
    
login_manager.login_view = "route.login"

@login_manager.user_loader  
def load_user(user_id):
    # db.session.get(UserData)
    return UserData.query.get(user_id)


@migrate.configure
def configure_alembic(config):
    return config

# @app.route('/set/')
# def set():
#     session['key'] = 'value'
#     return 'ok'

# @app.route('/get/')
# def get():
#     return session.get('key', 'not set')

app.register_blueprint(route)


if __name__ == "__main__":
    app.run(debug=True)