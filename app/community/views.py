from app.community import community_blueprint
from app.community.forms import NewCommunityForm, UpdateCommunityForm
from app import db
from app.models import Community, CommunityParticipant
from flask import render_template, redirect, url_for, flash, abort
from flask_login import login_required, current_user
from app.communities.views import join_or_leave

@community_blueprint.route('/community/r/<string:name>')
def get_community(name):
    community = Community.query.filter_by(name=name).first()
    if community:
        return render_template('community/get_community.html',community=community, join_or_leave=join_or_leave)
    else:
        abort(404)


@community_blueprint.route('/community/new', methods=['POST', 'GET'])
@login_required
def new_community():
    form = NewCommunityForm()
    if form.validate_on_submit():
        community = Community(name=form.name.data, description=form.description.data, user=current_user)
        db.session.add(community)
        db.session.commit()
        flash('Community created', 'success')
        return redirect(url_for('community.get_community', name=form.name.data))
    return render_template('community/new_community.html', form=form)

@community_blueprint.route('/community/update/<string:name>', methods=['POST', 'GET'])
@login_required
def update_community(name):
    form = UpdateCommunityForm()
    community = Community.query.filter_by(name=name).first()
    if form.validate_on_submit():
        community.description = form.description.data
        db.session.add(community)
        db.session.commit()
        flash('Community updated', 'success')
        return redirect(url_for('community.get_community', name=community.name))
    form.description.data   = community.description
    return render_template('community/update_community.html', form=form)

@community_blueprint.route('/community/delete/<string:name>')
@login_required
def delete_community(name):
    community = Community.query.filter_by(name=name).first()
    if community:
        if current_user.id == community.user.id:
            db.session.delete(community)
            db.session.commit()
            flash('Community deleted', 'danger')
            return redirect(url_for('main.home'))
        else:
            abort(403)
    else:
        abort(404)

@community_blueprint.route('/community/join/<string:name>')
@login_required
def join_community(name):
    community = Community.query.filter_by(name=name).first()
    if community:
        community_participant = CommunityParticipant.query.filter_by(user_id=current_user.id, community_id=community.id).first()
        if community_participant is None:
            community_participant = CommunityParticipant(community=community, user=current_user)
            db.session.add(community_participant)
            db.session.commit()
            flash(f'Joined r/{community.name} successfully', 'success')
            return redirect(url_for('community.get_community', name=community.name))
        else:
            flash(f'Already a member of r/{community.name}', 'primary')
            return redirect(url_for('community.get_community', name=community.name))
    else:
        abort(404)

@community_blueprint.route('/community/leave/<string:name>')
@login_required
def leave_community(name):
    community = Community.query.filter_by(name=name).first()
    if community:
        community_participant = CommunityParticipant.query.filter_by(user_id=current_user.id, community_id=community.id).first()
        if community_participant is None:
            flash(f'Cannot leave r/{community.name}, not a participant', 'danger')
            return redirect(url_for('community.get_community', name=community.name))
        else:
            db.session.delete(community_participant)
            db.session.commit()
            flash(f'Left r/{community.name}', 'danger')
            return redirect(url_for('community.get_community', name=community.name))
    else:
        abort(404)
    pass

