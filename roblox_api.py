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
    return None

def get_display_name(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    res = requests.get(url, headers=HEADERS)
    if res.ok:
        return res.json().get("displayName")
    return None

def set_rank_if_in_group(user_id):
    # Kolla om användaren är med i gruppen
    url_check = f"https://groups.roblox.com/v2/users/{user_id}/groups/roles"
    res_check = requests.get(url_check, headers=HEADERS)
    
    if not res_check.ok:
        print(f"[set_rank] Failed to check group membership for user {user_id}, status: {res_check.status_code}, response: {res_check.text}")
        return False

    groups = res_check.json().get("data", [])
    in_group = any(group["group"]["id"] == GROUP_ID for group in groups)

    if not in_group:
        print(f"[set_rank] User {user_id} is not in the group {GROUP_ID}.")
        return False

    # Användaren är i gruppen, försök ranka med CSRF-token hantering
    url_rank = f"https://groups.roblox.com/v1/groups/{GROUP_ID}/users/{user_id}"
    payload = {"roleId": RANK_2}

    # Första PATCH utan X-CSRF-TOKEN för att trigga token i svarshuvudena
    temp_headers = HEADERS.copy()
    if "X-CSRF-TOKEN" in temp_headers:
        del temp_headers["X-CSRF-TOKEN"]

    res_rank = requests.patch(url_rank, headers=temp_headers, json=payload)

    if res_rank.status_code == 403:
        # Hämta token från headers
        token = res_rank.headers.get("x-csrf-token")
        if not token:
            print("[set_rank] Failed to get X-CSRF-TOKEN from response headers.")
            return False

        # Skicka PATCH igen med korrekt token
        temp_headers["X-CSRF-TOKEN"] = token
        res_rank = requests.patch(url_rank, headers=temp_headers, json=payload)

    print(f"[set_rank] Rank response status: {res_rank.status_code}")
    print(f"[set_rank] Rank response content: {res_rank.text}")

    return res_rank.status_code == 200
