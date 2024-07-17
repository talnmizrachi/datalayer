from uuid import uuid4
from datetime import date, datetime
from models import ProcessModel, StageModel, MockInterviewModel, JobReadyStudentModel
from global_functions.general_functions import *
from global_functions.create_mock_interview import create_mock_interview_line_for_stage
from global_functions.LoggingGenerator import Logger
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def next_stager(this_stage):
    stages = [
            "1st Stage", "2nd Stage", "3rd Stage", "4th Stage",
            "5th Stage", "6th Stage", "7th Stage", "8th Stage", "9th Stage",
            "10th Stage", "11th Stage", "12th Stage", ]
    try:
        return stages[stages.index(this_stage) + 1]
    except ValueError:
        return f"{this_stage} + 1"


def parse_payload_and_write_to_db(payload, process_id):
    last_active_stage = StageModel.query.filter_by(process_id=process_id, is_pass="PENDING").first()
    last_active_stage.is_pass = "TRUE"
    last_active_stage.updated_at = datetime.now()
    
    next_stage = next_stager(last_active_stage.stage_in_funnel)

    stage_dict = {"process_id": process_id, "stage_in_funnel": next_stage,
                 "type_of_stage": payload.get("next_recruiting_step_type"),
                 "stage_date": payload.get("stage_date"), 'id': str(uuid4().hex)}
    
    mock_interview_dict = {
            'id': str(uuid4().hex),
            "process_id": process_id,
            "stage_id": stage_dict['id']}
    
    
    new_stage_object = StageModel(**stage_dict)
    new_mock_obj = MockInterviewModel(**mock_interview_dict)
    
    write_object_to_db(new_stage_object)
    write_object_to_db(new_mock_obj)
    