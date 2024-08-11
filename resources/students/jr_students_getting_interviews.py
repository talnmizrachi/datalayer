import datetime
from sqlalchemy import and_
from global_functions.ignoring_constants import MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE
from uuid import uuid4
from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db, update_objects_in_session
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentStagesV3, StudentCohortChangesModel, ProcessModel, StageModel
from platforms_webhooks_catchers.hubspot.getting_passing_payload_parser import parse_incoming_getting_passing_pipeline
from global_functions.models_resources import create_stage_dict, create_cohort_dict

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint("getting interviews Blueprint", __name__,
                      description="This_is_a_templated_blueprint")


@blueprint.route('/getting_interviews', methods=['POST'])
class JobReadyStudentDealChange(MethodView):
    
    def post(self):
        data = request.get_json()
        known_stages = {
                "Job Ready", "1st CSA Meeting Conducted", "Material Ready", "Job Seeking",
                "Contacted by Employer", "Closed Lost - Ghost", "Closed Won - Got an Interview"}
        
        this_student_hs_id = str(data.get('hubspot_id'))
        
        if this_student_hs_id in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
            logger.info(f"Skipping the job ready update. 200 OK")
            return {"message": f"Test students are ignored: {this_student_hs_id}"}, 200
        
        logger.info(f"GETTING_INTERVIEWS: incoming_payload - {this_student_hs_id}")
        
        job_ready_student_dict = parse_incoming_getting_passing_pipeline(data)
        
        this_stage = job_ready_student_dict.get("hubspot_current_deal_stage")
        this_student_cohort = job_ready_student_dict.get("active_cohort")
        student_name = job_ready_student_dict.get('student_first_name')
        student_surname = job_ready_student_dict.get('student_last_name')

        logger.info(f"The student {student_name} {student_surname} from {this_student_cohort} is in the {this_stage} stage")

        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=this_student_hs_id).first()
        
        if this_student is None:
            # Create new student, a new deal stage and a new cohort
            new_student_obj = JobReadyStudentModel(**job_ready_student_dict)
            student_stage_obj = StudentStagesV3(**create_stage_dict(this_student_hs_id, this_stage))
            student_cohort_obj = StudentCohortChangesModel(**create_cohort_dict(this_student_hs_id, this_student_cohort))
            
            write_object_to_db(new_student_obj)
            write_object_to_db(student_stage_obj)
            write_object_to_db(student_cohort_obj)
            
            logger.info(
                f"GETTING_INTERVIEWS: {student_name} {student_surname} - {this_stage} - ({this_student_hs_id}) Created")
            
            return {"message": f"getting_interviews: {this_stage} -  ({this_student_hs_id})"}, 201
        
        if this_stage in known_stages:
            # Update deal in the deal stages, update last stage in JobReadyStudentModel
            this_student.hubspot_current_deal_stage = this_stage
            this_student.updated_timestamp = datetime.datetime.now()
            stage_obj = StudentStagesV3(**create_stage_dict(this_student_hs_id, this_stage))
            
            write_object_to_db(stage_obj)
            
            logger.info(
                f"GETTING_INTERVIEWS: {student_name} {student_surname} - {this_stage} - ({this_student_hs_id}) Updated")
            
            return {"message": f"getting_interviews: {this_stage} - ({this_student_hs_id})"}, 201

        logger.error(f"GETTING INTERVIEWS: Unknown deal stage {this_stage} for {student_name} {student_surname} - ({this_student_hs_id})")
        return {"message": f"getting_interviews: Unknown Stage {this_stage} - ({this_student_hs_id})"}, 400
