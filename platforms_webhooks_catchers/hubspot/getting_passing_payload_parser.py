from uuid import uuid4
from global_functions.time_functions import utc_to_date
from platforms_webhooks_catchers.hubspot.catch_job_ready_change_in_deal_stage import deal_stage_dict
from platforms_webhooks_catchers.hubspot.get_owner_name import get_owner_name
from global_functions.LoggingGenerator import Logger
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def parse_incoming_getting_passing_pipeline(data):
    pipeline_dict = {}
    deal_stage_dictionary = deal_stage_dict()
    piepline = str(data.get("pipeline"))
    # Getting Interviews
    if piepline == "95522316":
        logger.info(f"GETTING_PIPELINES: incoming_payload - {data}")
        pipeline_dict = {
                "hubspot_id": str(data.get('hubspot_id')),
                "student_first_name": data.get('student_first_name'),
                "student_last_name": data.get('student_last_name'),
                "schoolmaster_id": data.get('schoolmaster_id'),
                "domain": data.get('domain'),
                "hubspot_current_deal_stage": deal_stage_dictionary.get(str(data['dealstage'])),
                "active_cohort": data.get('active_cohort'),
                "student_owner": get_owner_name(data.get('student_owner', None)),
                "current_program": data.get('bg___program')
        }
        if "created_at" in data:
            pipeline_dict["created_at"] = data.get("created_at")
            pipeline_dict["updated_timestamp"] = data.get("created_at")
        return pipeline_dict
    
    # Passing Interviews
    elif piepline == "95255387":
        
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
                "deal_stage": deal_stage_dictionary.get(str(data['dealstage'])),
                "stage_date": utc_to_date(data.get("next_recruiting_step")),
                "stage_in_funnel": "1st Stage",
        }
    
    # V3 Payments
    elif piepline == "107256463":
        ...
    
    return pipeline_dict
