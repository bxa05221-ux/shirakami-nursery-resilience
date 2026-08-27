"""Minimal reference API server for Shirakami Nursery Resilience alpha1.0.

This is a framework-free reference implementation intended for local prototyping.
It does not make professional, safeguarding, medical, or legal decisions.
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
from datetime import datetime, timezone

STATE = {"observations": [], "safety_signals": [], "anonymous_reports": []}


def now():
    return datetime.now(timezone.utc).isoformat()


def response(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/v1/landscape/daily":
            response(self, 200, {
                "date": now()[:10],
                "classes": [{"classId": f"class-{i}", "attendance": 0, "observationCount": 0, "supportLoad": 0} for i in range(1, 7)],
                "staffing": {"availableStaff": 0, "assignedStaff": 0, "requiredPolicyReference": "facility-policy", "surplusOrShortfall": 0},
                "external": {"weather": {}, "disaster": {}, "wildlife": {}, "local": {}, "sources": [], "retrievedAt": now()},
            })
            return
        if self.path == "/api/v1/external-landscape":
            response(self, 200, {"weather": {}, "disaster": {}, "wildlife": {}, "local": {}, "sources": [], "retrievedAt": now()})
            return
        response(self, 404, {"error": "not_found"})

    def do_POST(self):
        try:
            length = int(self.headers.get("Content-Length", "0"))
            data = json.loads(self.rfile.read(length) or b"{}")
        except (ValueError, json.JSONDecodeError):
            response(self, 400, {"error": "invalid_json"})
            return

        path = self.path
        if path.endswith("/observations") and "/children/" in path:
            record = {"id": f"obs-{len(STATE['observations'])+1}", "createdAt": now(), **data}
            STATE["observations"].append(record)
            response(self, 201, record)
            return
        if path == "/api/v1/safety/signals":
            record = {"id": f"safety-{len(STATE['safety_signals'])+1}", "createdAt": now(), "humanReviewRequired": True, **data}
            STATE["safety_signals"].append(record)
            response(self, 201, record)
            return
        if path == "/api/v1/reports/internal/anonymous":
            record = {"reportId": f"report-{len(STATE['anonymous_reports'])+1}", "receivedAt": now(), "status": "received", "identitySeparated": True, **data}
            STATE["anonymous_reports"].append(record)
            response(self, 202, record)
            return
        if path in ("/api/v1/plans/tomorrow",) or path.endswith("/plans/draft"):
            response(self, 200, {
                "status": "draft",
                "goals": [], "environment": [], "support": [], "checkpoints": [],
                "safetyPoints": [], "staffingConsiderations": [],
                "rationale": "Reference draft only. Human review and approval are required.",
                "sourceEvidenceIds": [],
            })
            return
        if path == "/api/v1/evaluation/evidence-summary":
            response(self, 200, {"period": "", "evidence": [], "improvementHistory": [], "openQuestions": [], "humanReviewRequired": True})
            return
        response(self, 404, {"error": "not_found"})

    def log_message(self, *_args):
        return


if __name__ == "__main__":
    print("Shirakami Nursery Resilience reference API: http://127.0.0.1:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
