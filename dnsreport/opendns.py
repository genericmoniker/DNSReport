import csv
import re

import requests

_RANK = 0
_NAME = 1
_COUNT = 2


def login(username, password):
    url = 'https://login.opendns.com/?source=dashboard'
    s = requests.Session()
    r = s.get(url)
    r.raise_for_status()
    token = _find_form_token(r)
    data = {'username': username, 'password': password, 'formtoken': token}
    r = s.post(url, data=data)
    r.raise_for_status()
    return s


def _find_form_token(r):
    pattern = r'name=\"formtoken\" value=\"([0-9a-f]+)'
    match = re.search(pattern, r.text)
    if not match:
        raise Exception("Couldn't find login form token!")
    return match.group(1)


def get_report_csv(s, network_id, date):
    url = (
        f'https://dashboard.opendns.com/stats/{network_id}/topdomains/'
        f'{date.isoformat()}/blocked.csv'
    )
    r = s.get(url)
    r.raise_for_status()
    return csv.reader(r.text.splitlines())


def render_report(buffer, data, date, whitelist):
    """Render the blocked domains report.

    :param buffer: buffer into which the report is rendered.
    :param data: CSV data of the report.
    :param date: date for the data.
    :param whitelist: list of domains to ignore in the report.
    :return: report subject, or None if no blocked domains.
    """
    print(f'Domains blocked on {date:%A, %B %d, %Y}:', file=buffer)
    print(file=buffer)
    data_iter = iter(data)
    header = next(data_iter)
    has_blocked_domains = False
    for domain in data_iter:
        name = domain[_NAME]
        if name in whitelist:
            continue
        rank = domain[_RANK]
        count = domain[_COUNT]
        reason = _get_block_reason(header, domain)
        print(f'{rank}. {name} ({count}) - {reason}', file=buffer)
        has_blocked_domains = True
    if has_blocked_domains:
        return f'OpenDNS report for {date:%A, %B %d, %Y}'
    return None


def _get_block_reason(header, domain):
    reason = []
    offset = 3  # Skip "rank, domain, total" columns.
    for index, item in enumerate(domain[3:]):
        if item != '0':
            reason.append(header[index + offset])
    return ', '.join(reason)
