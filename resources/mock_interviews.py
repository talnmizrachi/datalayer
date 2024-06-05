from global_functions.continue_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from models import MockInterviewModel
import os


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('mock_interview_details', __name__, description="A new stage in a job process")


@blueprint.route('/mock_interview_setting', methods=['POST'])
class MockInterviewSetting(MethodView):
    """
    Right now we have 2 options - from continuing a process or starting a new process.
    (+ask RnD to make sure that the calendly UTMs are the same)
    New process UTMS:
    utm_source=student_full_name&utm_medium=company_name&utm_content=stage_of_interview
    Continue process UTMS:
    utm_source=process_id&utm_medium=type_of_stage&utm_content=stage_of_interview
    """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_stage_dict = parse_and_write_to_db_new_stage_in_process(data, source='direct')
        return new_stage_dict['id'], 201


@blueprint.route('/continue_process_typeform', methods=['POST'])
class ContinueProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_stage_in_process(data, source='typeform')
        
        return new_process_dict['id'], 201


if __name__ == '__main__':
    pass
