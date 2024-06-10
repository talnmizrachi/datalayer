from global_functions.general_functions import write_object_to_db
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError
from models import MentorModel
import os
from db import db
from global_functions.LoggingGenerator import Logger

logger = Logger(os.path.basename(__file__).split('.')[0]).get_logger()
blueprint = Blueprint('mentor_blp', __name__, description="This blueprint is for adding new mentors")


@blueprint.route('/add_mentor')
class MethodTemplate(MethodView):

    def post(self):
        data = request.get_json()

        mentor_dict = {'mentor_fullname': data.get('mentor_fullname'), 'mentor_email': data.get('mentor_email'),
                       'mentor_languages': data.get('mentor_languages'), 'domain': data.get('domain'),
                       'created_at': data.get('created_at')}

        mentor_obj = MentorModel(**mentor_dict)
        write_object_to_db(mentor_obj)
