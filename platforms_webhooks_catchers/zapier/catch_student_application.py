import datetime


def catch_student_application_from_zapier(payload, source):
    """
    Catch student application from zapier -  https://zapier.com/editor/217954973/published
    This is stricctly from the smart matcher
    """
    
    this_dict = {"job_id": payload.get("job_id"),
                 "student_id": payload.get("student_id"),
                 "job_published_timestamp": payload.get("job_published_timestamp"),
                 "job_offered_to_student_timestamp": payload.get('job_offered_to_student_timestamp'),
                 "student_applied": payload.get("student_applied"),
                 "student_response_timestamp": datetime.datetime.now(),
                 "no_apply_reason": payload.get("no_apply_reason"),
                 "student_location_search": payload.get("location"),
                 "source": source
                 }
    
    return this_dict
