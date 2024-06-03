from uuid import uuid4


def payload_to_job_ready_student_dict(payload):
    job_ready_student_dict = {'id': str(uuid4().hex),
                              "masterschool_id": payload.get('masterschool_id'),
                              "hubspot_id": payload.get('hubspot_id'),
                              "domain": payload.get('domain'),
                              'student_firstname': payload.get('student_firstname'),
                              'student_lastname': payload.get('student_lastname'),
                              'student_email': payload.get('student_email'),
                              "student_country": payload.get('student_country'),
                              "student_state": payload.get('student_state'),
                              "student_city": payload.get('student_city'),
                              "student_github_link": payload.get('student_github_link'),
                              "student_linkedin_link": payload.get('student_linkedin_link'),
                              "student_cv_link": payload.get('student_cv_link'),
                              "languages_fluency": payload.get('languages_fluency'),
                              "tags": None,
                              "jaq": payload.get('jaq'),
                              "school_master_name": payload.get('school_master_name'),
                              "csa_hs_id": payload.get('csa_hs_id'),
                              }
    return job_ready_student_dict
