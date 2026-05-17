import os
import sys
import shutil
import requests

# --- CONFIGURATION ---
CITY = "Sydney,AU"
API_KEY = os.environ.get("OPENWEATHER_API_KEY")

if not API_KEY:
    print("[ERROR] Missing OPENWEATHER_API_KEY.", file=sys.stderr)
    sys.exit(1)

def update_current_weather():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API_KEY}"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] API connection failed: {e}")
        sys.exit(1)

    weather_main = data["weather"][0]["main"].lower()
    weather_id = data["weather"][0]["id"]
    temp = data["main"]["temp"]

    # --- MAPPING LOGIC ---
    if temp <= 5:
        image_name = "cat_cold.svg"
    elif "snow" in weather_main or (600 <= weather_id <= 622):
        image_name = "cat_snow.svg"
    elif "thunderstorm" in weather_main or (200 <= weather_id <= 232):
        image_name = "cat_stormy.svg"
    elif "rain" in weather_main or "drizzle" in weather_main:
        image_name = "cat_rainy.svg"
    elif "clear" in weather_main:
        image_name = "cat_sunny.svg"
    else:
        image_name = "cat_mild.svg"

    # Define paths based on your repository layout
    source_path = os.path.join("images", image_name)
    target_path = os.path.join("images", "current_weather.svg")

    # Overwrite current_weather.svg with the matching condition file
    if os.path.exists(source_path):
        shutil.copyfile(source_path, target_path)
        print(f"Successfully updated current_weather.svg to match {image_name} ({temp}°C)")
    else:
        print(f"[ERROR] Source image {source_path} not found.")
        sys.exit(1)

if __name__ == "__main__":
    update_current_weather()
