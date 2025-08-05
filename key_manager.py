import random
import string
import json
import os

KEYS_FILE = "keys.json"

def generate_key():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=16))

def load_keys():
    if not os.path.exists(KEYS_FILE):
        with open(KEYS_FILE, 'w') as f:
            json.dump({}, f)
    with open(KEYS_FILE, 'r') as f:
        return json.load(f)

def save_keys(keys):
    with open(KEYS_FILE, 'w') as f:
        json.dump(keys, f, indent=4)

def create_key(roblox_username):
    keys = load_keys()
    for key, data in keys.items():
        if data["roblox_username"].lower() == roblox_username.lower() and not data["used"]:
            return key  # Returnera gammal om finns
    new_key = generate_key()
    keys[new_key] = {
        "roblox_username": roblox_username,
        "used": False
    }
    save_keys(keys)
    return new_key

def validate_key(key, roblox_username):
    keys = load_keys()
    if key in keys and not keys[key]["used"]:
        if keys[key]["roblox_username"].lower() == roblox_username.lower():
            return True
    return False

def mark_key_used(key):
    keys = load_keys()
    if key in keys:
        keys[key]["used"] = True
        save_keys(keys)
