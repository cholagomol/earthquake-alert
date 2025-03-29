import os
import requests
from datetime import datetime

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

def get_country_flag(country_code):
    """แปลงรหัสประเทศ ISO 3166-1 Alpha-2 เป็นธง"""
    flag = ''.join([chr(ord(char) - 32 + 127397) for char in country_code.upper()])
    return flag

def format_earthquake_time(iso_time):
    """แปลงเวลาเป็นรูปแบบที่อ่านง่าย เช่น '2025-03-29 14:30:00'"""
    time_obj = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%S.%fZ")
    return time_obj.strftime("%Y-%m-%d %H:%M:%S")  # ปรับรูปแบบเวลาให้เหมาะสม

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
        time = quake["properties"]["time"] / 1000  # เวลาใน millisecond (ต้องแบ่งด้วย 1000 เพื่อแปลงเป็นวินาที)
        formatted_time = format_earthquake_time(datetime.utcfromtimestamp(time).strftime('%Y-%m-%dT%H:%M:%S.%fZ'))
        
        # สมมติว่าชื่อประเทศอยู่ใน "place"
        country_code = place.split()[-1]  # ใช้คำสุดท้ายเป็นรหัสประเทศ (ISO 3166-1 Alpha-2)

        flag = get_country_flag(country_code)  # แปลงรหัสประเทศเป็นธง
        color = get_color_for_magnitude(mag)
        message = f"{flag} 🌍 แผ่นดินไหวขนาด {mag} ที่ {place} เกิดขึ้นเมื่อ {formatted_time}"
        send_discord_message(message, color)

if __name__ == "__main__":
    main()
