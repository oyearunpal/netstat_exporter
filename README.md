# netstat_exporter
Prometheus exporter for netstat metrics. This exporter will give details about send queue, receive queues ,local port, foreign address etc.

The above script runs `netstat -tlnap` commands under hood to get the metrics, so this will work fine on any unix box. You need `root access` to run
the script as netstat require root access to give details about all ports.

# How to use it ?
```python
usage: netstat_exporter.py [-h] [-q QUEUELIMIT] [-i INTERVAL] [-p PORT]

A netstat exporter

options:
  -h, --help            show this help message and exit
  -q QUEUELIMIT, --QueueLimit QUEUELIMIT
                        Minimum queue length to report (default: 0)
  -i INTERVAL, --interval INTERVAL
                        Minimum interval before getting stats again (default: 1)
  -p PORT, --port PORT  Port on which it will export data. (default: 8100)
```
For example
`python3 netstat_exporter.py -q 100 -i 10`

This will generate stats at http://localhost:8100/ , it will exclude results having queue size less than 100.

This can be easily viewed in grafana dashboard.

