import requests
from datetime import datetime
import  smtplib
import time

MY_EMAIL = "yourdeeplynewsletter@gmail.com"
MY_PASSWORD = "g90pli()!?qw"

MY_LAT = 40.4778488
MY_LNG = 15.6301506

#-----track ISS-----#

def is_iss_overhead():
    response_iss = requests.get("http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_longitude = float(data_iss["iss_position"]["longitude"])
    iss_latitude = float(data_iss["iss_position"]["latitude"])

    iss_latitude = 40.4778488
    iss_longitude = 15.6301506
    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG -5<= iss_longitude <= MY_LNG +5:
        return True



#------My location sunrise & sunset time----#

def is_night():
    parameters = {
        "lat": 40.4778488,
        "lng": 15.6301506,
        "formatted": 0
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])



    time_now = datetime.now().hour
    if time_now >= sunset or time_now <= sunrise:
        return True


#----send email----#

def send_email():
    MY_EMAIL = "yourdeeplynewsletter@gmail.com"
    MY_PASSWORD = "g90pli()!?qw"

    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,to_addrs="saroantonello.lovito@gmail.com", msg=f"Subject: ISS overhead\n\n Just watch at the sky!")

while True:
    #run it every 60 seconds
    time.sleep(60)
    if is_night() and is_iss_overhead():
        send_email()


#Enjoy it