import uuid
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

        try:
            db.session.add(mentor_obj)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message=str(e))
