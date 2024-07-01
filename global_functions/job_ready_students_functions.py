from uuid import uuid4
from flask_smorest import abort
from models import JobReadyStudentModel, StudentStagesV3
from global_functions.general_functions import write_object_to_db
from global_functions.LoggingGenerator import Logger
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def payload_to_job_ready_student_dict(payload):
    if payload.get('domain') is None:
        abort(404, message="Domain was not found")
    
    job_ready_student_dict = {'id': payload.get('id') or str(uuid4().hex),
                              "student_ms_id": payload.get('student_ms_id'),
                              "hubspot_id": str(payload.get('hs_object_id')),
                              "domain": payload.get('domain'),
                              "student_country": payload.get('student_country'),
                              "student_state": payload.get('student_state'),
                              "student_city": payload.get('student_city'),
                              "schoolmaster_id": payload.get('school_master_name'),
                              "csa_hubspot_id": payload.get('hubspot_owner_id'),
                              "created_at": payload.get('created_at'),
                              "is_employed": payload.get('is_employed', False),
                              "hubspot_current_deal_stage": payload.get("hubspot_current_deal_stage", "Job Ready")
                              }
    
    stage_dict = {
            "student_id": job_ready_student_dict['id'],
            "hubspot_id": job_ready_student_dict['hubspot_id'],
            "stage": job_ready_student_dict['hubspot_current_deal_stage']
    }
    return job_ready_student_dict, stage_dict


def onboard_function(data):
    job_ready_student_dict, stage_dict = payload_to_job_ready_student_dict(data)
    
    job_ready_student_object = JobReadyStudentModel(**job_ready_student_dict)
    student_stage_obj = StudentStagesV3(**stage_dict)
    
    write_object_to_db(job_ready_student_object)
    write_object_to_db(student_stage_obj)
    
    logger.info(f"Onboarded new student:\t{job_ready_student_dict['id']}")
    return job_ready_student_dict
