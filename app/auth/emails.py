from app import mail
from flask_mail import Message
from flask import current_app, render_template
from threading import Thread

def send_async_mail(app, msg):
    with app.app_context():
        mail.send(msg)


def send_mail(to, subject, template, **kwargs):
    msg = Message(subject, sender=current_app.config['DEFAULT_MAIL_SENDER'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_mail, args=[current_app._get_current_object(), msg])
    thr.start()
    return thr
