import os
import requests

USGS_API = "https://earthquake.usgs.gov/fdsnws/event/1/query"

def get_earthquake_data():
    params = {"format": "geojson", "starttime": "2025-03-29", "minmagnitude": 4.5, "limit": 5}
    response = requests.get(USGS_API, params=params)
    return response.json()

def get_color_for_magnitude(mag):
    """เลือกสีตามระดับ magnitude ของแผ่นดินไหว"""
    if mag >= 7.0:
        return 0xFF0000  # สีแดง
    elif mag >= 6.0:
        return 0xFFA500  # สีส้ม
    elif mag >= 5.0:
        return 0xFFFF00  # สีเหลือง
    else:
        return 0x00FF00  # สีเขียว

def send_discord_message(message, color):
    """ส่งข้อความไปยัง Discord โดยใช้ Embed และกำหนดสี"""
    embed = {
        "embeds": [{
            "title": "แผ่นดินไหวเกิดขึ้น!",
            "description": message,
            "color": color
        }]
    }
    webhook_url = os.environ['DISCORD_WEBHOOK_URL']  # ใช้ secrets ใน GitHub
    requests.post(webhook_url, json=embed)

def main():
    data = get_earthquake_data()
    for quake in data["features"]:
        place = quake["properties"]["place"]
        mag = quake["properties"]["mag"]
        color = get_color_for_magnitude(mag)
        message = f"🌍 แผ่นดินไหวขนาด {mag} ที่ {place}"
        send_discord_message(message, color)

if __name__ == "__main__":
    main()
