import requests
from datetime import *  # type:ignore
import pytz


def get_api_key(filename):
    with open(filename) as file:
        key = file.readline()
        return key


API_KEY = str(get_api_key("./weather_api_key.txt"))
UNITS = "imperial"

lat = "43.086480"
long = "-77.667461"
url = "http://api.openweathermap.org/data/2.5/forecast?lat={0}&lon={1}&appid={2}&units={3}&cnt=4".format(lat, long, API_KEY, UNITS)


def get_forecast():
    '''
    gets the next forecast, one entry every 3 hours for the next 12 hours (4 total datapoints)
    This is limited by the free api tier
    '''
    # list to store results in (basically just re-packing the list that the API sends us to make it easier)
    results = []
    # make request to the api
    response = requests.get(url)
    response = response.json()
    # get list of data points
    list_of_forecasts = response["list"]
    # for every data point...
    for entry in list_of_forecasts:
        # get time object
        utc_timestamp = entry["dt_txt"]
        utc_obj = datetime.fromisoformat(utc_timestamp)
        utc_obj = utc_obj.replace(tzinfo=pytz.utc)
        # convert to local time
        local_obj = utc_obj.astimezone(None)
        time_string = local_obj.strftime("%I%p")
        # remove leading 0
        if time_string[0] == "0":
            time_string = time_string[1:]
        # get temperature
        temp = str(int(entry["main"]["temp"]))
        # wow that's a lot of type casting for the Percentage of Precipitation
        pop = str(int(entry["pop"]*100))
        #description (rainy, snowy, cloudy, etc)
        description = entry["weather"][0]["description"].strip()
        clouds = entry["clouds"]
        wind_speed = str(int(entry["wind"]["speed"]))
        # append completed dict to results
        results.append({"temp": temp, "description": description, "clouds": clouds, "wind_speed": wind_speed, "time": time_string, "pop": pop})

    return results
