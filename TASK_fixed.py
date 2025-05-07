import urllib.request
import json
from datetime import datetime, timedelta
import sys

def get_timezone_offset(latitude, longitude, api_key):    # PLEASE USE THIS API KEY TM9AQW3VI7AT
    url = f"http://api.timezonedb.com/v2.1/get-time-zone?key={api_key}&format=json&by=position&lat={latitude}&lng={longitude}"

    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            timezone_offset = data['gmtOffset']
            return timezone_offset
    except Exception as e:
        print(f"Error fetching timezone data: {e}")
        sys.exit(1)

def get_sun_times(latitude, longitude):
    today = datetime.utcnow().date()
    formatted_date = today.strftime('%Y-%m-%d')

    url = f"https://api.sunrise-sunset.org/json?lat={latitude}&lng={longitude}&date={formatted_date}&formatted=0"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode())
            sunrise = datetime.fromisoformat(data['results']['sunrise']).replace(tzinfo=None)
            sunset = datetime.fromisoformat(data['results']['sunset']).replace(tzinfo=None)
            return sunrise, sunset
    except Exception as e:
        print(f"Error fetching sunrise/sunset data: {e}")
        sys.exit(1)

def get_time_of_day(sunrise, sunset, timezone_offset):
    sunrise_local = sunrise + timedelta(seconds=timezone_offset)
    sunset_local = sunset + timedelta(seconds=timezone_offset)
    
    current_time = datetime.utcnow() + timedelta(seconds=timezone_offset)

    noon_start = datetime.utcnow().replace(hour=12, minute=0, second=0, microsecond=0)
    noon_end = sunset_local - timedelta(hours=3)
    evening_start = noon_end

    if sunrise_local - timedelta(hours=1) <= current_time < sunrise_local:
        return "sunrise"
    elif sunrise_local <= current_time < sunrise_local + timedelta(hours=6):
        return "morning"
    elif noon_start <= current_time < noon_end:
        return "noon"
    elif evening_start <= current_time < sunset_local:
        return "evening"
    elif sunset_local <= current_time < sunset_local + timedelta(hours=1):
        return "sunset"
    else:
        return "night"

def get_wallpaper(time_of_day):
    if time_of_day == "sunrise":
        return "sunrise.png"
    elif time_of_day == "morning":
        return "morning.png"
    elif time_of_day == "noon":
        return "noon.png"
    elif time_of_day == "evening":
        return "evening.png"
    elif time_of_day == "sunset":
        return "sunset.png"
    else:
        return "night.png"

def main():
    if len(sys.argv) != 4:
        print("Usage: python TASK_fixed.py <latitude> <longitude> <API_KEY>")
        sys.exit(1)

    latitude = float(sys.argv[1])
    longitude = float(sys.argv[2])
    api_key = sys.argv[3]

    timezone_offset = get_timezone_offset(latitude, longitude, api_key)

    sunrise, sunset = get_sun_times(latitude, longitude)

    time_of_day = get_time_of_day(sunrise, sunset, timezone_offset)

    wallpaper = get_wallpaper(time_of_day)

    print(f"Time of Day: {time_of_day}")
    print(f"Selected Wallpaper: {wallpaper}")

if __name__ == "__main__":
    main()
    
# PLEASE USE THIS API KEY TM9AQW3VI7AT
