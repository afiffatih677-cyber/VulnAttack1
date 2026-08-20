vulnAttack v3.0 – Full Exploit Chain Engine

Author: Apipboys
Version: 3.0 FINAL (INTEGRATED)
Support: Termux | Kali Linux | Windows | macOS | Docker

---

📌 Deskripsi

vulnAttack adalah tools all-in-one untuk:

· Google Dorking (Multi-source: Google, Bing, DuckDuckGo)
· Vulnerability Scanning (14 jenis serangan)
· Deep Analysis (HTTP, DOM, JS, Header, Cookie, AJAX, WebSocket, API)
· Minor Vulnerability Analysis (X-Frame-Options, CSP, HSTS, cookie flags, info leak)
· Exploit & Deploy Webshell (RCE, LFI, SQLi)
· Deface Website (dengan template kustom)
· Generate POC & Report (HTML + JSON)
· Multi-thread & Proxy Support
· WAF/Cloudflare Bypass (dengan cloudscraper & integrasi modul bypass)

---

🔥 Fitur Lengkap

14 Jenis Serangan

No Serangan File Payload
1 SQL Injection sqli.txt
2 XSS (Reflected + Stored) xss.txt
3 LFI (Local File Inclusion) lfi.txt
4 RCE (Remote Code Execution) rce.txt
5 SSRF (Server-Side Request Forgery) ssrf.txt
6 XXE (XML External Entity) xxe.txt
7 NoSQL Injection nosqli.txt
8 SSTI (Server-Side Template Injection) ssti.txt
9 Command Injection cmd_injection.txt
10 LDAP Injection ldap.txt
11 Open Redirect open_redirect.txt
12 CSRF (Cross-Site Request Forgery) csrf.txt
13 File Upload file_upload.txt
14 Directory Traversal directories.txt

Total payload: 70.000+ (5000+ per kategori)

Fitur Bypass (Terintegrasi)

· ✅ Cloudflare – Menggunakan cloudscraper dengan flag --bypass-waf
· ✅ WAF Detection & Retry – Deteksi otomatis pola WAF dan percobaan ulang dengan delay eksponensial
· ✅ User-Agent Rotation – Rotasi UA dari config/user_agents.txt setiap request
· ✅ Header Spoofing – Header standar browser (Accept, Accept-Language, dll)
· ✅ Rate Limiting – Delay configurable antar request
· ✅ Proxy Support – Dari config/proxy.txt dengan flag --proxy

---

📁 Struktur Folder

```
vulnAttack/
├── vulnAttack.py                 # Main engine (integrasi bypass)
├── generate_payloads.py          # Generator payload (5000+ per kategori)
├── requirements.txt              # Dependencies
├── README.md                     # Dokumentasi ini
├── index.html                    # File deface kustom (opsional)
├── bypass/                       # Modul bypass (terintegrasi)
│   ├── __init__.py
│   ├── cloudflare.py
│   ├── waf.py
│   ├── captcha.py
│   ├── headers.py
│   ├── utils.py
│   └── README.md
├── config/
│   ├── proxy.txt                 # Daftar proxy (opsional)
│   ├── user_agents.txt           # Daftar User-Agent (opsional)
│   └── bypass_settings.json      # Konfigurasi bypass WAF/Cloudflare
├── templates/                    # Auto-generated (webshell + deface)
│   ├── webshell_*.php            # 15 template webshell
│   └── deface_*.html             # 10 template deface
├── payloads/                     # Auto-generated (14 file .txt)
└── results/                      # Hasil scan (auto-generated)
    ├── poc_target.com.html
    └── report_target.com.json
```

---

🚀 Cara Install

1. Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
git clone https://github.com/Apipboys/vulnAttack
cd vulnAttack
pip install -r requirements.txt
python generate_payloads.py
```

2. Kali Linux

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install python3 python3-pip git -y
git clone https://github.com/Apipboys/vulnAttack
cd vulnAttack
pip3 install -r requirements.txt
python3 generate_payloads.py
```

3. Windows

```cmd
pip install requests colorama
git clone https://github.com/Apipboys/vulnAttack
cd vulnAttack
python generate_payloads.py
```

4. macOS

```bash
brew install python git
pip3 install -r requirements.txt
python3 generate_payloads.py
```

