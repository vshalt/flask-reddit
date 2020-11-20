from app.main import main_blueprint
from flask import render_template, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app.main.forms import EditProfileForm
from app.models import User, CommunityParticipant, Post, Community
from app import db
from app.communities.views import join_or_leave

@main_blueprint.route('/')
def home():
    if current_user.is_authenticated:
        communities = CommunityParticipant.query.filter_by(user_id=current_user.id).all()
        posts = []
        for community in communities:
            posts += Post.query.filter_by(community_id = community.community_id).all()
    else:
        posts = Post.query.all()
    def find_community(xpost):
        post_community = Post.query.filter_by(title=xpost.title).first()
        community = Community.query.get(int(post_community.community_id))
        return community
    return render_template('main/home.html', posts=posts, find_community=find_community, hide_vote='yes')

@main_blueprint.route('/profile/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        return render_template('main/profile.html', user=user, join_or_leave=join_or_leave)
    else:
        abort(404)

@main_blueprint.route('/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    user = User.query.filter_by(username=username).first()
    form = EditProfileForm()
    if form.validate_on_submit():
        user.name       = form.name.data
        user.location   = form.location.data
        user.about_me   = form.about_me.data
        db.session.add(user)
        db.session.commit()
        flash('Account updated', 'success')
        return redirect(url_for('main.profile', username=user.username))
    form.name.data      = user.name
    form.location.data  = user.location
    form.about_me.data  = user.about_me
    return render_template('main/edit_profile.html', form=form)
