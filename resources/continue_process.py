from global_functions.continue_process_functions import *
from flask import request
from flask.views import MethodView
from models import ProcessModel, StageModel
from flask_smorest import Blueprint
import os
from datetime import datetime
from sqlalchemy.inspection import inspect


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('continue_process', __name__, description="A new stage in a job process")


@blueprint.route('/continue_process_direct/', methods=['POST'])
class ContinueProcessInitiation(MethodView):
    """
    This class handles the initiation of a new stage within a process.
    It listens for a POST request at the '/continue_process_direct' endpoint open for the MS RnD team
    payload should include:
    the process_id, the type of stage done, domain.
    """
    def post(self):
        data = request.get_json()
        attrs = parse_and_write_to_db_new_stage_in_process(data, source='direct')
        
        return attrs, 201
        
        

@blueprint.route('/continue_process_typeform', methods=['POST'])
class ContinueProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_stage_in_process(data, source='typeform')
        
        return new_process_dict['id'], 201


if __name__ == '__main__':
    pass
