# DNSReport

This is a utility for emailing a report of [OpenDNS](https://www.opendns.com/) 
blocked domains. It can be run as a task to get a daily report of the previous
day's blocked domains, which can help you monitor internet activity on your network.

## Configuration

All configuration is done with environment variables:

* DNSREPORT_USERNAME - your OpenDNS account username
* DNSREPORT_PASSWORD - your OpenDNS account password
* DNSREPORT_NETWORK_ID - the ID of the network for which to report; see below
* DNSREPORT_SMTP_HOST - SMTP server host
* DNSREPORT_SMTP_USERNAME - SMTP server username
* DNSREPORT_SMTP_PASSWORD - SMTP server password
* DNSREPORT_SENDER - email address from which to send report messages
* DNSREPORT_RECIPIENTS - comma-separated email addresses to which to send
  report messages
* DNSREPORT_WHITELIST - comma-separated list of domain names to ignore for
  reporting; still blocked by OpenDNS

Your network ID can be seen in URLs on the dashboard. For example:

`https://dashboard.opendns.com/stats/<network-id>/totalrequests/`

## Running from source

Dependencies are managed with [poetry](https://poetry.eustace.io/), so you'll
want to install that first. Then, in the root directory of the project:

```shell
poetry install
poetry run python -m dnsreport
```

## Docker

DNSReport is also available as a Docker image at:

https://cloud.docker.com/u/genericmoniker/repository/docker/genericmoniker/dnsreport

Running it would be something like this:

```
docker run -t --rm --env-file /volume1/documents/tasks/dnsreport/settings.env --name dnsreport genericmoniker/dnsreport
```
