from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from global_functions.time_functions import utc_to_date
from flask import request
from models import MarketingMqlStudentsModel
from flask.views import MethodView
from flask_smorest import Blueprint
from global_functions.ignoring_constants import MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint("A new MQL student has entered", __name__,
                      description="This_is_a_templated_blueprint")


@blueprint.route('/log_new_mql_student', methods=['POST'])
class NewMqlStudent(MethodView):
    def post(self):
        
        data = request.get_json()
        
        if data['hubspot_id'] in MASTERSCHOOL_EMPLOYEE_HUBSPOT_TUPLE:
            logger.info(f"Skipping the job ready update. 200 OK")
            return {"message": f"Test students are ignored: {data['hubspot_id']}"}, 200
        
        existing_student = MarketingMqlStudentsModel.query.filter_by(hubspot_id=str(data['hubspot_id'])).first()
        if existing_student is not None:
            return {"message": 'MQL student already exists'}, 200
        
        data['hubspot_created_at'] = utc_to_date(data['hubspot_created_at'])
        data['date_mql_entered'] = utc_to_date(data['date_mql_entered'])
        new_mql_obj = MarketingMqlStudentsModel(**data)
        write_object_to_db(new_mql_obj)
        
        return {"message": 'New MQL student'}, 200
