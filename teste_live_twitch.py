import requests
import os
from dotenv import load_dotenv

load_dotenv()

client_id = os.getenv("TWITCH_CLIENT_ID")
oauth_token = os.getenv("TWITCH_OAUTH_TOKEN")
user = os.getenv("TWITCH_USERNAME")

url = f"https://api.twitch.tv/helix/streams?user_login={user}"
headers = {
    "Client-ID": client_id,
    "Authorization": f"Bearer {oauth_token}"
}

response = requests.get(url, headers=headers)
data = response.json()

print("📡 Resposta da Twitch:")
print(data)

if "data" in data and len(data["data"]) > 0:
    print("\n✅ A live está AO VIVO!")
else:
    print("\n❌ A live está OFFLINE (ou algo está errado)")
