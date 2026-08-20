#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_csrf():
    p = set()

    # ========== 1. BASIC CSRF DETECTION (50+) ==========
    csrf_indicators = [
        "No CSRF token",
        "Missing CSRF protection",
        "No CSRF protection",
        "CSRF token missing",
        "Missing anti-CSRF token",
        "No anti-CSRF token",
        "Anti-CSRF token missing",
        "No CSRF defense",
        "CSRF disabled",
        "CSRF protection disabled",
        "CSRF token not found",
        "CSRF token validation disabled",
        "No CSRF token validation",
        "CSRF token missing in request",
        "CSRF token missing in form",
        "CSRF token missing in header",
        "CSRF token missing in cookie",
        "CSRF token missing in session",
        "CSRF token missing in URL",
        "CSRF token missing in POST",
        "CSRF token missing in GET",
        "CSRF token missing in AJAX",
        "CSRF token missing in fetch",
        "CSRF token missing in XMLHttpRequest",
        "CSRF token missing in request body",
        "CSRF token missing in query string",
        "CSRF token missing in form data",
        "CSRF token missing in multipart form",
        "CSRF token missing in application/json",
        "CSRF token missing in application/x-www-form-urlencoded",
        "CSRF token missing in text/plain",
        "CSRF token missing in multipart/form-data",
        "CSRF token missing in application/xml",
        "CSRF token missing in text/xml",
        "CSRF token missing in application/soap+xml",
        "CSRF token missing in application/rss+xml",
        "CSRF token missing in application/atom+xml",
        "CSRF token missing in application/javascript",
        "CSRF token missing in application/ecmascript",
        "CSRF token missing in application/octet-stream"
    ]
    p.update(csrf_indicators)

    # ========== 2. CONTENT TYPE VARIATIONS (100+) ==========
    content_types = [
        "application/json", "application/x-www-form-urlencoded",
        "text/plain", "multipart/form-data", "application/xml",
        "text/xml", "application/soap+xml", "application/rss+xml",
        "application/atom+xml", "application/javascript",
        "application/ecmascript", "application/octet-stream",
        "application/pdf", "application/zip", "application/gzip",
        "application/x-tar", "application/x-gzip", "application/x-bzip2",
        "application/x-7z-compressed", "application/x-rar-compressed",
        "application/vnd.ms-excel",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        "application/msword",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
        "application/vnd.ms-powerpoint",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation",
        "image/jpeg", "image/png", "image/gif", "image/svg+xml",
        "image/webp", "image/bmp", "image/tiff", "audio/mpeg",
        "audio/ogg", "audio/wav", "audio/webm", "video/mp4",
        "video/webm", "video/ogg", "video/quicktime",
        "video/x-msvideo", "video/x-matroska", "font/ttf",
        "font/otf", "font/woff", "font/woff2", "text/html",
        "text/css", "text/javascript", "text/plain", "text/xml",
        "text/csv", "text/markdown", "text/calendar", "text/vcard",
        "text/rtf"
    ]
    for ct in content_types:
        p.add(f"CSRF token missing in {ct}")

    # ========== 3. PROG LANG VARIATIONS (50+) ==========
    prog_langs = [
        "python", "perl", "ruby", "php", "java", "c", "c++", "go",
        "rust", "swift", "kotlin", "scala", "clojure", "haskell",
        "erlang", "elixir", "lua", "r", "matlab", "julia", "dart",
        "typescript", "jsx", "tsx", "vue", "angular", "react",
        "svelte", "solidity", "asm", "verilog", "vhdl", "systemverilog",
        "mips", "arm", "x86", "riscv", "llvm", "wasm"
    ]
    for lang in prog_langs:
        p.add(f"CSRF token missing in text/x-{lang}")

    # ========== 4. CONFIG FILE VARIATIONS (50+) ==========
    config_files = [
        "json", "yaml", "toml", "ini", "env", "dockerfile", "nginx",
        "apache", "htaccess", "gitignore", "gitattributes", "gitmodules",
        "gitconfig", "ssh-config", "known-hosts", "authorized-keys",
        "id-rsa", "id-dsa", "id-ecdsa", "id-ed25519", "cert", "key",
        "crl", "pem", "der", "pkcs7", "pkcs8", "pkcs12", "spki",
        "ocsp", "tsa", "tsp", "jws", "jwe", "jwk", "jwks", "jwt"
    ]
    for cfg in config_files:
        p.add(f"CSRF token missing in text/x-{cfg}")

    # ========== 5. AUTH VARIATIONS (30+) ==========
    auth_types = [
        "oauth", "oauth2", "openid", "saml", "saml2", "ldap",
        "kerberos", "ntlm", "basic-auth", "bearer", "apikey",
        "api-token", "access-token", "refresh-token", "id-token",
        "session-token", "csrf-token", "xsrf-token", "xss-token"
    ]
    for auth in auth_types:
        p.add(f"CSRF token missing in text/x-{auth}")

    # ========== 6. VULN TYPES VARIATIONS (30+) ==========
    vuln_types = [
        "sql-injection", "command-injection", "lfi", "rfi", "ssrf",
        "xxe", "ssti", "ldap-injection", "nosql-injection",
        "open-redirect", "file-upload", "directory-traversal"
    ]
    for vuln in vuln_types:
        p.add(f"CSRF token missing in text/x-{vuln}")

    # ========== 7. RANDOM (4000+) ==========
    templates = [
        "No CSRF token",
        "CSRF token missing",
        "Missing anti-CSRF token",
        "CSRF token not found",
        "No CSRF protection",
        "CSRF protection disabled",
        "CSRF token validation disabled",
        "No CSRF token validation",
        "CSRF token missing in {field}",
        "CSRF token missing in {context}",
        "Anti-CSRF token missing in {field}",
        "Anti-CSRF token missing in {context}"
    ]
    fields = ["request", "form", "header", "cookie", "session", "URL", "POST", "GET", "AJAX", "fetch", "XMLHttpRequest"]
    contexts = ["request body", "query string", "form data", "multipart form", "application/json", "application/x-www-form-urlencoded", "text/plain", "multipart/form-data", "application/xml", "text/xml"]

    while len(p) < 5000:
        template = random.choice(templates)
        if "{field}" in template:
            field = random.choice(fields)
            p.add(template.format(field=field))
        elif "{context}" in template:
            context = random.choice(contexts)
            p.add(template.format(context=context))
        else:
            p.add(template)
        p.add(f"CSRF token missing in {random.choice(contexts)}")
        p.add(f"Missing CSRF token in {random.choice(fields)}")

    # ========== 8. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "csrf.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] csrf.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_csrf()