
# VulnAttack v3.0 – Full Exploit Chain Engine
**Author**   : Apipboys  
**Version**  : 3.0 FINAL (STABLE)  
**Support**  : Termux | Kali Linux | Windows | macOS | Docker  
**Payload**  : 140.000+ (14 kategori × 10.000+)  
**Bypass**   : Cloudflare | WAF | Header Rotation | Rate Limit | CAPTCHA (placeholder)  
**Status**   : READY TO USE



## 📌 Deskripsi

VulnAttack adalah tools all‑in‑one untuk penetration testing yang mencakup:

- 14 jenis scanning kerentanan (SQLi, XSS, LFI, RCE, SSRF, XXE, NoSQLi, SSTI, Command Injection, LDAP, Open Redirect, CSRF, File Upload, Directory Traversal).
- Google Dorking multi‑source (Google, Bing, DuckDuckGo) untuk menemukan target.
- Deep Analysis otomatis: HTTP header, cookie, form, AJAX, WebSocket, API endpoint, hidden input, komentar tersembunyi, dan file JavaScript.
- Exploit & Deploy Webshell (20+ template, termasuk 5 super persistent).
- Deface Website (10 template HTML kustom).
- Generate POC & Report (HTML + JSON).
- Multi‑thread & Proxy support.
- Bypass WAF/Cloudflare terintegrasi (cloudscraper, retry, header rotation).



## 🔥 Fitur Lengkap

### 1. 14 Jenis Serangan

| No | Jenis | File Payload |
|----|-------|--------------|
| 1 | SQL Injection | `sqli.txt` |
| 2 | XSS (Reflected + Stored) | `xss.txt` |
| 3 | LFI (Local File Inclusion) | `lfi.txt` |
| 4 | RCE (Remote Code Execution) | `rce.txt` |
| 5 | SSRF (Server‑Side Request Forgery) | `ssrf.txt` |
| 6 | XXE (XML External Entity) | `xxe.txt` |
| 7 | NoSQL Injection | `nosqli.txt` |
| 8 | SSTI (Server‑Side Template Injection) | `ssti.txt` |
| 9 | Command Injection | `cmd_injection.txt` |
| 10 | LDAP Injection | `ldap.txt` |
| 11 | Open Redirect | `open_redirect.txt` |
| 12 | CSRF (Cross‑Site Request Forgery) | `csrf.txt` |
| 13 | File Upload | `file_upload.txt` |
| 14 | Directory Traversal | `directories.txt` |

**Total payload: 140.000+** (masing‑masing kategori 10.000+)



### 2. Bypass & Evasion

- **Cloudflare** – Menggunakan `cloudscraper` dengan flag `--bypass-waf`.
- **WAF Detection & Retry** – Deteksi otomatis pola WAF dan retry dengan delay eksponensial.
- **User‑Agent Rotation** – Rotasi dari `config/user_agents.txt` (50+ UA).
- **Header Spoofing** – Header standar browser (Accept, Accept‑Language, dll).
- **Rate Limiting** – Delay acak (dapat diatur di `bypass_settings.json`).
- **Proxy Support** – Dari `config/proxy.txt` dengan flag `--proxy`.
- **CAPTCHA Solver (placeholder)** – Dapat diintegrasikan dengan 2captcha/anticaptcha.



### 3. Deep Analysis & Audit

- Crawling hingga kedalaman 5.
- Deteksi semua form (termasuk hidden form).
- Ekstraksi parameter dari URL, form, dan JavaScript.
- Analisis file JS (endpoint API, token, komentar).
- Pemindaian komentar HTML (mencari `todo`, `fix`, `secret`).
- Deteksi hidden input (`<input type="hidden">`).
- Analisis header & cookie (HttpOnly, Secure, SameSite).
- Deteksi direktori tersembunyi (5000+ list).
- Pemindaian port internal (jika ada SSRF).
- Pembuatan peta situs (sitemap) dari semua link.



### 4. Exploit & Deploy

- **Deploy Webshell** – Otomatis unggah webshell (20 template) melalui RCE/LFI/SQLi.
- **Deface Website** – Ganti `index.html` dengan template deface (10 pilihan).
- **Generate POC** – Laporan HTML + JSON.



### 5. Dorking Engine

- Multi‑source: **Google, Bing, DuckDuckGo**.
- Hasil dorking otomatis discan untuk kerentanan.



### 6. Multi‑Thread & Batch Scan

- Scan banyak target dari file (`--list`) dengan jumlah thread adjustable (`--threads`).



