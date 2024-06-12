from uuid import uuid4
from datetime import date, datetime
from models import ProcessModel, StageModel, MockInterviewModel, JobReadyStudentModel
from global_functions.general_functions import *
from global_functions.create_mock_interview import create_mock_interview_line_for_stage
from global_functions.LoggingGenerator import Logger
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def rename_key(d, old_key, new_key):
    if old_key in d:
        d[new_key] = d.pop(old_key)
    return d


def split_process_and_stage_dict(payload_dict):
    process_keys = {"id", "student_id", "student_firstname", "student_ms_id", "student_lastname", "domain",
                    "email_address", "company_name", "job_title", "job_description", 'cv_url', 'process_start_date',
                    'source_1', 'source_2'}
    
    stage_keys = {"id", "stage_in_funnel", 'student_firstname', 'student_lastname', "type_of_stage",
                  "had_home_assignment", 'home_assignment_questions', 'home_assignment_answers', 'stage_date'}
    
    process_dict = {k: v for k, v in payload_dict.items() if k in process_keys}
    stage_dict = {k: v for k, v in payload_dict.items() if k in stage_keys}
    rename_key(stage_dict, 'id', 'process_id')
    stage_dict['id'] = str(uuid4().hex)
    
    if "student_id" not in process_dict:
        process_dict['student_id'] = f"temp_{str(uuid4().hex)}"
    
    return process_dict, stage_dict


def parse_and_write_to_db_new_processes(incoming_data, source='direct'):
    if source == 'direct':
        process_dict, stage_dict = direct_payload_to_new_process_dict(incoming_data)
    elif source.find('typeform') > -1:
        logger.info("typeform data")
        process_dict, stage_dict = typeform_payload_to_new_process_dict(incoming_data)
    elif source == 'smart_matcher':
        logger.info("smart matcher data")
        process_dict, stage_dict = new_process_from_smart_matcher_payload(incoming_data)
    else:
        abort(400, message="source must be 'direct' or 'typeform'")
    new_mock_interview_dict = create_mock_interview_line_for_stage(process_dict, stage_dict)
    
    new_process_object = ProcessModel(**process_dict)
    new_stage_object = StageModel(**stage_dict)
    new_mock_interview_object = MockInterviewModel(**new_mock_interview_dict)
    
    write_object_to_db(new_process_object)
    write_object_to_db(new_stage_object)
    write_object_to_db(new_mock_interview_object)
    
    return process_dict


def direct_payload_to_new_process_dict(direct_payload):
    new_process_for_student_dict = {
            "id": str(uuid4().hex),
            "job_id": direct_payload.get("job_id"),
            "student_ms_id": direct_payload.get("student_ms_id", "not_provided"),
            "email_address": direct_payload.get("email_address"),
            "student_firstname": direct_payload.get("student_firstname"),
            "student_lastname": direct_payload.get("student_lastname"),
            "domain": direct_payload.get("domain"),
            "company_name": direct_payload.get("company_name"),
            "job_title": direct_payload.get("job_title"),
            "job_description": direct_payload.get("job_description"),
            "cv_url": direct_payload.get("cv_url"),
            "drive_url": direct_payload.get("drive_url"),
            "process_start_date": date.today(),
            "stage_in_funnel": direct_payload.get("stage_in_funnel"),
            "type_of_stage": direct_payload.get("type_of_stage"),
            "had_home_assignment": direct_payload.get("had_home_assignment", False),
            "home_assignment_questions": direct_payload.get("home_assignment_questions"),
            "home_assignment_answers": direct_payload.get("home_assignment_answers"),
            "stage_date": direct_payload.get("stage_date"),
    }
    
    student_is_listed_as_jr = JobReadyStudentModel.query.filter_by(
        student_ms_id=new_process_for_student_dict.get("student_ms_id")).first()
    logger.info(f"student_is_listed_as_jr: {student_is_listed_as_jr},"
                f" student_ms_id: {new_process_for_student_dict.get('student_ms_id')}")
    if student_is_listed_as_jr is None:
        # If the student is not listed as Job ready, we need to keep the process, and make sure that the student is
        # Identifiable for next iterations, based on the process - student_id will be the student_ms_id
        new_process_for_student_dict['student_id'] = new_process_for_student_dict.get("student_ms_id")
    else:
        new_process_for_student_dict['student_id'] = student_is_listed_as_jr.id
    
    process_dict, stage_dict = split_process_and_stage_dict(new_process_for_student_dict)
    
    return process_dict, stage_dict


