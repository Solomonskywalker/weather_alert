import requests
from twilio.rest import Client
import os
from flask import Flask
from twilio.rest import Client

app = Flask(__name__)

def weather_alert():
    account_sid = "AC66ab645970868cf3faeda1738b7ce4ac"
    auth_token = "9afd3ad4acf217a5a94125e8ebbc0234"
    client = Client(account_sid, auth_token)

    #return f"Connected to Twilio Account: {client.api.accounts(account_sid).fetch().friendly_name}"

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
            break
    if will_rain:
            message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:+905338620109',
                body=f'The weather description says: {current_weather_description}, take an umbrella',
            )
            return  message.status
    else:
        return "No rain forecast"

@app.route('/')
def home():
    return weather_alert()

@app.route('/trigger')
def trigger():
    result = weather_alert()
    return result

if __name__ == "__main__":
    # Render provides a PORT environment variable
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)