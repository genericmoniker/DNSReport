import csv
import re

import requests

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
    if b'Forgot password?' in r.content:
        raise Exception('Invalid OpenDNS credentials.')
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

    filtered = [d for d in data_iter if d[_NAME] not in whitelist]
    if not filtered:
        return None

    for i, domain in enumerate(filtered, start=1):
        name = domain[_NAME]
        count = domain[_COUNT]
        reason = _get_block_reason(header, domain)
        # Note: We use `i` instead of the rank from the domain so that
        # whitelisted domains don't leave gaps in the numbering.
        print(f'{i}. {name} ({count}) - {reason}', file=buffer)

    return f'OpenDNS report for {date:%A, %B %d, %Y}'


def _get_block_reason(header, domain):
    reason = []
    offset = 3  # Skip "rank, domain, total" columns.
    for index, item in enumerate(domain[3:]):
        if item != '0':
            reason.append(header[index + offset])
    return ', '.join(reason)
