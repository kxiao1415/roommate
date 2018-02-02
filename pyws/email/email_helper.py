from flask import current_app

from flask_mail import Mail
from flask_mail import Message
from pyws.helper.decorator import async
from config import Config

mail = Mail()


@async
def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(recipients, subject, text_body, html_body, sender=Config.MAIL_USERNAME):
    app = current_app._get_current_object()
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    send_async_email(app, msg)
