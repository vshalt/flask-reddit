from app.communities import communities_blueprint
from app.models import CommunityParticipant, Community
from flask import render_template

@communities_blueprint.route('/communities')
def communities():
    communities = Community.query.all()
    return render_template('communities/communities.html', communities=communities)
