from datetime import datetime

from global_functions.LoggingGenerator import Logger
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import BGStudentModel, BGStudentChangesModel
import os
from sqlalchemy.exc import SQLAlchemyError
from db import db
from global_functions.general_functions import write_object_to_db

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Update BG student got a job', __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/close_process_bg', methods=['POST'])
class NewBGStudent(MethodView):

    def post(self):
        """
        workflow url =

        :return:
        """
        data = request.get_json()
        logger.info(data)
        existing_student = BGStudentModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()

        if existing_student is None:
            logger.debug(f"Student is missing (BG Change bg student): {data}")
            abort(400, description="Hubspot ID is required")

        existing_student.is_employed = True
        existing_student.updated_timestamp = datetime.now()
        
        try:
            db.session.commit()
        except SQLAlchemyError as e:
            logger.error(e)
            db.session.rollback()
            abort(500, description="Failed to update student")
        
        return str(data['hubspot_id']), 201
