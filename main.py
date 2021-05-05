import requests
from datetime import datetime
import  smtplib
import time

MY_EMAIL = "enter_your_email"
MY_PASSWORD = "enter_your_password"

MY_LAT = "enter_your_latitude"
MY_LONG = "enter_your_longitude"

#-----track ISS-----#

def is_iss_overhead():
    response_iss = requests.get("http://api.open-notify.org/iss-now.json")
    response_iss.raise_for_status()
    data_iss = response_iss.json()

    iss_longitude = float(data_iss["iss_position"]["longitude"])
    iss_latitude = float(data_iss["iss_position"]["latitude"])

    
    #Your position is within +5 or -5 degrees of the ISS position.
    if MY_LAT-5 <= iss_latitude <= MY_LAT+5 and MY_LNG -5<= iss_longitude <= MY_LNG +5:
        return True



#------My location sunrise & sunset time----#

def is_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
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
    
        connection = smtplib.SMTP("smtp.gmail.com") 
        #if you have gmail account smtp == "smtp.gmail.com",
        # yahoo account smtp == smtp.mail.yahoo.com,
        # hotmail account smtp =="smtp.live.com"
        # outlook smtp == "smtp-mail.outlook.com"
        
        connection.starttls()
        connection.login(MY_EMAIL,MY_PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL,to_addrs="enter_destination_email", msg=f"Subject: ISS overhead\n\n Just watch at the sky!")

#save it on Cloud with Python Anywhere and it will run every 60 seconds
while True:
    #run it every 60 seconds
    time.sleep(60)
    if is_night() and is_iss_overhead():
        send_email()


#Enjoy it
