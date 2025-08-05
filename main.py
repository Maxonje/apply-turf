import discord
from discord import app_commands
from discord.ext import commands
from config import DISCORD_BOT_TOKEN, ALLOWED_ROLE_ID
from key_manager import create_key, validate_key, mark_key_used
from roblox_api import get_user_id, get_display_name, set_rank_if_in_group

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f"Logged in as {bot.user}!")

def embed_message(title: str, description: str, color=discord.Color.blurple()):
    return discord.Embed(title=title, description=description, color=color)

@bot.tree.command(name="apply", description="Apply for access with your Roblox username")
@app_commands.describe(username="Your Roblox username")
async def apply(interaction: discord.Interaction, username: str):
    if ALLOWED_ROLE_ID not in [role.id for role in interaction.user.roles]:
        embed = embed_message("Access Denied", "You don't have permission to use this command.", discord.Color.red())
        await interaction.response.send_message(embed=embed, ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)

    user_id = get_user_id(username)
    if not user_id:
        embed = embed_message("Error", "Roblox user not found.", discord.Color.red())
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    display_name = get_display_name(user_id)
    if not display_name or "FL13" not in display_name.upper().replace("_", "").replace(" ", ""):
        embed = embed_message("Display Name Check Failed", "Your Roblox display name must include `FL13`.", discord.Color.orange())
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    key = create_key(username)
    try:
        dm_embed = embed_message("Your Access Key", f"✅ Your unique key is:\n`{key}`\n\nUse it with:\n`/freeaccess {key} {username}`")
        await interaction.user.send(embed=dm_embed)

        success_embed = embed_message("Key Sent", "📬 Your key has been sent via DM.")
        await interaction.followup.send(embed=success_embed, ephemeral=True)
    except:
        error_embed = embed_message("DM Failed", "❌ Unable to send DM. Please enable DMs from server members.", discord.Color.red())
        await interaction.followup.send(embed=error_embed, ephemeral=True)

@bot.tree.command(name="freeaccess", description="Use your key to unlock access")
@app_commands.describe(key="The key you received", username="Your Roblox username")
async def freeaccess(interaction: discord.Interaction, key: str, username: str):
    await interaction.response.defer(ephemeral=True)

    if not validate_key(key, username):
        embed = embed_message("Invalid Key", "❌ The key is invalid or doesn't match the username.", discord.Color.red())
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    user_id = get_user_id(username)
    if not user_id:
        embed = embed_message("Error", "Could not find the Roblox user.", discord.Color.red())
        await interaction.followup.send(embed=embed, ephemeral=True)
        return

    success = set_rank_if_in_group(user_id)
    if success:
        mark_key_used(key)
        embed = embed_message("Access Granted", "✅ You have been successfully ranked in the Roblox group!")
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        embed = embed_message("Ranking Failed", "❌ Could not rank the user. Make sure they are already in the group.", discord.Color.red())
        await interaction.followup.send(embed=embed, ephemeral=True)

bot.run(DISCORD_BOT_TOKEN)
