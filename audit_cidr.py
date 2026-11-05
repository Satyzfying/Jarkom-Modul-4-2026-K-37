#!/usr/bin/env python3
"""Audit gns3_configs/*.sh terhadap Sheet 4 (Pembagian IP - CIDR) di spreadsheet kelompok.

Cek:
1. Setiap alamat interface berada di subnet Sheet 4 dengan prefix yang sama dan tidak memakai
   network/broadcast address.
2. Setiap subnet Sheet 4 terpakai di konfigurasi.
3. Tidak ada IP ganda.
4. Simulasi forwarding: dari setiap node ke setiap IP interface lain harus sampai tanpa loop.
"""
import glob
import ipaddress
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.abspath(__file__))
XLSX = os.path.join(ROOT, "Kelompok 37 - Spreadsheet Modul 4 Komdat Jarkom 2026.xlsx")
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}


def read_sheet4():
    z = zipfile.ZipFile(XLSX)
    ss = [''.join(t.text or '' for t in si.iter('{%s}t' % NS["m"]))
          for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS)]
    root = ET.fromstring(z.read("xl/worksheets/sheet4.xml"))
    rows = []
    for row in root.iter('{%s}row' % NS["m"]):
        vals = []
        for c in row.findall("m:c", NS):
            v = c.find("m:v", NS)
            if v is None:
                vals.append(None)
                continue
            vals.append(ss[int(v.text)] if c.get("t") == "s" else v.text)
        rows.append(vals)
    out = {}
    for r in rows[1:]:
        if r and r[0] and r[0].startswith("A"):
            out[r[0]] = ipaddress.ip_network("%s/%s" % (r[1], r[2]))
    return out


def parse_configs():
    nodes = {}
    for path in sorted(glob.glob(os.path.join(ROOT, "gns3_configs", "*.sh"))):
        name = os.path.basename(path)[:-3]
        addrs, routes = [], []
        for line in open(path):
            m = re.match(r"ip addr add (\S+) dev (\S+)", line)
            if m:
                addrs.append((ipaddress.ip_interface(m.group(1)), m.group(2)))
            m = re.match(r"ip route add (\S+) via (\S+)", line)
            if m:
                net = "0.0.0.0/0" if m.group(1) == "default" else m.group(1)
                routes.append((ipaddress.ip_network(net), ipaddress.ip_address(m.group(2))))
        nodes[name] = {"addrs": addrs, "routes": routes}
    return nodes


def lookup(node, dst):
    best = None
    for a, _ in node["addrs"]:
        if dst in a.network and (best is None or a.network.prefixlen > best[0]):
            best = (a.network.prefixlen, None)
    for net, nh in node["routes"]:
        if dst in net and (best is None or net.prefixlen > best[0]):
            best = (net.prefixlen, nh)
    return best


def main():
    sheet = read_sheet4()
    nodes = parse_configs()
    errors = 0
    used = set()
    owner = {}
    print("Subnet  Sheet 4             Node:Interface = IP")
    for sid, net in sorted(sheet.items(), key=lambda x: int(x[0][1:])):
        members = []
        for name, n in nodes.items():
            for a, dev in n["addrs"]:
                if a.network == net:
                    members.append("%s:%s=%s" % (name, dev, a.ip))
        print("%-6s  %-18s  %s" % (sid, net, ", ".join(members) if members else "-"))
    for name, n in nodes.items():
        for a, dev in n["addrs"]:
            if str(a.network).startswith("192.168.122."):
                continue
            match = [sid for sid, net in sheet.items() if a.network == net]
            if not match:
                print("MISMATCH %s %s %s tidak ada di Sheet 4" % (name, dev, a))
                errors += 1
                continue
            if a.ip in (a.network.network_address, a.network.broadcast_address):
                print("INVALID %s %s %s network/broadcast" % (name, dev, a))
                errors += 1
            used.add(match[0])
            if a.ip in owner:
                print("DUPLICATE %s dipakai %s dan %s" % (a.ip, owner[a.ip], name))
                errors += 1
            owner[a.ip] = name
    for sid in sheet:
        if sid not in used:
            print("UNUSED subnet %s %s" % (sid, sheet[sid]))
            errors += 1

    # simulasi forwarding hop-by-hop
    ip_owner = {ip: name for ip, name in owner.items()}
    fails = 0
    pairs = 0
    for src in nodes:
        for dst_ip, dst_name in ip_owner.items():
            pairs += 1
            cur, seen = src, []
            ok = False
            while len(seen) < 20:
                if cur == dst_name:
                    ok = True
                    break
                seen.append(cur)
                r = lookup(nodes[cur], dst_ip)
                if r is None:
                    break
                nh = r[1] if r[1] is not None else dst_ip
                if nh not in ip_owner:
                    break
                cur = ip_owner[nh]
            if not ok:
                fails += 1
                if fails <= 10:
                    print("UNREACHABLE %s -> %s (%s) jalur: %s" % (src, dst_ip, dst_name, " > ".join(seen)))
    print()
    print("Subnet Sheet 4 : %d, terpakai: %d" % (len(sheet), len(used)))
    print("Uji jalur forwarding: %d pasang, gagal: %d" % (pairs, fails))
    errors += fails
    print("HASIL: %s" % ("0 mismatch, konfigurasi sesuai Sheet 4" if errors == 0 else "%d masalah" % errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
