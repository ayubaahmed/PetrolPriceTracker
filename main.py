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
        section = soup.find("section", class_="mb-8")

        if not section:
            logging.error("No section found")
            return None
        avg_prices = section.find(
            "div", class_='grid grid-cols-2 md:grid-cols-4 gap-3 md:gap-4 mb-4')
        if not avg_prices:
            logging.error("No prices found")
            return None

        petrol_avg = avg_prices.find(
            "div", class_='stat-card')

        if not petrol_avg:
            logging.error("No petrol avg found")
            return None

        price = petrol_avg.find(
            "div", class_= 'figure figure-petrol')

        if not price:
            logging.error("No petrol price  found")
            return None
        logging.info(f"Price of petrol is: {price}")

        return price
    except Exception as e:
        logging.error(f"Error parsing the HTML content: {e}")
        return None


page = get_html('https://www.petrolprices.co.uk/uk-fuel-prices-live.php')
parsed = parse_html(page)

print(parsed)
