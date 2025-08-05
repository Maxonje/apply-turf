import requests
from config import ROBLOX_COOKIE, GROUP_ID, RANK_2

HEADERS = {
    "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}",
    "User-Agent": "RobloxDiscordBot/1.0"
}

def get_user_id(username):
    res = requests.get(f"https://users.roblox.com/v1/usernames/users", json={"usernames": [username]})
    if res.ok and res.json()["data"]:
        return res.json()["data"][0]["id"]
    return None

def get_display_name(user_id):
    res = requests.get(f"https://users.roblox.com/v1/users/{user_id}")
    if res.ok:
        return res.json()["displayName"]
    return None

def set_rank(user_id):
    url = f"https://groups.roblox.com/v1/groups/{GROUP_ID}/users/{user_id}"
    payload = {"roleId": RANK_2}
    res = requests.patch(url, headers=HEADERS, json=payload)
    return res.status_code == 200
