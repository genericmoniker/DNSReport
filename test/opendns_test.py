import io
import pytest
import re
import responses
import requests

from datetime import date

from dnsreport.opendns import get_report_csv, render_report

CSV_URL = re.compile(
    'https://dashboard.opendns.com/stats/.+/topdomains/.+/blocked.csv'
)


@pytest.fixture
def csv():
    body = '''Rank,Domain,Total,Blacklisted,"Blocked by Category","Blocked as Botnet","Blocked as Malware","Blocked as Phishing","Resolved by SmartCache","Academic Fraud","Adult Themes",Adware,Alcohol,Anime/Manga/Webcomic,Auctions,Automotive,Blogs,"Business Services",Chat,Classifieds,Dating,Drugs,Ecommerce/Shopping,"Educational Institutions","File Storage","Financial Institutions","Forums/Message boards",Gambling,Games,"German Youth Protection",Government,Hate/Discrimination,"Health and Fitness",Humor,"Instant Messaging",Jobs/Employment,Lingerie/Bikini,Movies,Music,News/Media,Non-Profits,Nudity,"P2P/File sharing","Parked Domains","Photo Sharing",Podcasts,Politics,Pornography,Portals,Proxy/Anonymizer,Radio,Religious,Research/Reference,"Search Engines",Sexuality,"Social Networking",Software/Technology,Sports,Tasteless,Television,Tobacco,Travel,"Video Sharing","Visual Search Engines",Weapons,"Web Spam",Webmail
1,proxy.googlezip.net,139,0,139,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
2,www.yourtango.com,11,0,11,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0
3,www.3wishes.com,2,0,2,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
4,noruleshere.com,1,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
5,www.cosmopolitan.com,1,0,1,0,0,0,0,0,1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0'
'''  # noqa
    with responses.RequestsMock() as r:
        r.add(responses.GET, CSV_URL, body=body)
        yield


@pytest.fixture
def csv_empty():
    body = 'Rank,Domain,Total,Blacklisted,"Blocked by Category","Blocked as Botnet","Blocked as Malware","Blocked as Phishing","Resolved by SmartCache","Academic Fraud","Adult Themes",Adware,Alcohol,Anime/Manga/Webcomic,Auctions,Automotive,Blogs,"Business Services",Chat,Classifieds,Dating,Drugs,Ecommerce/Shopping,"Educational Institutions","File Storage","Financial Institutions","Forums/Message boards",Gambling,Games,"German Youth Protection",Government,Hate/Discrimination,"Health and Fitness",Humor,"Instant Messaging",Jobs/Employment,Lingerie/Bikini,Movies,Music,News/Media,Non-Profits,Nudity,"P2P/File sharing","Parked Domains","Photo Sharing",Podcasts,Politics,Pornography,Portals,Proxy/Anonymizer,Radio,Religious,Research/Reference,"Search Engines",Sexuality,"Social Networking",Software/Technology,Sports,Tasteless,Television,Tobacco,Travel,"Video Sharing","Visual Search Engines",Weapons,"Web Spam",Webmail'  # noqa
    with responses.RequestsMock() as r:
        r.add(responses.GET, CSV_URL, body=body)
        yield


def get_report(whitelist):
    today = date.today()
    csv = get_report_csv(requests.session(), 'id', today)
    buffer = io.StringIO()
    render_report(buffer, csv, today, whitelist)
    return buffer.getvalue()


def test_all_data_rows_returned(csv):
    csv = get_report_csv(requests.session(), 'id', date.today())
    data = list(csv)
    assert data[1][1] == 'proxy.googlezip.net'
    assert data[2][1] == 'www.yourtango.com'
    assert data[3][1] == 'www.3wishes.com'
    assert data[4][1] == 'noruleshere.com'
    assert data[5][1] == 'www.cosmopolitan.com'


def test_empty_report_returns_only_header_row(csv_empty):
    csv = get_report_csv(requests.session(), 'id', date.today())
    assert len(list(csv)) == 1


def test_report_with_data_has_subject(csv):
    today = date.today()
    csv = get_report_csv(requests.session(), 'id', today)
    buffer = io.StringIO()
    subject = render_report(buffer, csv, today, [])
    assert subject


def test_report_without_data_does_not_have_subject(csv_empty):
    today = date.today()
    csv = get_report_csv(requests.session(), 'id', today)
    buffer = io.StringIO()
    subject = render_report(buffer, csv, today, [])
    assert subject is None


def test_block_reason_is_correct(csv):
    report = get_report([])
    matches = 0
    for line in report.splitlines():
        if 'proxy.googlezip.net' in line:
            assert 'Proxy/Anonymizer' in line
            matches += 1
        elif 'www.yourtango.com' in line:
            assert 'Adult Themes' in line
            matches += 1
        elif 'www.3wishes.com' in line:
            assert 'Pornography' in line
            matches += 1
        elif 'noruleshere.com' in line:
            assert 'Proxy/Anonymizer' in line
            matches += 1
        elif 'www.cosmopolitan.com' in line:
            assert 'Lingerie/Bikini' in line
            matches += 1
    assert matches == 5


def test_whitelist_domains_not_in_report(csv):
    whitelist = ['proxy.googlezip.net', 'noruleshere.com']
    report = get_report(whitelist)
    assert 'proxy.googlezip.net' not in report
    assert 'noruleshere.com' not in report


def test_non_whitelist_domains_are_numbered_sequentially(csv):
    whitelist = ['www.yourtango.com']
    report = get_report(whitelist)
    assert '1. proxy.googlezip.net' in report
    assert '2. www.3wishes.com' in report
    assert '3. noruleshere.com' in report
    assert '4. www.cosmopolitan.com' in report
