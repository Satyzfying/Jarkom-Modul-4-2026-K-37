#!/usr/bin/env python3
"""Deploy gns3_configs/<Node>.sh ke /root/setup.sh tiap node lalu jalankan uji ping.

Hanya membaca daftar node dari project K-37-MODUL-4 (REST API GNS3 v3) dan mengakses
console telnet node. Tidak membuat / menghapus / menutup project maupun node.

Pemakaian (password dibaca dari environment, tidak disimpan di repo):
    export GNS3_PASS='...'
    python3 deploy_and_test_gns3.py            # deploy + test
    python3 deploy_and_test_gns3.py --test     # test saja
    python3 deploy_and_test_gns3.py --only Wired,Deus   # deploy node tertentu + test
"""
import base64
import json
import os
import random
import socket
import sys
import time
import urllib.request

SERVER = os.environ.get("GNS3_SERVER_URL", "http://10.4.89.247:80")
USER = os.environ.get("GNS3_USER", "K-37")
PASS = os.environ.get("GNS3_PASS")
if not PASS:
    sys.exit("Set dulu environment variable GNS3_PASS (password akun GNS3 kelompok)")
PROJECT_ID = "bcd23270-81df-44e6-ac2e-b2b331f3dbef"
PROJECT_NAME = "K-37-MODUL-4"
CONSOLE_HOST = SERVER.split("://")[1].split(":")[0]
CONF_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gns3_configs")

ORDER = ["Cyberia", "Wired", "Psyche", "Copland", "Schumann", "Accela", "Navi",
         "Tachibana", "Deus", "Protocol7", "Knights", "Phantoma", "Shibuya"]

TESTS = [
    # (node, target, keterangan)
    ("JJ", "10.82.24.3", "intra-LAN Switch1 (JJ -> MyuMyu)"),
    ("Karl", "10.82.10.83", "Karl -> Copland (Switch2)"),
    ("Karl", "10.82.8.2", "Karl -> Masayuki (lintas Switch2)"),
    ("Juri", "10.82.10.74", "Juri -> Akashic"),
    ("Akashic", "10.82.4.2", "Akashic -> Omnipresence"),
    ("Denpa", "10.82.0.3", "Denpa -> Lin"),
    ("Alice", "10.82.22.2", "Alice -> Taro (Navi)"),
    ("Kuma", "10.82.16.2", "Kuma -> Collective"),
    ("Collective", "10.82.18.2", "Collective -> Lilith"),
    ("Specter", "10.82.18.130", "Specter -> Chisa"),
    ("Hodgeson", "10.82.19.34", "Hodgeson -> Eiri"),
    ("Eiri", "10.82.19.2", "Eiri -> Semi"),
    ("Semi", "10.82.18.194", "Semi -> Lain"),
    ("Lain", "10.82.0.2", "Lain -> Karl (ujung ke ujung)"),
    ("Mika", "10.82.21.3", "Mika -> Miho (ujung ke ujung)"),
    ("Psyche", "10.82.19.41", "Psyche -> Wired eth2"),
    ("Shibuya", "10.82.19.46", "Shibuya -> Deus eth0"),
    ("Taro", "10.82.24.1", "Taro -> Cyberia"),
    ("JJ", "8.8.8.8", "JJ -> Internet (NAT Cyberia)"),
    ("Lain", "8.8.8.8", "Lain -> Internet (NAT Cyberia)"),
    ("Omnipresence", "8.8.8.8", "Omnipresence -> Internet (NAT Cyberia)"),
]

IAC, DONT, DO, WONT, WILL, SB, SE = 255, 254, 253, 252, 251, 250, 240


