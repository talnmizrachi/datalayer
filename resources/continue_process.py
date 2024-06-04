from global_functions.continue_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('continue_process', __name__, description="A new stage in a job process")


@blueprint.route('/new_stage_for_process', methods=['POST'])
class ContinueProcessInitiation(MethodView):
    """
    This class handles the initiation of a new stage within a process.
    It listens for a POST request at the '/new_stage_for_process' endpoint open for the MS RnD team
        """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_stage_dict = parse_and_write_to_db_new_stage_in_process(data)
        return new_stage_dict['id'], 201


@blueprint.route('/continue_process_direct', methods=['POST'])
class ContinueProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='typeform')
        
        return new_process_dict['id'], 201


if __name__ == '__main__':
    pass
