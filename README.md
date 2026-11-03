# Praktikum Jaringan Komputer 2026 - Modul 4 (Kelompok 37)

Repositori ini berisi seluruh deliverable untuk **Orang 1: Full Cisco Packet Tracer (CPT) + VLSM Subnetting** Praktikum Modul 4 Jarkom 2026.

---

## 1. Ringkasan Pengalamatan IP & Subnetting VLSM
- **Prefix Kelompok**: `10.82.0.0/19`
- **Subnet Mask Supernet**: `255.255.224.0`
- **Total Alokasi Host**: 8,192 IP Addresses
- **Jumlah Subnet**: 25 Subnet (16 LAN/Multi-Access + 9 Link Point-to-Point WAN)
- **Metode**: Variable Length Subnet Masking (VLSM) diurutkan dari kebutuhan host terbesar ke terkecil.

### Tabel Perhitungan VLSM (25 Subnet)

| No | Subnet Name | Kebutuhan Host | Netmask (/Prefix) | Network IP | Usable IP Range | Broadcast IP | Gateway IP |
|:---|:---|:---:|:---|:---|:---|:---|:---|
| 1 | **Switch3** | 881 | 255.255.252.0 (/22) | `10.82.0.0` | `10.82.0.1 - 10.82.3.254` | `10.82.3.255` | `10.82.0.1` (R-Psyche Fa0/1) |
| 2 | **Switch5** | 514 | 255.255.252.0 (/22) | `10.82.4.0` | `10.82.4.1 - 10.82.7.254` | `10.82.7.255` | `10.82.4.1` (R-Accela Fa0/1) |
| 3 | **Switch4** | 301 | 255.255.254.0 (/23) | `10.82.8.0` | `10.82.8.1 - 10.82.9.254` | `10.82.9.255` | `10.82.8.1` (R-Copland Fa0/1) |
| 4 | **Switch9** | 287 | 255.255.254.0 (/23) | `10.82.10.0` | `10.82.10.1 - 10.82.11.254` | `10.82.11.255` | `10.82.10.1` (R-Tachibana Fa0/1) |
| 5 | **Switch6** | 254 | 255.255.255.0 (/24) | `10.82.12.0` | `10.82.12.1 - 10.82.12.254` | `10.82.12.255` | `10.82.12.1` (R-Navi Fa0/0) |
| 6 | **Switch8** | 143 | 255.255.255.0 (/24) | `10.82.13.0` | `10.82.13.1 - 10.82.13.254` | `10.82.13.255` | `10.82.13.1` (R-Navi Fa0/1) |
| 7 | **Switch10** | 99 | 255.255.255.128 (/25) | `10.82.14.0` | `10.82.14.1 - 10.82.14.126` | `10.82.14.127` | `10.82.14.1` (R-Deus Fa0/1) |
| 8 | **Switch1** | 86 | 255.255.255.128 (/25) | `10.82.14.128` | `10.82.14.129 - 10.82.14.254` | `10.82.14.255` | `10.82.14.129` (R-Cyberia Fa0/1) |
| 9 | **Switch13** | 62 | 255.255.255.192 (/26) | `10.82.15.0` | `10.82.15.1 - 10.82.15.62` | `10.82.15.63` | `10.82.15.1` (R-Shibuya Fa0/1) |
| 10 | **Switch7** | 58 | 255.255.255.192 (/26) | `10.82.15.64` | `10.82.15.65 - 10.82.15.126` | `10.82.15.127` | `10.82.15.65` (R-Navi Fa1/0) |
| 11 | **Switch11** | 33 | 255.255.255.192 (/26) | `10.82.15.128` | `10.82.15.129 - 10.82.15.190` | `10.82.15.191` | `10.82.15.129` (R-Protocol7 Fa0/1) |
| 12 | **Juri (P2P)** | 32 | 255.255.255.192 (/26) | `10.82.15.192` | `10.82.15.193 - 10.82.15.254` | `10.82.15.255` | `10.82.15.193` (R-Copland Fa1/0) |
| 13 | **Switch12** | 15 | 255.255.255.224 (/27) | `10.82.16.0` | `10.82.16.1 - 10.82.16.30` | `10.82.16.31` | `10.82.16.1` (R-Phantoma Fa0/1) |
| 14 | **Switch2 (Multi-Access)** | 4 | 255.255.255.248 (/29) | `10.82.16.32` | `10.82.16.33 - 10.82.16.38` | `10.82.16.39` | Multi-Access Bus |
| 15 | **Akashic (P2P)** | 4 | 255.255.255.248 (/29) | `10.82.16.40` | `10.82.16.41 - 10.82.16.46` | `10.82.16.47` | `10.82.16.41` (R-Schumann Fa0/1) |
| 16 | **Eiri (P2P)** | 3 | 255.255.255.248 (/29) | `10.82.16.48` | `10.82.16.49 - 10.82.16.54` | `10.82.16.55` | `10.82.16.49` (R-Knights Fa0/1) |
| 17 | **P2P Cyberia - Wired** | 2 | 255.255.255.252 (/30) | `10.82.16.56` | `10.82.16.57 - 10.82.16.58` | `10.82.16.59` | `10.82.16.57` (Cyberia Fa1/0) |
| 18 | **P2P Wired - Navi** | 2 | 255.255.255.252 (/30) | `10.82.16.60` | `10.82.16.61 - 10.82.16.62` | `10.82.16.63` | `10.82.16.61` (Wired Eth0/0/0) |
| 19 | **P2P Wired - Tachibana** | 2 | 255.255.255.252 (/30) | `10.82.16.64` | `10.82.16.65 - 10.82.16.66` | `10.82.16.67` | `10.82.16.65` (Wired Fa1/0) |
| 20 | **P2P Schumann - Accela** | 2 | 255.255.255.252 (/30) | `10.82.16.68` | `10.82.16.69 - 10.82.16.70` | `10.82.16.71` | `10.82.16.69` (Schumann Fa1/0) |
| 21 | **P2P Tachibana - Deus** | 2 | 255.255.255.252 (/30) | `10.82.16.72` | `10.82.16.73 - 10.82.16.74` | `10.82.16.75` | `10.82.16.73` (Tachibana Fa1/0) |
| 22 | **P2P Deus - Protocol7** | 2 | 255.255.255.252 (/30) | `10.82.16.76` | `10.82.16.77 - 10.82.16.78` | `10.82.16.79` | `10.82.16.77` (Deus Fa1/0) |
| 23 | **P2P Protocol7 - Knights** | 2 | 255.255.255.252 (/30) | `10.82.16.80` | `10.82.16.81 - 10.82.16.82` | `10.82.16.83` | `10.82.16.81` (Protocol7 Fa1/0) |
| 24 | **P2P Knights - Phantoma** | 2 | 255.255.255.252 (/30) | `10.82.16.84` | `10.82.16.85 - 10.82.16.86` | `10.82.16.87` | `10.82.16.85` (Knights Fa1/0) |
| 25 | **P2P Phantoma - Shibuya** | 2 | 255.255.255.252 (/30) | `10.82.16.88` | `10.82.16.89 - 10.82.16.90` | `10.82.16.91` | `10.82.16.89` (Phantoma Fa1/0) |

