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
parsed = parse_html(page)

print(parsed)
