#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_file_upload():
    p = set()

    # ========== 1. PHP EXTENSIONS (50+) ==========
    php_ext = ["php", "php5", "phtml", "php4", "php3", "php2", "php1", "phps", "php7", "php8"]
    for ext in php_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")
        p.add(f"shell.{ext}.zip")
        p.add(f"shell.{ext}.tar")
        p.add(f"shell.{ext}.gz")
        p.add(f"shell.{ext}.bz2")
        p.add(f"shell.{ext}.7z")
        p.add(f"shell.{ext}.rar")

    # ========== 2. ASP/ASPX EXTENSIONS (30+) ==========
    asp_ext = ["asp", "aspx", "asa", "cer", "cdx", "ashx", "asmx", "axd", "asax", "ascx"]
    for ext in asp_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 3. JSP EXTENSIONS (20+) ==========
    jsp_ext = ["jsp", "jspx", "jhtml", "jspf", "jspa", "jsw", "jsv", "jspx"]
    for ext in jsp_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 4. PYTHON EXTENSIONS (20+) ==========
    py_ext = ["py", "pyc", "pyo", "pyd", "pyw", "pyz", "pyi"]
    for ext in py_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 5. RUBY EXTENSIONS (20+) ==========
    rb_ext = ["rb", "rbx", "ruby", "rbw"]
    for ext in rb_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 6. PERL EXTENSIONS (20+) ==========
    pl_ext = ["pl", "pm", "plx", "perl", "cgi"]
    for ext in pl_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 7. NODEJS EXTENSIONS (20+) ==========
    node_ext = ["js", "node", "mjs", "cjs"]
    for ext in node_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 8. GO EXTENSIONS (10+) ==========
    go_ext = ["go"]
    for ext in go_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 9. OTHER EXTENSIONS (20+) ==========
    other_ext = ["exe", "bat", "cmd", "sh", "ps1", "vbs", "wsf", "wsh", "hta"]
    for ext in other_ext:
        p.add(f"shell.{ext}")
        p.add(f"shell.{ext}.jpg")
        p.add(f"shell.gif.{ext}")
        p.add(f"shell.{ext}.png")
        p.add(f"shell.{ext}.txt")
        p.add(f"shell.{ext}.html")
        p.add(f"shell.{ext}.bak")
        p.add(f"shell.{ext}.old")
        p.add(f"shell.{ext}.tmp")

    # ========== 10. NO EXTENSION VARIATIONS (100+) ==========
    suffixes = ["", ".jpg", ".png", ".gif", ".txt", ".html", ".bak", ".old", ".tmp",
                ".backup", ".save", ".original", ".org", ".sav"]
    for suffix in suffixes:
        p.add(f"shell{suffix}")
        for i in range(2, 11):
            p.add(f"shell{suffix}{i}")
            p.add(f"shell{suffix}_{i}")

    # ========== 11. RANDOM (1000+) ==========
    all_ext = php_ext + asp_ext + jsp_ext + py_ext + rb_ext + pl_ext + node_ext + go_ext + other_ext
    while len(p) < 5000:
        ext = random.choice(all_ext)
        ext2 = random.choice(["jpg", "png", "gif", "txt", "html", "bak", "old", "tmp"])
        p.add(f"shell.{ext}.{ext2}")
        p.add(f"shell.{ext2}.{ext}")
        p.add(f"shell.{ext}.{ext2}2")
        p.add(f"shell.{ext}.{ext2}3")
        p.add(f"shell.{ext}.{ext2}4")
        p.add(f"shell.{ext}.{ext2}5")

    # ========== 12. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "file_upload.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] file_upload.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_file_upload()