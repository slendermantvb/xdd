import os
import socket
import json
import time
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

# PUERTOS
HTTP_PORT = int(os.environ.get("PORT", 9000))
UDP_PORT = 9001

# =========================
# UDP SERVER
# =========================
def udp_loop():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("0.0.0.0", UDP_PORT))
    print(f"UDP activo en {UDP_PORT}")

    while True:
        data, addr = udp.recvfrom(4096)
        udp.sendto(b"OK", addr)

# =========================
# HTTP HEALTHCHECK
# =========================
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def http_loop():
    print(f"HTTP activo en {HTTP_PORT}")
    HTTPServer(("0.0.0.0", HTTP_PORT), Handler).serve_forever()

# =========================
# START
# =========================
threading.Thread(target=udp_loop, daemon=True).start()
http_loop()   # ⚠️ BLOQUEANTE (OBLIGATORIO)
