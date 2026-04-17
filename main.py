import os
import smtplib
import requests
from twilio.rest import Client

MY_EMAIL = os.environ.get("MY_EMAIL")
TO_EMAIL = os.environ.get("TO_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")

def send_email(message):
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=MY_PASSWORD)
        connection.sendmail(
                            from_addr=MY_EMAIL,
                            to_addrs=TO_EMAIL,
                            msg=f"Subject:😺Weather Update!\n\n{message}"
                            )

OPEN_WEATHER_API_KEY = os.environ.get("OWM_API_KEY")
MY_LAT = 53.285347
MY_LONG = -9.012642
parameters = {
    "lat": MY_LAT,
    "lon": MY_LONG,
    "appid":OPEN_WEATHER_API_KEY,
    "cnt":3,
    "units":"metric"
}
response = requests.get(url="https://api.openweathermap.org/data/2.5/forecast", params=parameters)
response.raise_for_status()
data = response.json()

RAINY_WEATHER_MESSAGE = "Its Gonna rain🌧️. Carry an Umbrella☔!"
CLEAR_WEATHER_MESSAGE = "It's Sunny☀️ Outside! Got to the beach🏖️"

will_rain = False
weather_codes = [int(data_point["weather"][0]["id"]) for data_point in data["list"] if int(data_point["weather"][0]["id"]) < 700]
for codes in weather_codes:
    if codes < 700:
        will_rain = True

if will_rain:
    send_email(RAINY_WEATHER_MESSAGE)
else:
    send_email(CLEAR_WEATHER_MESSAGE)

    

