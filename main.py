import requests
from bs4 import BeautifulSoup
import time
import logging
import os
from requests.exceptions import Timeout, RequestException

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%d-%b-%y %H:%M:%S',
    filename='logFile.txt',
    filemode='a'
)

def get_html(url):
    try:
        logging.info("Getting html from {}".format(url))
        cert = r"C:\Users\ayahmed\SSL Certificates\awokiproxy.woki.uk.ssg.crt"
        x = requests.get(
            url,
            timeout=5
        )
        x.raise_for_status()
        logging.info("Successfully got html from {}".format(url))
        return x
    except Timeout:
        print("The request timed out")
    except Exception as e:
        logging.error(f"Error: {e}")

def parse_html(html):
    if html is None:
        logging.error("No html found")
        return None
    soup = BeautifulSoup(
        html,
        'html.parser')
    price = soup.find(
        "td",
        class_="force-padding type-number dw-bold align-center align-vertical-middle    td cell  svelte-5rcs0n")
    logging.info(f"Price of petrol is: {price}")
    return price


print(parse_html(get_html(r'https://www.rac.co.uk/drive/advice/fuel-watch/')))