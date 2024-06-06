from global_functions.LoggingGenerator import Logger
from global_functions.new_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('Initiate a Process', __name__, description="A process is the combination of "
                                                                  "Company-Job-Student, and will include at least one"
                                                                  " process event")


@blueprint.route('/new_process_start', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process.
    It listens for a POST request at the '/new_process_start' endpoint open for the MS RnD team
        """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='direct')
        
        return new_process_dict['id'], 201


@blueprint.route('/new_process_typeform', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    """
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='typeform')
        
        return new_process_dict['id'], 201


@blueprint.route('/close_process', methods=['POST'])
class ProcessTermination(MethodView):
    """ Close process through hubspot workflow
    https://app.hubspot.com/workflows/9484219/platform/flow/584835155/edit
    """
    def post(self):
        data = request.get_json()
        logger.info(data)
        
        return data

if __name__ == '__main__':
    pass
