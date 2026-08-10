from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import uuid
from datetime import datetime

from planner import create_scene_plan
from video_jobs import create_job, get_job


class BrajVideoAPI(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_OPTIONS(self):
        self.send_json({"ok": True})

    def do_GET(self):

        if self.path == "/":
            self.send_json({
                "name": "BrajVideo AI",
                "status": "online",
                "version": "0.1.0"
            })
            return

        if self.path.startswith("/job/"):
            job_id = self.path.split("/job/")[1]
            job = get_job(job_id)

            if job is None:
                self.send_json({"error": "Job not found"}, 404)
            else:
                self.send_json(job)

            return

        self.send_json({"error": "Not found"}, 404)

    def do_POST(self):

        if self.path != "/generate":
            self.send_json({"error": "Not found"}, 404)
            return

        try:
            length = int(self.headers.get("Content-Length", 0))
            raw_data = self.rfile.read(length)

            data = json.loads(raw_data.decode("utf-8"))

            prompt = data.get("prompt", "").strip()
            duration = int(data.get("duration_minutes", 10))
            language = data.get("language", "Hindi")

            if not prompt:
                self.send_json({
                    "error": "Please provide a video prompt."
                }, 400)
                return

            if duration < 1 or duration > 12:
                self.send_json({
                    "error": "Duration must be between 1 and 12 minutes."
                }, 400)
                return

            job = create_job(
                prompt=prompt,
                duration_minutes=duration,
                language=language
            )

            scene_plan = create_scene_plan(
                prompt,
                duration
            )

            job["scene_plan"] = scene_plan

            self.send_json({
                "success": True,
                "job": job
            })

        except ValueError:
            self.send_json({
                "error": "Duration must be a number."
            }, 400)

        except Exception as error:
            self.send_json({
                "error": str(error)
            }, 500)


if __name__ == "__main__":

    print("===================================")
    print("       BRAJVIDEO AI SERVER")
    print("===================================")
    print("Server running on port 8000")
    print("")

    server = HTTPServer(
        ("0.0.0.0", 8000),
        BrajVideoAPI
    )

    server.serve_forever()
