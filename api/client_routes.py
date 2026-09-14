import json
from http.server import BaseHTTPRequestHandler
from core.client.client_lifecycle import start_onboarding, complete_onboarding
from core.client.project_manager import create_project
from core.client.projects import update_task_status


def send_json(handler, payload, status=200):
    body=json.dumps(payload, ensure_ascii=False).encode()
    handler.send_response(status); handler.send_header('Content-Type','application/json; charset=utf-8'); handler.send_header('Content-Length',str(len(body))); handler.end_headers(); handler.wfile.write(body)


def handle_client_post(handler, path, data):
    if path == '/api/clients/onboarding/start': return send_json(handler, start_onboarding(int(data['client_id'])))
    if path == '/api/clients/onboarding/complete': return send_json(handler, complete_onboarding(int(data['client_id'])))
    if path == '/api/projects': return send_json(handler, create_project(int(data['client_id']), data['services']), 201)
    if path == '/api/tasks/status': return send_json(handler, update_task_status(int(data['task_id']), data['status']))
    return None
