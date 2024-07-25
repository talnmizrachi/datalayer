from global_functions.general_functions import write_object_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from platforms_webhooks_catchers.campus.catch_student_application import catch_student_application_from_campus
from platforms_webhooks_catchers.zapier.catch_student_application import catch_student_application_from_zapier
from models import StudentToJobApplication
import os
from db import db
from global_functions.LoggingGenerator import Logger

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('student_applications', __name__, description="How are our students applying?")


@blueprint.route('/student_application_from_smart_matcher')
class MethodTemplate(MethodView):

    def post(self):
        data = request.get_json()
        student_applied_dict = catch_student_application_from_zapier(data, source="Smart Matcher")
        
        information = {"student_id": student_applied_dict['student_id'], "job_id": student_applied_dict['job_id']}
        
        existing_application = StudentToJobApplication.query.filter_by(student_id=information['student_id'],
                                                                       job_id=information['job_id']).first()
        student_application_obj = StudentToJobApplication(**student_applied_dict)
        
        if existing_application is None:
            write_object_to_db(student_application_obj)
        else:
            for key, value in student_applied_dict.items():
                setattr(existing_application, key, value)
            db.session.commit()
            
        return information, 201
