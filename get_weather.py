import requests

def get_api_key(filename):
    with open(filename) as file:
        return file.next()

url = "api.openweathermap.org/data/2.5/forecast?lat=%s&lon=%s&appid=%s" % (lat, long, get_api_key())