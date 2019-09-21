import os
from pathlib import Path


def get(key):
    # Try Docker secrets.
    try:
        return (Path('/run/secrets') / key).read()
    except Exception:
        pass
    # Try environment variable.
    return os.getenv(key)


OPEN_DNS_USERNAME = get('DNSREPORT_USERNAME')
OPEN_DNS_PASSWORD = get('DNSREPORT_PASSWORD')
OPEN_DNS_NETWORK_ID = get('DNSREPORT_NETWORK_ID')

SMTP_HOST = get('DNSREPORT_SMTP_HOST')
SMTP_PORT = get('DNSREPORT_SMTP_PORT')  # defaults to 465
SMTP_USERNAME = get('DNSREPORT_SMTP_USERNAME')
SMTP_PASSWORD = get('DNSREPORT_SMTP_PASSWORD')
MAIL_SENDER = get('DNSREPORT_SENDER')  # may be ignored by SMTP server
MAIL_RECIPIENTS = get('DNSREPORT_RECIPIENTS')
