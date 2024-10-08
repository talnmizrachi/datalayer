import datetime

from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentOwnerChangesModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("owners' change from hubspot", __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/owner_change', methods=['POST'])
class JobReadyStudent(MethodView):
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
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=str(data['hs_object_id'])).first()
        if this_student is None:
            return f"{this_student} id is missing from the job ready students.", 202

        logger.info(f"Got a owner change:\t{data}")
        
        new_contact_owner = {
                "student_hubspot_id": str(data['hs_object_id']),
                "student_hubspot_owner_id": str(data['hubspot_owner_id']),
                      }
        
        if (new_contact_owner['student_hubspot_owner_id'].isspace() or
                new_contact_owner['student_hubspot_owner_id'] in ("None", "undefined")):
            new_contact_owner['student_hubspot_owner_id'] = None
        
        for msg in ["student_hubspot_owner_id", "firstname", "lastname"]:
            setattr(this_student, msg, data.get(msg))

        this_student.updated_timestamp = datetime.datetime.now()
        
        student_owner_change = StudentOwnerChangesModel(**new_contact_owner)
        write_object_to_db(student_owner_change)
        
        return str(new_contact_owner['student_hubspot_id']), 201


if __name__ == '__main__':
    
    print(datetime.datetime.now())