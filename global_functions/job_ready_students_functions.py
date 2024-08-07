from uuid import uuid4
from flask_smorest import abort
from models import JobReadyStudentModel, StudentStagesV3, ProcessModel, StudentCohortChangesModel
from global_functions.general_functions import write_object_to_db
from global_functions.LoggingGenerator import Logger
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def check_if_student_has_id_from_legacy_mocks(_payload):
	return ProcessModel.query.filter_by(hubspot_id=str(_payload.get('hs_object_id'))).first()


def payload_to_job_ready_student_dict(payload):
	existing_id = check_if_student_has_id_from_legacy_mocks(payload)

	#keep this student_id - it'll keep consistency across past and present
	job_ready_student_dict = {'id': existing_id.student_id if existing_id else str(uuid4().hex),
	                          "student_ms_id": str(payload.get('student_ms_id')),
	                          "hubspot_id": str(payload.get('hs_object_id')),
	                          "domain": payload.get('domain', "TBD"),
	                          "student_first_name": payload.get('student_first_name'),
	                          "student_last_name": payload.get('student_last_name'),
	                          "schoolmaster_id": payload.get('school_master_name'),
	                          "student_owner": payload.get('hubspot_owner_id'),
	                          "created_at": payload.get('created_at'),
	                          "is_employed": payload.get('is_employed', False),
	                          "hubspot_current_deal_stage": payload.get("hubspot_current_deal_stage", "Job Ready"),
	                          "active_cohort": payload.get("current_enrollment_cohort"),
	                          "current_program": "BG" if payload.get("bg___program", "") != "" else "deferred"
	                          }

	stage_dict = {
		"hubspot_id": job_ready_student_dict['hubspot_id'],
		"stage": job_ready_student_dict['hubspot_current_deal_stage']
	}

	cohort_dict = {
		"hubspot_id": job_ready_student_dict['hubspot_id'],
		"student_cohort": job_ready_student_dict['active_cohort']

	}
	return job_ready_student_dict, stage_dict, cohort_dict


def onboard_function(data):
	logger.info(f"Onboarding student - {data}")
	is_existing = JobReadyStudentModel.query.filter_by(hubspot_id=str(data['hs_object_id'])).first()

	if is_existing is not None:
		logger.info(f"Student {data['hs_object_id']} is already onboarded")
		return {"id": data['hs_object_id'], "message": "Student is already onboarded"}

	job_ready_student_dict, stage_dict, cohort_dict = payload_to_job_ready_student_dict(data)

	job_ready_student_object = JobReadyStudentModel(**job_ready_student_dict)
	student_stage_obj = StudentStagesV3(**stage_dict)
	student_cohort_obj = StudentCohortChangesModel(**cohort_dict)

	write_object_to_db(job_ready_student_object)
	write_object_to_db(student_stage_obj)
	write_object_to_db(student_cohort_obj)

	logger.info(f"Onboarded new student:\t{job_ready_student_dict['id']}")
	return job_ready_student_dict
