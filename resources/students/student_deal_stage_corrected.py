import datetime
from sqlalchemy import and_
from global_functions.ignoring_constants import MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE
from uuid import uuid4
from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db, update_objects_in_session
from global_functions.time_functions import utc_to_date
from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import deal_stage_dict
from platforms_webhooks_catchers.hubspot.get_owner_name import get_owner_name
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel, StudentStagesV3, StudentCohortChangesModel, ProcessModel, StageModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint("deals' change from hubspot - Second version", __name__,
                      description="This_is_a_templated_blueprint")


def update_student_stage(this_student, this_process, this_stage):
    if this_student is not None:
        this_student.hubspot_current_deal_stage = this_stage
        this_student.updated_timestamp = datetime.datetime.now()
    
    this_process.latest_stage = this_stage
    this_process.updated_at = datetime.datetime.now()

    logger.info(f"Updated stage to {this_stage} for student {this_student}")
    update_objects_in_session()


def next_stager(this_stage):
    stages = [
            "1st Stage", "2nd Stage", "3rd Stage", "4th Stage",
            "5th Stage", "6th Stage", "7th Stage", "8th Stage", "9th Stage",
            "10th Stage", "11th Stage", "12th Stage", ]
    try:
        return stages[stages.index(this_stage) + 1]
    except ValueError:
        return f"{this_stage} + 1"


def split_process_and_stage_dict(payload_dict):
    def rename_key(d, old_key, new_key):
        if old_key in d:
            d[new_key] = d.pop(old_key)
        return d
    
    process_keys = {"id", "hubspot_id", "domain", 'hubspot_deal_id',
                    "company_name", "job_title", 'process_start_date','student_first_name', 'student_last_name',
                    'source_1', 'source_2'}
    
    stage_keys = {"id", 'hubspot_deal_id', "stage_in_funnel", "type_of_stage", "deal_stage", 'stage_date'}
    
    process_dict = {k: v for k, v in payload_dict.items() if k in process_keys}
    stage_dict = {k: v for k, v in payload_dict.items() if k in stage_keys}
    rename_key(stage_dict, 'id', 'process_id')
    
    stage_dict['id'] = str(uuid4().hex)
    process_dict['latest_stage'] = stage_dict['deal_stage']
    logger.info(f"Created process dict {process_dict}")
    logger.info(f"Created stage dict {stage_dict}")
    
    return process_dict, stage_dict


def create_cohort_dict(this_student_hs_id_, active_cohort_):
    cohort_dict = {
            "hubspot_id": this_student_hs_id_,
            "student_cohort": active_cohort_
        
    }
    return cohort_dict


def create_stage_dict(this_student_hs_id_, this_stage_, company_=None):
    stage_dict = {
            "hubspot_id": this_student_hs_id_,
            "stage": this_stage_
    }
    if company_ is not None:
        stage_dict["company_if_rel"] = company_
        
    return stage_dict


def parse_incoming_getting_passing_pipeline(data):
    pipeline_dict = {}
    deal_stage_dictionary = deal_stage_dict()
    piepline = data.get("pipeline")
    # Getting Interviews
    if piepline == 95522316:
        pipeline_dict = {
                "hubspot_id": str(data.get('hubspot_id')),
                "student_first_name": data.get('student_first_name'),
                "student_last_name": data.get('student_last_name'),
                "schoolmaster_id": data.get('schoolmaster_id'),
                "domain": data.get('domain'),
                "hubspot_current_deal_stage": deal_stage_dictionary.get(data['dealstage']),
                "active_cohort": data.get('active_cohort'),
                "student_owner": get_owner_name(data.get('student_owner', None)),
                "current_program": data.get('bg___program')
        }
        return pipeline_dict
    
    # Passing Interviews
    elif piepline == 95255387:
        
        pipeline_dict = {
                "id": str(uuid4().hex),
                "hubspot_deal_id": str(data.get('hubspot_deal_id')),
                "hubspot_id": str(data.get('hubspot_id')),
                "student_first_name": data.get('student_first_name'),
                "student_last_name": data.get('student_last_name'),
                "domain": data.get('domain'),
                "company_name": data.get('company_name'),
                "job_title": data.get('job_title'),
                "process_start_date": utc_to_date(data.get('createdate')),
                "type_of_stage": data.get("next_recruiting_step_type"),
                "deal_stage": deal_stage_dictionary.get(data['dealstage']),
                "stage_date": utc_to_date(data.get("next_recruiting_step")),
                "stage_in_funnel": "1st Stage",
        }
    
    # V3 Payments
    elif piepline == 107256463:
        ...
    
    return pipeline_dict