---

## 2. Diagram Pohon VLSM (Binary Tree)

Struktur pembagian blok IP hierarkis dari supernet `10.82.0.0/19`:

```text
10.82.0.0/19 (Kelompok 37 - 8192 IPs)
├── 10.82.0.0/20 (Subnet 1 - 12: 4096 IPs)
│   ├── 10.82.0.0/21 (2048 IPs)
│   │   ├── 10.82.0.0/22  --> [Subnet 1] Switch3 (881 IPs, Psyche)
│   │   └── 10.82.4.0/22  --> [Subnet 2] Switch5 (514 IPs, Accela)
│   └── 10.82.8.0/21 (2048 IPs)
│       ├── 10.82.8.0/22 (1024 IPs)
│       │   ├── 10.82.8.0/23   --> [Subnet 3] Switch4 (301 IPs, Copland)
│       │   └── 10.82.10.0/23  --> [Subnet 4] Switch9 (287 IPs, Tachibana)
│       └── 10.82.12.0/22 (1024 IPs)
│           ├── 10.82.12.0/23 (512 IPs)
│           │   ├── 10.82.12.0/24  --> [Subnet 5] Switch6 (254 IPs, Navi)
│           │   └── 10.82.13.0/24  --> [Subnet 6] Switch8 (143 IPs, Navi)
│           └── 10.82.14.0/23 (512 IPs)
│               ├── 10.82.14.0/24 (256 IPs)
│               │   ├── 10.82.14.0/25   --> [Subnet 7] Switch10 (99 IPs, Deus)
│               │   └── 10.82.14.128/25 --> [Subnet 8] Switch1 (86 IPs, Cyberia)
│               └── 10.82.15.0/24 (256 IPs)
│                   ├── 10.82.15.0/25 (128 IPs)
│                   │   ├── 10.82.15.0/26   --> [Subnet 9] Switch13 (62 IPs, Shibuya)
│                   │   └── 10.82.15.64/26  --> [Subnet 10] Switch7 (58 IPs, Navi)
│                   └── 10.82.15.128/25 (128 IPs)
│                       ├── 10.82.15.128/26 --> [Subnet 11] Switch11 (33 IPs, Protocol7)
│                       └── 10.82.15.192/26 --> [Subnet 12] Juri (32 IPs, Copland)
└── 10.82.16.0/20 (Subnet 13 - 25 + Unallocated: 4096 IPs)
    └── 10.82.16.0/24 (256 IPs)
        ├── 10.82.16.0/27  --> [Subnet 13] Switch12 (15 IPs, Phantoma)
        ├── 10.82.16.32/29 --> [Subnet 14] Switch2 Multi-Access (Wired, Psyche, Copland, Schumann)
        ├── 10.82.16.40/29 --> [Subnet 15] Akashic (Schumann)
        ├── 10.82.16.48/29 --> [Subnet 16] Eiri (Knights)
        ├── 10.82.16.56/30 --> [Subnet 17] P2P Cyberia - Wired
        ├── 10.82.16.60/30 --> [Subnet 18] P2P Wired - Navi
        ├── 10.82.16.64/30 --> [Subnet 19] P2P Wired - Tachibana
        ├── 10.82.16.68/30 --> [Subnet 20] P2P Schumann - Accela
        ├── 10.82.16.72/30 --> [Subnet 21] P2P Tachibana - Deus
        ├── 10.82.16.76/30 --> [Subnet 22] P2P Deus - Protocol7
        ├── 10.82.16.80/30 --> [Subnet 23] P2P Protocol7 - Knights
        ├── 10.82.16.84/30 --> [Subnet 24] P2P Knights - Phantoma
        ├── 10.82.16.88/30 --> [Subnet 25] P2P Phantoma - Shibuya
        └── 10.82.16.92 - 10.82.31.255 (Unallocated reserve)
```

