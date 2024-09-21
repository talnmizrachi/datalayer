import datetime

from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentSchoolMasterChangesModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("schoolmasters' change from hubspot", __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/school_master_change', methods=['POST'])
class JobReadyStudent(MethodView):
    """
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/590583907/edit
    
    Included deals - Getting Interviews, Passing Interviews
    
    incoming payload -
    {
    "hs_object_id":
    "students_school_masters_blp":
    }
    """
    
    def post(self):
        data = request.get_json()
        logger.info(f"Got a Schoolmasters change:\t{data}")
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=str(data['hs_object_id'])).first()
        if this_student is None:
            return f"{this_student} id is missing from the job ready students.", 202
        
        new_contact_schoolmaster = {
                "student_hubspot_id": str(data['hs_object_id']),
                "student_hubspot_schoolmaster_id": str(data['current_enrollment_school']),
                      }
        
        if (new_contact_schoolmaster['student_hubspot_schoolmaster_id'].isspace() or
                new_contact_schoolmaster['student_hubspot_schoolmaster_id'] in ("None", "undefined")):
            new_contact_schoolmaster['student_hubspot_schoolmaster_id'] = None
        
        for i in ['student_hubspot_schoolmaster_id', 'firstname', 'lastname']:
            setattr(this_student, i, data.get(i))

        this_student.updated_timestamp = datetime.datetime.now()
        
        student_schoolmaster_change = StudentSchoolMasterChangesModel(**new_contact_schoolmaster)
        write_object_to_db(student_schoolmaster_change)
        
        return str(new_contact_schoolmaster['student_hubspot_id']), 201


if __name__ == '__main__':
    
    print(datetime.datetime.now())