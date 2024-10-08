from global_functions.LoggingGenerator import Logger
from global_constants import MARKETING_MQL_DATE_OBJECTS
from global_functions.general_functions import write_object_to_db, update_objects_in_session, \
    hubspot_id_in_known_ignorable_tuple_of_ms_employees
from global_functions.time_functions import utc_to_date
from flask import request
from models import MarketingMqlStudentsModel
from flask.views import MethodView
from flask_smorest import Blueprint
import os
from uuid import uuid4

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint("A new MQL student has entered", __name__,
                      description="This_is_a_templated_blueprint")


@blueprint.route('/log_new_mql_student', methods=['POST'])
class NewMqlStudent(MethodView):
    def post(self):
        """
        Handles POST requests to log a new MQL student.

        The function receives JSON data from the request, checks if the student is a test student,
        and then either updates an existing student record or creates a new one.

        Parameters:
        None (The function reads data from the Flask request object.)

        Returns:
        dict: A dictionary containing a message indicating the outcome of the operation.
        HTTP status code: 200 if the operation is successful, 400 if the request data is invalid.
        """
        data = request.get_json()
        try:
            if hubspot_id_in_known_ignorable_tuple_of_ms_employees(data):
                return {"message": f"Test students are ignored: {data['hubspot_id']}"}, 200
    
            student_record = MarketingMqlStudentsModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()
    
            if student_record is not None:
                for date_data in MARKETING_MQL_DATE_OBJECTS:
                    setattr(student_record, date_data, utc_to_date(data[date_data]))
                try:
                    setattr(student_record, "lp_variant", data.get("lp_variant"))
                except KeyError:
                    logger.debug(f"Missing 'lpvariant' in data: {data}")
                update_objects_in_session()
                return {"message": 'MQL student exists - updateing'}, 200
    
            if student_record is None:
                for date_data in MARKETING_MQL_DATE_OBJECTS:
                    data[date_data] = utc_to_date(data[date_data])
    
                new_mql_obj = MarketingMqlStudentsModel(**data)
                write_object_to_db(new_mql_obj)
    
                return {"message": 'New MQL student'}, 200
        except Exception as e:
            error_id = uuid4().__str__()
            logger.error(f"Error ID: {error_id} - Error handling POST request: {str(e)}")
            logger.info(f"Error ID: {error_id} - Request data : {data}")
            return {"message": f"Error handling POST request: {str(e)}"}, 400