@blueprint.route('/deal_stage_change_getting_interviews', methods=['POST'])
class JobReadyStudentDealChange(MethodView):
    
    def post(self):
        logger.info(f"GETTING_INTERVIEWS: Hello world")
        data = request.get_json()
        known_stages = ("Job Ready", "1st CSA Meeting Conducted", "Material Ready", "Job Seeking",
                        "Contacted by Employer", "Closed Lost - Ghost", "Closed Won - Got an Interview")
        if data['hubspot_id'] in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
            logger.info(f"Skipping the job ready update. 200 OK")
            return {"message": f"Test students are ignored: {data['hubspot_id']}"}, 200
        
        logger.info(f"GETTING_INTERVIEWS: incoming_payload - {data['hubspot_id']}")
        
        job_ready_student_dict = parse_incoming_getting_passing_pipeline(data)
        
        this_stage = job_ready_student_dict.get("hubspot_current_deal_stage")
        this_student_hs_id = job_ready_student_dict.get("hubspot_id")
        this_student_cohort = job_ready_student_dict.get("active_cohort")
        student_name = job_ready_student_dict.get('student_first_name')
        student_surname = job_ready_student_dict.get('student_last_name')
        
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=this_student_hs_id).first()
        
        if this_student is None:
            # Create new student, a new deal stage and a new cohort
            new_student_obj = JobReadyStudentModel(**job_ready_student_dict)
            deal_stage_dict = create_stage_dict(this_student_hs_id, this_stage)
            student_stage_obj = StudentStagesV3(**deal_stage_dict)
            student_cohort_obj = StudentCohortChangesModel(
                **create_cohort_dict(this_student_hs_id, this_student_cohort))
            
            write_object_to_db(new_student_obj)
            write_object_to_db(student_stage_obj)
            write_object_to_db(student_cohort_obj)
            
            logger.info(f"GETTING_INTERVIEWS: {student_name} {student_surname} - {this_stage} - ({this_student_hs_id})"
                        f"Created")
            
            return {"message": f"getting_interviews: {this_stage} -  ({this_student_hs_id})"}, 201
        
        elif this_stage in known_stages:
            # Update deal in the deal stages, update last stage in JobReadyStudentModel
            this_student.hubspot_current_deal_stage = job_ready_student_dict.get('hubspot_current_deal_stage')
            this_student.updated_timestamp = datetime.datetime.now()
            stage_obj = StudentStagesV3(**create_stage_dict(this_student_hs_id, this_stage))

            write_object_to_db(stage_obj)
            
            logger.info(f"GETTING_INTERVIEWS: {student_name} {student_surname} - {this_stage} - ({this_student_hs_id})"
                        f" Updated")
            message = {"message": f"getting_interviews: {this_stage} -  ({this_student_hs_id})"}
            
            return message, 201
        
        else:
            logger.error(f"GETTING INTERVIEWS : Unknown deal stage : {this_stage} - {student_name} {student_surname} - {this_student_hs_id}")
            return {"message": f"getting_interviews: Unknown Stage {this_stage} -  ({this_student_hs_id})"}


