from global_functions.LoggingGenerator import Logger
from global_functions.general_functions import write_object_to_db
from global_functions.time_functions import utc_to_date
from flask import request
from models import MarketingMqlStudentsModel
from flask.views import MethodView
from flask_smorest import Blueprint
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint("A new MQL student has entered", __name__,
                      description="This_is_a_templated_blueprint")


@blueprint.route('/log_new_mql_student', methods=['POST'])
class Dummy(MethodView):
    def post(self):
        
        data = request.get_json()
        data['hubspot_created_at'] = utc_to_date(data['hubspot_created_at'])
        new_mql_obj = MarketingMqlStudentsModel(**data)
        write_object_to_db(new_mql_obj)
        
        return {"message": 'New MQL student'}, 200
