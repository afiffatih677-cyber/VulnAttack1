#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_open_redirect():
    p = set()

    # ========== 1. KNOWN DOMAINS (50+) ==========
    domains = [
        "google.com", "facebook.com", "twitter.com", "youtube.com",
        "instagram.com", "linkedin.com", "github.com", "stackoverflow.com",
        "reddit.com", "amazon.com", "microsoft.com", "apple.com",
        "netflix.com", "spotify.com", "whatsapp.com", "telegram.org",
        "discord.com", "slack.com", "zoom.us", "dropbox.com",
        "onedrive.live.com", "drive.google.com", "docs.google.com",
        "mail.google.com", "calendar.google.com", "translate.google.com",
        "maps.google.com", "x.com", "tiktok.com", "snapchat.com",
        "pinterest.com", "tumblr.com", "flickr.com", "vimeo.com",
        "twitch.tv", "steamcommunity.com", "epicgames.com",
        "playstation.com", "xbox.com", "nintendo.com", "ubuntu.com",
        "debian.org", "archlinux.org", "fedora.org", "centos.org",
        "redhat.com", "oracle.com", "ibm.com", "hp.com", "dell.com"
    ]
    for domain in domains:
        p.add(f"//{domain}")
        p.add(f"https://{domain}")
        p.add(f"http://{domain}")

    # ========== 2. MALICIOUS DOMAINS (20+) ==========
    malicious = [
        "evil.com", "attacker.com", "malicious.com", "phishing.com",
        "hacker.com", "cracker.com", "exploit.com", "payload.com",
        "shell.com", "backdoor.com", "malware.com", "virus.com",
        "trojan.com", "ransomware.com", "spyware.com", "adware.com",
        "worm.com", "keylogger.com", "rootkit.com", "bootkit.com",
        "exploit-kit.com", "cve.com", "0day.com", "pwn.com",
        "owned.com", "hacked.com", "breached.com", "leaked.com"
    ]
    for mal in malicious:
        p.add(f"http://{mal}")
        p.add(f"https://{mal}")
        p.add(f"//{mal}")

    # ========== 3. RAW/CDN URLS (50+) ==========
    raw_cdn = [
        "pastebin.com", "hastebin.com", "gist.github.com",
        "codeshare.io", "collabedit.com", "raw.githubusercontent.com",
        "cdn.jsdelivr.net", "unpkg.com", "cdnjs.cloudflare.com",
        "fonts.googleapis.com", "ajax.googleapis.com",
        "code.jquery.com"
    ]
    for url in raw_cdn:
        p.add(f"http://{url}")
        p.add(f"https://{url}")
        p.add(f"//{url}")

    # ========== 4. LIBRARY/FRAMEWORK URLS (50+) ==========
    libs = [
        "jquery", "bootstrap", "font-awesome", "popper.js",
        "angular.js", "react", "react-dom", "vue", "axios",
        "lodash.js", "moment.js"
    ]
    versions = ["3.6.0", "4.7.0", "5.15.4", "6.5.1", "1.16.1", "2.0.2", "4.0.0", "3.4.0"]
    for lib in libs:
        for ver in versions[:3]:
            p.add(f"http://cdnjs.cloudflare.com/ajax/libs/{lib}/{ver}/")
            p.add(f"http://cdn.jsdelivr.net/npm/{lib}@{ver}/")
            p.add(f"http://unpkg.com/{lib}@{ver}/")
            p.add(f"http://raw.githubusercontent.com/{lib}/{lib}/{ver}/")

    # ========== 5. RANDOM (4000+) ==========
    while len(p) < 5000:
        domain = random.choice(domains + malicious)
        p.add(f"//{domain}")
        p.add(f"https://{domain}")
        p.add(f"http://{domain}")
        p.add(f"//{domain}/path")
        p.add(f"https://{domain}/path")
        p.add(f"http://{domain}/path")
        p.add(f"//{domain}?query=value")
        p.add(f"https://{domain}?query=value")
        p.add(f"http://{domain}?query=value")

    # ========== 6. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "open_redirect.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] open_redirect.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_open_redirect()