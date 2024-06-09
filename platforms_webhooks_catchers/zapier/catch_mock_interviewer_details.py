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
    :return:
    """
    
    return_dict = {"additional_details": incoming_webhook_data.get('additional_details'),
                   "mentor_email": incoming_webhook_data.get('mentor_email'),
                   "mentor_name": incoming_webhook_data.get('mentor_name'),
                   "mock_interview_datetime": incoming_webhook_data.get('mock_interview_datetime'),
                   "process_id": incoming_webhook_data.get('process_id'),
                   "stage_in_funnel": incoming_webhook_data.get('stage_in_funnel'),
                   "type_of_process": incoming_webhook_data.get('type_of_process'),
                   "type_of_stage": incoming_webhook_data.get('type_of_stage')
                   }
    
    return return_dict

