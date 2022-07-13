import os
import requests
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient

OWM_ENDPOINT = "https://api.openweathermap.org/data/3.0/onecall"
api_key = os.environ.get('API_KEY')

account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
auth_token = os.environ.get('TWILIO_AUTH_TOKEN')

sender = os.environ.get('SENDER_NUMBER')
receiver = os.environ.get('RECEIVER_NUMBER')

MY_LAT = 6.874128
MY_LON = 79.859329

parameters = {
    "lat": MY_LAT,
    "lon": MY_LON,
    "appid": api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(OWM_ENDPOINT, params=parameters)
response.raise_for_status()

weather_data = response.json()
weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]

    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}

    client = Client(account_sid, auth_token, http_client=proxy_client)

    message = client.messages \
        .create(
        body="It's going to rain today. Remember to bring an umbrella ☔",
        from_=sender,
        to=receiver
    )

    print(message.status)
