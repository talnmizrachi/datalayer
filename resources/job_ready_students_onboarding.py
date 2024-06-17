from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from global_functions.job_ready_students_functions import payload_to_job_ready_student_dict
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import os
from models import JobReadyStudentModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Onboard a student', __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/onboard_student', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):

        data = request.get_json()
        if data.get('email__deal_', "test").lower().find("test") == -1:
            abort(404, message='no email found')
            
        logger.info(f"Onboarding new student:\t{data}")

        job_ready_student_dict = payload_to_job_ready_student_dict(data)
        job_ready_student_object = JobReadyStudentModel(**job_ready_student_dict)
        
        write_object_to_db(job_ready_student_object)
        
        return job_ready_student_dict['id'], 201


@blueprint.route('/onboard_students', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):
        data = request.get_json()
        student_ids = []
        for student in data:
            job_ready_student_dict = payload_to_job_ready_student_dict(student)
            job_ready_student_object = JobReadyStudentModel(**job_ready_student_dict)
            student_ids.append(job_ready_student_object.id)
            
            write_object_to_db(job_ready_student_object)
        
        return {"ids": student_ids}, 201


@blueprint.route('/auto_onboard_student_from_hubspot', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):
        data = request.get_json()
        student_ids = []
        for student in data:
            job_ready_student_dict = payload_to_job_ready_student_dict(student)
            job_ready_student_object = JobReadyStudentModel(**job_ready_student_dict)
            student_ids.append(job_ready_student_object.id)
            
            write_object_to_db(job_ready_student_object)
        
        return {"ids": student_ids}, 201