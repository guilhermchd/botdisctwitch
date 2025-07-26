import os
import discord
import requests
from discord.ext import tasks, commands
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = int(os.getenv("DISCORD_CHANNEL_ID"))
TWITCH_TOKEN = os.getenv("TWITCH_OAUTH_TOKEN")
TWITCH_CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
TWITCH_USER = os.getenv("TWITCH_USERNAME")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())

last_stream_status = None

def is_stream_live():
    url = f"https://api.twitch.tv/helix/streams?user_login={TWITCH_USER}"
    headers = {
        "Client-ID": TWITCH_CLIENT_ID,
        "Authorization": f"Bearer {TWITCH_TOKEN}"
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    if "data" in data and len(data["data"]) > 0:
        return True, data["data"][0]
    return False, None

@tasks.loop(minutes=1)
async def check_live():
    global last_stream_status
    print("⏱️ Verificando status da live...")  # DEBUG

    is_live, stream_data = is_stream_live()

    print("✅ is_live:", is_live)              # DEBUG
    print("📦 stream_data:", stream_data)      # DEBUG

    if is_live and last_stream_status != True:
        last_stream_status = True
        channel = bot.get_channel(CHANNEL_ID)
        print("📢 Enviando mensagem no canal:", channel)  # DEBUG EXTRA
        title = stream_data['title']
        game = stream_data.get('game_name', 'jogando algo')
        url = f"https://twitch.tv/{TWITCH_USER}"
        await channel.send(f"@everyone\n🎮 **{TWITCH_USER} está AO VIVO!**\n🔴 **{title}** jogando *{game}*\n👉 {url}")

    elif not is_live:
        last_stream_status = False


@bot.event
async def on_ready():
    print(f"Bot conectado como {bot.user}")
    check_live.start()

bot.run(DISCORD_TOKEN)
