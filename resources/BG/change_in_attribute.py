from global_functions.LoggingGenerator import Logger
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import BGStudentModel, BGStudentChangesModel
import os
from sqlalchemy.exc import SQLAlchemyError
from db import db
from global_functions.general_functions import write_object_to_db
from resources.BG.onboarding_student import onboard_bg_function

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Change an attribute for a BG student', __name__, description="This_is_a_templated_blueprint")


def get_existing_student_dictionary(data):
	logger.info(f"Onboarding BG student - {data}")

	stages_dict = {"62780568": "Dropped", "62515535": "Active", "62780567": "Graduated"}

	job_ready_student_dict = {
		"enrolment_pipeline_stage": stages_dict.get(str(data['hs_pipeline_stage']), data['hs_pipeline_stage']),
		"hubspot_id": str(data['hubspot_id']),
		"active_cohort": data['enrolment_cohort'],
		"is_job_ready": data['is_job_ready']
	}

	return job_ready_student_dict


@blueprint.route('/change_bg_student', methods=['POST'])
class NewBGStudent(MethodView):

	def post(self):
		"""
		workflow url =

		:return:
		"""
		logger.info("hello")
		data = request.get_json()
		logger.info(data)
		existing_student = BGStudentModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()

		if existing_student is None:
			logger.debug(f"Student is missing (BG Change bg student): {data}")
			try:
				onboard_bg_function(data)
			except Exception as e:
				logger.error(f"Error onboarding student: {e}")
				abort(400, description="Hubspot ID is required")

		job_ready_student_dict = get_existing_student_dictionary(data)
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

				write_object_to_db(change_object)

		return str(job_ready_student_dict['hubspot_id']), 201
