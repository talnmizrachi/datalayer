import os
from global_functions.LoggingGenerator import Logger

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def get_mock_interviewer_data_from_zapier(incoming_webhook_data: dict) -> dict:
    """
    An incoming webhook from Zapier is used to get the interviewer data from calendly
    the data is moved from the url direction in the end of the typeform (when an interview is being set through there)
    (#todo - ask RnD to use the UTMs)
    UTMs can be found here:
    resources/mock_interviews.py -> mock_interview_setting blueprint
    
    and from there the data is moved to calendly's mechanism
    The Zap is catching any invite created in calendly and filters out based on the name of the event (contains "interview")
    and tracking utm source, medium, content and term existing in calendly's invite url.
    
    The data should be matched with the data in the mock_interview_setting blueprint
    
    This Zap:
    https://zapier.com/editor/243216601/draft/243216602/fields
    
    student_email - sent through the UTMs from typeform to the calendly and
     forwarded to the calendly invite url
     calendly_reg_email is the email the student registered with
    :return:
    """
    
    process_type = incoming_webhook_data.get('is_new_process')
    
    if process_type == "new_process":
        return_dict = {
                "calendly_reg_email": incoming_webhook_data.get('email').lower(),
                "student_email": incoming_webhook_data.get('utm_source').lower(),
                "company_name": incoming_webhook_data.get('utm_medium').title(),
                "job_title": incoming_webhook_data.get('utm_content').title(),
                "is_new_process": process_type,
                "student_name": incoming_webhook_data.get('student_name').title(),
                "mock_interview_datetime": incoming_webhook_data.get('mock_interview_datetime'),
                "additional_details": incoming_webhook_data.get('additional_details'),
                "mentor_email": incoming_webhook_data.get('mentor_email').lower(),
                "mentor_name": incoming_webhook_data.get('mentor_name').title(),
        }
    elif process_type == "continue_process":
        return_dict = {
                "calendly_reg_email": incoming_webhook_data.get('email').lower(),
                "process_id": incoming_webhook_data.get('utm_source'),
                "type_of_stage": incoming_webhook_data.get('utm_medium'),
                "stage_in_funnel": incoming_webhook_data.get('utm_content'),
                "is_new_process": process_type,
                "student_name": incoming_webhook_data.get('student_name').title(),
                "mock_interview_datetime": incoming_webhook_data.get('mock_interview_datetime'),
                "additional_details": incoming_webhook_data.get('additional_details'),
                "mentor_email": incoming_webhook_data.get('mentor_email').lower(),
                "mentor_name": incoming_webhook_data.get('mentor_name').title(),
        }
    else:
        return_dict = {"error": "Invalid type of process"}
    
    return return_dict
