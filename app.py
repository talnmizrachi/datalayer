from flask import Flask
import os
from db import db
from flask_smorest import Api
from resources.general.dummwebhook import dummy_blueprint as dummy_webhook_blp
from resources.students.job_ready_students_onboarding import blueprint as jr_students_blp
from resources.v3.processes_endpoints import blueprint as new_process_init_blp
from resources.v3.mock_interviews import blueprint as mock_interview_details_blp
from resources.student_applications import blueprint as student_applications_blp
from resources.students.job_ready_students_deals import blueprint as job_ready_students_deals_blp
from resources.students.job_ready_students_owners import blueprint as student_owners_change_blp
from resources.students.job_ready_students_school_masters import blueprint as students_school_masters_blp
from resources.students.job_ready_cohorts_changes import blueprint as cohorts_changes_blp
from resources.v3.first_payment_logging import blueprint as first_payment_logging_blp
from resources.BG.onboarding_student import blueprint as bg_students_blp
from resources.BG.change_in_attribute import blueprint as bg_students_change_in_attribute
from resources.BG.student_got_a_job_update import blueprint as student_got_a_job_update_blp
from resources.v3.updateing_tuition_after_discount import blueprint as updating_tuition_after_discount_blp
from resources.students.student_deal_stage_corrected import blueprint as student_deal_stage_corrected_blp
from resources.BG.student_csat_temp import blueprint as bg_students_ms_score
from resources.students.students_passing_interviews import blueprint as students_passing_interviews_blp
from resources.students.jr_students_getting_interviews import blueprint as jr_students_getting_interviews_blp
from flask_migrate import Migrate
from dotenv import load_dotenv
from global_functions.LoggingGenerator import Logger

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()



def create_app(db_url=None):
    is_local = os.getenv("FLASK_ENV") == "development"
    
    if not is_local:
        import sentry_sdk
    
        sentry_sdk.init(
            dsn="https://8578be764d8d0797ae52d1874117aee8@o4507679066292224.ingest.de.sentry.io/4507689973645392",
            # Set traces_sample_rate to 1.0 to capture 100%
            # of transactions for performance monitoring.
            traces_sample_rate=1.0,
            # Set profiles_sample_rate to 1.0 to profile 100%
            # of sampled transactions.
            # We recommend adjusting this value in production.
            profiles_sample_rate=1.0,
        )
    
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
    api.register_blueprint(mock_interview_details_blp)
    api.register_blueprint(student_applications_blp)
    api.register_blueprint(job_ready_students_deals_blp)
    api.register_blueprint(student_owners_change_blp)
    api.register_blueprint(students_school_masters_blp)
    api.register_blueprint(cohorts_changes_blp)
    api.register_blueprint(first_payment_logging_blp)
    api.register_blueprint(bg_students_blp)
    api.register_blueprint(bg_students_change_in_attribute)
    api.register_blueprint(student_got_a_job_update_blp)
    api.register_blueprint(updating_tuition_after_discount_blp)
    api.register_blueprint(bg_students_ms_score)
    api.register_blueprint(student_deal_stage_corrected_blp)
    api.register_blueprint(jr_students_getting_interviews_blp)
    api.register_blueprint(students_passing_interviews_blp)
    api.register_blueprint(dummy_webhook_blp)
    
    return app
    
    
if __name__ == '__main__':
    app = create_app()
    app.run()
