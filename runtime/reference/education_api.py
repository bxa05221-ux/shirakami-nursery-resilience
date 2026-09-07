#!/usr/bin/env python3
"""Dependency-free reference server for Shirakami Education API v0.1.

This is a prototype, not a production childcare system. Data is in-memory.
The implementation demonstrates the protocol boundary and the key rule:
report-time checklists are derived from approved plan goals.
"""
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
import json
import uuid
from urllib.parse import urlparse

PLANS = {}
PRACTICE = {}
REPORTS = {}
REFLECTIONS = {}


def new_id(prefix):
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def send_json(handler, status, payload):
    body = json.dumps(payload, ensure_ascii=False, indent=2).encode("utf-8")
    handler.send_response(status)
    handler.send_header("Content-Type", "application/json; charset=utf-8")
    handler.send_header("Content-Length", str(len(body)))
    handler.end_headers()
    handler.wfile.write(body)


class Handler(BaseHTTPRequestHandler):
    def read_json(self):
        length = int(self.headers.get("Content-Length", "0"))
        if length == 0:
            return {}
        return json.loads(self.rfile.read(length))

    def do_GET(self):
        path = urlparse(self.path).path
        parts = [p for p in path.split("/") if p]

        if parts == ["health"]:
            return send_json(self, 200, {"status": "ok", "service": "shirakami-education-api", "version": "0.1"})

        if len(parts) == 4 and parts[:3] == ["api", "v1", "education"] and parts[3] == "openapi":
            return send_json(self, 200, {"message": "Use api/education-openapi.yaml from the repository."})

        if len(parts) == 5 and parts[:3] == ["api", "v1", "education"]:
            resource, ident = parts[3], parts[4]
            stores = {"plans": PLANS, "reports": REPORTS}
            if resource in stores and ident in stores[resource]:
                return send_json(self, 200, stores[resource][ident])
            if resource == "reflection" and ident in REFLECTIONS:
                return send_json(self, 200, REFLECTIONS[ident])

        if len(parts) == 6 and parts[:3] == ["api", "v1", "education"] and parts[3] == "reflection" and parts[5] == "answers":
            return send_json(self, 200, REFLECTIONS.get(parts[4], {"reportId": parts[4], "questions": []}))

        if len(parts) == 6 and parts[:3] == ["api", "v1", "education"] and parts[3] == "continuity":
            student_id = parts[4]
            records = [r for r in REPORTS.values() if r.get("studentId") == student_id]
            return send_json(self, 200, {
                "studentId": student_id,
                "stage": "practicum",
                "learningRecords": records,
                "unresolvedQuestions": [q for r in records for q in r.get("questions", [])],
                "humanReviewRequired": True,
            })

        return send_json(self, 404, {"error": "not_found"})

    def do_POST(self):
        path = urlparse(self.path).path
        parts = [p for p in path.split("/") if p]
        try:
            data = self.read_json()
        except (json.JSONDecodeError, ValueError):
            return send_json(self, 400, {"error": "invalid_json"})

        if parts == ["api", "v1", "education", "plans"]:
            if not data.get("studentId") or not data.get("date") or not data.get("class") or not data.get("goals"):
                return send_json(self, 400, {"error": "studentId, date, class and goals are required"})
            plan_id = new_id("plan")
            plan = {**data, "planId": plan_id, "status": data.get("status", "draft")}
            PLANS[plan_id] = plan
            return send_json(self, 201, {"planId": plan_id, "status": plan["status"], "humanApprovalRequired": True})

        if parts == ["api", "v1", "education", "practice"]:
            if not data.get("planId") or not data.get("events"):
                return send_json(self, 400, {"error": "planId and events are required"})
            practice_id = new_id("practice")
            PRACTICE[practice_id] = {**data, "practiceId": practice_id}
            return send_json(self, 201, {"practiceId": practice_id})

        if parts == ["api", "v1", "education", "reports"]:
            plan_id = data.get("planId")
            if plan_id not in PLANS:
                return send_json(self, 404, {"error": "plan_not_found"})
            plan = PLANS[plan_id]
            if plan.get("status") != "approved":
                return send_json(self, 409, {"error": "plan_must_be_approved_before_report"})
            results_by_goal = {r.get("goal"): r for r in data.get("goalResults", [])}
            checklist = []
            questions = []
            for goal in plan["goals"]:
                result = results_by_goal.get(goal, {"goal": goal, "status": "not_observed"})
                checklist.append(result)
                if result["status"] in ("partial", "not_achieved"):
                    questions.append(f"『{goal}』について、実際の子どもの姿と計画の間にどんな違いがありましたか？")
            report_id = new_id("report")
            report = {
                "reportId": report_id,
                "planId": plan_id,
                "studentId": plan["studentId"],
                "checklist": checklist,
                "questions": questions,
                "humanReviewRequired": True,
            }
            REPORTS[report_id] = report
            REFLECTIONS[report_id] = {"reportId": report_id, "questions": questions}
            return send_json(self, 201, report)

        if len(parts) == 7 and parts[:3] == ["api", "v1", "education"] and parts[3] == "reflection" and parts[5] == "answers":
            report_id = parts[4]
            if report_id not in REPORTS:
                return send_json(self, 404, {"error": "report_not_found"})
            REPORTS[report_id]["reflectionAnswers"] = data.get("answers", [])
            return send_json(self, 201, {"reportId": report_id, "recorded": True})

        return send_json(self, 404, {"error": "not_found"})

    def log_message(self, fmt, *args):
        print(fmt % args)


if __name__ == "__main__":
    host, port = "0.0.0.0", 8000
    print(f"Shirakami Education API listening on http://localhost:{port}")
    ThreadingHTTPServer((host, port), Handler).serve_forever()
