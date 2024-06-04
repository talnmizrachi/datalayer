from flask import Flask, request
import os
from db import db
from flask_smorest import Api
from resources.job_ready_students_onboarding import blueprint as jr_students_blp
from flask_migrate import Migrate


def create_app(db_url=None):
    app = Flask(__name__)
    app.config["API_TITLE"] = "Template for flask API with flask-smorest"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", 'sqlite:///data.db')
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["PROPAGATE_EXCEPTIONS"] = True
    
    db.init_app(app)
    api = Api(app)
    migrate = Migrate(app, db)
    
    api.register_blueprint(jr_students_blp)
    
    return app
    
    
if __name__ == '__main__':
    app = create_app()
    app.run()