def api(method, path, data=None, token=None):
    headers = {"Content-Type": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    body = json.dumps(data).encode() if data is not None else None
    req = urllib.request.Request(SERVER + "/v3" + path, data=body, headers=headers, method=method)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.load(r)


def console_ports():
    token = api("POST", "/access/users/authenticate", {"username": USER, "password": PASS})["access_token"]
    project = api("GET", "/projects/%s" % PROJECT_ID, token=token)
    if project["name"] != PROJECT_NAME:
        sys.exit("Project ID tidak cocok dengan %s" % PROJECT_NAME)
    nodes = api("GET", "/projects/%s/nodes" % PROJECT_ID, token=token)
    return {n["name"]: n["console"] for n in nodes if n["node_type"] == "docker"}


def _strip_telnet(data, sock):
    out = bytearray()
    i = 0
    while i < len(data):
        b = data[i]
        if b == IAC and i + 1 < len(data):
            c = data[i + 1]
            if c in (DO, DONT, WILL, WONT) and i + 2 < len(data):
                if c == DO:
                    sock.sendall(bytes([IAC, WONT, data[i + 2]]))
                elif c == WILL:
                    sock.sendall(bytes([IAC, DONT, data[i + 2]]))
                i += 3
                continue
            if c == SB:
                j = data.find(bytes([IAC, SE]), i)
                i = j + 2 if j >= 0 else len(data)
                continue
            i += 2
            continue
        out.append(b)
        i += 1
    return bytes(out)


def run(port, cmd, timeout=60):
    tag = "M%06d" % random.randint(0, 999999)
    s = socket.create_connection((CONSOLE_HOST, port), timeout=10)
    s.settimeout(0.5)
    t0 = time.time()
    while time.time() - t0 < 1.0:
        try:
            if not s.recv(65536):
                break
        except socket.timeout:
            pass
    s.sendall(("echo %s''B; %s; echo %s''E\n" % (tag, cmd, tag)).encode())
    buf = b""
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            d = s.recv(65536)
            if not d:
                break
            buf += _strip_telnet(d, s)
            if (tag + "E").encode() in buf:
                break
        except socket.timeout:
            pass
    s.close()
    txt = buf.decode(errors="replace").replace("\r", "")
    a, b = txt.find(tag + "B"), txt.find(tag + "E")
    return txt[a + len(tag) + 1:b].strip("\n") if a >= 0 and b > a else txt


def deploy(ports, only=None):
    names = ORDER + sorted(n[:-3] for n in os.listdir(CONF_DIR) if n[:-3] not in ORDER)
    if only:
        names = [n for n in names if n in only]
    for name in names:
        body = open(os.path.join(CONF_DIR, name + ".sh"), "rb").read()
        b64 = base64.b64encode(body).decode()
        cmd = ("echo %s | base64 -d > /root/setup.sh && chmod +x /root/setup.sh && "
               "sh /root/setup.sh >/dev/null 2>&1; ip -4 -br a | grep -v '^lo'" % b64)
        print("[%s]" % name)
        print(run(ports[name], cmd))
        time.sleep(1.2)


def test(ports):
    passed = 0
    for node, target, desc in TESTS:
        out = run(ports[node], "ping -c 3 -W 2 %s" % target, timeout=30)
        ok = " 0% packet loss" in out
        passed += ok
        stat = [l for l in out.splitlines() if "packet loss" in l]
        print("%-4s %-42s %s" % ("PASS" if ok else "FAIL", desc, stat[0] if stat else out[-200:]))
        time.sleep(0.5)
    print("\n%d/%d uji ping berhasil" % (passed, len(TESTS)))
    return passed == len(TESTS)


def node_ips():
    ips = {}
    for f in sorted(os.listdir(CONF_DIR)):
        for line in open(os.path.join(CONF_DIR, f)):
            if line.startswith("ip addr add 10."):
                ips.setdefault(f[:-3], line.split()[3].split("/")[0])
    return ips


def mesh(ports):
    """Setiap node ping ke satu IP milik setiap node lain."""
    ips = node_ips()
    total = fail = 0
    for src in sorted(ips):
        targets = " ".join(ip for n, ip in sorted(ips.items()) if n != src)
        cmd = ("ok=0; bad=''; for t in %s; do if ping -c1 -W1 $t >/dev/null 2>&1; "
               "then ok=$((ok+1)); else bad=\"$bad $t\"; fi; done; echo \"$ok$bad\"" % targets)
        out = run(ports[src], cmd, timeout=120).strip().splitlines()[-1]
        ok = int(out.split()[0])
        bad = out.split()[1:]
        total += len(ips) - 1
        fail += len(bad)
        print("%-13s %2d/%d %s" % (src, ok, len(ips) - 1, ("GAGAL: " + " ".join(bad)) if bad else "OK"))
        time.sleep(0.3)
    print("\nFull-mesh: %d/%d ping berhasil" % (total - fail, total))
    return fail == 0


if __name__ == "__main__":
    if "--mesh" in sys.argv:
        sys.exit(0 if mesh(console_ports()) else 1)
    ports = console_ports()
    only = None
    if "--only" in sys.argv:
        only = sys.argv[sys.argv.index("--only") + 1].split(",")
    if "--test" not in sys.argv:
        deploy(ports, only)
        time.sleep(2)
    sys.exit(0 if test(ports) else 1)
