import requests
import smtplib
import os

owm_api_key = os.environ["owm_api_key"]

OWM_Endpoint = "https://api.openweathermap.org/data/2.5/onecall"

weather_params = {
    "lat": 40.7934,
    "lon": -77.86,
    "appid": owm_api_key,
    "exclude": "current,minutely,daily"
}

rain_weather_params = {
    "lat": 41.8781,
    "lon": -87.6298,
    "appid": owm_api_key,
    "exclude": "current,minutely,daily"
}

response = requests.get(url=OWM_Endpoint, params=rain_weather_params)
response.raise_for_status()

weather_data = response.json()

weather_slice = weather_data["hourly"][:12]

will_rain = False

for hour_data in weather_slice:
    condition_code = hour_data["weather"][0]["id"]
    if int(condition_code) < 700:
        will_rain = True

password = os.environ["yesmanvongpass"]
email = "yesmanvong@gmail.com"

if will_rain:
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=email, password=password)
        connection.sendmail(
            from_addr=email,
            to_addrs="gudiedryan@gmail.com",
            msg=f"Subject: Rain expected\n\nHey, bring an umbrella, it's supposed to rain today."
        )