#!/usr/bin/env python3
"""Generate /root/setup.sh untuk setiap node GNS3 (Modul 4, CIDR, Kelompok 37).

Seluruh alamat mengikuti Sheet 4 "Pembagian IP - CIDR" pada spreadsheet kelompok.
Hasil disimpan di folder gns3_configs/<Node>.sh
"""
import ipaddress
import os

OUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gns3_configs")

# Sheet 4 - Pembagian IP CIDR
SUBNETS = {
    "A1":  "10.82.24.0/25",     # Cyberia > Switch1 > JJ, MyuMyu
    "A2":  "10.82.24.128/30",   # Cyberia > Wired
    "A3":  "10.82.19.40/30",    # Wired > Tachibana
    "A4":  "10.82.22.64/30",    # Wired > Navi
    "A5":  "10.82.10.80/29",    # Wired > Switch2 > Psyche, Copland, Schumann
    "A6":  "10.82.0.0/22",      # Psyche > Switch3 > Karl, Lin
    "A7":  "10.82.8.0/23",      # Copland > Switch4 > Masayuki
    "A8":  "10.82.10.0/26",     # Copland > Juri
    "A9":  "10.82.10.72/29",    # Schumann > Akashic
    "A10": "10.82.10.64/30",    # Schumann > Accela
    "A11": "10.82.4.0/22",      # Accela > Switch5 > Omnipresence, Denpa
    "A12": "10.82.20.0/24",     # Navi > Switch6 > Alice, Reika
    "A13": "10.82.21.0/24",     # Navi > Switch8 > Yasuo, Miho, Kuma
    "A14": "10.82.22.0/26",     # Navi > Switch7 > Taro
    "A15": "10.82.16.0/23",     # Tachibana > Switch9 > Collective, Ghost
    "A16": "10.82.19.44/30",    # Tachibana > Deus
    "A17": "10.82.18.0/25",     # Deus > Switch10 > Lilith, Specter
    "A18": "10.82.19.48/30",    # Deus > Protocol7
    "A19": "10.82.18.128/26",   # Protocol7 > Switch11 > Chisa, Hodgeson
    "A20": "10.82.19.52/30",    # Protocol7 > Knights
    "A21": "10.82.19.32/29",    # Knights > Eiri
    "A22": "10.82.19.56/30",    # Knights > Phantoma
    "A23": "10.82.19.0/27",     # Phantoma > Switch12 > Semi
    "A24": "10.82.19.60/30",    # Phantoma > Shibuya
    "A25": "10.82.18.192/26",   # Shibuya > Switch13 > Lain, Mika
}

# Uplink Cyberia ke NAT1 (virbr0 GNS3)
NAT_IP = "192.168.122.50/24"
NAT_GW = "192.168.122.1"


def ip(subnet, n):
    net = ipaddress.ip_network(SUBNETS[subnet])
    return str(net.network_address + n)


def cidr(subnet, n):
    return "%s/%d" % (ip(subnet, n), ipaddress.ip_network(SUBNETS[subnet]).prefixlen)


# Router: interface -> (subnet, host index), default gateway, static route
ROUTERS = {
    "Cyberia": {
        "ifaces": {"eth1": ("A1", 1), "eth2": ("A2", 1)},
        "default": None,
        "routes": [("10.82.0.0/19", ip("A2", 2))],
    },
    "Wired": {
        "ifaces": {"eth0": ("A2", 2), "eth1": ("A5", 1), "eth2": ("A3", 1), "eth3": ("A4", 1)},
        "default": ip("A2", 1),
        "routes": [
            # sayap barat (Switch2)
            ("10.82.0.0/22", ip("A5", 2)),     # Psyche LAN (A6)
            ("10.82.4.0/22", ip("A5", 4)),     # Accela LAN (A11)
            ("10.82.8.0/22", ip("A5", 3)),     # Copland: Switch4 (A7) + Juri (A8)
            ("10.82.10.64/28", ip("A5", 4)),   # Schumann: A10 + A9
            # sayap timur (Tachibana chain)
            ("10.82.16.0/22", ip("A3", 2)),
            # cabang Navi
            ("10.82.20.0/22", ip("A4", 2)),
        ],
    },
    "Psyche": {
        "ifaces": {"eth0": ("A5", 2), "eth1": ("A6", 1)},
        "default": ip("A5", 1),
        "routes": [],
    },
    "Copland": {
        "ifaces": {"eth0": ("A5", 3), "eth1": ("A7", 1), "eth2": ("A8", 1)},
        "default": ip("A5", 1),
        "routes": [],
    },
    "Schumann": {
        "ifaces": {"eth0": ("A5", 4), "eth1": ("A9", 1), "eth2": ("A10", 1)},
        "default": ip("A5", 1),
        "routes": [("10.82.4.0/22", ip("A10", 2))],
    },
    "Accela": {
        "ifaces": {"eth0": ("A10", 2), "eth1": ("A11", 1)},
        "default": ip("A10", 1),
        "routes": [],
    },
    "Navi": {
        "ifaces": {"eth0": ("A12", 1), "eth1": ("A13", 1), "eth2": ("A14", 1), "eth3": ("A4", 2)},
        "default": ip("A4", 1),
        "routes": [],
    },
    "Tachibana": {
        "ifaces": {"eth0": ("A3", 2), "eth1": ("A15", 1), "eth2": ("A16", 1)},
        "default": ip("A3", 1),
        "routes": [("10.82.18.0/23", ip("A16", 2))],
    },
    "Deus": {
        "ifaces": {"eth0": ("A16", 2), "eth1": ("A17", 1), "eth2": ("A18", 1)},
        "default": ip("A16", 1),
        "routes": [
            ("10.82.18.128/25", ip("A18", 2)),  # Switch11 + Switch13
            ("10.82.19.0/26", ip("A18", 2)),    # Switch12, Eiri, P2P sisi bawah
            ("10.82.19.40/30", ip("A16", 1)),   # P2P Wired-Tachibana (keluar dari /26 di atas)
        ],
    },
    "Protocol7": {
        "ifaces": {"eth0": ("A18", 2), "eth1": ("A19", 1), "eth2": ("A20", 1)},
        "default": ip("A18", 1),
        "routes": [
            ("10.82.18.192/26", ip("A20", 2)),  # Switch13
            ("10.82.19.0/26", ip("A20", 2)),    # Switch12, Eiri, P2P sisi bawah
            ("10.82.19.40/29", ip("A18", 1)),   # P2P Wired-Tachibana & Tachibana-Deus
        ],
    },
    "Knights": {
        "ifaces": {"eth0": ("A20", 2), "eth1": ("A21", 1), "eth2": ("A22", 1)},
        "default": ip("A20", 1),
        "routes": [
            ("10.82.18.192/26", ip("A22", 2)),
            ("10.82.19.0/27", ip("A22", 2)),
            ("10.82.19.60/30", ip("A22", 2)),
        ],
    },
    "Phantoma": {
        "ifaces": {"eth0": ("A22", 2), "eth1": ("A23", 1), "eth2": ("A24", 1)},
        "default": ip("A22", 1),
        "routes": [("10.82.18.192/26", ip("A24", 2))],
    },
    "Shibuya": {
        "ifaces": {"eth0": ("A24", 2), "eth1": ("A25", 1)},
        "default": ip("A24", 1),
        "routes": [],
    },
}

