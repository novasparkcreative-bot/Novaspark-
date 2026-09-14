from http.server import BaseHTTPRequestHandler, HTTPServer
from database.db import init_db, connect

HTML = '''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>NovaSpark CEO</title><style>body{font-family:system-ui;max-width:1100px;margin:40px auto;padding:0 18px;background:#f5f7fb;color:#172033}.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:14px}.card{background:white;border:1px solid #e4e8f0;border-radius:14px;padding:20px}.num{font-size:30px;font-weight:700}h1{margin-bottom:4px}.muted{color:#667085}</style></head><body><h1>🤖 NovaSpark — Alex CEO</h1><p class="muted">Local operator dashboard</p><div class="grid">{cards}</div></body></html>'''


def stats():
    init_db()
    with connect() as con:
        def count(table, where="", args=()):
            q=f"SELECT COUNT(*) FROM {table}" + (f" WHERE {where}" if where else "")
            return con.execute(q,args).fetchone()[0]
        return {
            "Leads": count("leads"),
            "Qualified": count("leads", "status='qualified'"),
            "Outreach Queue": count("leads", "status='qualified'"),
            "Clients": count("clients"),
            "Paid": count("clients", "payment_status='paid'"),
            "Pending Approvals": count("approvals", "status='pending'"),
            "Open Tasks": count("tasks", "status NOT IN ('completed','cancelled')"),
        }


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        cards=''.join(f'<div class="card"><div class="muted">{k}</div><div class="num">{v}</div></div>' for k,v in stats().items())
        body=HTML.format(cards=cards).encode()
        self.send_response(200); self.send_header('Content-Type','text/html; charset=utf-8'); self.send_header('Content-Length',str(len(body))); self.end_headers(); self.wfile.write(body)
    def log_message(self, *_): pass


def run(host='127.0.0.1', port=8000):
    init_db(); print(f'NovaSpark dashboard: http://{host}:{port}')
    HTTPServer((host,port), Handler).serve_forever()

if __name__ == '__main__': run()
