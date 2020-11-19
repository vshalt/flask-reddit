from app.communities import communities_blueprint
from app.models import CommunityParticipant, Community
from flask import render_template

def join_or_leave(user, community):
    return CommunityParticipant.query.filter_by(community_id=community.id, user_id=user.id).first()

@communities_blueprint.route('/communities')
def communities():
    communities = Community.query.all()
    return render_template('communities/communities.html', communities=communities, join_or_leave=join_or_leave)
