import os

from flask import Flask

from os import path
from flask_login import LoginManager

from .extensions import db
from .models import User

def create_app():
    app = Flask(__name__)
     
    app.config['SECRET_KEY'] = 'hjshjhdjah kjshkjdhjs'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")

    from .views import views
    from .auth import auth

    db.init_app(app)

    app.register_blueprint(views)
    app.register_blueprint(auth)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app