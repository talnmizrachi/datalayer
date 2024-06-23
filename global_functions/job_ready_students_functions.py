from uuid import uuid4
from flask_smorest import abort



def payload_to_job_ready_student_dict(payload):
    if payload.get('domain') is None:
        abort(404, message="Domain was not found")
    
    job_ready_student_dict = {'id': payload.get('id') or str(uuid4().hex),
                              "student_ms_id": payload.get('student_ms_id'),
                              "hubspot_id": payload.get('hs_object_id'),
                              "domain": payload.get('domain'),
                              "student_country": payload.get('student_country'),
                              "student_state": payload.get('student_state'),
                              "student_city": payload.get('student_city'),
                              "tags": None,
                              "jaq": payload.get('jaq'),
                              "school_master_name": payload.get('school_master_name'),
                              "csa_fullname": payload.get('hubspot_owner_id'),
                              "created_at": payload.get('created_at'),
                              "is_employed": payload.get('is_employed', False),
                              "hubspot_current_deal_stage": "Job Ready"
                              }
    
    stage_dict = {
            "student_id": job_ready_student_dict['id'],
            "hubspot_id": job_ready_student_dict['hubspot_id'],
            "stage": job_ready_student_dict['hubspot_current_deal_stage']
    }
    return job_ready_student_dict, stage_dict
