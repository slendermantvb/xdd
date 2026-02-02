# server.py
import socket
import json
import time

nodes = {}  # node_id -> {addr, pub, last_seen}

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(("0.0.0.0", 9000))

print("🌍 GCP Rendezvous Server activo en UDP 9000")

while True:
    data, addr = sock.recvfrom(4096)
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
        print(f"✔ Nodo registrado {msg['node_id'][:12]} {addr}")

    elif msg.get("type") == "LOOKUP":
        target = msg.get("target")
        if target in nodes:
            sock.sendto(json.dumps({
                "type": "FOUND",
                "addr": nodes[target]["addr"],
                "pub": nodes[target]["pub"]
            }).encode(), addr)
        else:
            sock.sendto(json.dumps({
                "type": "NOT_FOUND"
            }).encode(), addr)

    # limpieza simple
    for k in list(nodes.keys()):
        if now - nodes[k]["last"] > 120:
            del nodes[k]
