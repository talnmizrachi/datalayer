from global_functions.continue_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from models import MockInterviewModel
from platforms_webhooks_catchers.zapier.catch_mock_interviewer_details import get_mock_interviewer_data_from_zapier
import os
from db import db


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
        logger.info(mock_int_dict)
        this_mock_object = MockInterviewModel.query.filter_by(
            process_id=mock_int_dict.get('process_id'),
            stage_in_funnel=mock_int_dict.get('stage_in_funnel'),
            type_of_stage=mock_int_dict.get('type_of_stage')).first()
        logger.info(this_mock_object)
        if this_mock_object is None:
            abort(404, description="Mock interview not found")
            
        this_mock_object.mentor_name = mock_int_dict.get('mentor_name')
        this_mock_object.mentor_email = mock_int_dict.get('mentor_email')
        this_mock_object.mock_interview_datetime = mock_int_dict.get('mock_interview_datetime')
        this_mock_object.additional_details = mock_int_dict.get('additional_details')
        db.session.commit()
        return mock_int_dict, 201



if __name__ == '__main__':
    pass
