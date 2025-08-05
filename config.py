import os

DISCORD_BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN")
ROBLOX_COOKIE = os.environ.get("ROBLOX_COOKIE")
GROUP_ID = int(os.environ.get("GROUP_ID"))
RANK_1 = int(os.environ.get("RANK_1", 1))   # Standard = 1
RANK_2 = int(os.environ.get("RANK_2", 2))   # Standard = 2
ALLOWED_ROLE_ID = int(os.environ.get("ALLOWED_ROLE_ID"))
