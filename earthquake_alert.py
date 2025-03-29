import os
import requests

USGS_API = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def get_earthquake_data():
    params = {"format": "geojson", "starttime": "2025-03-29", "minmagnitude": 4.5, "limit": 5}
    response = requests.get(USGS_API, params=params)
    return response.json()

def send_discord_message(message):
    data = {"content": message}
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']  # ใช้ secrets ใน GitHub
    requests.post(webhook_url, json=data)

def main():
    data = get_earthquake_data()
    for quake in data["features"]:
        place = quake["properties"]["place"]
        mag = quake["properties"]["mag"]
        message = f"🌍 แผ่นดินไหวขนาด {mag} ที่ {place}"
        send_discord_message(message)

if __name__ == "__main__":
    main()