# Host: subnet, host index (gateway = IP pertama subnet, yaitu interface router)
HOSTS = {
    "JJ": ("A1", 2), "MyuMyu": ("A1", 3),
    "Karl": ("A6", 2), "Lin": ("A6", 3),
    "Masayuki": ("A7", 2),
    "Juri": ("A8", 2),
    "Akashic": ("A9", 2),
    "Omnipresence": ("A11", 2), "Denpa": ("A11", 3),
    "Alice": ("A12", 2), "Reika": ("A12", 3),
    "Yasuo": ("A13", 2), "Miho": ("A13", 3), "Kuma": ("A13", 4),
    "Taro": ("A14", 2),
    "Collective": ("A15", 2), "Ghost": ("A15", 3),
    "Lilith": ("A17", 2), "Specter": ("A17", 3),
    "Chisa": ("A19", 2), "Hodgeson": ("A19", 3),
    "Eiri": ("A21", 2),
    "Semi": ("A23", 2),
    "Lain": ("A25", 2), "Mika": ("A25", 3),
}


def iface_block(dev, addr):
    return ["ip addr flush dev %s" % dev,
            "ip addr add %s dev %s" % (addr, dev),
            "ip link set %s up" % dev,
            ""]


def router_script(name, r):
    lines = ["#!/bin/sh", "sysctl -w net.ipv4.ip_forward=1", ""]
    if name == "Cyberia":
        lines += iface_block("eth0", NAT_IP)
        lines += ["ip route add default via %s" % NAT_GW, ""]
    for dev, (sn, n) in sorted(r["ifaces"].items()):
        lines += iface_block(dev, cidr(sn, n))
    if r["default"]:
        lines += ["ip route add default via %s" % r["default"], ""]
    for net, nh in r["routes"]:
        lines.append("ip route add %s via %s" % (net, nh))
    if r["routes"]:
        lines.append("")
    if name == "Wired":
        # Switch2 multi-access: paket Psyche/Copland/Schumann di-forward balik ke eth1,
        # matikan ICMP redirect agar ping antar router di segmen ini bersih
        lines += ["sysctl -w net.ipv4.conf.all.send_redirects=0",
                  "sysctl -w net.ipv4.conf.eth1.send_redirects=0", ""]
    if name == "Cyberia":
        lines += ["iptables -t nat -F POSTROUTING",
                  "iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE",
                  "echo 'nameserver 8.8.8.8' > /etc/resolv.conf", ""]
    return "\n".join(lines).rstrip() + "\n"


def host_script(name, sn, n):
    lines = ["#!/bin/sh"]
    lines += iface_block("eth0", cidr(sn, n))
    lines += ["ip route add default via %s" % ip(sn, 1),
              "echo 'nameserver 8.8.8.8' > /etc/resolv.conf"]
    return "\n".join(lines) + "\n"


def build():
    scripts = {}
    for name, r in ROUTERS.items():
        scripts[name] = router_script(name, r)
    for name, (sn, n) in HOSTS.items():
        scripts[name] = host_script(name, sn, n)
    return scripts


def main():
    os.makedirs(OUT_DIR, exist_ok=True)
    scripts = build()
    for name, body in scripts.items():
        with open(os.path.join(OUT_DIR, name + ".sh"), "w", newline="\n") as f:
            f.write(body)
    print("%d file setup.sh ditulis ke %s" % (len(scripts), OUT_DIR))


if __name__ == "__main__":
    main()
