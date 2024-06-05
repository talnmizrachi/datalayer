from uuid import uuid4


def create_mock_interview_line_for_stage(process_dict, stage_dict):
    mock_interview_dict = {
            'id': str(uuid4().hex),
            "process_id": process_dict['id'],
            "stage_id": stage_dict['id']}
    
    return mock_interview_dict


def create_mock_interview_line_for_stage_continue(stage_dict):
    mock_interview_dict = {
            'id': str(uuid4().hex),
            "process_id": stage_dict['process_id'],
            "stage_id": stage_dict['id']}
    
    return mock_interview_dict

