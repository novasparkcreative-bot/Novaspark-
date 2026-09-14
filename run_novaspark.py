#!/usr/bin/env python3
"""Start the NovaSpark local services without hosting or a domain."""
import argparse
import threading
from api.server import run as run_api
from dashboard.app import run as run_dashboard
from api.worker_server import run as run_worker


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--api-port', type=int, default=8080)
    parser.add_argument('--dashboard-port', type=int, default=8000)
    parser.add_argument('--worker-port', type=int, default=8081)
    args = parser.parse_args()

    services = [
        ('api', lambda: run_api(port=args.api_port)),
        ('dashboard', lambda: run_dashboard(port=args.dashboard_port)),
        ('worker', lambda: run_worker(port=args.worker_port)),
    ]
    threads=[]
    for name, target in services:
        t=threading.Thread(target=target, name=name, daemon=True)
        t.start(); threads.append(t)
    print(f'NovaSpark running locally: http://127.0.0.1:{args.dashboard_port}')
    print('API: http://127.0.0.1:%d | Worker: http://127.0.0.1:%d' % (args.api_port, args.worker_port))
    try:
        threading.Event().wait()
    except KeyboardInterrupt:
        print('\nNovaSpark stopped.')


if __name__ == '__main__':
    main()
