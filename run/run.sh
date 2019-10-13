#! /bin/sh
# Note: For trouble-shooting, enable email for the task.

# Get the latest image.
docker pull genericmoniker/dnsreport

# Run it as a new container.
docker run -t --rm --env-file /volume1/documents/tasks/dnsreport/settings.env --name dnsreport genericmoniker/dnsreport
