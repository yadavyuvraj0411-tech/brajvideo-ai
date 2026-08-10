from http.server import BaseHTTPRequestHandler, HTTPServer
import json

class VideoAIHandler(BaseHTTPRequestHandler):

    def send_json(self, data, status=200):
        body = json.dumps(data).encode("utf-8")

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()

        self.wfile.write(body)

    def do_GET(self):
        if self.path == "/":
            self.send_json({
                "name": "BrajVideo AI",
                "status": "online",
                "message": "Video generation backend is ready."
            })
        else:
            self.send_json({"error": "Not found"}, 404)

    def do_POST(self):
        if self.path != "/generate":
            self.send_json({"error": "Not found"}, 404)
            return

        length = int(self.headers.get("Content-Length", 0))
        raw_data = self.rfile.read(length)

        try:
            data = json.loads(raw_data.decode("utf-8"))
            prompt = data.get("prompt", "")
            duration = data.get("duration", "10 minutes")
            language = data.get("language", "Hindi")

            if not prompt.strip():
                self.send_json({
                    "error": "Please provide a video prompt."
                }, 400)
                return

            self.send_json({
                "success": True,
                "status": "queued",
                "prompt": prompt,
                "duration": duration,
                "language": language,
                "message": "Your video generation request has been received."
            })

        except Exception:
            self.send_json({
                "error": "Invalid request."
            }, 400)


if __name__ == "__main__":
    server = HTTPServer(("0.0.0.0", 8000))

    print("BrajVideo AI backend running on port 8000...")

    server.serve_forever()