## 📁 Struktur Folder

```

vulnAttack1/
├── .gitignore
├── .gitkeep
├── vulnAttack.py                 # MAIN ENGINE
├── generate_payloads.py          # GENERATOR UTAMA
├── generate_.py (14 file)       # Generator per kategori
├── requirements.txt
├── README.md
├── index.html
├── payloads/                     (auto‑generated)
│   └── 14 file .txt
├── templates/
│   ├── deface_.html (10)
│   └── webshell_*.php / .asp / .jsp / .py (20)
├── bypass/
│   ├── init.py
│   ├── cloudflare.py
│   ├── waf.py
│   ├── headers.py
│   ├── utils.py
│   └── captcha.py
├── config/
│   ├── proxy.txt
│   ├── user_agents.txt
│   └── bypass_settings.json
├── results/                      (auto‑generated)
└── logs/                         (auto‑generated)

```

---

## 🛠️ Instalasi & Penggunaan (Step‑by‑Step)

### 1. Clone Repository
```bash
git clone https://github.com/afiffatih677-cyber/VulnAttack1.git
cd VulnAttack1
```

2. Install Dependencies

```bash
pip install -r requirements.txt
# (Opsional) pip install cloudscraper
```

3. Generate Payload (Hanya Sekali)

```bash
python generate_payloads.py
```

Proses ini akan membuat 14 file .txt di folder payloads/ dengan total 140.000+ payload.

4. Jalankan Tools

```bash
python vulnAttack.py
```

Setelah dijalankan, akan muncul BANNER dan MAIN MENU:

