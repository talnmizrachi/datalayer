from global_functions.LoggingGenerator import Logger
from global_functions.new_process_functions import *
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
import os
from models import ProcessModel, JobReadyStudentModel
from platforms_webhooks_catchers.hubspot.catch_pass_interview_closed_deal import v3_pass_close_deal_webhook_catcher


logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('Initiate a Process', __name__, description="A process is the combination of "
                                                                  "Company-Job-Student, and will include at least one"
                                                                  " process event")


@blueprint.route('/new_process_start', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process.
    It listens for a POST request at the '/new_process_start' endpoint open for the MS RnD team
    """
    
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='direct')
        
        return new_process_dict['id'], 201


@blueprint.route('/new_process_typeform', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    """
    def post(self):
        data = request.get_json()
        new_process_dict = parse_and_write_to_db_new_processes(data, source='typeform')
        
        return new_process_dict['id'], 201


@blueprint.route('/new_process_typeform_old', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    This is the old version of the typeform initiation endpoint.
    """
    
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='old_typeform')
        
        return new_process_dict['id'], 201


@blueprint.route('/new_process_smart_matcher', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This class handles the initiation of a new process via typeform (to be legacy).
    This is the old version of the typeform initiation endpoint.
    """
    
    def post(self):
        data = request.get_json()
        logger.info(data)
        new_process_dict = parse_and_write_to_db_new_processes(data, source='smart_matcher')
        
        return new_process_dict['id'], 201

@blueprint.route('/close_process', methods=['POST'])
class ProcessTermination(MethodView):
    """ Close process through hubspot workflow
    https://app.hubspot.com/workflows/9484219/platform/flow/584835155/edit
    
    Once a deal is closed (either closed won or closed lost, the process is terminated.
    
    """
    def post(self):
        
        data = request.get_json()
        logger.info(f"incoming data from hubspot: {data}")
        identifying_dict = v3_pass_close_deal_webhook_catcher(data)

        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=identifying_dict['hs_object_id']).first()
        
        if this_student is None:
            logger.error(f"Missing student from Job ready students: {identifying_dict}")
            
        this_deal = ProcessModel.query.filter_by(hubspot_id=identifying_dict['hs_object_id'],
                                                company_name=identifying_dict['company'],
                                                job_title=identifying_dict['job_title']
                                                ).first()
        if this_deal is None:
            logger.error(f"Deal with details: {identifying_dict} is not matching")
            abort(404, message='no deal found')
        
        process_id = this_deal.process_id
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
            # todo - write the code to get the current status after failre
            #  (either another process they have or Job seeking)
            logger.debug(f"lose_deal object : {this_deal}")
            this_deal.is_closed_won = False
            this_deal.is_process_active = False
            this_deal.process_end_date = date.today()
            if latest_stage:
                latest_stage.is_pass = "FALSE"
            db.session.commit()
            
        return data


@blueprint.route('/open_process_legacy', methods=['POST'])
class ProcessInitiation(MethodView):
    """
    This is for manual uploading, this will open the process, and after that the loading of stages and mocks should
    be done seperatlely.
    """
    
    def post(self):
        data = request.get_json()
        logger.info(data)
        
        process_exists = ProcessModel.query.filter_by(id= data['id']).first()
        if process_exists is not None:
            logger.debug(f"{process_exists} id already exists in the processes.")
            return f"{process_exists} id is missing from the job ready students.", 208
        new_process_obj = ProcessModel(**data)
        
        write_object_to_db(new_process_obj)
        
        return new_process_obj.id, 201


if __name__ == '__main__':
    pass
