from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

sql_db = SQLAlchemy()

def create_app():
    
    app = Flask(__name__, instance_relative_config=True)

    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-change-me')
    
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'database.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


    sql_db.init_app(app)

    with app.app_context():

        from . import routes
        app.register_blueprint(routes.main_blueprint)
        
        sql_db.create_all()

    return app