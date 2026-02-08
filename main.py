import requests
from twilio.rest import Client
import os
from flask import Flask
from twilio.rest import Client

app = Flask(__name__)

def weather_alert():
    account_sid = os.environ.get("TWILIO_ACCOUNT_SID")
    auth_token = os.environ.get("TWILIO_AUTH_TOKEN")
    client = Client(account_sid, auth_token)

    #return f"Connected to Twilio Account: {client.api.accounts(account_sid).fetch().friendly_name}"

    api_kay = os.environ.get("OWM_API_KEY")
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

    list_weather_data = weather_data["list"]
    will_rain = False
    # We start our message with a header
    message_body = "Rain Alert for Today! ☔\n"

    # 2. Loop through all slots to find rain and build the list
    for weather in list_weather_data:
        weather_id = weather["weather"][0]["id"]
        
        if int(weather_id) < 700:
            will_rain = True
            
            # Extract time and description
            time_raw = weather["dt_txt"] # e.g., "2026-02-08 12:00:00"
            # Get just the hour/minute: "12:00"
            time_short = time_raw.split(" ")[1][:5]
            description = weather["weather"][0]["description"]
            
            # Add this specific rain slot to our message
            message_body += f"\n- {time_short}: {description.capitalize()}"
    if will_rain:
        message_body += "\n\nDon't forget your umbrella! 🧥"
        message = client.messages.create(
                from_='whatsapp:+14155238886',
                to='whatsapp:+905338620109',
                body=message_body,
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
