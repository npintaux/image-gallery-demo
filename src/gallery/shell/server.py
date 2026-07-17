"""Development server for the Visual Shell."""

import json
from http.server import SimpleHTTPRequestHandler, HTTPServer
import os
import sys

# Ensure src/ is on PYTHONPATH so we can import gallery.core
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))

# pylint: disable=import-error,wrong-import-position
from gallery.core.models import Request
from gallery.core.engine import LayoutEngine

PORT = 8080
SHELL_DIR = os.path.dirname(os.path.abspath(__file__))

class GalleryShellHandler(SimpleHTTPRequestHandler):
    """HTTP Request Handler that serves frontend assets and exposes layout API."""

    def __init__(self, *args, **kwargs):
        # Always serve files relative to the shell directory
        super().__init__(*args, directory=SHELL_DIR, **kwargs)

    def do_POST(self):  # pylint: disable=invalid-name
        """Handle POST requests, specifically /api/evaluate."""
        if self.path == "/api/evaluate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_data = self.rfile.read(content_length)

            try:
                data = json.loads(post_data.decode("utf-8"))
                viewport_width = int(data.get("viewport_width", 1024))
                photo_count = int(data.get("photo_count", 6))

                # Run the decision engine
                request = Request(viewport_width=viewport_width, photo_count=photo_count)
                engine = LayoutEngine()
                decision = engine.evaluate(request)

                response_data = {
                    "outcome": decision.outcome,
                    "rule_ids": decision.rule_ids,
                    "evaluated_at": decision.evaluated_at
                }

                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

            except Exception as e: # pylint: disable=broad-exception-caught
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

def run(server_class=HTTPServer, handler_class=GalleryShellHandler):
    """Run the development server."""
    server_address = ("", PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Development Server running at http://localhost:{PORT}")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    run()
