from global_functions.LoggingGenerator import Logger
from global_functions.job_ready_students_functions import onboard_function
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Onboard a student', __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/onboard_student', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):
        """
        workflow url = https://app.hubspot.com/workflows/9484219/platform/flow/585666594
        
        :return:
        """
        data = request.get_json()
        logger.debug(f"data type: {type(data)}")
        job_ready_student_dict = onboard_function(data)
        return str(job_ready_student_dict['id']), 201
