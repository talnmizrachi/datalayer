from global_functions.continue_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from models import MockInterviewModel, ProcessModel
from platforms_webhooks_catchers.zapier.catch_mock_interviewer_details import get_mock_interviewer_data_from_zapier
import os
from db import db

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('mock_interview_details', __name__, description="A new stage in a job process")


# todo - Add cancellation option

@blueprint.route('/mock_interview_setting_new', methods=['POST'])
class MockInterviewSetting(MethodView):
    """
    A mock interview is created in one of two options:
    1. Automatic - A process is being initiated/continued -> A stage is being initiated -> a mock is being created
    1.a. Automatic - A mock interview line will be created automatically with every new stage created
    2. Manual - When the relevant POC decides that an additional mock is required.
    1.b. Manual - TBD
    
    This is for the new V3 settings
    """
    
    def post(self):
        data = request.get_json()
        logger.info(data)
        mock_int_dict = get_mock_interviewer_data_from_zapier(data)
        logger.info(mock_int_dict)

        if data.get('is_new_process') not in ("new_process", "continue_process"):
            abort(400, message="is_new_process must be 'new_process' or 'continue_process'")

        if data.get('is_new_process') == "new_process":
            this_mock_object = add_mock_interview_details_for_new_processes(mock_int_dict)
        else:
            #only for continue process
            # data.get('is_new_process') == "continue_process"
            ...

        db.session.commit()
        
        return mock_int_dict, 201


def add_mock_interview_details_for_new_processes(_mock_int_dict):
    # identify the process_id and stage_in_funnel
    active_process_id = ProcessModel.query.filter_by(company_name=_mock_int_dict.get('company_name'),
                                                     email_address=_mock_int_dict.get('student_email'),
                                                     job_title=_mock_int_dict.get('job_title')).first().id
    
    active_stage = StageModel.query.filter_by(process_id=active_process_id,
                                              is_pass="PENDING").first()
    
    # take data from teh stage active stage
    active_stage_id = active_stage.id
    active_stage_funnel_location = active_stage.stage_in_funnel
    active_stage_type = active_stage.type_of_stage
    active_stage_date = active_stage.stage_date
    active_stage_had_home_assignment = active_stage.had_home_assignment
    
    # Find the Mock interview
    
    this_mock_object = MockInterviewModel.query.filter(
        MockInterviewModel.process_id == active_process_id,
        MockInterviewModel.stage_id == active_stage_id,
        MockInterviewModel.mentor_email.is_(None)
    ).first()
    logger.info(this_mock_object)
    
    if this_mock_object is None:
        abort(404, description="Mock interview not found")
    
    this_mock_object.mentor_name = _mock_int_dict.get('mentor_name')
    this_mock_object.mentor_email = _mock_int_dict.get('mentor_email')
    this_mock_object.mock_interview_datetime = _mock_int_dict.get('mock_interview_datetime')
    this_mock_object.additional_details = _mock_int_dict.get('additional_details')
    this_mock_object.stage_in_funnel = active_stage_funnel_location
    this_mock_object.type_of_stage = active_stage_type
    this_mock_object.stage_date = active_stage_date
    this_mock_object.had_home_assignment = active_stage_had_home_assignment
    
    return this_mock_object


def add_mock_interview_details_for_existing_processes(_mock_int_dict):
    # Identify the stage and mock interview row
    
    active_mock = MockInterviewModel.query.filter(MockInterviewModel.process_id == _mock_int_dict.get('process_id'),
                                                  MockInterviewModel.stage_in_funnel == _mock_int_dict.get(
                                                      'stage_in_funnel'),
                                                  MockInterviewModel.type_of_stage == _mock_int_dict.get(
                                                      'type_of_stage'),
                                                  MockInterviewModel.mentor_email.is_(None)
                                                  ).first()
    
    active_mock.mentor_name = _mock_int_dict.get('mentor_name')
    active_mock.mentor_email = _mock_int_dict.get('mentor_email')
    active_mock.mock_interview_datetime = _mock_int_dict.get('mock_interview_datetime')
    active_mock.additional_details = _mock_int_dict.get('additional_details')
    
    return active_mock


if __name__ == '__main__':
    pass
