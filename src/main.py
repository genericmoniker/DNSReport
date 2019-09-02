import requests

import csv
import io
import os
import re

from datetime import datetime, timedelta


def main():
    username, password = get_credentials()
    print('Logging in...')
    s = login(username, password)
    network_id = get_network_id()
    date = (datetime.today() - timedelta(days=2)).date()
    print('Fetching report...')
    data = get_report_csv(s, network_id, date)
    if data:
        print('Rendering report...')
        buffer = io.StringIO()
        render_message(buffer, data, date)
        print(buffer.getvalue())
    else:
        print(f'No domains blocked on {date}.')


def get_credentials():
    return os.getenv('DNSREPORT_USERNAME'), os.getenv('DNSREPORT_PASSWORD')


def get_network_id():
    return os.getenv('DNSREPORT_NETWORK_ID')


def login(username, password):
    url = 'https://login.opendns.com/?source=dashboard'
    s = requests.Session()
    r = s.get(url)
    r.raise_for_status()
    token = find_form_token(r)
    data = {'username': username, 'password': password, 'formtoken': token}
    r = s.post(url, data=data)
    r.raise_for_status()
    return s


def find_form_token(r):
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


def render_message(buffer, data, date):
    print(f'Domains blocked on {date}:', file=buffer)
    data_iter = iter(data)
    header = next(data_iter)
    for domain in data_iter:
        rank = domain[0]
        name = domain[1]
        count = domain[2]
        reason = get_block_reason(header, domain)
        print(f'{rank}. {name} ({count}) - {reason}', file=buffer)


def get_block_reason(header, domain):
    reason = []
    offset = 3  # Skip "rank, domain, total" columns.
    for index, item in enumerate(domain[3:]):
        if item != '0':
            reason.append(header[index + offset])
    return ', '.join(reason)


if __name__ == '__main__':
    main()
