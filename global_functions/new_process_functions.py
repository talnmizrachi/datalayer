from uuid import uuid4
from datetime import date
from models import Process, Stage
from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import abort


def rename_key(d, old_key, new_key):
    if old_key in d:
        d[new_key] = d.pop(old_key)
    return d


def split_process_and_stage_dict(payload_dict):
    process_keys = {"id", "student_id", "student_firstname", "student_lastname", "domain", "email_address",
                    "company_name", "job_title", "job_description", 'cv_url', 'process_start_date',
                    'source_1', 'source_2'}
    
    stage_keys = {"id", "stage_in_funnel",'student_firstname', 'student_lastname', "type_of_stage", "had_home_assignment", 'home_assignment_questions',
                  'home_assignment_answers', 'stage_date'}
    
    process_dict = {k: v for k, v in payload_dict.items() if k in process_keys}
    stage_dict = {k: v for k, v in payload_dict.items() if k in stage_keys}
    rename_key(stage_dict, 'id', 'process_id')
    stage_dict['id'] = str(uuid4().hex)
    
    return process_dict, stage_dict


def parse_and_write_to_db_new_processes(incoming_data, source='direct'):
    if source == 'direct':
        process_dict, stage_dict = direct_payload_to_new_process_dict(incoming_data)
    elif source == 'typeform':
        process_dict, stage_dict = typeform_payload_to_new_process_dict(incoming_data)
    else:
        abort(400, message="source must be 'direct' or 'typeform'")
    new_process_object = Process(**process_dict)
    new_stage_object = Stage(**stage_dict)

    try:
        db.session.add(new_process_object)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message=str(e))
    
    try:
        db.session.add(new_stage_object)
        db.session.commit()
    except SQLAlchemyError as e:
        db.session.rollback()
        abort(500, message=str(e))
    
    return process_dict


def direct_payload_to_new_process_dict(direct_payload):
    job_ready_student_dict = {
            "id": str(uuid4().hex),
            "job_id": direct_payload.get("job_id"),
            "student_id": direct_payload.get("student_id"),
            "email_address": direct_payload.get("email_address"),
            "student_firstname": direct_payload.get("student_firstname"),
            "student_lastname": direct_payload.get("student_lastname"),
            "domain": direct_payload.get("domain"),
            "company_name": direct_payload.get("company_name"),
            "job_title": direct_payload.get("job_title"),
            "job_description": direct_payload.get("job_description"),
            "drive_url": direct_payload.get("drive_url"),
            "process_start_date": date.today(),
            "stage_in_funnel": direct_payload.get("stage_in_funnel"),
            "type_of_stage": direct_payload.get("type_of_stage"),
            "had_home_assignment": direct_payload.get("had_home_assignment"),
            "home_assignment_questions": direct_payload.get("home_assignment_questions"),
            "home_assignment_answers": direct_payload.get("home_assignment_answers"),
            "stage_date": direct_payload.get("stage_date"),
    }
    
    process_dict, stage_dict = split_process_and_stage_dict(job_ready_student_dict)
    
    return process_dict, stage_dict


def typeform_payload_to_new_process_dict(typeform_payload):
    typeform_questions_ids_ = {
            "uGidsoDwfCES": "domain",
            "FBYMmvdFNhfw": "email_address",
            "Kys4EcJ4WViT": "full_name",
            "hhV0z2H3bFbC": "company_name",
            "dQbDwUKSTl7G": "job_title",
            "xeaPZrcMGmR4": "stage_date",
            "yFyfpcjPDaal": "stage_in_funnel",
            "BFsWH2TPzBlH": "had_home_assignment",
            "qgbW21oTd1mO": "home_assignment_questions",
            "BzKp7H4TwZxn": "home_assignment_answers",
            "BVIHyvpqVsNS": "type_of_stage",
            "YIXeDQWMVqLr": "resume_url",
            "06oyTS92IyDZ": "job_description",
            "n6j9MkBtbqcF": "source_1",
            "ysVEuC3W9lKV": "source_2",
    }
    
    new_dict = {}
    for answer in typeform_payload['form_response']['answers']:
        key = typeform_questions_ids_.get(answer['field']['id'])
        if key is None:
            continue
        if key == 'full_name':
            name_parts = answer['text'].split(" ")
            new_dict['student_firstname'] = " ".join(name_parts[:-1])
            new_dict['student_lastname'] = name_parts[-1]
            continue
        value = answer.get('choice', {}).get('other') or answer.get('choice', {}).get('label', answer.get(answer['type']))
        new_dict[key] = value
    
    new_dict['id'] = str(uuid4().hex)
    new_dict['drive_url'] = "drive_url"
    new_dict['process_start_date'] = new_dict['stage_date']
    
    process_dict, stage_dict = split_process_and_stage_dict(new_dict)
    
    return process_dict, stage_dict


if __name__ == '__main__':
    import json
    
    direct_payload = {
    "job_id": "job_id",
    "student_id": "student_id",
    "email_address": "email_address",
    "student_firstname": "student_firstname",
    "student_lastname": "student_lastname",
    "domain": "domain",
    "company_name": "company_name",
    "job_title": "job_title",
    "job_description": "job_description",
    "drive_url": "drive_url",
    "process_start_date": "process_start_date",
    "stage_in_funnel": "stage_in_funnel",
    "type_of_stage": "type_of_stage",
    "had_home_assignment": "had_home_assignment",
    "home_assignment_questions": "home_assignment_questions",
    "home_assignment_answers": "home_assignment_answers",
    "stage_date": "stage_date",
    
    
    }
    job_ready_student_dict = {
            "id": str(uuid4().hex),
            "job_id": direct_payload.get("job_id"),
            "student_id": direct_payload.get("student_id"),
            "email_address": direct_payload.get("email_address"),
            "student_firstname": direct_payload.get("student_firstname"),
            "student_lastname": direct_payload.get("student_lastname"),
            "domain": direct_payload.get("domain"),
            "company_name": direct_payload.get("company_name"),
            "job_title": direct_payload.get("job_title"),
            "job_description": direct_payload.get("job_description"),
            "drive_url": direct_payload.get("drive_url"),
            "process_start_date": date.today(),
            "stage_in_funnel": direct_payload.get("stage_in_funnel"),
            "type_of_stage": direct_payload.get("type_of_stage"),
            "had_home_assignment": direct_payload.get("had_home_assignment"),
            "home_assignment_questions": direct_payload.get("home_assignment_questions"),
            "home_assignment_answers": direct_payload.get("home_assignment_answers"),
            "stage_date": direct_payload.get("stage_date"),
    }
    a,b = direct_payload_to_new_process_dict(job_ready_student_dict)
    
    ...
   