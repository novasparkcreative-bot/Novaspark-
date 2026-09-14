import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from core.orchestrator.run import run_ready_tasks


class WorkerAPI(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != '/api/tasks/run':
            self.send_response(404); self.end_headers(); return
        try:
            results = run_ready_tasks()
            body = json.dumps({'results': results}, ensure_ascii=False).encode()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers(); self.wfile.write(body)
        except Exception as exc:
            body = json.dumps({'error': str(exc)}).encode()
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Content-Length', str(len(body)))
            self.end_headers(); self.wfile.write(body)

    def log_message(self, *_): pass


def run(host='127.0.0.1', port=8081):
    print(f'NovaSpark worker API: http://{host}:{port}')
    HTTPServer((host, port), WorkerAPI).serve_forever()


if __name__ == '__main__': run()