5. Docker

```bash
docker build -t vulnattack .
docker run -it --rm vulnattack http://target.com
```

---

🛠 Cara Pakai

Basic Usage

```bash
# Scan single target
python vulnAttack.py http://target.com

# Dengan proxy
python vulnAttack.py http://target.com --proxy

# Bypass WAF/Cloudflare (memerlukan cloudscraper)
python vulnAttack.py http://target.com --bypass-waf

# Delay antar request (detik)
python vulnAttack.py http://target.com --delay 2

# Output ke direktori kustom
python vulnAttack.py http://target.com --output /path/to/output
```

Dorking

```bash
# Multi-dork (Google + Bing + DuckDuckGo)
python vulnAttack.py --dork "inurl:index.php?id="

# Dengan proxy dan bypass WAF
python vulnAttack.py --dork "inurl:index.php?id=" --proxy --bypass-waf
```

Multi-target (List)

```bash
# Scan dari file (satu URL per baris)
python vulnAttack.py --list targets.txt --threads 20
```

Menu Interaktif

Jika dijalankan tanpa argumen:

```bash
python vulnAttack.py
```

Akan muncul menu:

```
MAIN MENU
  [1] Scan Target
  [2] Dorking
  [3] Scan List Target
  [4] Help
  [5] Exit
```

Setelah scan selesai, muncul menu:

```
INTERACTIVE MENU
  [1] Deploy Webshell
  [2] Deface Website
  [3] Generate POC
  [4] Show Deep Analysis
  [5] Show Minor Vulnerabilities
  [6] Scan Another Target
  [7] Exit
```

---

⚙️ Konfigurasi

config/proxy.txt

```
# Format: http://user:pass@ip:port
# http://127.0.0.1:8080
# http://192.168.1.1:3128
# socks5://127.0.0.1:9050
```

config/user_agents.txt

Satu User-Agent per baris. Contoh:

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0
```

config/bypass_settings.json

Konfigurasi bypass WAF/Cloudflare. Contoh:

```json
{
  "bypass": {
    "waf": {
      "detection": true,
      "retry_on_block": true,
      "max_retries": 3,
      "retry_delay": 5
    },
    "delay": {
      "min": 1,
      "max": 3,
      "randomize": true
    }
  }
}
```

---

📦 Dependencies

· requests>=2.28.0
· colorama>=0.4.6
· cloudscraper (opsional, untuk bypass WAF/Cloudflare)

---

🧪 Contoh Output

Terminal

```
[+] Target: http://target.com
[+] Crawling: http://target.com (depth 0)
[+] Testing SQL Injection...
[+] SQLi found: http://target.com?id=1' OR '1'='1
[+] Found 3 major vulnerabilities.
  - SQLi @ http://target.com?id=1' OR '1'='1
  - XSS (Reflected) @ http://target.com?q=<script>alert(1)</script>
  - RCE @ http://target.com?cmd=id
```

POC Report (results/poc_target.com.html)

· Daftar semua kerentanan (major + minor)
· Payload dan evidence
· Webshell & Deface URL
· Deep Analysis (headers, cookies, forms, ajax, api)

---

📝 Catatan

· Payload generator (generate_payloads.py) hanya perlu dijalankan sekali (saat pertama install atau update payload).
· Template webshell dan deface akan otomatis di-generate oleh TemplateLoader saat vulnAttack.py pertama kali dijalankan.
· Untuk bypass WAF/Cloudflare, install cloudscraper: pip install cloudscraper
· Index.html di root akan otomatis di-copy ke templates/deface_apip.html sebagai template deface kustom.
· Modul bypass (bypass/) sudah terintegrasi penuh; tidak perlu konfigurasi tambahan.

---

⚠️ Disclaimer

Tools ini dibuat untuk tujuan edukasi dan pengujian keamanan sistem sendiri. Penulis tidak bertanggung jawab atas penyalahgunaan. Gunakan dengan bijak dan hanya di lingkungan yang Anda miliki atau memiliki izin untuk diuji.

---

📄 Lisensi

MIT License – silakan digunakan, dimodifikasi, dan didistribusikan dengan tetap mencantumkan nama penulis.

---

Selamat mencoba! 🔥