from app.reply import reply_blueprint
from flask import render_template, redirect, url_for, abort, flash
from app.models import Reply, ReplyVote, Community, Post
from app.reply.forms import NewReplyForm, EditReplyForm
from flask_login import current_user
from app import db

@reply_blueprint.route('/community/r/<string:name>/get/<string:title>/reply', methods=['GET', 'POST'])
def new_reply(name, title):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            form=NewReplyForm()
            if form.validate_on_submit():
                reply = Reply(body=form.body.data, author=current_user, post=post)
                db.session.add(reply)
                db.session.commit()
                flash('Commented on post', 'primary')
                return redirect(url_for('post.get_post', name=community.name, title=post.title))
            return render_template('reply/new_reply.html', form=form)
        else:
            abort(404)
    else:
        abort(404)
@reply_blueprint.route('/community/r/<string:name>/get/<string:title>/reply/edit/<int:reply_id>', methods=['GET', 'POST'])
def edit_reply(name, title, reply_id):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            reply = Reply.query.get(int(reply_id))
            if reply and reply.author.id == current_user.id:
                form=EditReplyForm()
                if form.validate_on_submit():
                    reply.body = form.body.data
                    db.session.add(reply)
                    db.session.commit()
                    flash('Reply edited', 'primary')
                    return redirect(url_for('post.get_post', name=community.name, title=post.title))
                form.body.data = reply.body
                return render_template('reply/edit_reply.html', form=form)
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)

@reply_blueprint.route('/community/r/<string:name>/get/<string:title>/reply/delete/<int:reply_id>')
def delete_reply(name, title, reply_id):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            reply = Reply.query.get(int(reply_id))
            if reply and reply.author.id == current_user.id:
                db.session.delete(reply)
                db.session.commit()
                flash('Reply deleted', 'danger')
                return redirect(url_for('post.get_post', name=community.name, title=post.title))
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)

@reply_blueprint.route('/community/r/<string:name>/get/<string:title>/reply/upvote/<int:reply_id>')
def upvote_reply(name, title, reply_id):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            reply = Reply.query.get(int(reply_id))
            if reply:
                reply_vote = ReplyVote.query.filter_by(reply_id=reply_id, user_id=current_user.id).first()
                print(reply_vote)
                if reply_vote is None:
                    reply_vote = ReplyVote(user_id=current_user.id, reply_id=reply.id, count=1)
                    db.session.add(reply_vote)
                elif (reply_vote.count) == 1:
                    reply_vote.count = 0
                else:
                    reply_vote.count=1
                db.session.commit()
                return redirect(url_for('post.get_post', name=community.name, title=post.title))
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)

@reply_blueprint.route('/community/r/<string:name>/get/<string:title>/reply/downvote/<int:reply_id>')
def downvote_reply(name, title, reply_id):
    community = Community.query.filter_by(name=name).first()
    if community:
        post = Post.query.filter_by(title=title).first()
        if post:
            reply = Reply.query.get(int(reply_id))
            if reply:
                reply_vote = ReplyVote.query.filter_by(reply_id=reply_id, user_id=current_user.id).first()
                if reply_vote is None:
                    reply_vote = ReplyVote(user_id=current_user.id, reply_id=reply.id, count=-1)
                    db.session.add(reply_vote)
                elif (reply_vote.count) == -1:
                    reply_vote.count = 0
                else:
                    reply_vote.count=-1
                db.session.commit()
                return redirect(url_for('post.get_post', name=community.name, title=post.title))
            else:
                abort(404)
        else:
            abort(404)
    else:
        abort(404)
