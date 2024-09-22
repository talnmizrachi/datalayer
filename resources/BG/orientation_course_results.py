from global_functions.LoggingGenerator import Logger
from global_functions.time_functions import infer_and_transform_date, utc_to_date
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from models import V2OC2FPStatus
import os
from global_constants import V2_OC2FP_STATUS_DEAL_STAGE_MAPPING
from global_functions.general_functions import write_object_to_db, is_candidate_ms_employee

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Orientation course reader', __name__, description="This_is_a_templated_blueprint")


def orientation_course_result(data):
	"""https://app.hubspot.com/workflows/9484219/platform/flow/612903318/edit"""
	logger.info(f"Orientation course to Full time - {data}")

	# This shouldn't happen - the term to get into this function is
	if data['hubspot_id'] == "":
		logger.info(f"Empty process - hubspot id is empty")
		return {"id": None, "message": "Empty process - hubspot id is empty"}

	orientation_course_result_dict = {
		"deal_id": str(data['deal_id']),
		"hubspot_id": str(data['hubspot_id']),
		"first_name": data['first_name'],
		"last_name": data['last_name'],
		"closed_lost_reason": data['closed_lost_reason'],
		"enrollment_cohort": infer_and_transform_date(data['enrollment_cohort']),
		"bg_disapproval_reason": data['bg_disapproval_reason'],
		"dealstage": V2_OC2FP_STATUS_DEAL_STAGE_MAPPING.get(str(data['dealstage'])),
		"closed_date": utc_to_date(data['close_date']),
	}

	orientation_course_result_obj = V2OC2FPStatus(**orientation_course_result_dict)

	write_object_to_db(orientation_course_result_obj)

	return orientation_course_result_dict


@blueprint.route('/orientation_course_final_status', methods=['POST'])
class NewOCStatusStudent(MethodView):

	def post(self):
		data = request.get_json()

		if is_candidate_ms_employee(data):
			return {"message": "Hubspot ID is a Master School employee"}, 201

		logger.debug(f"data type: {type(data)}")
		job_ready_student_dict = orientation_course_result(data)
		logger.debug(f"Debugging problem - {job_ready_student_dict}")
		return job_ready_student_dict, 201


if __name__ == '__main__':
	print(orientation_course_result({'deal_id': 20460437029,
	                                 'last_name': 'Winschermann',
	                                 'close_date': 1724231572964,
	                                 'dealstage': 161070367,
	                                 'first_name': 'Marcel',
	                                 'hubspot_id': 33119859114,
	                                 'enrollment_cohort': 'July 2024',
	                                 'closed_lost_reason': 'Unresponsive',
	                                 'bg_disapproval_reason': None}))
