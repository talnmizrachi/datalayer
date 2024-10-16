from global_constants import V2_ENROLLMENT_STATUS_DEAL_STAGE_MAPPING
from datetime import datetime
from global_functions.LoggingGenerator import Logger
from global_functions.time_functions import infer_and_transform_date
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import BGStudentModel, BGStudentChangesModel
import os
from global_functions.general_functions import write_object_to_db, is_candidate_ms_employee
from resources.BG.onboarding_student import onboard_bg_function

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Change an attribute for a BG student', __name__, description="This_is_a_templated_blueprint")


def get_existing_student_dictionary(data, _existing_student):
	logger.info(f"Onboarding BG student - {data}")

	if data.get('hs_pipline_stage') is None:
		current_stage = _existing_student.enrolment_pipeline_stage
	else:
		current_stage = V2_ENROLLMENT_STATUS_DEAL_STAGE_MAPPING.get(str(data['hs_pipeline_stage']), data['hs_pipeline_stage'])
	
	if data.get('enrollment_id') != _existing_student.enrollment_id:
		logger.warning(f"Enrollment ID mismatch: {data['enrollment_id']} vs {_existing_student.enrollment_id} for student {data['hubspot_id']}")
		
	job_ready_student_dict = {
		"enrolment_pipeline_stage": current_stage,
		"hubspot_id": str(data['hubspot_id']),
		"active_cohort": infer_and_transform_date(data['enrolment_cohort']),
		"is_job_ready": True if str(data['is_job_ready']).lower().find('true')>-1 else False,
		"plan_duration": data['plan_duration'],
	}

	return job_ready_student_dict


@blueprint.route('/change_bg_student', methods=['POST'])
class NewBGStudent(MethodView):

	def post(self):
		"""
		workflow url =

		:return:
		"""
		data = request.get_json()
		if is_candidate_ms_employee(data):
			return {"message": "Hubspot ID is a Master School employee"}, 201

		logger.info(data)
		existing_student = BGStudentModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()

		if existing_student is None:
			logger.debug(f"Student is missing (BG Change bg student): {data}")
			try:
				onboard_bg_function(data)
				return str(data['hubspot_id']), 207
			except Exception as e:
				logger.error(f"Error onboarding student: {e}")
				abort(400, description="Hubspot ID is required")

		job_ready_student_dict = get_existing_student_dictionary(data, existing_student)
		logger.info(job_ready_student_dict)
		for key, value in job_ready_student_dict.items():
			# Using getattr and setattr to get and set attributes
			if getattr(existing_student, key) != value:
				change_dict = {
					"hubspot_id": existing_student.hubspot_id,
					"key": key,
					"from_value": getattr(existing_student, key),
					"to_value": value
				}

				change_object = BGStudentChangesModel(**change_dict)
				setattr(existing_student, key, value)
				existing_student.updated_timestamp = datetime.now()
				
				write_object_to_db(change_object)

		return str(job_ready_student_dict['hubspot_id']), 201