```
  _   _         _          ___   _    _                 _    
 | | | |       | |        / _ \ | |  | |               | |   
 | | | | _   _ | | _ __  / /_\ \| |_ | |_   __ _   ___ | | __
 | | | || | | || || '_ \ |  _  || __|| __| / _` | / __|| |/ /
 \ \_/ /| |_| || || | | || | | || |_ | |_ | (_| || (__ |   < 
  \___/  \__,_||_||_| |_|\_| |_/ \__| \__| \__,_| \___||_|\_\
                                                             
                                                             

[+] Author  : Apipboys
[+] Version : 3.0 FINAL (STABLE)
[+] Payload : 140.000+ (14 kategori x 10000+)
[+] Support : Termux | Kali | Windows | macOS | Docker
[+] Bypass  : Cloudflare | WAF | Header Rotation | Rate Limit
[+] Status  : READY TO USE

[+] INSTALLATION COMPLETE!
[+] You can now run:
    python vulnAttack.py http://target.com
    python vulnAttack.py --dork "inurl:index.php?id="
    python vulnAttack.py --list targets.txt --threads 20
    python vulnAttack.py --bypass-waf --dork ...
    python vulnAttack.py --proxy --list targets.txt

[+] MAIN MENU
    [1] Scan Target
    [2] Dorking
    [3] Scan List Target
    [4] Help
    [5] Exit
```

---

🖥️ Cara Penggunaan (Detail)

A. Scan Target Tunggal

1. Via Menu Interaktif

· Jalankan python vulnAttack.py
· Pilih [1] Scan Target
· Masukkan URL target (contoh: http://target.com)
· Pilih opsi proxy, bypass WAF, dan deep scan sesuai kebutuhan

2. Via CLI (Langsung)

```bash
python vulnAttack.py http://target.com
```

3. Dengan Bypass WAF/Cloudflare

```bash
python vulnAttack.py http://target.com --bypass-waf
```

4. Dengan Proxy

```bash
python vulnAttack.py http://target.com --proxy
```

5. Dengan Deep Scan (Audit Mendalam)

```bash
python vulnAttack.py http://target.com --deep-scan
```

6. Kombinasi

```bash
python vulnAttack.py http://target.com --bypass-waf --proxy --deep-scan
```

---

B. Dorking (Mencari Target)

1. Via Menu Interaktif

· Jalankan python vulnAttack.py
· Pilih [2] Dorking
· Masukkan dork (contoh: inurl:index.php?id=)

2. Via CLI

```bash
python vulnAttack.py --dork "inurl:index.php?id="
```

3. Dengan Bypass & Proxy

```bash
python vulnAttack.py --dork "inurl:index.php?id=" --bypass-waf --proxy
```

---

C. Scan Banyak Target (Batch)

1. Via Menu Interaktif

· Jalankan python vulnAttack.py
· Pilih [3] Scan List Target
· Masukkan path file target (contoh: targets.txt)
· Tentukan jumlah thread (default 10)

2. Via CLI

```bash
python vulnAttack.py --list targets.txt --threads 20
```

Format File targets.txt (satu URL per baris):

```
http://target1.com
http://target2.com
https://target3.com
```

---

D. Menu Interaktif (Setelah Scan Selesai)

Setelah scanning selesai, akan muncul menu interaktif:

```
[+] INTERACTIVE MENU
    [1] Deploy Webshell
    [2] Deface Website
    [3] Generate POC
    [4] Show Deep Analysis
    [5] Show Minor Vulnerabilities
    [6] Deep Audit (Analisis Mendalam)
    [7] Show Hidden Findings
    [8] Scan Another Target
    [9] Exit
```

Penjelasan Opsi:

Opsi Fungsi
[1] Deploy Webshell – Upload webshell ke target (20 template)
[2] Deface Website – Ganti index.html dengan template deface
[3] Generate POC – Buat laporan HTML + JSON di results/
[4] Show Deep Analysis – Lihat analisis header, cookie, form, API, dll
[5] Show Minor Vulnerabilities – Lihat celah kecil (X-Frame-Options, CSP, HSTS)
[6] Deep Audit – Pemindaian ultra‑mendalam (hidden input, hidden dir, JS endpoint)
[7] Show Hidden Findings – Lihat hasil temuan tersembunyi dari Deep Audit
[8] Scan Another Target – Kembali ke menu utama
[9] Exit – Keluar dari program

---

E. Deploy Webshell (Step‑by‑Step)

1. Setelah scan, pilih [1] Deploy Webshell
2. Pilih kerentanan yang akan digunakan (RCE, LFI, atau SQLi)
3. Pilih template webshell dari daftar (20 template tersedia)

Contoh template webshell super persistent:

· webshell_extreme_persistent.php – auto‑replikasi, cron job, chattr +i
· webshell_super_hidden.php – tersembunyi dengan nama acak
· webshell_immunity.php – kebal hapus (saling backup)
· webshell_cron_agent.php – reverse shell via cron
· webshell_stealth_encoder.php – perintah terenkripsi XOR + base64

---

F. Deface Website (Step‑by‑Step)

1. Setelah scan, pilih [2] Deface Website
2. Pilih kerentanan (RCE atau Command Injection)
3. Pilih template deface dari daftar (10 template tersedia)

Contoh template deface:

· deface_basic.html – tampilan sederhana
· deface_advanced.html – tampilan profesional
· deface_cyber.html – tema cyber
· deface_apip.html – template kustom dari index.html
· dan lainnya

---

G. Generate POC (Step‑by‑Step)

1. Setelah scan, pilih [3] Generate POC
2. Laporan akan tersimpan di folder results/ dengan format:
   · poc_{domain}.html
   · report_{domain}.json

Isi laporan:

· Target URL
· Scan Date
· Total Major Vulnerabilities (dengan payload & evidence)
· Minor Vulnerabilities (dengan severity)
· Hidden Findings (JSON)
· Webshell URL (jika berhasil deploy)
· Deface URL (jika berhasil deface)
· Deep Analysis (header, cookie, form, API, dll)

---

🖥️ Perintah Terminal (CLI) Lengkap

Perintah Fungsi
python vulnAttack.py Menu utama (interaktif)
python vulnAttack.py http://target.com Scan langsung target
python vulnAttack.py --dork "dork" Dorking multi‑source
python vulnAttack.py --list targets.txt --threads 20 Scan massal
python vulnAttack.py --bypass-waf http://target.com Scan + bypass WAF
python vulnAttack.py --proxy http://target.com Scan + proxy
python vulnAttack.py --deep-scan http://target.com Scan + deep audit otomatis
python vulnAttack.py --audit http://target.com Audit ekstrem (sama dengan --deep-scan)
python vulnAttack.py --delay 3 Set delay antar request (detik)
python vulnAttack.py --output /path/to/dir Output directory kustom
python vulnAttack.py --menu Paksa masuk ke menu utama
python vulnAttack.py --help Tampilkan bantuan

---

⚙️ Konfigurasi

config/proxy.txt

Daftar proxy (satu per baris). Format:

```
http://user:pass@ip:port
http://127.0.0.1:8080
socks5://127.0.0.1:9050
```

config/user_agents.txt

Daftar User‑Agent (satu per baris) untuk rotasi. Contoh:

```
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36
Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/121.0
```

config/bypass_settings.json

Konfigurasi bypass WAF/Cloudflare. Bisa diedit sesuai kebutuhan.

```json
{
  "bypass": {
    "enabled": true,
    "cloudscraper": {
      "use_cloudscraper": true,
      "browser": "chrome",
      "platform": "windows",
      "captcha_solver": "none",
      "timeout": 15
    },
    "delay": {
      "min": 1,
      "max": 3,
      "randomize": true
    },
    "waf": {
      "detection": true,
      "retry_on_block": true,
      "max_retries": 3,
      "retry_delay": 5
    }
  }
}
```

---

📊 Contoh Output Terminal

Saat menjalankan python vulnAttack.py http://target.com:

```
╔════════════════════════════════════════════════════════════════╗
║  🚀 VulnAttack v3.0 - Full Exploit Chain Engine              ║
║  Author: Apipboys                                            ║
║  Payload: 140.000+  |  Bypass: Cloudflare, WAF, Rate Limit   ║
╚════════════════════════════════════════════════════════════════╝

[+] Target: http://target.com
[+] Domain: target.com

[~] Crawling: http://target.com (depth 0)
[~] Crawling: http://target.com/login (depth 1)
[~] Crawling: http://target.com/admin (depth 1)
[+] Crawling complete. Total pages: 12

[+] Testing SQL Injection...
  [✓] SQLi found: http://target.com?id=1' OR '1'='1
[+] Testing XSS...
  [✓] XSS (Reflected) found: http://target.com?q=<script>alert(1)</script>
[+] Testing LFI...
  [✗] No LFI found
[+] Testing RCE...
  [✓] RCE found: http://target.com?cmd=id
[+] Testing SSRF...
  [✗] No SSRF found
[+] Testing XXE...
  [✗] No XXE found
[+] Testing NoSQLi...
  [✗] No NoSQLi found
[+] Testing SSTI...
  [✗] No SSTI found
[+] Testing Command Injection...
  [✗] No Command Injection found
[+] Testing LDAP...
  [✗] No LDAP found
[+] Testing Open Redirect...
  [✗] No Open Redirect found
[+] Testing CSRF...
  [✓] CSRF found: http://target.com (no token)
[+] Testing File Upload...
  [✗] No File Upload found
[+] Testing Directory Traversal...
  [✗] No Directory Traversal found

[+] Found 4 major vulnerabilities.
  - SQLi @ http://target.com?id=1' OR '1'='1
  - XSS (Reflected) @ http://target.com?q=<script>alert(1)</script>
  - RCE @ http://target.com?cmd=id
  - CSRF @ http://target.com

[+] Found 2 minor vulnerabilities.
  - Missing X-Frame-Options
  - Missing CSP

[+] Deep Analysis:
  - Forms: 5
  - AJAX endpoints: 3
  - API endpoints: 2
  - Hidden inputs: 4
  - Comments with clues: 2
  - JavaScript files: 3

[+] Interactive Menu:
  [1] Deploy Webshell
  [2] Deface Website
  [3] Generate POC
  [4] Show Deep Analysis
  [5] Show Minor Vulnerabilities
  [6] Deep Audit (Analisis Mendalam)
  [7] Show Hidden Findings
  [8] Scan Another Target
  [9] Exit
```


🧪 Troubleshooting

Masalah Solusi
ModuleNotFoundError: No module named 'requests' pip install requests
ModuleNotFoundError: No module named 'cloudscraper' pip install cloudscraper (opsional)
No payloads found! Run generate_payloads.py first! python generate_payloads.py
Permission denied di Termux chmod +x vulnAttack.py
Tools lambat / banyak timeout Kurangi delay: python vulnAttack.py http://target.com --delay 1
Hasil scan tidak akurat Gunakan --deep-scan untuk analisis lebih mendalam


📝 Catatan Penting

· Generate payload hanya perlu dijalankan sekali (saat pertama kali).
· Cloudscraper bersifat opsional, install jika ingin bypass Cloudflare.
· Template webshell & deface akan otomatis dibuat saat pertama kali tools dijalankan.
· Hasil scan tersimpan di folder results/ (POC HTML + JSON).
· Log aktivitas tersimpan di logs/vulnAttack.log.


⚠️ Disclaimer

Tools ini dibuat untuk tujuan edukasi dan pengujian keamanan sistem sendiri (authorized penetration testing).
Penulis tidak bertanggung jawab atas penyalahgunaan tools ini.
Gunakan dengan bijak dan hanya di lingkungan yang Anda miliki atau memiliki izin untuk diuji.


📄 Lisensi

MIT License – silakan digunakan, dimodifikasi, dan didistribusikan dengan tetap mencantumkan nama penulis.