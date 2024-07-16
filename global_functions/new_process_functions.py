from uuid import uuid4
from datetime import date, datetime
from models import ProcessModel, StageModel, MockInterviewModel, JobReadyStudentModel
from global_functions.general_functions import *
from global_functions.create_mock_interview import create_mock_interview_line_for_stage
from global_functions.LoggingGenerator import Logger
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def split_process_and_stage_dict(payload_dict):
    def rename_key(d, old_key, new_key):
        if old_key in d:
            d[new_key] = d.pop(old_key)
        return d
    process_keys = {"id", "student_id", "student_ms_id", "domain",
                    "company_name", "job_title", 'process_start_date',
                    'source_1', 'source_2'}
    
    stage_keys = {"id", "stage_in_funnel",  "type_of_stage",
                  "had_home_assignment", 'stage_date'}
    
    process_dict = {k: v for k, v in payload_dict.items() if k in process_keys}
    stage_dict = {k: v for k, v in payload_dict.items() if k in stage_keys}
    rename_key(stage_dict, 'id', 'process_id')
    stage_dict['id'] = str(uuid4().hex)
    
    if "student_id" not in process_dict:
        process_dict['student_id'] = f"temp_{str(uuid4().hex)}"
    
    return process_dict, stage_dict


def parse_and_write_to_db_new_processes(incoming_data):

    process_dict, stage_dict = direct_payload_to_new_process_dict(incoming_data)
 
    new_mock_interview_dict = create_mock_interview_line_for_stage(process_dict, stage_dict)
    
    new_process_object = ProcessModel(**process_dict)
    new_stage_object = StageModel(**stage_dict)
    new_mock_interview_object = MockInterviewModel(**new_mock_interview_dict)
    
    write_object_to_db(new_process_object)
    write_object_to_db(new_stage_object)
    write_object_to_db(new_mock_interview_object)
    
    return process_dict['id']


def direct_payload_to_new_process_dict(direct_payload):
    new_process_for_student_dict = {
            "id": str(uuid4().hex),
            "job_id": direct_payload.get("job_id"),
            "student_ms_id": direct_payload.get("hs_object_id", "not_provided"),
            "domain": direct_payload.get("program_domain"),
            "company_name": direct_payload.get("company"),
            "job_title": direct_payload.get("job_title"),
            "process_start_date": date.today(),
            "stage_in_funnel": "1st Stage",
            "type_of_stage": direct_payload.get("type_of_stage"),
            "had_home_assignment": direct_payload.get("had_home_assignment", False),
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


if __name__ == '__main__':
    ...
