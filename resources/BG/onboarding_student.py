from global_constants import V2_ENROLLMENT_STATUS_DEAL_STAGE_MAPPING
from global_functions.LoggingGenerator import Logger
from global_functions.time_functions import infer_and_transform_date, utc_to_date
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from models import BGStudentModel, BGStudentModel2
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
    
    job_ready_student_dict = {
            "enrolment_pipeline_stage": V2_ENROLLMENT_STATUS_DEAL_STAGE_MAPPING.get(str(data['hs_pipeline_stage']), data['hs_pipeline_stage']),
            "hubspot_id": str(data['hubspot_id']),
            "first_name": data['firstname'],
            "last_name": data['lastname'],
            "domain": data['program'],
            "active_cohort": infer_and_transform_date(data['enrolment_cohort'], '%b-%Y'),
            "student_owner": data['hubspot_owner_id'],
            "hs_pipeline": data['hs_pipeline'],
            "is_job_ready": True if str(data['is_job_ready']).lower().find('true')>-1 else False,
            "email": data['email'],
            "plan_duration": data['plan_duration'],
            'enrollment_id': data.get('enrollment_id')
    }
    
    job_ready_student_object = BGStudentModel(**job_ready_student_dict)
    
    write_object_to_db(job_ready_student_object)
    
    logger.info(f"Onboarded new student:\t{job_ready_student_dict['hubspot_id']}")
    return job_ready_student_dict


def onboard_bg_function_2(data):
    logger.info(f"Onboarding BG student - {data}")
    
    is_existing = BGStudentModel2.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()
    
    # This shouldn't happen - the term to get into this function is
    if data['hubspot_id'] == "":
        logger.info(f"Empty process - hubspot id is empty")
        return {"id": None, "message": "Empty process - hubspot id is empty"}
    
    if is_existing is not None:
        logger.info(f"BG Student {data['hubspot_id']} is already onboarded")
        return {"id": data['hubspot_id'], "message": "BG Student is already onboarded"}
    
    job_ready_student_dict = {
            "enrolment_pipeline_stage": V2_ENROLLMENT_STATUS_DEAL_STAGE_MAPPING.get(str(data['hs_pipeline_stage']),
                                                                                    data['hs_pipeline_stage']),
            "hubspot_id": str(data['hubspot_id']),
            "first_name": data.get('firstname'),
            "last_name": data.get('lastname'),
            "domain": data.get('program'),
            "active_cohort": infer_and_transform_date(data['enrolment_cohort'], '%b-%Y'),
            "student_owner": data.get('hubspot_owner_id'),
            "hs_pipeline": data.get('hs_pipeline'),
            "is_job_ready_text": str(data['is_job_ready']),
            "is_job_ready": True if str(data['is_job_ready']).lower().find('true') > -1 else False,
            "email": data['email'],
            "plan_duration": data['plan_duration'],
            'enrollment_id': data.get('enrollment_id'),
            'source': data.get('source'),
            "object_modified": utc_to_date(data.get('hs_lastmodifieddate'))
            
    }
    
    job_ready_student_object = BGStudentModel2(**job_ready_student_dict)
    
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


@blueprint.route('/onboard_bg_student_2', methods=['POST'])
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
        job_ready_student_dict = onboard_bg_function_2(data)
        logger.debug(f"Debugging problem - {job_ready_student_dict}")
        return job_ready_student_dict, 201


if __name__ == '__main__':
    def test(data):
        job_ready_student_dict = {
                "enrolment_pipeline_stage": V2_ENROLLMENT_STATUS_DEAL_STAGE_MAPPING.get(str(data['hs_pipeline_stage']), data['hs_pipeline_stage']),
                "hubspot_id": str(data['hubspot_id']),
                "first_name": data['firstname'],
                "last_name": data['lastname'],
                "domain": data['program'],
                "active_cohort": infer_and_transform_date(data['enrolment_cohort'], '%b-%Y'),
                "student_owner": data['hubspot_owner_id'],
                "hs_pipeline": data['hs_pipeline'],
                "is_job_ready": True if str(data['is_job_ready']).lower().find('true')>-1 else False,
                "email": data['email'],
                "plan_duration": data['plan_duration'],
        }
        
        return job_ready_student_dict
    
    print(test({'hubspot_id': '123', 'firstname': 'John', 'lastname': 'Doe',
                'program': 'MS', 'enrolment_cohort': 'Oct-2020',
                'hs_pipeline_stage': '62780568', 'hubspot_owner_id': '123456789',
                'is_job_ready': 'True', 'email': 'john','hs_pipeline':'hs_pipeline',
                "plan_duration":"8 Months"}))