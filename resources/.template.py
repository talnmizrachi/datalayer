import uuid
from flask import request
from flask.views import MethodView
from flask_smorest import abort, Blueprint
from sqlalchemy.exc import SQLAlchemyError

from db import db

blueprint = Blueprint('templated_blp', __name__, description="This_is_a_templated_blueprint")


@blueprint.route('/api/template')
class MethodTemplate(MethodView):
    
    def get(self):
        ...
    
    
    def post(self):
        data = request.get_json()
        
        
        try:
            db.session.add(data)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.error(e)
            abort(500, message=str(e))