import datetime


def catch_student_application_from_campus(payload, source):
    """
    Catch student application from the campus
    
    payload looks like this:
    {"job_id": "123456",
    "student_id": ""
    "job_published_timestamp": ""
    "job_offered_to_student_timestamp": ""
    "student_applied": ""
    "no_apply_reason": ""
    "location": ""
    }
    
    """
    
    this_dict = {"job_id": payload.get("job_id"),
                 "student_id": payload.get("student_id"),
                 "job_published_timestamp": payload.get("job_published_timestamp"),
                 "job_offered_to_student_timestamp": payload.get('job_offered_to_student_timestamp'),
                 "student_applied": True if payload.get("student_applied") == 'applied' else False,
                 "student_response_timestamp": datetime.datetime.now(),
                 "no_apply_reason": payload.get("no_apply_reason"),
                 "student_location_search": payload.get("location"),
                 "source": source
                 }
    
    return this_dict
