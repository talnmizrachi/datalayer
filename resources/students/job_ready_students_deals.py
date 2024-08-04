import datetime
from global_functions.ignoring_constants import MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE
import sqlalchemy

from global_functions.LoggingGenerator import Logger
from db import db
from global_functions.general_functions import write_object_to_db
from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import job_ready_catch_deal_stage, \
    deal_stage_dict
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentStagesV3

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("deals' change from hubspot", __name__, description="This_is_a_templated_blueprint")


def change_last_deal_to_deal_with_relevance(hubspot_id, current_deal):
    valid_stages = ("First Interview Scheduled", "First Interview",
                    "Additional Interview", "Final Interview", "Job Offer Received")
    stages = StudentStagesV3.query.filter_by(hubspot_id=hubspot_id).order_by(
        StudentStagesV3.created_at.desc()).all()
    
    if current_deal in ("Fraudulent", "Closed Lost - Job Not Secured"):
        for stage in stages:
            if stage.stage in valid_stages:
                return stage.stage
            else:
                return "Job Seeking"
    
    if current_deal in ("Double", "Closed Won - Got an Interview"):
        return "Closed Won - Got an Interview"
    
    return current_deal


@blueprint.route('/deal_stage_change', methods=['POST'])
class JobReadyStudent(MethodView):
    """
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit
    
    Included deals - Getting Interviews, Passing Interviews
    
    incoming payload -
    {"dealstage":
    "hs_object_id":
    "hubspot_owner_id":
    }
    """
    
    def post(self):
        data = request.get_json()
        
        if data['hs_object_id'] in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
            logger.info(f"Test student: {data['hs_object_id']} is a test student. Skipping the job ready update. 200 OK")
            return {"message": f"Test students are ignored: {data['hs_object_id']}"}, 200
        
        logger.info(f"Got a deal change:\t{data}")
        job_ready_student_dict = job_ready_catch_deal_stage(data)
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=job_ready_student_dict['hubspot_id']).first()
        
        if this_student is None:
            return f"{this_student} id is missing from the job ready students.", 404
        
        this_stage = job_ready_student_dict.get("hubspot_current_deal_stage")
        correct_stage = change_last_deal_to_deal_with_relevance(job_ready_student_dict['hubspot_id'], this_stage)
        
        if correct_stage  == "Closed Won - Job Secured":
            this_student.is_employed = True
        
        this_student.hubspot_current_deal_stage = correct_stage
        this_student.student_owner = job_ready_student_dict.get('csa_fullname')
        this_student.current_program = job_ready_student_dict.get('current_program')
        this_student.updated_timestamp = datetime.datetime.now()
        this_student.student_first_name = job_ready_student_dict.get('firstname')
        this_student.student_last_name = job_ready_student_dict.get('lastname')
        
        stage_dict = {
                      "hubspot_id": this_student.hubspot_id,
                      "stage": correct_stage,
                      "company_if_rel": job_ready_student_dict.get('company')
                      }
        student_stage_obj = StudentStagesV3(**stage_dict)
        write_object_to_db(student_stage_obj)
        
        return str(job_ready_student_dict['hubspot_id']), 201


@blueprint.route('/manual_deal_stage_change', methods=['POST'])
class JobReadyStudent(MethodView):
    """

    """
    
    def post(self):
        
        def convert_to_datetime(date_str):
            # Parse the datetime string to a datetime object
            dt_with_timezone = datetime.datetime.fromisoformat(date_str)
            # Remove the timezone info
            dt_without_timezone = dt_with_timezone.replace(tzinfo=None)
            return dt_without_timezone
        
        data = request.get_json()
        logger.info(f"Got a manual deal change:\t{data['created_at']}")
        id_to_name = deal_stage_dict()

        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()
        
        if this_student is None:
            logger.error(f"Student with hubspot_id {data['hubspot_id']} doesn't exist")
            response = {"message": f"Student doesn't exist", "student": data}
            return response, 202
        
        stage_dict = {
                      "hubspot_id": data['hubspot_id'],
                      "stage": id_to_name.get(int(data["deal_stage"])),
                      "created_at": convert_to_datetime(data['created_at']),
                      }
        
        logger.info(f"Stage Created at: {stage_dict['created_at']}")
        
        existing_entry = (StudentStagesV3.
                          query.
                          filter(StudentStagesV3.hubspot_id == stage_dict['hubspot_id'],
                                 StudentStagesV3.stage == stage_dict['stage'],
                                 sqlalchemy.func.date(StudentStagesV3.created_at) == stage_dict['created_at'].date()).
                          first())

        if existing_entry is None:
            student_stage_obj = StudentStagesV3(**stage_dict)
            write_object_to_db(student_stage_obj)
            response = {"message": f"Success", "hubspot_id": this_student.hubspot_id, "stage": stage_dict["stage"]}
        else:
            logger.info(f"Stage for {stage_dict['hubspot_id']} already listed with {stage_dict['stage']} on {stage_dict['created_at'].date()}")
            response = {"message": f"Success with hold", "hubspot_id": this_student.hubspot_id, "stage": stage_dict["stage"]}
            
        return response, 201