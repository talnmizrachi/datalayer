import datetime
from global_functions.ignoring_constants import MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE
from uuid import uuid4
from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db, update_objects_in_session
from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import deal_stage_dict
from platforms_webhooks_catchers.hubspot.get_owner_name import get_owner_name
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentStagesV3, StudentCohortChangesModel, ProcessModel, StageModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("deals' change from hubspot - Second version", __name__,
                      description="This_is_a_templated_blueprint")


def create_cohort_dict(this_student_hs_id_, active_cohort_):
	cohort_dict = {
		"hubspot_id": this_student_hs_id_,
		"student_cohort": active_cohort_

	}
	return cohort_dict


def create_stage_dict(this_student_hs_id_, this_stage_):
	stage_dict = {
		"hubspot_id": this_student_hs_id_,
		"stage": this_stage_
	}
	return stage_dict


def parse_incoming_getting_passing_pipeline(data):
	pipeline_dict = {}
	deal_stage_dictionary = deal_stage_dict()
	piepline = data.get("pipeline")
	# Getting Interviews
	if piepline == 95522316:
		pipeline_dict = {
			"hubspot_id": str(data.get('hubspot_id')),
			"student_first_name": data.get('student_first_name'),
			"student_last_name": data.get('student_last_name'),
			"schoolmaster_id": data.get('schoolmaster_id'),
			"domain": data.get('domain'),
			"deal_stage_name": deal_stage_dictionary.get(data['dealstage']),
			"active_cohort": data.get('active_cohort'),
			"student_owner": get_owner_name(data.get('student_owner', None)),
			"current_program": data.get('bg___program')
		}
		return pipeline_dict

	# Passing Interviews
	elif piepline == 95255387:

		process_dict = {
			"id": str(uuid4().hex),
			"hubspot_deal_id": data.get('hubspot_deal_id'),
			"hubspot_id": data.get('hubspot_id'),
			"student_first_name": data.get('student_first_name'),
			"student_last_name": data.get('student_last_name'),
			"domain": data.get('domain'),
			"company_name": data.get('company_name'),
			"job_title": data.get('job_title'),
			"process_start_date": datetime.date.today(),
		}

		pipeline_dict = {
			"hubspot_id": data.get("hubspot_id"),
			"domain": data.get("domain"),
			"hubspot_deal_id": data.get("hubspot_deal_id"),
			"student_last_name": data.get("student_last_name"),
			"next_recruiting_step_date": data.get("next_recruiting_step"),
			"dealstage": data.get("dealstage"),
			"job_title": data.get("job_title"),
			"company_name": data.get("company"),
			"student_first_name": data.get("student_first_name"),
			"next_recruiting_step_type": data.get("next_recruiting_step")
		}

	# V3 Payments
	elif piepline == 107256463:
		...

	return pipeline_dict


@blueprint.route('/deal_stage_change_getting_interviews', methods=['POST'])
class JobReadyStudentDealChange(MethodView):
	"""
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit

    Included deals - Getting Interviews, Passing Interviews

    incoming payload -
    {"dealstage":
    "hs_object_id":
    "hubspot_owner_id":
    }
    """

	def post(self):
		data = request.get_json()

		if data['hubspot_id'] in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
			logger.info(f"Skipping the job ready update. 200 OK")
			return {"message": f"Test students are ignored: {data['hubspot_id']}"}, 200

		job_ready_student_dict = parse_incoming_getting_passing_pipeline(data)

		this_stage = job_ready_student_dict.get("deal_stage_name")
		this_student_hs_id = job_ready_student_dict.get("hubspot_id")
		this_student_cohort = job_ready_student_dict.get("active_cohort")

		this_student = JobReadyStudentModel.query.filter_by(hubspot_id=this_student_hs_id).first()

		if this_student is None:
			# Create new student, a new deal stage and a new cohort
			new_student_obj = JobReadyStudentModel(**job_ready_student_dict)
			student_stage_obj = JobReadyStudentDealChange(**create_stage_dict(this_student_hs_id, this_stage))
			student_cohort_obj = StudentCohortChangesModel(
				**create_cohort_dict(this_student_hs_id, this_student_cohort))

			write_object_to_db(new_student_obj)
			write_object_to_db(student_stage_obj)
			write_object_to_db(student_cohort_obj)

		# Check if student in the Not job ready table already, if so - >???

		continuous_stage = ("1st CSA Meeting Conducted", "Material Ready", "Job Seeking", "Contacted by Employer",
		                    "Closed Lost - Ghost", "Closed Won - Got an Interview")
		if this_stage in continuous_stage:
			this_student.hubspot_current_deal_stage = job_ready_student_dict.get('deal_stage_name')
			this_student.updated_timestamp = datetime.datetime.now()
			# Update deal in the deal stages, update last stage in JobReadyStudentModel

			stage_obj = StudentStagesV3(**create_stage_dict(this_student_hs_id, this_stage))
			write_object_to_db(stage_obj)


@blueprint.route('/deal_stage_change_passing_interviews', methods=['POST'])
class JobReadyStudentDealChange(MethodView):
	"""
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit

    """

	def post(self):
		data = request.get_json()

		if data['hubspot_id'] in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
			logger.info(f"Skipping the job ready update. 200 OK")
			return {"message": f"Test students are ignored: {data['hubspot_id']}"}, 200

		job_ready_student_dict = parse_incoming_getting_passing_pipeline(data)

		this_stage = job_ready_student_dict.get("hubspot_current_deal_stage")
		this_student_hs_id = job_ready_student_dict.get("hubspot_id")

		this_student = JobReadyStudentModel.query.filter_by(hubspot_id=this_student_hs_id).first()

		if this_student is None:
			# Create new student in a not-job-ready but with an interview?
			# Add process and stage

			...

		if this_stage in (
				"First Interview Scheduled", "First Interview", "Additional Interview", "Final Interview",
				"Job Offer Received"):
			# if there is a process - create a stage
			# if there's no process - create a new process, and a new stage
			# update last stage in JobReadyStudentModel
			# Update deal in the deal stages

			this_student.hubspot_current_deal_stage = this_stage
			this_student.updated_timestamp = datetime.datetime.now()

			process_obj = ProcessModel(**create_process_dict(this_student_hs_))
			stage_obj = StudentStagesV3(**create_stage_dict(this_student_hs_id, this_stage))

			# Check if process exists, if not - create a new process, and a new stage
			...

		if this_stage in ("Closed Won - Job Secured", 'Double'):
			# Update is_employed
			# update closed process
			# if Double - don't update JobReadyStudentModel
			...

		if this_stage in ("Closed Lost - Job Not Secured", "Fraudulent"):
			# Check if we have another process, if so - take the last stage, if not - return to Job seeking
			# Update process as closed, and stage as closed
			...

		if this_stage == "Special Cases":
			...