def get_current_process(hubspot_id_, company_name_, job_title_):
    this_process_ = ProcessModel.query.filter_by(hubspot_id=hubspot_id_,
                                                 company_name=company_name_,
                                                 job_title=job_title_).first()
    
    return this_process_


def create_new_process_and_stage(job_ready_student_dict_, write_to_db=True):
    logger.info(f"PASSING_INTERVIEWS: Entering create_new_process_and_stage function")
    process_dict, stage_dict = split_process_and_stage_dict(job_ready_student_dict_)
    
    process_obj = ProcessModel(**process_dict)
    stage_obj = StageModel(**stage_dict)
    
    if write_to_db:
        logger.info(f"PASSING_INTERVIEWS: Creating new process, stage an deal stage")
        write_object_to_db(process_obj)
        write_object_to_db(stage_obj)
        
    return process_obj, stage_obj

    
# def close_and_update_process_as_win(_this_process, _past_stage, new_stage=None):
#     logger.info(f"PASSING_INTERVIEWS: updating_closed_won for {_this_process.student_first_name} {_this_process.student_last_name} in {_this_process.company_name} - {_this_process.job_title}")
#     _this_process.is_employed = True
#     _this_process.latest_stage = "Closed Won"
#     _this_process.is_closed_won = True
#     logger.info(f"PASSING_INTERVIEWS: thi process is active before {_this_process.is_process_active}")
#     _this_process.is_process_active = False
#     logger.info(f"PASSING_INTERVIEWS: thi process is active after {_this_process.is_process_active}")
#     _this_process.job_secured_date = datetime.datetime.now()
#     _this_process.updated_at = datetime.datetime.now()
#     _this_process.process_end_date = datetime.datetime.now()
#     logger.info(f"PASSING_INTERVIEWS: Closed won for {_past_stage}")
#     _past_stage.is_pass = "TRUE"
#
#     _past_stage.updated_at = datetime.datetime.now()
#
#     if new_stage is not None:
#         new_stage.is_pass = "TRUE"
#
#     update_objects_in_session()


