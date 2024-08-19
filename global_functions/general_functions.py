from db import db
from sqlalchemy.exc import SQLAlchemyError
from flask_smorest import abort
from global_functions.LoggingGenerator import Logger
from models import StudentStagesV3
import os
from flask import jsonify
from sqlalchemy import and_, func

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()


def read_typeform_answers(typeform_payload, typeform_questions_ids_dict):
    new_dict = {}
    for answer in typeform_payload['form_response']['answers']:
        key = typeform_questions_ids_dict.get(answer['field']['id'])
        if key is None:
            continue
        if key == 'full_name':
            name_parts = answer['text'].split(" ")
            new_dict['student_firstname'] = " ".join(name_parts[:-1])
            new_dict['student_lastname'] = name_parts[-1]
            continue
        value = answer.get('choice', {}).get('other') or answer.get('choice', {}).get('label', answer.get(answer['type']))
        new_dict[key] = value
    return new_dict


def update_objects_in_session():
    try:
        db.session.commit()
    except SQLAlchemyError as e:
        logger.error(f"Error writing object to db: {str(e)}")
        db.session.rollback()
        abort(400, message=str(e))


# def write_object_to_db(object_to_write):
#     try:
#         logger.debug(f"writing object to db: {object_to_write}")
#         db.session.add(object_to_write)
#         db.session.commit()
#     except SQLAlchemyError as e:
#         logger.error(f"Error writing object to db: {str(e)}")
#         db.session.rollback()
#         abort(400, message=str(e))


def write_object_to_db(object_to_write):
    try:
        logger.debug(f"writing object to db: {object_to_write}")

        # Check if object_to_write is an instance of StudentStagesV3
        if isinstance(object_to_write, StudentStagesV3):
            # Check for existing record with the same constraints
            existing_record = db.session.query(StudentStagesV3).filter(
                StudentStagesV3.hubspot_id == object_to_write.hubspot_id,
                StudentStagesV3.stage == object_to_write.stage,
                StudentStagesV3.company_if_rel == object_to_write.company_if_rel,
                func.date(StudentStagesV3.created_at) == func.date(object_to_write.created_at)
            ).first()

            if existing_record:
                logger.debug("Duplicate record found, doing nothing.")
                return jsonify({"message": "Record already exists."}), 200

        # If no matching record, add the new object to the DB
        db.session.add(object_to_write)
        db.session.commit()
        return jsonify({"message": "Object successfully written to the database."}), 200

    except SQLAlchemyError as e:
        logger.error(f"Error writing object to db: {str(e)}")
        db.session.rollback()
        abort(400, message=str(e))


def delete_object_from_db(object_class, object_id):
    try:
        logger.debug(f"deleting object with id {object_id} from db")
        obj = db.session.query(object_class).get(object_id)  # Replace MyObjectClass with the actual class name
        if obj:
            db.session.delete(obj)
            db.session.commit()
            logger.debug(f"object with id {object_id} successfully deleted")
        else:
            logger.error(f"object with id {object_id} not found")
            abort(404, message="Object not found")
    except SQLAlchemyError as e:
        logger.error(f"Error deleting object from db: {str(e)}")
        db.session.rollback()
        abort(500, message=str(e))
