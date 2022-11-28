#! /usr/bin/python3

import collections
import glob
import json
import os
import socket
import statistics

from prometheus_client import CollectorRegistry, Gauge, write_to_textfile

registry = CollectorRegistry()

uwsgi_workers_rss_avg = Gauge(
    "ts_uwsgi_workers_rss_avg",
    "Average RSS of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_rss_med = Gauge(
    "ts_uwsgi_workers_rss_med",
    "Median RSS of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_rss_max = Gauge(
    "ts_uwsgi_workers_rss_max",
    "Maximum RSS of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_rss_total = Gauge(
    "ts_uwsgi_workers_rss_total",
    "Total RSS of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_vsz_avg = Gauge(
    "ts_uwsgi_workers_vsz_avg",
    "Average VSZ of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_vsz_med = Gauge(
    "ts_uwsgi_workers_vsz_med",
    "Median VSZ of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_vsz_max = Gauge(
    "ts_uwsgi_workers_vsz_max",
    "Maximum VSZ of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_vsz_total = Gauge(
    "ts_uwsgi_workers_vsz_total",
    "Total VSZ of uwsgi workers",
    ["app", "client_id", "name"],
    registry=registry,
)
uwsgi_workers_status = Gauge(
    "ts_uwsgi_workers_status",
    "uwsgi workers status",
    ["app", "status", "client_id", "name"],
    registry=registry,
)
app_name = None

for stats_sock in glob.glob("/run/*/stats.sock"):
    app_name = stats_sock.split("/")[2]
    app_name = app_name.replace("authentic2-multitenant", "authentic")
    if app_name == "authentic":
         # do not collect authentic data as it triggers some uwsgi bug
         # https://dev.entrouvert.org/issues/54624
         continue
    stats_json = ""
    with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as s:
        s.connect(stats_sock)
        while True:
            data = s.recv(4096)
            if not data:
                break
            stats_json += data.decode("utf8", "ignore")
    stats_data = json.loads(stats_json)

    listen_queue = stats_data["listen_queue"]
    workers_rss = []
    workers_vsz = []
    workers_status = collections.defaultdict(int)
    workers_status["idle"] = 0
    workers_status["busy"] = 0
    for worker in stats_data["workers"]:
        if worker["status"] == "cheap":
            continue
        workers_status[worker["status"]] += 1
        workers_rss.append(worker["rss"])
        workers_vsz.append(worker["vsz"])
    client_id = os.getenv("HOSTNAME").replace("teleservices", "")
    name = f"{client_id}_teleservices"
    uwsgi_workers_rss_total.labels(app=app_name, client_id=client_id, name=name).set(
        sum(workers_rss)
    )
    uwsgi_workers_rss_max.labels(app=app_name, client_id=client_id, name=name).set(
        max(workers_rss)
    )
    uwsgi_workers_rss_avg.labels(app=app_name, client_id=client_id, name=name).set(
        statistics.mean(workers_rss)
    )
    uwsgi_workers_rss_med.labels(app=app_name, client_id=client_id, name=name).set(
        statistics.median(workers_rss)
    )
    uwsgi_workers_vsz_total.labels(app=app_name, client_id=client_id, name=name).set(
        sum(workers_vsz)
    )
    uwsgi_workers_vsz_max.labels(app=app_name, client_id=client_id, name=name).set(
        max(workers_vsz)
    )
    uwsgi_workers_vsz_avg.labels(app=app_name, client_id=client_id, name=name).set(
        statistics.mean(workers_vsz)
    )
    uwsgi_workers_vsz_med.labels(app=app_name, client_id=client_id, name=name).set(
        statistics.median(workers_vsz)
    )
    for k in workers_status:
        uwsgi_workers_status.labels(
            app=app_name, status=k, client_id=client_id, name=name
        ).set(workers_status[k])


write_to_textfile(
    f"/var/lib/prometheus/node-exporter/{client_id}_uwsgi.prom", registry
)
