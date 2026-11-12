from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
from bs4 import BeautifulSoup
import time
import smtplib
import logging
import os
from requests.exceptions import Timeout, RequestException
from dotenv import load_dotenv

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    filename='logFile.txt',
    filemode='a'
)

def get_html(url):
    try:
        logging.info(f"Getting html from {url}")
        page = requests.get(
            url,
            timeout=5
        )
        page.raise_for_status()
        logging.info("Successfully got html from {}".format(url))
        return page.text
    except Timeout:
        print("The request timed out")
        return None
    except Exception as e:
        logging.error(f"Error: {e}")
        return None

# Parse HTML to extract price of petrol
def parse_html(html):
    try:
        if html is None:
            logging.error("No html found")
            return None
        soup = BeautifulSoup(
            html, 'html.parser')
        extract = soup.select_one(".figure-petrol")
        if extract is None:
            logging.error("No petrol found")
        price = extract.get_text(strip=True)
        logging.info(f"Price of petrol is: {price}")

        return price
    except Exception as e:
        logging.error(f"Error parsing the HTML content: {e}")
        return None

page = get_html('https://www.petrolprices.co.uk/uk-fuel-prices-live.php')
price = parse_html(page)

# Environment variables

load_dotenv()
my_email = os.getenv("MY_EMAIL")
my_password = os.getenv("MY_PASSWORD")
target_email = os.getenv("TARGET_EMAIL")

# def send_mail(subject, to, html):
# function will send an email composing of the reduction in price

def send_mail(subject, to, html):
    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = my_email
    msg["To"] = target_email
    msg.attach(MIMEText(html, "html"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(my_email, my_password)  # use a Gmail App Password
            logging.info("Successfully logged in")
            server.sendmail(my_email, to, msg.as_string())
            logging.info("Successfully sent email")
    except smtplib.SMTPAuthenticationError as e:
        logging.error(f"Login failed (check your App Password): {e}")
    except smtplib.SMTPConnectError as e:
        logging.error(f"Could not connect to the server: {e}")
    except Exception as e:
        logging.error(e)

# Test email
# send_mail("Test Email - Price Reduction",target_email, "This is a test email")

# Loop
while True:
    newPrice = parse_html(page)
    if newPrice >= price:
        logging.info(f"Price is {newPrice}, no reduction seen")
        time.sleep(30)
    else:
        logging.info(f"Price is {newPrice}, reduction seen {price}")
        send_mail("Price Reduction In Petrol",
                  "ayub.120@hotmail.com",
                  f"<p>Price of petrol has reduced and is: -{newPrice}\n")
        price = newPrice
        break
