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
        if data.get("data"):
            return data["data"][0]["id"]
    print(f"[get_user_id] Failed to get ID for username: {username}, status: {res.status_code}, response: {res.text}")
    return None

def get_display_name(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    res = requests.get(url, headers=HEADERS)
    if res.ok:
        return res.json().get("displayName")
    print(f"[get_display_name] Failed to get display name for user_id: {user_id}, status: {res.status_code}, response: {res.text}")
    return None

def set_rank(user_id):
    # Kontrollera om användaren är i gruppen
    url_check = f"https://groups.roblox.com/v1/users/{user_id}/groups"
    res_check = requests.get(url_check, headers=HEADERS)
    if not res_check.ok:
        print(f"[set_rank] Failed to check group membership for user {user_id}, status: {res_check.status_code}, response: {res_check.text}")
        return False

    groups = res_check.json()
    is_member = any(group.get("id") == GROUP_ID for group in groups.get("data", []))

    if not is_member:
        print(f"[set_rank] User {user_id} is NOT in group {GROUP_ID}")
        return False

    # Användaren är i gruppen, försök sätta rank
    url_rank = f"https://groups.roblox.com/v1/groups/{GROUP_ID}/users/{user_id}"
    payload = {"roleId": RANK_2}
    res_rank = requests.patch(url_rank, headers=HEADERS, json=payload)
    print(f"[set_rank] Rank response status: {res_rank.status_code}")
    print(f"[set_rank] Rank response content: {res_rank.text}")

    return res_rank.status_code == 200
