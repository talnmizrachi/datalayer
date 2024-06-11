from flask import Flask
import os
from db import db
from flask_smorest import Api
from resources.job_ready_students_onboarding import blueprint as jr_students_blp
from resources.processes_endpoints import blueprint as new_process_init_blp
from resources.continue_process import blueprint as continue_process_blp
from resources.mock_interviews import blueprint as mock_interview_details_blp
from resources.adding_mentors import blueprint as add_mentors_blp
from flask_migrate import Migrate
from dotenv import load_dotenv


def create_app(db_url=None):
    app = Flask(__name__)
    load_dotenv()
    app.config["API_TITLE"] = "Datalayer endpoints V3"
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
    api.register_blueprint(new_process_init_blp)
    api.register_blueprint(continue_process_blp)
    api.register_blueprint(add_mentors_blp)
    api.register_blueprint(mock_interview_details_blp)
    
    return app
    
    
if __name__ == '__main__':
    print(os.getenv("DATABASE_URL"))
    app = create_app()
    app.run()
