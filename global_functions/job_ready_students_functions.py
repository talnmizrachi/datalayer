from uuid import uuid4


def payload_to_job_ready_student_dict(payload):
    job_ready_student_dict = {'id': payload.get('id') or str(uuid4().hex),
                              "student_ms_id": payload.get('student_ms_id'),
                              "hubspot_id": payload.get('hubspot_id'),
                              "domain": payload.get('domain'),
                              'student_firstname': payload.get('student_firstname'),
                              'student_lastname': payload.get('student_lastname'),
                              'student_email': payload.get('student_email'),
                              "student_country": payload.get('student_country'),
                              "student_state": payload.get('student_state'),
                              "student_city": payload.get('student_city'),
                              "student_affiliation_project": payload.get('student_affiliation_project'),
                              "student_linkedin_link": payload.get('student_linkedin_link'),
                              "student_cv_link": payload.get('student_cv_link'),
                              "languages_fluency": payload.get('languages_fluency'),
                              "tags": None,
                              "jaq": payload.get('jaq'),
                              "school_master_name": payload.get('school_master_name'),
                              "csa_hs_id": payload.get('csa_hs_id'),
                              "created_at": payload.get('created_at'),
                              "smart_matcher_notification": payload.get('smart_matcher_notification'),
                              }
    return job_ready_student_dict
