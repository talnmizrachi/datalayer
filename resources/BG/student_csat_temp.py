from platforms_webhooks_catchers.typeform.v2_csat import process_form_response
from global_functions.LoggingGenerator import Logger
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import BGStudentModel, BGStudentMSScoreModel
import os
from sqlalchemy.exc import SQLAlchemyError
from db import db
from global_functions.general_functions import write_object_to_db

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Catch student CSAT on typeform', __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/temp_csat_datalayer', methods=['POST'])
class NewBGStudent(MethodView):

	def post(self):
		"""
		workflow url =

		:return:
		"""
		logger.info("hello")
		data = request.get_json()
		logger.info(data)
		payload = process_form_response(data)
		
		existing_student = BGStudentModel.query.filter_by(email=str(data['email'])).first()

		if existing_student is None:
			logger.debug(f"Student is missing (BG Change bg student): {data}")
			abort(400, description="Hubspot ID is required")

		payload['hubspot_id'] = existing_student.hubspot_id
		payload['domain'] = existing_student.domain
		payload['cohort'] = existing_student.cohort
		
		csat_object = BGStudentMSScoreModel(**payload)
		
		write_object_to_db(csat_object)
		
		return str(existing_student.hubspot_id), 201
