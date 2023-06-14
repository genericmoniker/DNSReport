from email.message import EmailMessage


class Mailer:
    def __init__(self, smtp):
        self._smtp = smtp

    def send_message(self, recipients, sender, subject, body):
        msg = EmailMessage()
        msg['To'] = recipients
        msg['From'] = sender
        msg['Subject'] = subject
        msg.set_content(body)
        self._smtp.send_message(msg)
