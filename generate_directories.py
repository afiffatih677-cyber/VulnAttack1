#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_directories():
    p = set()

    # ========== 1. BASE DIRECTORIES (100+) ==========
    base_dirs = [
        "admin", "login", "dashboard", "panel", "cpanel", "wp-admin",
        "wp-content", "wp-includes", "uploads", "backup", "temp", "tmp",
        "test", "dev", "shell", "phpmyadmin", "mysql", "database",
        "config", "conf", "htdocs", "www", "public_html", "html",
        "site", "web", "app", "assets", "css", "js", "images", "img",
        "media", "files", "download", "downloads", "cache", "logs",
        "log", "error", "debug", "info", "data", "db", "sql", "dump",
        "export", "import", "docs", "doc", "documentation", "help",
        "support", "faq", "about", "contact", "blog", "news", "events",
        "products", "services", "shop", "store", "cart", "checkout",
        "payment", "order", "tracking", "profile", "account", "settings",
        "preferences", "security", "privacy", "terms", "conditions",
        "policy", "legal", "license", "api", "v1", "v2", "v3", "rest",
        "graphql", "gql", "swagger", "redoc", "adminer", "phpinfo",
        "info.php", "test.php", "index.php", "index.html", "default.php",
        "default.html", "home.php", "home.html", "main.php", "main.html",
        "page.php", "page.html", "view.php", "view.html", "detail.php",
        "detail.html", "item.php", "item.html", "product.php",
        "product.html", "category.php", "category.html", "user.php",
        "user.html", "profile.php", "profile.html", "setting.php",
        "setting.html", "config.php", "config.inc.php", "wp-config.php",
        ".env", ".htaccess", ".htpasswd", ".git", ".svn", ".cvs", ".idea",
        ".vscode", ".DS_Store", "Thumbs.db", "desktop.ini", "robots.txt",
        "sitemap.xml", "crossdomain.xml", "humans.txt", "security.txt",
        "README.md", "CHANGELOG.md", "CONTRIBUTING.md", "LICENSE",
        "COPYING", "INSTALL", "UPGRADE", "CHANGELOG", "AUTHORS", "CREDITS",
        "TODO", "NOTICE", "README", "CHANGES", "COPYRIGHT", "LICENSE.txt",
        "README.txt", "CHANGELOG.txt", "INSTALL.txt", "UPGRADE.txt",
        "NOTICE.txt"
    ]
    p.update(base_dirs)

    # ========== 2. ADMIN VARIATIONS (100+) ==========
    suffixes = ["", "_backup", "_old", "_temp", "_test", "_dev", "_bak", "_original", "_save"]
    numbers = ["", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    for suffix in suffixes:
        for num in numbers:
            p.add(f"admin{suffix}{num}")
            p.add(f"admin{suffix}_{num}")

    # ========== 3. BACKUP VARIATIONS (100+) ==========
    backup_prefix = ["", "db_", "sql_", "data_", "file_", "site_", "web_", "app_", "config_", "conf_"]
    backup_suffix = ["", "_db", "_sql", "_data", "_files", "_www", "_public", "_html", "_site", "_web", "_app", "_config", "_conf"]
    backup_years = ["2019", "2020", "2021", "2022", "2023", "2024"]
    for pref in backup_prefix:
        p.add(f"{pref}backup")
        p.add(f"{pref}backup_old")
        p.add(f"{pref}backup_new")
    for suf in backup_suffix:
        p.add(f"backup{suf}")
    for year in backup_years:
        p.add(f"backup_{year}")
        p.add(f"db_backup_{year}")
        p.add(f"sql_backup_{year}")

    # ========== 4. CONFIG VARIATIONS (100+) ==========
    config_prefix = ["", "config_", "conf_", "settings_"]
    config_suffix = ["", "_inc", "_default", "_local", "_dev", "_prod", "_test", "_stage"]
    config_files = ["database", "app", "services", "cache", "session", "mail", "queue",
                    "logging", "auth", "broadcasting", "cors", "hashing", "view",
                    "filesystems", "sanctum", "tinker", "trustedproxy"]
    for pref in config_prefix:
        p.add(f"{pref}config")
        p.add(f"{pref}conf")
        p.add(f"{pref}settings")
    for suf in config_suffix:
        p.add(f"config{suf}")
        p.add(f"conf{suf}")
        p.add(f"settings{suf}")
    for file in config_files:
        p.add(f"config/{file}.php")
        p.add(f"config/{file}.yml")
        p.add(f"config/{file}.yaml")
        p.add(f"config/{file}.json")

    # ========== 5. LOG VARIATIONS (100+) ==========
    log_prefix = ["", "log_", "logs_", "error_", "debug_", "info_", "access_"]
    log_suffix = ["", ".log", ".txt", ".1", ".2", ".3", ".4", ".5", ".gz", ".zip"]
    log_types = ["system", "web", "app", "db", "mysql", "postgres", "redis",
                 "apache", "nginx", "php", "python", "ruby", "java", "node",
                 "error", "debug", "info", "warning", "critical", "access",
                 "event", "security", "audit", "transaction", "request",
                 "response", "activity", "user", "admin", "auth", "payment",
                 "order", "product", "category", "comment", "post", "page",
                 "media", "upload", "download", "backup", "restore", "export",
                 "import", "cron", "schedule", "job", "task", "worker", "queue",
                 "session", "cookie", "cache"]
    for pref in log_prefix:
        for log_type in log_types[:10]:
            p.add(f"{pref}{log_type}")
            p.add(f"{pref}{log_type}.log")
            p.add(f"{pref}{log_type}.txt")
    for log_type in log_types:
        p.add(f"{log_type}.log")
        p.add(f"logs/{log_type}.log")
        p.add(f"log/{log_type}.log")

    # ========== 6. UPLOAD VARIATIONS (100+) ==========
    upload_prefix = ["", "upload_", "uploads_", "file_", "image_", "media_"]
    upload_suffix = ["", "_dir", "_folder", "_path", "_file", "_files", "_image", "_images",
                     "_media", "_assets", "_resources", "_tmp", "_temp", "_old", "_new",
                     "_data", "_db", "_backup", "_export", "_import", "_archive"]
    upload_ext = ["php", "php5", "phtml", "asp", "aspx", "jsp", "jspx", "py", "rb", "pl", "js", "go"]
    for pref in upload_prefix:
        p.add(f"{pref}upload")
        for suf in upload_suffix[:10]:
            p.add(f"{pref}upload{suf}")
    for ext in upload_ext:
        p.add(f"upload_{ext}")
        p.add(f"uploads_{ext}")
        p.add(f"upload/{ext}")
        p.add(f"uploads/{ext}")

    # ========== 7. SHELL VARIATIONS (100+) ==========
    shell_prefix = ["", "shell_", "webshell_", "cmd_", "backdoor_"]
    shell_suffix = ["", "_backdoor", "_upload", "_uploader", "_php", "_asp", "_aspx", "_jsp", "_py", "_rb", "_pl", "_js", "_go"]
    shell_types = ["shell", "webshell", "backdoor", "cmd", "shell.php", "webshell.php", "backdoor.php", "cmd.php"]
    for pref in shell_prefix:
        for suf in shell_suffix[:10]:
            p.add(f"{pref}shell{suf}")
    for shell_type in shell_types:
        p.add(shell_type)
        p.add(f"uploads/{shell_type}")
        p.add(f"tmp/{shell_type}")

    # ========== 8. DATABASE VARIATIONS (100+) ==========
    db_prefix = ["", "db_", "sql_", "database_", "data_"]
    db_suffix = ["", "_backup", "_dump", "_export", "_import", "_restore", "_mysql", "_postgres",
                 "_redis", "_elastic", "_sqlite", "_mongo", "_couch", "_neo4j", "_cassandra",
                 "_dynamo", "_firebase", "_realtime", "_firestore", "_supabase"]
    db_types = ["mysql", "postgres", "redis", "elastic", "sqlite", "mongo", "couch", "neo4j",
                "cassandra", "dynamo", "firebase", "supabase", "document", "graph", "keyvalue",
                "column", "time", "array", "json", "xml", "yaml", "csv", "excel", "parquet"]
    for pref in db_prefix:
        for suf in db_suffix[:10]:
            p.add(f"{pref}db{suf}")
            p.add(f"{pref}sql{suf}")
            p.add(f"{pref}data{suf}")
    for db_type in db_types:
        p.add(f"db_{db_type}")
        p.add(f"sql_{db_type}")
        p.add(f"database_{db_type}")
        p.add(f"data_{db_type}")

    # ========== 9. RANDOM (2000+) ==========
    all_dirs = list(base_dirs) + ["admin", "backup", "config", "log", "upload", "shell", "db", "sql", "data"]
    suffixes = ["", "_old", "_new", "_backup", "_tmp", "_temp", "_test", "_dev", "_prod", "_stage", "_local"]
    numbers = ["", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    while len(p) < 5000:
        dir_name = random.choice(all_dirs)
        suffix = random.choice(suffixes)
        num = random.choice(numbers)
        p.add(f"{dir_name}{suffix}{num}")
        p.add(f"{dir_name}{suffix}_{num}")
        p.add(f"{dir_name}_{suffix}{num}")
        p.add(f"{dir_name}_{suffix}_{num}")

    # ========== 10. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "directories.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] directories.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_directories()