Diagram visual tersimpan dalam:
- [pohon_vlsm.svg](pohon_vlsm.svg) (Format Vector High Definition)
- [pohon_vlsm.png](pohon_vlsm.png) (Format Gambar Bitmap Raster)

---

## 3. Topologi Cisco Packet Tracer (`Modul4_K37_Topology.pkt`)

File `.pkt` dibangun secara otomatis menggunakan library crypt/compression Twofish-EAX + qCompress dan telah divalidasi dengan `pkt audit` (**RESULT: PASSED (0 failures, 0 warnings)**).

### Perangkat yang Dibangun:
1. **13 Router Cisco 2811**:
   - `Cyberia` (Gateway Internet & NAT Overload)
   - `Wired` (Core Hub Barat & Timur)
   - `Navi` (Distribution Hub Switch 6, 7, 8)
   - `Psyche`, `Copland`, `Schumann`, `Accela` (West Branch)
   - `Tachibana`, `Deus`, `Protocol7`, `Knights`, `Phantoma`, `Shibuya` (East Daisy Chain)
   - Modul Tambahan Terpasang:
     - `PT-ROUTER-NM-1CFE` di Slot 5 (menghasilkan FastEthernet1/0)
     - `WIC-1ENET` di Slot 1 (menghasilkan Ethernet0/0/0 untuk link Wired - Navi)
2. **13 Switch Cisco 2960-24TT**:
   - Switch1 s.d. Switch13.
3. **25 End Devices (PC, Laptop, Server)**:
   - Terkonfigurasi IP Address, Subnet Mask, dan Default Gateway sesuai tabel VLSM.
4. **1 Cloud-PT (Internet)**:
   - Terhubung ke `Cyberia` Fa0/0 via `Ethernet6` (DHCP client / NAT Overload).

---

## 4. Konfigurasi Cisco IOS Router (`configs/`)

Seluruh file konfigurasi native Cisco IOS CLI disimpan di direktori `configs/`:
- `R-Cyberia.cfg`: NAT Overload ke Cloud, static route ke seluruh subnet LAN, default route `0.0.0.0 0.0.0.0 Fa0/0`.
- `R-Wired.cfg`: Central transit router untuk Switch2 multi-access, Tachibana, Navi, dan Cyberia.
- `R-Psyche.cfg`, `R-Copland.cfg`, `R-Schumann.cfg`, `R-Accela.cfg`: Subnet routing sisi barat.
- `R-Tachibana.cfg`, `R-Deus.cfg`, `R-Protocol7.cfg`, `R-Knights.cfg`, `R-Phantoma.cfg`, `R-Shibuya.cfg`: Subnet routing daisy chain sisi timur.
- `R-Navi.cfg`: Router tiga subnet LAN (Switch6, Switch7, Switch8).

Semua routing menggunakan **Static Routing murni** (tanpa dynamic routing) sesuai aturan modul.

---

## 5. Deliverables Checklist

- [x] **File .PKT Topologi**: `Modul4_K37_Topology.pkt` (Tersedia, tervalidasi 0 fail).
- [x] **Spreadsheet Perhitungan VLSM**: `Template Spreadsheet Modul 4 Komdat Jarkom 2026 - Kelompok 37.xlsx` (Stylized & auto-calculated).
- [x] **Diagram Tree VLSM**: `pohon_vlsm.svg` dan `pohon_vlsm.png`.
- [x] **Running Config 13 Router**: `configs/R-*.cfg`.
- [x] **Rollback Script**: `../rollback_orang1.sh`.

---

## 6. Verifikasi & Pengujian

Untuk membuka dan memverifikasi topologi:
1. Buka aplikasi **Cisco Packet Tracer**.
2. Klik **File -> Open...** lalu pilih `Modul4_K37_Topology.pkt`.
3. Seluruh link antar perangkat akan berstatus hijau (up/up).
4. Lakukan ping test dari end device (contoh: PC JJ `10.82.14.130`) ke Server Karl (`10.82.0.2`) atau ke PC Mika (`10.82.15.3`).
