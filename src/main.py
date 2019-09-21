import io
import smtplib

from datetime import datetime, timedelta

import config
import opendns
import notify


def main():
    print('Logging in...')
    s = opendns.login(config.OPEN_DNS_USERNAME, config.OPEN_DNS_PASSWORD)
    date = (datetime.today() - timedelta(days=1)).date()
    print('Fetching report...')
    data = opendns.get_report_csv(s, config.OPEN_DNS_NETWORK_ID, date)
    if data:
        print('Rendering report...')
        buffer = io.StringIO()
        subject = opendns.render_report(buffer, data, date)
        print()
        print(buffer.getvalue())
        try:
            print('Sending email...')
            notify.send_report(subject, buffer.getvalue())
        except Exception as e:
            print('Failed to send email:', e)
        else:
            print('Done!')
    else:
        print(f'No OpenDNS domains blocked on {date:%A, %B %d, %Y}.')


if __name__ == '__main__':
    main()
