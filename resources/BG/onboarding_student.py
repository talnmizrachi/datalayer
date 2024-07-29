from global_functions.LoggingGenerator import Logger
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import BGStudentModel
import os
from global_functions.general_functions import write_object_to_db


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Onboard a BG student', __name__, description="This_is_a_templated_blueprint")


def onboard_bg_function(data):
    logger.info(f"Onboarding BG student - {data}")
    
    is_existing = BGStudentModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()
    
    if is_existing is not None:
        logger.info(f"BG Student {data['hubspot_id']} is already onboarded")
        return {"id": data['hubspot_id'], "message": "BG Student is already onboarded"}
    
    job_ready_student_dict = {
            "enrolment_pipeline_stage": data['hs_pipeline_stage'],
            "hubspot_id": str(data['hubspot_id']),
            "first_name": data['firstname'],
            "last_name": data['lastname'],
            "domain": data['program'],
            "active_cohort": data['enrolment_cohort'],
            "student_owner": data['hubspot_owner_id'],
            "hs_pipeline":data['hs_pipeline']
    }
    
    job_ready_student_object = BGStudentModel(**job_ready_student_dict)

    write_object_to_db(job_ready_student_object)
    
    logger.info(f"Onboarded new student:\t{job_ready_student_dict['hubspot_id']}")
    return job_ready_student_dict


@blueprint.route('/onboard_bg_student', methods=['POST'])
class NewBGStudent(MethodView):
    
    def post(self):
        """
        workflow url =

        :return:
        """
        data = request.get_json()
        logger.debug(f"data type: {type(data)}")
        job_ready_student_dict = onboard_bg_function(data)
        
        return str(job_ready_student_dict['hubspot_id']), 201
