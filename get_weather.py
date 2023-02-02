import requests
from datetime import *


def get_api_key(filename):
    with open(filename) as file:
        key = file.readline()
        return key


API_KEY = str(get_api_key("./weather_api_key.txt"))
UNITS = "imperial"

lat = "43.086480"
long = "-77.667461"
url = "http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid={2}&units={3}&cnt=4".format(lat, long, API_KEY, UNITS)
# print(url)
response = requests.get(url)
response = response.json()
print(response)
list = response["list"]
for entry in list:
    # time
    utc_timestamp = entry["dt_txt"]
    utc_obj = datetime.fromisoformat(utc_timestamp)
    local_obj = utc_obj.astimezone(None)
    # temp
    temp = entry["main"]["temp"]
    print("{0} - {1}".format(local_obj.strftime("%I %p"), temp))
