import requests

def get_api_key(filename):
    with open(filename) as file:
        key = file.readline()
        return key

API_KEY = str(get_api_key("./weather_api_key.txt"))
UNITS = "imperial"

lat = "43.086480"
long = "-77.667461"
url = "http://api.openweathermap.org/data/2.5/weather?lat={0}&lon={1}&appid={2}&units={3}"\
        .format(lat, long, API_KEY, UNITS)
# print(url)
response=requests.get(url)
response=response.json()
print(response)
max_temp=response["main"]["temp_max"]
min_temp=response["main"]["temp_min"]

print("MAX TEMP: {0}".format(max_temp))
print("MIN TEMP: {0}".format(min_temp))