@blueprint.route('/deal_stage_change_passing_interviews', methods=['POST'])
class JobReadyStudentDealChange(MethodView):
    """
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit

    """
    
    def post(self):
        data = request.get_json()
        
        if data['hubspot_id'] in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
            logger.info(f"Skipping the job ready update. 200 OK")
            return {"message": f"Test students are ignored: {data['hubspot_id']}"}, 200
        
        past_stage_in_funnel = "1st Stage"
        past_stage, new_stage_obj = None, None
        
        job_ready_student_dict = parse_incoming_getting_passing_pipeline(data)
        logger.info(f"PASSING_INTERVIEWS: incoming_payload - job_ready_student_dict")
        
        this_stage = job_ready_student_dict.get("deal_stage")
        this_student_hs_id = job_ready_student_dict.get("hubspot_id")
        this_process_company = job_ready_student_dict['company_name']
        this_process_title = job_ready_student_dict['job_title']
        write_object_to_db(StudentStagesV3(**create_stage_dict(this_student_hs_id, this_stage, this_process_company)))
        
        # check if student, process, process stage exists
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=this_student_hs_id).first()
        this_process = get_current_process(this_student_hs_id, this_process_company, this_process_title)
        if this_process is not None:
            past_stage = StageModel.query.filter_by(process_id=this_process.id, is_pass='PENDING').first()
        
        logger.info(f"PASSING_INTERVIEWS: Got this student - {this_student}")
        logger.info(f"PASSING_INTERVIEWS: Got this process - {this_process}")
        
        # There is no process listed
        if this_process is None:
            logger.info(f"PASSING_INTERVIEWS: No process found for {job_ready_student_dict['student_first_name']} {job_ready_student_dict['student_last_name']}")
            this_process, new_stage_obj = create_new_process_and_stage(job_ready_student_dict, write_to_db=True)
            if this_student is not None:
                logger.info(f"PASSING_INTERVIEWS: The process is None and this student is not None")
                update_student_stage(this_student, this_process, this_stage)
        logger.info(f"This stage is {this_stage}")
        
        if this_stage in ("First Interview Scheduled", "First Interview", "Additional Interview", "Final Interview",
                          "Job Offer Received"):
            # if there is a process - create a stage
            # if there's no process - create a new process, and a new stage
            # Update JobReadyStudentModel
            update_student_stage(this_student, this_process, this_stage)
            
            # Update process, update past stage, create new stage
            if past_stage is not None:
                logger.info("Past stage is not None")
                past_stage.is_pass = "TRUE"
                past_stage.updated_at = datetime.datetime.now()
                past_stage_in_funnel = past_stage.stage_in_funnel
            if new_stage_obj is None:
                _, new_stage_obj = create_new_process_and_stage(job_ready_student_dict, write_to_db=False)
                new_stage_obj.process_id = this_process.id
                new_stage_obj.stage_in_funnel = next_stager(past_stage_in_funnel)
            
                this_process.updated_at = datetime.datetime.now()
                write_object_to_db(new_stage_obj)
            
            return {"message": f"passing_interviews: {this_stage} -  ({this_student_hs_id})"}, 201
        
        if this_stage == "Closed Won - Job Secured":
            close_and_update_process_as_win(this_process, past_stage)
            return {"message": f"passing_interviews: {this_stage} -  ({this_student_hs_id})"}, 201
        
        if this_stage == 'Double':
            return {"message": f"passing_interviews: {this_stage} -  ({this_student_hs_id})"}
        
        logger.debug(f"Unhandled stage: {past_stage}")
        if this_stage in ("Closed Lost - Job Not Secured", "Fraudulent"):
            # Check if we have another process, if so - take the last stage, if not - return to Job seeking
            # Update process as closed, and stage as closed
            logger.info("Closed lost or Fraud, update existing process for failure")
            logger.debug(f"Unhandled stage: {past_stage}")
            past_stage.is_pass = "CANCELLED"
            past_stage.updated_at = datetime.datetime.now()
            this_process.process_end_date = datetime.date.today()
            this_process.is_process_active = False
            this_process.updated_at = datetime.datetime.now()
            this_process.is_closed_won = False
            this_process.latest_stage = this_stage
            update_objects_in_session()
            
            # Check if the student has other open processes
            other_process = ProcessModel.query.filter(
                and_(
                    ProcessModel.hubspot_id == this_student_hs_id,
                    ProcessModel.id != this_process.id,
                    ProcessModel.is_process_active == True,
                    )
            ).first()
            
            if other_process is None:
                if this_student is not None:
                    this_student.hubspot_current_deal_stage = "Job Seeking"
                else:
                    logger.info(f"No other open processes found for {job_ready_student_dict['student_first_name']} {job_ready_student_dict['student_last_name']}")
                    return {"message": f"passing_interviews: {this_stage} -  ({this_student_hs_id})"}
            else:
                if this_student is not None:
                    this_student.hubspot_current_deal_stage = other_process.latest_stage
                    return {"message": f"passing_interviews: {this_stage} -  ({this_student_hs_id})"}
                else:
                    return {"message": f"passing_interviews: {this_stage} -  ({this_student_hs_id})"}
        
        if this_stage == "Special Cases":
            update_student_stage(this_student, this_process, this_stage)
            past_stage.is_pass = "CANCELLED"
            this_process.latest_stage = this_stage
            this_process.updated_at = datetime.datetime.now()
            this_process.process_end_date = datetime.date.today()
            this_process.is_process_active = False
            update_objects_in_session()
            return {"message": f"passing_interviews: {this_stage} -  ({this_student_hs_id})"}
        
        else:
            return {"message": f"NO REAL STAGE NAME passing_interviews: {this_stage}"}
    
