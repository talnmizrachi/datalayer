import datetime

from global_functions.LoggingGenerator import Logger
from db import db
from global_functions.general_functions import write_object_to_db
from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import job_ready_catch_deal_stage
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentStagesV3

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("deals' change from hubspot", __name__, description="This_is_a_templated_blueprint")


def change_last_deal_to_deal_with_relevance(this_student_id, current_deal):
    valid_stages = ("First Interview Scheduled", "First Interview",
                    "Additional Interview", "Final Interview", "Job Offer Received")
    stages = StudentStagesV3.query.filter_by(student_id=this_student_id).order_by(
        StudentStagesV3.created_at.desc()).all()
    
    if current_deal in ("Fraudulent", "Closed Lost - Job Not Secured"):
        for stage in stages:
            if stage.stage in valid_stages:
                return stage.stage
            else:
                return "Job Seeking"
    
    if current_deal in ("Double"):
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
        logger.info(f"Got a deal change:\t{data}")
        job_ready_student_dict = job_ready_catch_deal_stage(data)
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=job_ready_student_dict['hubspot_id']).first()
        
        if this_student is None:
            return f"{this_student} id is missing from the job ready students.", 404
        
        this_stage = job_ready_student_dict.get("hubspot_current_deal_stage")
        correct_stage = change_last_deal_to_deal_with_relevance(this_student.id, this_stage)
        
        if this_stage == "Closed Won - Job Secured":
            this_student.is_employed = True
        
        this_student.hubspot_current_deal_stage = correct_stage
        this_student.student_owner = job_ready_student_dict.get('csa_fullname')
        this_student.updated_timestamp = datetime.datetime.now()
        
        stage_dict = {"student_id": this_student.id,
                      "hubspot_id": this_student.hubspot_id,
                      "stage": this_stage,
                      }
        student_stage_obj = StudentStagesV3(**stage_dict)
        write_object_to_db(student_stage_obj)
        
        return str(job_ready_student_dict['hubspot_id']), 201
