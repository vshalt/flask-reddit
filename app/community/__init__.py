from flask import Blueprint

community_blueprint = Blueprint('community', __name__)

from app.community import views
