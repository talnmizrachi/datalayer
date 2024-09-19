from global_functions.LoggingGenerator import Logger
from global_functions.time_functions import infer_and_transform_date
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import BGStudentModel
import os
from global_functions.general_functions import write_object_to_db, is_candidate_ms_employee

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint('Onboard a BG student', __name__, description="This_is_a_templated_blueprint")


def onboard_bg_function(data):
    logger.info(f"Onboarding BG student - {data}")
    
    is_existing = BGStudentModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()

    #This shouldn't happen - the term to get into this function is
    if data['hubspot_id'] == "":
        logger.info(f"Empty process - hubspot id is empty")
        return {"id": None, "message": "Empty process - hubspot id is empty"}
    
    if is_existing is not None:
        logger.info(f"BG Student {data['hubspot_id']} is already onboarded")
        return {"id": data['hubspot_id'], "message": "BG Student is already onboarded"}
    
    stages_dict = {"62780568": "Dropped", "62515535": "Active", "62780567": "Graduated"}
    
    job_ready_student_dict = {
            "enrolment_pipeline_stage": stages_dict.get(str(data['hs_pipeline_stage']), data['hs_pipeline_stage']),
            "hubspot_id": str(data['hubspot_id']),
            "first_name": data['firstname'],
            "last_name": data['lastname'],
            "domain": data['program'],
            "active_cohort": infer_and_transform_date(data['enrolment_cohort'], '%b-%Y'),
            "student_owner": data['hubspot_owner_id'],
            "hs_pipeline": data['hs_pipeline'],
            "is_job_ready": True if str(data['is_job_ready']).lower().find('true') else False,
            "email": data['email'],
            "plan_duration": data['plan_duration'],
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
        if is_candidate_ms_employee(data):
            return {"message": "Hubspot ID is a Master School employee"}, 201

        if data['hubspot_id'] == "":
            logger.debug(f"Hubspot ID is missing for BG student: {data}")
            abort(400, description="Hubspot ID is required")

        logger.debug(f"data type: {type(data)}")
        job_ready_student_dict = onboard_bg_function(data)
        logger.debug(f"Debugging problem - {job_ready_student_dict}")
        return job_ready_student_dict, 201
