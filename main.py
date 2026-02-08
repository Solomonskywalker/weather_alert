import requests
from twilio.rest import Client
import os
import json



account_sid = "AC66ab645970868cf3faeda1738b7ce4ac"
auth_token = "9afd3ad4acf217a5a94125e8ebbc0234"
client = Client(account_sid, auth_token)

print(f"Connected to Twilio Account: {client.api.accounts(account_sid).fetch().friendly_name}")

api_kay = "afdecab46fea1c76b8e64294dcc705b4"
url = "https://api.openweathermap.org/data/2.5/forecast"

#   WE GET THE LAT AND LONG OF OUR LOCATION AND CREATE A DICTIONARY TO HOLD IT
MY_LAT = 35.125
MY_LONG = 33.95

parameters = {
    "lat":MY_LAT,
    "lon":MY_LONG,
    "appid":api_kay,
    "cnt": 4
}
# WE CREATE API REQUEST AND PASS IN OUR PARAMETERS
response = requests.get(url, params=parameters)
response.raise_for_status()
weather_data = response.json()
current_weather_dic = weather_data["list"][0]["weather"][0]

# we get a list of the data for the 5 days
list_weather_data = weather_data["list"]
# we also get the description
weather_description = current_weather_dic["description"]
# we loop through the list_weather_data
will_rain = False
for weather in list_weather_data:
    weather_id = weather["weather"][0]["id"]
   # We get weather description for each item
    current_weather_description = weather["weather"][0]["description"]

    if int(weather_id) < 700:
        will_rain = True
if will_rain:
        print(f"The weather description says: {current_weather_description}, bring an umbrella with you")

        message = client.messages.create(
            from_='whatsapp:+14155238886',
            to='whatsapp:+905338620109',
            body=f'The weather description says: {current_weather_description}, take an umbrella',
        )
        print(message.status)
        print(message.body)
else:
    print("No rain forecast")



