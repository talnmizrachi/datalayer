from global_functions.continue_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from models import MockInterviewModel
from platforms_webhooks_catchers.zapier.catch_mock_interviewer_details import get_mock_interviewer_data_from_zapier
import os


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('mock_interview_details', __name__, description="A new stage in a job process")


@blueprint.route('/mock_interview_setting', methods=['POST'])
class MockInterviewSetting(MethodView):
    """
    A mock interview is created in one of two options:
    1. Automatic - A process is being initiated/continued -> A stage is being initiated -> a mock is being created
    1.a. Automatic - A mock interview line will be created automatically with every new stage created
    2. Manual - When the relevant POC decides that an additional mock is required.
    1.b. Manual - TBD
    """

    def post(self):
        data = request.get_json()
        logger.info(data)
        mock_int_dict = get_mock_interviewer_data_from_zapier(data)
        MockInterviewModel.query.filter_by(process_id=mock_int_dict.get('process_id')  )
        return mock_int_dict, 201


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
