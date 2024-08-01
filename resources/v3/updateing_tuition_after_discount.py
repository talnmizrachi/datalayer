import datetime
from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import update_objects_in_session
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentNewPaymentModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("Updating tuition after discount", __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/update_tuition', methods=['POST'])
class UpdatePayment(MethodView):
    """
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/597429020/edit/actions/1/webhook
    
    Included deals - Getting Interviews, Passing Interviews
    
    incoming payload -
    {
    "hs_object_id":
    "current_enrollment_school":
    }
    """
    
    def post(self):
        data = request.get_json()
        hubspot_id = str(data["hubspot_id"])

        existing_first_payment = StudentNewPaymentModel.query.filter(StudentNewPaymentModel.hubspot_id == hubspot_id).first()
        if existing_first_payment is None:
            logger.error(f"Student {hubspot_id} is not in the payments table yet")
            return str('hubspot_id'), 201

        logger.error(f"Changing amount from {existing_first_payment.amount} to {data['tuition_after_discount___usd_']}")
        existing_first_payment.amount = data['tuition_after_discount___usd_']

        update_objects_in_session()

        return str(data['hubspot_id']), 201

    
if __name__ == '__main__':
    
    print(datetime.datetime.now())