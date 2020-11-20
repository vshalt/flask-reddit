from flask import render_template, redirect, url_for, abort, flash
from flask_login import current_user, login_required
from app.post import post_blueprint
from app import db
from app.models import Community, Post, PostVote, Reply, ReplyVote
from app.post.forms import NewPostForm, UpdatePostForm
from app.communities.views import join_or_leave

@post_blueprint.route('/community/r/<string:name>/posts')
def get_posts(name):
    community = Community.query.filter_by(name=name).first()
    if community:
        posts = Post.query.filter_by(community=community).all()
        return render_template('post/get_posts.html', posts=posts, community=community, join_or_leave=join_or_leave)
    else:
        abort(404)

@post_blueprint.route('/community/r/<string:name>/get/<string:title>')
def get_post(name, title):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            replies = Reply.query.filter_by(post_id=post.id)
            post_votes = PostVote.query.filter_by(post_id=post.id).all()
            sum = 0
            for post_vote in post_votes:
                sum += post_vote.count
            def get_votes(reply):
                replies = ReplyVote.query.filter_by(reply_id=reply.id).all()
                sum = 0
                for reply in replies:
                    sum += reply.count
                return sum
            return render_template('post/get_post.html', post=post, community=community, get_votes=get_votes,post_vote=sum, replies=replies, hide_view='yes')
        else:
            abort(404)
    else:
        abort(404)

@post_blueprint.route('/community/r/<string:name>/post', methods=['GET', 'POST'])
@login_required
def new_post(name):
    community = Community.query.filter_by(name=name).first()
    if community:
        form = NewPostForm()
        if form.validate_on_submit():
            post = Post(title=form.title.data, body=form.body.data, author=current_user, community=community)
            post.remove_space_from_title()
            db.session.commit()
            flash(f'Posted on r/{community.name}', 'success')
            return redirect(url_for('post.get_post', name=community.name, title=post.title))
        return render_template('post/new_post.html', form=form)
    else:
        abort(404)

@post_blueprint.route('/community/r/<string:name>/edit/<string:title>', methods=['GET', 'POST'])
@login_required
def update_post(name, title):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post and post.author.id == current_user.id:
            form = UpdatePostForm()
            if form.validate_on_submit():
                post.title  = form.title.data
                post.body   = form.body.data
                post.remove_space_from_title()
                db.session.commit()
                flash('Post edited', 'primary')
                return redirect(url_for('post.get_post', name=community.name, title=post.title))
            form.title.data = post.title
            form.body.data  = post.body
            return render_template('post/update_post.html', form=form)
        else:
            abort(404)
    else:
        abort(404)

@post_blueprint.route('/community/r/<string:name>/delete/<string:title>')
@login_required
def delete_post(name, title):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post and post.author.id == current_user.id:
            db.session.delete(post)
            db.session.commit()
            flash('Post deleted')
            return redirect(url_for('community.get_community', name=community.name))
        else:
            abort(404)
    else:
        abort(404)

@post_blueprint.route('/community/r/<string:name>/upvote/<string:title>')
@login_required
def upvote_post(name, title):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            post_vote = PostVote.query.filter_by(post_id=post.id, user_id=current_user.id).first()
            if post_vote is None:
                post_vote = PostVote(user_id=current_user.id, post_id=post.id, count=1)
                db.session.add(post_vote)
            elif abs(post_vote.count) == 1:
                post_vote.count=0
            else:
                post_vote.count = 1
            db.session.commit()
            return redirect(url_for('post.get_post', name=community.name, title=post.title))
        else:
            abort(404)
    else:
        abort(404)

@post_blueprint.route('/community/r/<string:name>/downvote/<string:title>')
@login_required
def downvote_post(name, title):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            post_vote = PostVote.query.filter_by(post_id=post.id, user_id=current_user.id).first()
            if post_vote is None:
                post_vote = PostVote(user_id=current_user.id, post_id=post.id, count=-1)
                db.session.add(post_vote)
            elif abs(post_vote.count) == 1:
                post_vote.count=0
            else:
                post_vote.count = -1
            db.session.commit()
            return redirect(url_for('post.get_post', name=community.name, title=post.title))
        else:
            abort(404)
    else:
        abort(404)
