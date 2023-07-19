import requests
from bs4 import BeautifulSoup
from twilio.rest import Client
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By

# Fill in the URL and the element to find on the website
URL = 'https://www.spicinemas.in/moviesessions/Chennai/OPPENHEIMER/NHO00021362?language=ENGLISH'


# Twilio credentials
TWILIO_ACCOUNT_SID = 'AC8331ee5f766dec59c925241dbce18ee8'
TWILIO_AUTH_TOKEN = 'c626fac4733e72b85b23cfc7b506962d'
TWILIO_PHONE_NUMBER = '+14066428904'
YOUR_PHONE_NUMBER = '+917550119733'  # The phone number to which the message will be sent

chrome_options = Options()
chrome_options.add_argument("--headless")

# Replace 'chrome_driver_path' with the actual path to your ChromeDriver executable
chrome_driver_path = "R:\Downloads\chromedriver_win32new\chromedriver.exe"

def check_date_exists(url, target_date):
    s = Service(chrome_driver_path)
    # Use the ChromeDriver executable path we defined above
    driver = webdriver.Chrome(service=s, options=chrome_options)
    driver.get(url)
    html_code = driver.page_source
    driver.quit()

    soup = BeautifulSoup(html_code, 'html.parser')
    date_items = soup.find_all('div', class_='date-item')

    for date_item in date_items:
        date_label = date_item.find('label', class_='date')
        if date_label and date_label.text == str(target_date):
            return True

    return False

def send_notification(message):
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    try:
        client.messages.create(
            body=message,
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
    except Exception as e:
        print(f"Error sending the notification: {e}")

if __name__ == "__main__":
    
    if check_date_exists(URL, target_date=31):
        send_notification("Tickets are open. Book Now!!!!")
    else:
        send_notification("Booking is not open yet. Keep checking!")
