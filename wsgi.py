from app import create_app, db
from app.models import User, Reply

app = create_app('default')

@app.shell_context_processor
def make_shell_context():
    return dict(db=db)

# @app.context_processor
# def get_votes(reply):
#     replies = ReplyVote.query.filter_by(reply_id=reply.id).all()
#     sum = 0
#     for reply in replies:
#         sum += reply.count
#     return sum
