import smtplib

import config
import mailer


def send_report(report_subject, report_body):
    with _configure_smtp() as client:
        mail = mailer.Mailer(client)
        mail.send_message(
            config.MAIL_RECIPIENTS,
            config.MAIL_SENDER,
            report_subject,
            report_body,
        )


def _configure_smtp():
    client = smtplib.SMTP_SSL(config.SMTP_HOST, config.SMTP_PORT)
    client.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)
    return client
