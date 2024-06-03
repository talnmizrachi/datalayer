from global_functions.LoggingGenerator import Logger
from global_functions.new_process_functions import payload_to_new_process_dict
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
import os
from models import Process
from db import db

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('templated_blp', __name__, description="This_is_a_templated_blueprint")


def parse_and_write_to_db_new_processes(incoming_date):
    new_process_dict = payload_to_new_process_dict(incoming_date)
    new_process_object = Process(**new_process_dict)

    try:
        db.session.add(new_process_object)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        # logger.error(e)
        abort(500, message=str(e))

    return new_process_dict


@blueprint.route('/new_process_start', methods=['POST'])
class ProcessInitiation(MethodView):
    
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data)
        
        return new_process_dict['id'], 201


@blueprint.route('/onboard_students', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):
        data = request.get_json()
        student_ids = []
        for student in data:
            student_ids.append(parse_and_write_to_db_new_processes(student))
        
        return {"ids": student_ids}, 201
