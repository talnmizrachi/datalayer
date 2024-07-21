import datetime
from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import deal_stage_dict
import os
from models import JobReadyStudentModel, StudentNewPaymentModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("Logging first payment", __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/log_first_payment', methods=['POST'])
class FirstPayment(MethodView):
    """
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/590608921/edit
    
    Included deals - Getting Interviews, Passing Interviews
    
    incoming payload -
    {
    "hs_object_id":
    "current_enrollment_school":
    }
    """
    
    def post(self):
        data = request.get_json()
        hubspot_id = str(data["hs_object_id"])
        existing_student = JobReadyStudentModel.query.filter(StudentNewPaymentModel.hubspot_id == hubspot_id).first()

        if existing_student:
            student_id = existing_student.id
        else:
            student_id = hubspot_id

        existing_first_payment = StudentNewPaymentModel.query.filter(StudentNewPaymentModel.hubspot_id == hubspot_id).first()

        if existing_student:
            logger.info(f"Student {existing_student} already exists")
            return {"message": f"Student {existing_student} already exists"}, 201

        new_first_payment = {"hubspot_id": hubspot_id,
        "student_id":student_id,
        "type_of_collection": data['type_of_collection'],
        "amount": data['amount'],
        }

        student_payment_obj = StudentNewPaymentModel(**new_first_payment)
        write_object_to_db(student_payment_obj)
        
        return str(new_first_payment['hubspot_id']), 201


if __name__ == '__main__':
    
    print(datetime.datetime.now())