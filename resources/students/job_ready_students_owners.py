from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentOwnerChanges

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("owners' change from hubspot", __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/owner_change', methods=['POST'])
class JobReadyStudent(MethodView):
    """
    Workflow URL -
    
    Included deals - Getting Interviews, Passing Interviews
    
    incoming payload -
    {
    "hs_object_id":
    "hubspot_owner_id":
    }
    """
    
    def post(self):
        data = request.get_json()
        logger.info(f"Got a deal change:\t{data}")
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=data['hs_object_id']).first()
        if this_student is None:
            return f"{this_student} id is missing from the job ready students.", 202
        
        new_contact_owner = {
                "student_hubspot_id": data['hs_object_id'],
                "student_hubspot_owner_id": data['hubspot_owner_id'],
                      }
        this_student.csa_hubspot_id = data['hubspot_owner_id']
        student_owner_change = StudentOwnerChanges(**new_contact_owner)
        write_object_to_db(student_owner_change)
        
        return str(new_contact_owner['hubspot_id']), 201
