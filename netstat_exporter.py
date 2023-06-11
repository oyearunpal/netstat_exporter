#!/usr/bin/python3.6
import subprocess
import time
from prometheus_client import start_http_server, Gauge
import argparse

# Define Prometheus metrics
metric_labels = [
    "protocol",
    "local_ip",
    "local_port",
    "foreign_ip",
    "foreign_port",
    "pid",
    "process_name",
    "state",
]
sendQ_gauge = Gauge("netstat_sendQ", "Send queue size in bytes", metric_labels)
recvQ_gauge = Gauge("netstat_recvQ", "Receive queue size in bytes", metric_labels)


def run():
    # Set the loop interval in seconds
    interval = args.interval
    while True:
        sendQ_gauge._metrics.clear()
        recvQ_gauge._metrics.clear()
        # Run the netstat command and capture its output
        output = subprocess.check_output(["netstat", "-tlnap"])

        # Split the output into lines and iterate over them
        for line in output.decode().splitlines():
            # Check if the line starts with "tcp" or "udp"
            fields = line.split()
            protocol = fields[0]
            # process only tcp connections
            if protocol == "tcp":
                sendQ = int(fields[1])
                recvQ = int(fields[2])
                local_ip, local_port = fields[3].split(":")
                foreign_ip, foreign_port = fields[4].split(":")
                state = fields[5]
                try:
                    _ = fields[6].replace(".", "/")
                    _ = _.split("/")
                    pid = _[0]
                    process_name = _[-1]
                except:
                    pid = fields[6]
                    process_name = "-"
                # Update Prometheus metrics with the values
                if sendQ > args.QueueLimit:
                    sendQ_gauge.labels(
                        protocol=protocol,
                        local_ip=local_ip,
                        local_port=local_port,
                        foreign_ip=foreign_ip,
                        foreign_port=foreign_port,
                        state=state,
                        pid=pid,
                        process_name=process_name,
                    ).set(sendQ)
                if recvQ > args.QueueLimit:
                    recvQ_gauge.labels(
                        protocol=protocol,
                        local_ip=local_ip,
                        local_port=local_port,
                        foreign_ip=foreign_ip,
                        foreign_port=foreign_port,
                        state=state,
                        pid=pid,
                        process_name=process_name,
                    ).set(recvQ)
        time.sleep(interval)


def read_arguments():
    parser = argparse.ArgumentParser(
        description="A netstat exporter",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-q", "--QueueLimit", help="Minimum queue length to report", default=0, type=int
    )
    parser.add_argument(
        "-i", "--interval", help="Minimum interval before getting stats again", default=1, type=int
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Port on which it will export data.",
        default=8100,
        type=int,
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = read_arguments()
    # Start Prometheus server
    start_http_server(args.port)
    run()
