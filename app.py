from flask import Flask
import os
from db import db
from flask_smorest import Api
from resources.students.job_ready_students_onboarding import blueprint as jr_students_blp
from resources.v3.processes_endpoints import blueprint as new_process_init_blp
from resources.v3.mock_interviews import blueprint as mock_interview_details_blp
from resources.student_applications import blueprint as student_applications_blp
from resources.students.job_ready_students_deals import blueprint as job_ready_students_deals_blp
from resources.students.job_ready_students_owners import blueprint as student_owners_change_blp
from resources.students.job_ready_students_school_masters import blueprint as students_school_masters_blp
from resources.students.job_ready_cohorts_changes import blueprint as cohorts_changes_blp
from flask_migrate import Migrate
from dotenv import load_dotenv
from global_functions.LoggingGenerator import Logger

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


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
    with app.app_context():
        db.create_all()
    migrate = Migrate(app, db)
    
    api.register_blueprint(jr_students_blp)
    api.register_blueprint(new_process_init_blp)
    api.register_blueprint(continue_process_blp)
    api.register_blueprint(mock_interview_details_blp)
    api.register_blueprint(student_applications_blp)
    api.register_blueprint(job_ready_students_deals_blp)
    api.register_blueprint(student_owners_change_blp)
    api.register_blueprint(students_school_masters_blp)
    api.register_blueprint(cohorts_changes_blp)
    
    return app
    
    
if __name__ == '__main__':
    app = create_app()
    app.run()