def typeform_payload_to_new_process_dict(typeform_payload):
    typeform_questions_ids_ = {
            "uGidsoDwfCES": "domain",
            "FBYMmvdFNhfw": "email_address",
            "Kys4EcJ4WViT": "full_name",
            "hhV0z2H3bFbC": "company_name",
            "dQbDwUKSTl7G": "job_title",
            "xeaPZrcMGmR4": "stage_date",
            "yFyfpcjPDaal": "stage_in_funnel",
            "BFsWH2TPzBlH": "had_home_assignment",
            "qgbW21oTd1mO": "home_assignment_questions",
            "BzKp7H4TwZxn": "home_assignment_answers",
            "BVIHyvpqVsNS": "type_of_stage",
            "YIXeDQWMVqLr": "cv_url",
            "06oyTS92IyDZ": "job_description",
            "n6j9MkBtbqcF": "source_1",
            "ysVEuC3W9lKV": "source_2",
            # start legacy old typeform questions
            "uvAp6UdsBo6t": "domain",
            "lovnA3yOgQvh": "email_address",
            "jOtZui7dWULc": "full_name",
            "xG46N5VUGkhU": "company_name",
            "oX0jd0hBxJ9W": "job_title",
            "I6rmXpvTBdcL": "stage_date",
            "vHThsj2tIryq": "stage_in_funnel",
            "EwRF9XrUF5TV": "type_of_stage",
            "x8mzI8oTaxSf": "cv_url",
            "uPCVXBbisxbA": "job_description",
            "zLrnwv7yoTFO": "source_1",
            # start legacy of smart matcher
            "ak6f7SBAmjeV": "cv_url",
            "ho7Zc8mJVDM0": "type_of_stage",
            "PXdz2BkjAwWR": "stage_date",
    }
    
    new_dict = read_typeform_answers(typeform_payload, typeform_questions_ids_)
    logger.info(f"new_dict: {new_dict}")
    new_dict['id'] = str(uuid4().hex)
    new_dict['drive_url'] = "drive_url"
    new_dict['process_start_date'] = new_dict['stage_date']
    
    process_dict, stage_dict = split_process_and_stage_dict(new_dict)
    
    logger.info(f"process_dict: {process_dict}")
    logger.info(f"stage_dict: {stage_dict}")
    
    return process_dict, stage_dict


def new_process_from_smart_matcher_payload(smart_matcher_payload):
    def extract_interview_details(data):
        # Extracting the hidden fields
        hidden_fields = data['form_response']['hidden']
        answers = data['form_response']['answers']
        
        extracted_data = {
                "job_id": hidden_fields['job_id'],
                "student_id": data['form_response']['token'],  # student_id is called token in the data
                "student_firstname": hidden_fields['student_name'].split()[0],
                "student_lastname": hidden_fields['student_name'].split()[-1],
                "domain": hidden_fields['domain'],
                "email_address": hidden_fields['email'],
                "company_name": hidden_fields['comany_name'],
                "job_title": hidden_fields['job_title'],
                "stage_date": next((answer['date'] for answer in answers if answer['field']['type'] == 'date'),
                                          None),
                "type_of_stage": next(
                    (answer['choice']['label'] for answer in answers if answer['field']['type'] == 'multiple_choice'),
                    None),
                "stage_in_funnel":"1st Interview",
                "cv_url": next((answer['file_url'] for answer in answers if answer['field']['type'] == 'file_upload'), None),
                "is_process_active": True,
                "source_1": "Smart Matching",
                "source_2": "Smart Matching emails",
        }
        
        return extracted_data
    
    this_dictionary = extract_interview_details(smart_matcher_payload)
    this_dictionary['id'] = str(uuid4().hex)
    this_dictionary['process_id'] = this_dictionary['id']
    this_dictionary['process_start_date'] = this_dictionary['stage_date']
    this_dictionary['job_description'] = ""
    
    process_dict, stage_dict = split_process_and_stage_dict(this_dictionary)
    
    return process_dict, stage_dict


if __name__ == '__main__':
    ...
