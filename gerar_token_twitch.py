import requests

client_id = "iupbnhc328jj2xalgnsd8ffp4rejgy"
client_secret = "2689s2ucc0grhy8pn2h18z6btl9w48"

url = "https://id.twitch.tv/oauth2/token"

params = {
    "client_id": client_id,
    "client_secret": client_secret,
    "grant_type": "client_credentials"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=params, headers=headers)

try:
    data = response.json()
    if "access_token" in data:
        print("\n🔑 Seu OAuth Token é:")
        print(data["access_token"])
    else:
        print("\n❌ Erro ao gerar token. Resposta da Twitch:")
        print(data)
except Exception as e:
    print("❌ Erro ao processar a resposta:", e)
