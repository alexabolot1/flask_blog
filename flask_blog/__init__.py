from flask_bcrypt import Bcrypt
from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

from flask_blog.config import Config

db = SQLAlchemy()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    login_manager.init_app(app)
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from flask_blog.main.views import main
    from flask_blog.users.views import users
    from flask_blog.posts.views import posts
    from flask_blog.errors.handlers import errors
    app.register_blueprint(errors)
    app.register_blueprint(main)
    app.register_blueprint(users)
    app.register_blueprint(posts)

    return app
