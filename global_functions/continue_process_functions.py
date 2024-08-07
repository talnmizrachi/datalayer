import os
from datetime import datetime
from uuid import uuid4

from sqlalchemy import inspect

from global_functions.LoggingGenerator import Logger
from global_functions.create_mock_interview import create_mock_interview_line_for_stage_continue
from global_functions.general_functions import write_object_to_db
from models import ProcessModel, StageModel, MockInterviewModel
from flask_smorest import abort
from global_functions.general_functions import read_typeform_answers

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def direct_payload_to_new_stage_in_process_dict(data):
    process_id = data.get('process_id')
    next_stage_in_funnel = data.get('next_stage_in_funnel')
    type_of_next_stage = data.get('type_of_next_stage')
    next_stage_date = data.get('next_stage_date')
    is_home_assignment = data.get('is_home_assignment')
    
    current_success_stage = StageModel.query.filter_by(process_id=process_id, is_pass="PENDING").first()
    
    if current_success_stage is None:
        return abort(400, message=f"No current pending stage in process {process_id}")
    attrs = {c.key: getattr(current_success_stage, c.key) for c in
             inspect(current_success_stage).mapper.column_attrs}
    # mark the passed stage as done
    current_success_stage.is_pass = "TRUE"
    current_success_stage.updated_at = datetime.now()
    # current_success_stage.commit()
    
    # create a new stage in the process
    attrs.pop('id')
    attrs['stage_in_funnel'] = next_stage_in_funnel
    attrs['type_of_stage'] = type_of_next_stage
    attrs['stage_date'] = next_stage_date
    attrs['created_at'] = datetime.now()
    attrs['updated_at'] = datetime.now()
    # if the stage is a home assignment stage or the process had a home assignment,
    # add the questions and answers to the new stage
    
    return attrs


def typeform_payload_to_new_stage_in_process_dict(data):
    """
    Continue an interview coming from the typeform
    https://forms.masterschool.com/to/grhKmF8r?process_id=xxxxx
    domain - for proper mock determination
    process_id - to find the right process in db
    :param data:
    :return:
    """
    interim_stage_dict = {"process_id": data['form_response'].get("hidden", {}).get("process_id")}
    
    process_id = interim_stage_dict['process_id']
    current_success_stage = StageModel.query.filter_by(process_id=process_id, is_pass="PENDING").first()
    if current_success_stage is None:
        return abort(400, message=f"No current pending stage in process {process_id}")
    
    typeform_questions_ids_ = {
            "jiM5UWIk3FSm": "stage_date",
            "2DGB3brWY15C": "stage_in_funnel",
            "UOTR1srsxOii": "type_of_stage",
            "BFsWH2TPzBlH": "had_home_assignment",
            "hPpjZaBRkcX2": "home_assignment_questions",
            "xKZNNRB7SLqf": "home_assignment_answers",
    }
    
    parsed_typeform = read_typeform_answers(data, typeform_questions_ids_)
    interim_stage_dict |= parsed_typeform
    
    logger.critical(f"interim_stage_dict: {interim_stage_dict}")
    
    attrs = {c.key: getattr(current_success_stage, c.key) for c in
             inspect(current_success_stage).mapper.column_attrs}
    logger.critical(f"attrs: {attrs}")
    # mark the passed stage as done
    current_success_stage.is_pass = "TRUE"
    current_success_stage.updated_at = datetime.now()
    # current_success_stage.commit()
    
    # create a new stage in the process
    attrs.pop('id')
    
    is_home_assignment = interim_stage_dict.get("type_of_stage", "").lower() == "home assignment"
    attrs['stage_in_funnel'] = interim_stage_dict.get("stage_in_funnel")
    attrs['type_of_stage'] = interim_stage_dict.get("type_of_stage")
    attrs['stage_date'] = interim_stage_dict.get("stage_date")
    attrs['created_at'] = datetime.now()
    attrs['updated_at'] = datetime.now()
    # if the stage is a home assignment stage or the process had a home assignment,
    # add the questions and answers to the new stage
    # if current_success_stage.had_home_assignment:
    #     attrs['home_assignment_questions'] = current_success_stage.home_assignment_questions
    #     attrs['home_assignment_answers'] = current_success_stage.home_assignment_answers
    # elif is_home_assignment:
    #     attrs['had_home_assignment'] = True
    #     attrs['home_assignment_questions'] = interim_stage_dict.get('home_assignment_questions')
    #     attrs['home_assignment_answers'] = interim_stage_dict.get('home_assignment_answers')
    # else:
    #     attrs['home_assignment_questions'] = None
    #     attrs['home_assignment_answers'] = None
    
    return attrs


def parse_and_write_to_db_new_stage_in_process(data, source):
    if source == "direct":
        stage_dict = direct_payload_to_new_stage_in_process_dict(data)
    elif source == "typeform":
        stage_dict = typeform_payload_to_new_stage_in_process_dict(data)
    else:
        abort(400, message="Invalid source")
    
    stage_dict['id'] = str(uuid4().hex)
    mock_int_dict = create_mock_interview_line_for_stage_continue(stage_dict)
    
    new_stage_obj = StageModel(**stage_dict)
    new_mock_obj = MockInterviewModel(**mock_int_dict)
    write_object_to_db(new_stage_obj)
    write_object_to_db(new_mock_obj)
    
    return {"stage_id": stage_dict['id'], "process_id": new_stage_obj.process_id}, 201


if __name__ == '__main__':
    pass
