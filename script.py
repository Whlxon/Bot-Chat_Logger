import discord
from discord.ext import commands
import yt_dlp as youtube_dl
import yt_dlp
import asyncio
import os
import json
from discord import FFmpegPCMAudio

intents = discord.Intents.default()
intents.message_content = True
intents.messages = True
intents.guilds = True

LOG_FILE = "logs.json"

bot = commands.Bot(intents=discord.Intents.all(), command_prefix="log/", description = "Bot pour tout le monde!")

def load_logs():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_logs(logs):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=4, ensure_ascii=False)


@bot.event
async def on_ready():
    print("Ready")
    
    activity = discord.Game("fl/whats list")
    await bot.change_presence(status=discord.Status.online, activity=activity)
    

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # ignore ses propres messages
    
    logs = load_logs()
    
    # Crée une entrée de log
    log_entry = {
        "auteur": str(message.author),
        "id_auteur": message.author.id,
        "serveur": message.guild.name if message.guild else "DM",
        "salon": message.channel.name if message.guild else "Privé",
        "contenu": message.content,
        "date": str(message.created_at)
    }
    
    logs.append(log_entry)
    save_logs(logs)
    
    await bot.process_commands(message)

token = ""
with open('./token.txt', 'r+') as data:
    token = data.readlines()[0]

bot.run(token)