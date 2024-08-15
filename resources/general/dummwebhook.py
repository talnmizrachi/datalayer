from global_functions.LoggingGenerator import Logger
from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint
import os

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
dummy_blueprint = Blueprint("Dummy webhook", __name__,
                      description="This_is_a_templated_blueprint")


@dummy_blueprint.route('/dummy_webhook', methods=['POST'])
class Dummy(MethodView):
    def post(self):
        logger.info(f"Dummy webhook triggered")
        logger.debug(request.get_json())
        
        return {"message": 'Dummy webhook triggered'}, 200
