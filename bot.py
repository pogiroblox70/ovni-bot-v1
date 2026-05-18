import discord
from discord.ext import commands
import json
import os

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

CONFIG_FILE = "config.json"


# -------------------------
# 💾 CONFIG SYSTEM
# -------------------------
def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {}

def save_config(data):
    with open(CONFIG_FILE, "w") as f:
        json.dump(data, f, indent=4)

config = load_config()


# -------------------------
# 🚀 BOT READY
# -------------------------
@bot.event
async def on_ready():
    print(f"✅ OVNI BOT connecté : {bot.user}")


# -------------------------
# 👋 WELCOME SYSTEM
# -------------------------
@bot.event
async def on_member_join(member):
    guild_id = str(member.guild.id)

    if guild_id in config:
        data = config[guild_id]
        channel = bot.get_channel(data["welcome_channel"])
        message = data["welcome_message"]

        if channel:
            msg = message.replace("{user}", member.mention)
            await channel.send(msg)


# -------------------------
# ⚙️ CONFIG WELCOME
# -------------------------
@bot.command()
@commands.has_permissions(administrator=True)
async def setwelcome(ctx, channel: discord.TextChannel, *, message: str):
    guild_id = str(ctx.guild.id)

    config[guild_id] = {
        "welcome_channel": channel.id,
        "welcome_message": message
    }

    save_config(config)

    await ctx.send("✅ Système de bienvenue configuré !")


# -------------------------
# 🧹 MODERATION
# -------------------------
@bot.command()
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.kick(reason=reason)
    await ctx.send(f"👢 {member} kick | raison: {reason}")


@bot.command()
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: discord.Member, *, reason="Aucune raison"):
    await member.ban(reason=reason)
    await ctx.send(f"🔨 {member} ban | raison: {reason}")


# -------------------------
# 📊 INFO COMMANDS
# -------------------------
@bot.command()
async def ping(ctx):
    await ctx.send(f"🏓 Pong ! {round(bot.latency * 1000)}ms")


@bot.command()
async def serverinfo(ctx):
    guild = ctx.guild
    await ctx.send(
        f"📊 **{guild.name}**\n"
        f"👥 Membres: {guild.member_count}\n"
        f"🆔 ID: {guild.id}"
    )


# -------------------------
# 🚀 START BOT (RAILWAY SAFE)
# -------------------------
TOKEN = os.getenv("TOKEN")

if __name__ == "__main__":
    bot.run(TOKEN)