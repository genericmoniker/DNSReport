import json
import os
from pathlib import Path


# Load config from secrets, if possible.
try:
    _secret_conf = json.loads(Path('/run/secrets/conf').read())
    print('Using config from secrets.')
except Exception:
    _secret_conf = {}
    print('Using config from environment.')


def get(key):
    """Get a config value.

    Tries to get the value from a secret file, otherwise from an environment
    variable. See https://docs.docker.com/compose/compose-file/#secrets
    """
    return _secret_conf.get(key, os.getenv(key))


# OpenDNS settings
OPEN_DNS_USERNAME = get('DNSREPORT_USERNAME')
OPEN_DNS_PASSWORD = get('DNSREPORT_PASSWORD')
OPEN_DNS_NETWORK_ID = get('DNSREPORT_NETWORK_ID')

# SMTP settings
SMTP_HOST = get('DNSREPORT_SMTP_HOST')
SMTP_PORT = get('DNSREPORT_SMTP_PORT')  # defaults to 465
SMTP_USERNAME = get('DNSREPORT_SMTP_USERNAME')
SMTP_PASSWORD = get('DNSREPORT_SMTP_PASSWORD')
MAIL_SENDER = get('DNSREPORT_SENDER')  # may be ignored by SMTP server
MAIL_RECIPIENTS = get('DNSREPORT_RECIPIENTS')

# Don't send notifications for blocked domain listed here.
_raw = get('DNSREPORT_WHITELIST')
WHITELIST = _raw.split(',') if _raw else []
