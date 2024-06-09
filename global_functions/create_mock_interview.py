from uuid import uuid4
import os
from global_functions.LoggingGenerator import Logger

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

def create_mock_interview_line_for_stage(process_dict, stage_dict):
    mock_interview_dict = {
            'id': str(uuid4().hex),
            "process_id": process_dict['id'],
            "stage_id": stage_dict['id']}
    
    return mock_interview_dict


def create_mock_interview_line_for_stage_continue(stage_dict):
  
    mock_interview_dict = {
            'id': str(uuid4().hex),
            "process_id": stage_dict.get('process_id'),
            "stage_date": stage_dict.get('stage_date'),
            "stage_id": stage_dict.get('id'),
            "stage_in_funnel": stage_dict.get('stage_in_funnel'),
            "type_of_stage": stage_dict.get('type_of_stage'),
            "had_home_assignment": stage_dict.get('had_home_assignment'),
            "home_assignment_questions": stage_dict.get('home_assignment_questions'),
            "home_assignment_answers": stage_dict.get('home_assignment_answers'),
    }
    
    return mock_interview_dict

