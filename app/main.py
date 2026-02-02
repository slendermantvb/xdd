import threading
import socket
from http.server import BaseHTTPRequestHandler, HTTPServer

# ----------------------------
# HTTP HEALTHCHECK (9000)
# ----------------------------
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path in ("/", "/status", "/health"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"GCPNode ONLINE")
        else:
            self.send_response(404)
            self.end_headers()

def start_http():
    server = HTTPServer(("0.0.0.0", 9000), HealthHandler)
    print("[HTTP] Healthcheck en puerto 9000")
    server.serve_forever()

# ----------------------------
# TU PROTOCOLO REAL (9001)
# ----------------------------
def start_gcpnode():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 9001))
    s.listen()
    print("[GCPNode] Protocolo activo en puerto 9001")

    while True:
        conn, addr = s.accept()
        print("Nodo conectado:", addr)
        conn.send(b"GCPNode E2E READY\n")
        conn.close()

# ----------------------------
# START
# ----------------------------
if __name__ == "__main__":
    threading.Thread(target=start_http, daemon=True).start()
    start_gcpnode()
