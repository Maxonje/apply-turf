import requests
from config import ROBLOX_COOKIE, GROUP_ID, RANK_2

HEADERS = {
    "Cookie": f".ROBLOSECURITY={ROBLOX_COOKIE}",
    "User-Agent": "RobloxDiscordBot/1.0",
    "Content-Type": "application/json"
}

def get_user_id(username):
    url = "https://users.roblox.com/v1/usernames/users"
    payload = {"usernames": [username]}
    res = requests.post(url, json=payload, headers=HEADERS)
    if res.ok:
        data = res.json()
        if data["data"]:
            return data["data"][0]["id"]
    return None

def get_display_name(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    res = requests.get(url, headers=HEADERS)
    if res.ok:
        return res.json()["displayName"]
    return None

def set_rank(user_id):
    url = f"https://groups.roblox.com/v1/groups/{GROUP_ID}/users/{user_id}"
    payload = {"roleId": RANK_2}
    res = requests.patch(url, headers=HEADERS, json=payload)
    return res.status_code == 200
