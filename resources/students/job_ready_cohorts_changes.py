import datetime

from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentCohortChangesModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("cohorts' change from hubspot", __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/cohort_change', methods=['POST'])
class JobReadyStudent(MethodView):
    """
    Workflow URL - *****
    
    when the property current_enrollment_cohort changes
    
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
            return f"{this_student} id is missing from the job ready students for the purpose of cohorts change.", 202

        logger.info(f"Got a owner change:\t{data}")
        
        new_student_cohort = {
                "hubspot_id": str(data['hs_object_id']),
                "student_cohort": str(data['current_enrollment_cohort']),
                      }
        
        if (new_student_cohort['student_cohort'].isspace() or
                new_student_cohort['student_cohort'] in ("None", "undefined")):
            new_student_cohort['student_cohort'] = None
            
        this_student.active_cohort = new_student_cohort['student_cohort']
        this_student.updated_timestamp = datetime.datetime.now()
        
        student_cohort_change = StudentCohortChangesModel(**new_student_cohort)
        write_object_to_db(student_cohort_change)
        
        return str(new_student_cohort['hubspot_id']), 201


if __name__ == '__main__':
    
    print(datetime.datetime.now())