from global_functions.LoggingGenerator import Logger
from global_functions.job_ready_students_functions import onboard_function
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Onboard a student', __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/onboard_student', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):

        data = request.get_json()
        job_ready_student_dict = onboard_function(data)
        return job_ready_student_dict['id'], 201


@blueprint.route('/onboard_students', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):
        data = request.get_json()
        student_ids = []
        for student in data:
            job_ready_student_dict = onboard_function(student)
            student_ids.append(job_ready_student_dict['id'])
            
        return {"ids": student_ids}, 201


@blueprint.route('/auto_onboard_student_from_hubspot', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):
        data = request.get_json()
        student_ids = []
        for student in data:
            job_ready_student_dict = onboard_function(student)
            student_ids.append(job_ready_student_dict['id'])
            
        return {"ids": student_ids}, 201