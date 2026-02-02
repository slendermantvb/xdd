import socket
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# =========================
# UDP RENDEZVOUS SERVER
# =========================
nodes = {}

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(("0.0.0.0", 9000))

print("🌍 GCP Rendezvous UDP activo en 9000")

def udp_loop():
    while True:
        data, addr = udp.recvfrom(4096)
        try:
            msg = json.loads(data.decode())
        except:
            continue

        now = time.time()

        if msg.get("type") == "REGISTER":
            nodes[msg["node_id"]] = {
                "addr": addr,
                "pub": msg["pub"],
                "last": now
            }

        elif msg.get("type") == "LOOKUP":
            target = msg.get("target")
            if target in nodes:
                udp.sendto(json.dumps({
                    "type": "FOUND",
                    "addr": nodes[target]["addr"],
                    "pub": nodes[target]["pub"]
                }).encode(), addr)
            else:
                udp.sendto(json.dumps({"type": "NOT_FOUND"}).encode(), addr)

        # cleanup
        for k in list(nodes.keys()):
            if now - nodes[k]["last"] > 120:
                del nodes[k]

# =========================
# HTTP HEALTHCHECK
# =========================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ["/", "/health", "/status"]:
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"OK")
        else:
            self.send_response(404)
            self.end_headers()

def http_loop():
    server = HTTPServer(("0.0.0.0", 9000), HealthHandler)
    print("🩺 HTTP healthcheck activo en 9000")
    server.serve_forever()

# =========================
# START
# =========================
threading.Thread(target=udp_loop, daemon=True).start()
http_loop()
