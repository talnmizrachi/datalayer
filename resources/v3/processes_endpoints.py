from global_functions.new_process_functions import *
from global_functions.general_functions import delete_object_from_db
from resources.v3.continue_process_functions import parse_payload_and_write_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import datetime, timedelta
from db import db
import os
from models import ProcessModel, JobReadyStudentModel, StageModel
from platforms_webhooks_catchers.hubspot.catch_pass_interview_closed_deal import v3_pass_close_deal_webhook_catcher

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('Initiate a Process', __name__, description="A process is the combination of "
                                                                  "Company-Job-Student, and will include at least one"
                                                                  " process event")


@blueprint.route('/process_update', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process.
    
    Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit
    """
    
    def post(self):
        """
            We need to check if this process already exists in the database. If not, we create a new process,
            Process is defined as the combination of a company, title and student.
        """
        
        def utc_to_date(utc_timestamp):
            if utc_timestamp is not None:
                # Convert from milliseconds to seconds if necessary
                # This checks if the timestamp is far greater than typical Unix epoch time in seconds
                if utc_timestamp > 1e12:
                    utc_timestamp /= 1000
                return datetime.utcfromtimestamp(utc_timestamp).date()
            else:
                # Return today's date plus 7 days
                return datetime.utcnow().date() + timedelta(days=7)
        
        data = request.get_json()
        data["stage_date"] = utc_to_date(data.get("next_recruiting_step_date"))
        
        existing_process = ProcessModel.query.filter_by(hubspot_id=str(data['hs_object_id']),
                                                        company_name=data['company'],
                                                        job_title=data['job_title']).first()
        
        if existing_process:
            last_active_stage = StageModel.query.filter_by(process_id=existing_process.id, is_pass="PENDING").first()

        if existing_process is None and last_active_stage is None:
            # This is a new process
            logger.debug(f"New process initiated: {data}")
            process_id = parse_and_write_to_db_new_processes(data)
        elif existing_process and last_active_stage is None:
            delete_object_from_db(ProcessModel, existing_process)
            data['id'] = existing_process.id
            process_id = parse_and_write_to_db_new_processes(data)

        else:
            logger.debug("Passing through to existing process")
            process_id = parse_payload_and_write_to_db(data, existing_process.id)
            
        
        return process_id, 201


@blueprint.route('/close_process', methods=['POST'])
class ProcessTermination(MethodView):
    """ Close process through hubspot workflow
    https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit
    
    Once a deal is closed (either closed won or closed lost, the process is terminated.
    
    """
    
    def post(self):
        
        data = request.get_json()
        logger.info(f"incoming data from hubspot for a closed process: {data}")
        identifying_dict = v3_pass_close_deal_webhook_catcher(data)
        student_hs_id = identifying_dict['hs_object_id']
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=student_hs_id).first()
        
        if this_student is None:
            logger.error(f"Missing student from Job ready students: {identifying_dict}")
        
        this_deal = ProcessModel.query.filter_by(hubspot_id=student_hs_id,
                                                 company_name=identifying_dict['company'],
                                                 job_title=identifying_dict['job_title']
                                                 ).first()
        if this_deal is None:
            logger.error(f"Deal with details: {identifying_dict} is not matching")
            abort(404, message='no deal found')
        
        process_id = this_deal.id
        latest_stage = StageModel.query.filter_by(process_id=process_id).order_by(StageModel.created_at.desc()).first()
        if identifying_dict['hs_is_closed_won']:
            logger.debug(f"win_deal object : {this_deal}")
            this_deal.is_closed_won = True
            this_deal.is_process_active = False
            this_deal.process_end_date = date.today()
            if this_student is not None:
                this_student.is_employed = True
                this_student.hubspot_current_deal_stage = "Closed Won - Job Secured"
            if latest_stage:
                latest_stage.is_pass = "TRUE"
            db.session.commit()
        
        else:
            logger.debug(f"lose_deal object : {this_deal}")
            this_deal.is_closed_won = False
            this_deal.is_process_active = False
            this_deal.process_end_date = date.today()
            if latest_stage:
                latest_stage.is_pass = "FALSE"
                latest_stage.updated_at = datetime.now()
            
            get_other_processes_for_student(student_hs_id, process_id)
            
            db.session.commit()
        
        return data


def get_other_processes_for_student(student_hubspot_id, this_process_id):
    process_exists = ProcessModel.query.filter(
        ProcessModel.hubspot_id == student_hubspot_id,
        ProcessModel.id != this_process_id,
        ProcessModel.is_process_active == True).order_by(ProcessModel.updated_at.desc()).first()
    
    this_student = JobReadyStudentModel.query.filter_by(hubspot_id=student_hubspot_id)
    
    if process_exists is not None:
        active_stage = StageModel.query.filter_by(process_id=process_exists.id,
                                   is_pass="PENDING").order_by(StageModel.updated_at.desc()
                                                               ).first().deal_stage
        this_student.hubspot_current_deal_stage = active_stage
    else:
        this_student.hubspot_current_deal_stage = "Job Seeking"


@blueprint.route('/manual_process', methods=['POST'])
class ProcessTermination(MethodView):
    """ Close process through hubspot workflow
    https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit

    Once a deal is closed (either closed won or closed lost, the process is terminated.

    """
    
    def post(self):
        data = request.get_json()
        process_obj = ProcessModel(**data)
        
        write_object_to_db(process_obj)
        
        return process_obj.id, 201


@blueprint.route('/manual_process_stages', methods=['POST'])
class ProcessTermination(MethodView):
    """ Close process through hubspot workflow
    https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit

    Once a deal is closed (either closed won or closed lost, the process is terminated.

    """
    
    def post(self):
        data = request.get_json()
        stage_obj= StageModel(**data)
        
        write_object_to_db(stage_obj)
        
        return stage_obj.id, 201
if __name__ == '__main__':
    pass
