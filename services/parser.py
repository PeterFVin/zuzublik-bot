import re

import requests
from bs4 import BeautifulSoup


def extract_class_from_xpath(xpath):
    match = re.search(r"@class=['\"](.*?)['\"]", xpath)
    return match.group(1) if match else None


def parse_price(url, xpath, parse_list):
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/125.0.0.0 Safari/537.36"
        )
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "lxml")
        for xpath_class in parse_list:
            if xpath_class in xpath:
                price_element = soup.find("span", class_=xpath_class)
        if price_element:
            price_text = price_element.get_text(strip=True)
            return int("".join(filter(str.isdigit, price_text)))
    except Exception as e:
        print(f"Error parsing {url}: {str(e)}")
    return None
