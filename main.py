import requests
import datetime
import smtplib
import time

# Constants
LAT = 8.825367
LONG = 78.121922
MY_EMAIL = "gnanaganesh1999@yahoo.com"
PASSWORD = "fzpwrezdxcjxzmns"


def iss_over_head():
    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()

    data = response.json()
    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if LAT - 5 <= iss_latitude <= LAT + 5 and LONG - 5 <= iss_longitude <= LONG + 5:
        return True


def is_night():
    params = {
        "lat": LAT,
        "lng": LONG,
        "formatted": 0
    }

    response = requests.get(url=" https://api.sunrise-sunset.org/json", params=params)
    response.raise_for_status()

    data = response.json()
    sunrise = int(data['results']['sunrise'].split('T')[1].split(":")[0])
    sunset = int(data['results']['sunset'].split('T')[1].split(":")[0])

    time_now = datetime.datetime.now().hour

    if time_now >= sunset or time_now <= sunrise:
        return True


while True:
    time.sleep(300)
    if iss_over_head() and is_night():
        with smtplib.SMTP() as connection:
            connection.login(user=MY_EMAIL, password=PASSWORD)
            connection.starttls()
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs="gnanaganesh1999@gmail.com",
                msg="Subject:ISS is visible today\n\nHi there,\nToday you will find ISS above you. Don't miss it!\nThank you"
            )
