import os
from global_functions.LoggingGenerator import Logger
from global_functions.create_mock_interview import create_mock_interview_line_for_stage_continue
from global_functions.general_functions import write_object_to_db
from models import ProcessModel, StageModel, MockInterviewModel
from flask_smorest import abort
from global_functions.general_functions import read_typeform_answers

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def direct_payload_to_new_stage_in_process_dict(data):
    interim_stage_dict = {'process_id': data['process_id']}
    
    process = ProcessModel.query.filter_by(id=interim_stage_dict['process_id']).first()
    if not process:
        abort(404, message="Process not found")
    
    interim_stage_dict['student_firstname'] = process.student_firstname
    interim_stage_dict['student_lastname'] = process.student_lastname
    
    interim_stage_dict['stage_in_funnel'] = data.get('stage_in_funnel')
    interim_stage_dict['type_of_stage'] = data.get('type_of_stage')
    interim_stage_dict['had_home_assignment'] = data.get('had_home_assignment')
    interim_stage_dict['home_assignment_questions'] = data.get('home_assignment_questions')
    interim_stage_dict['home_assignment_answers'] = data.get('home_assignment_answers')
    interim_stage_dict['stage_date'] = data.get('stage_date')
    
    return interim_stage_dict


def typeform_payload_to_new_stage_in_process_dict(data):
    """
    Continue an interview coming from the typeform
    https://forms.masterschool.com/to/grhKmF8r
    #prev_stage=xxxxx&process_id=xxxxx&domain=xxxxx
    prev_stage - for personalization
    domain - for proper mock determination
    process_id - to find the right process in db
    :param data:
    :return:
    """
    interim_stage_dict = {"process_id": data['form_response'].get("hidden", {}).get("process_id")}
   
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
    return interim_stage_dict


def parse_and_write_to_db_new_stage_in_process(data, source):
    if source == "direct":
        stage_dict = direct_payload_to_new_stage_in_process_dict(data)
    elif source == "typeform":
        stage_dict = typeform_payload_to_new_stage_in_process_dict(data)
    else:
        abort(400, message="Invalid source")
    mock_int_dict = create_mock_interview_line_for_stage_continue(stage_dict)
    
    new_stage_obj = StageModel(**stage_dict)
    new_mock_obj = MockInterviewModel(**mock_int_dict)
    write_object_to_db(new_stage_obj)
    write_object_to_db(new_mock_obj)
    
    return stage_dict


if __name__ == '__main__':
    pass