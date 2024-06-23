from global_functions.LoggingGenerator import Logger
from db import db
from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import job_ready_catch_deal_stage
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from models import JobReadyStudentModel

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()

blueprint = Blueprint("deals' change from hubspot", __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/deal_stage_change', methods=['POST'])
class JobReadyStudent(MethodView):
    
    def post(self):
        data = request.get_json()
        logger.info(f"Got a deal change:\t{data}")
        job_ready_student_dict = job_ready_catch_deal_stage(data)
        this_student = JobReadyStudentModel.query.filter_by(hubspot_id=job_ready_student_dict['hubspot_id']).first()
        if this_student is None:
            return  f"{this_student} id is missing from the job ready students.", 404
        logger.info(f"Th student {this_student} changed from {this_student.hubspot_current_deal_stage} to"
                    f" {job_ready_student_dict.get('hubspot_current_deal_stage')}")
        
        this_student.hubspot_current_deal_stage = job_ready_student_dict.get('hubspot_current_deal_stage')
        
        db.session.commit()
        
        return str(job_ready_student_dict['hubspot_id']), 201

