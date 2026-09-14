import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from database.db import init_db, connect
from core.sales.lead_pipeline import add_lead, qualify_lead, get_leads
from core.sales.outreach import create_draft
from core.approvals.gates import request_approval, set_approval


def json_response(handler, payload, status=200):
    body = json.dumps(payload, ensure_ascii=False).encode()
    handler.send_response(status)
    handler.send_header('Content-Type', 'application/json; charset=utf-8')
    handler.send_header('Content-Length', str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class API(BaseHTTPRequestHandler):
    def read_json(self):
        length = int(self.headers.get('Content-Length', '0'))
        return json.loads(self.rfile.read(length) or b'{}')

    def do_GET(self):
        init_db()
        path = urlparse(self.path).path
        if path == '/api/health':
            return json_response(self, {'ok': True, 'service': 'novaspark'})
        if path == '/api/leads':
            return json_response(self, {'leads': get_leads()})
        if path == '/api/approvals':
            with connect() as con:
                rows = con.execute('SELECT * FROM approvals ORDER BY id DESC').fetchall()
            return json_response(self, {'approvals': [dict(r) for r in rows]})
        return json_response(self, {'error': 'not found'}, 404)

    def do_POST(self):
        try:
            init_db(); path = urlparse(self.path).path; data = self.read_json()
            if path == '/api/leads':
                lead_id = add_lead(data['business_name'], data.get('website',''), data.get('industry',''), data.get('location',''), data.get('contact',''), data.get('notes',''))
                return json_response(self, {'lead_id': lead_id}, 201)
            if path == '/api/leads/qualify':
                return json_response(self, qualify_lead(int(data['lead_id']), int(data.get('minimum_score', 60))))
            if path == '/api/outreach/draft':
                draft = create_draft(data['business_name'], data.get('industry',''), data.get('website',''), data.get('opportunity',''))
                approval = request_approval('send_outreach', {'business_name': data['business_name'], 'subject': draft.subject, 'body': draft.body})
                return json_response(self, {'subject': draft.subject, 'body': draft.body, 'approval': approval})
            if path == '/api/approvals/decision':
                return json_response(self, set_approval(int(data['approval_id']), data['status']))
            return json_response(self, {'error': 'not found'}, 404)
        except (KeyError, ValueError, json.JSONDecodeError) as exc:
            return json_response(self, {'error': str(exc)}, 400)

    def log_message(self, *_):
        pass


def run(host='127.0.0.1', port=8080):
    init_db(); print(f'NovaSpark API: http://{host}:{port}')
    HTTPServer((host, port), API).serve_forever()


if __name__ == '__main__':
    run()
