# import datetime
# from global_functions.ignoring_constants import MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE
# import sqlalchemy
# from global_functions.LoggingGenerator import Logger
# from db import db
# from global_functions.general_functions import write_object_to_db
# from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import job_ready_catch_deal_stage, \
#     deal_stage_dict
# from flask import request
# from flask.views import MethodView
# from flask_smorest import Blueprint
# import os
# from models import JobReadyStudentModel, StudentStagesV3
#
# logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
#
# blueprint = Blueprint("deals' change from hubspot - Second version", __name__, description="This_is_a_templated_blueprint")
#
#
# @blueprint.route('/deal_stage_change_2', methods=['POST'])
# class JobReadyStudent(MethodView):
#     """
#     Workflow URL - https://app.hubspot.com/workflows/9484219/platform/flow/587156903/edit
#
#     Included deals - Getting Interviews, Passing Interviews
#
#     incoming payload -
#     {"dealstage":
#     "hs_object_id":
#     "hubspot_owner_id":
#     }
#     """
#
#     def post(self):
#         data = request.get_json()
#
#         if data['hs_object_id'] in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
#             logger.info(f"Skipping the job ready update. 200 OK")
#             return {"message": f"Test students are ignored: {data['hs_object_id']}"}, 200
#
#         job_ready_student_dict = job_ready_catch_deal_stage(data)
#
#         this_stage = job_ready_student_dict.get("hubspot_current_deal_stage")
#         this_student_hs_id = job_ready_student_dict.get("hubspot_id")
#
#         this_student = JobReadyStudentModel.query.filter_by(hubspot_id=this_student_hs_id).first()
#
#         if this_student is None and this_stage == 'Job Ready':
#             # Create new student
#             ...
#         if this_student is None and this_stage != 'Job Ready':
#             # Student doesn't exist and this stage is not Job Ready -> when we get an interview unintended
#             ...
#
#
#