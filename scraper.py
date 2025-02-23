from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
import os
from dotenv import load_dotenv
import re

load_dotenv()

class Scraper:
    def __init__(self, url, long, lat):
        self.url = url
        self.html = None
        # idk how ethical this is but I'm mimicking a real browser :)
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.long = long
        self.lat = lat

    #scraping using playwright - should work with proxies from oxylab :)
    def scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, proxy={'server': os.getenv("PROXY_SERVER"), 
                                                              'username': os.getenv("PROXY_USERNAME"), 
                                                              'password': os.getenv("PROXY_PASSWORD")})
            context = browser.new_context(user_agent=self.ua, geolocation={'latitude' : self.lat, 
                                          'longitude': self.long}, permissions=['geolocation']) 
            page = context.new_page()
            page.goto(self.url)
            #necessary to wait until all stuff has loaded :)
            page.wait_for_load_state('domcontentloaded', timeout=60000)
            self.html = page.content()

    #read contents and actually receive the egg prices and stuff
    def read_walmart(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        spans = soup.find_all('span', class_='w_iUH7')
        filter = [span.getText(strip=True) for span in spans if "egg" in span.text.lower() or "current price" in span.text.lower()]
        eggs = {}
        entry_ind = 0
        #there should always be a product - price pair, so we can divide by 2
        while entry_ind < int(len(filter)/2):
            product_name = filter[entry_ind]
            price = float(filter[entry_ind+1].split('current price $')[1])
            eggs[product_name] = price
            entry_ind+=2
        return eggs
    
    def return_soup(self):
        return BeautifulSoup(self.html, 'html.parser')


def main():
    #debugging to make sure this actually works :crying:
    url = 'https://www.walmart.com/search?q=egg&facet=facet_product_type%3AEggs%7C%7Cfood_form%3AWhole%7C%7Cnumber_of_pieces%3A12%7C%7Cnumber_of_pieces%3A18'
    lat = 38.0372329
    long = -78.5706529
    scraper = Scraper(url, lat, long)
    scraper.scrape()
    print(scraper.read_walmart())
    with open ('output.html', 'w', encoding='utf-8') as f:
        f.write(scraper.return_soup().prettify())

if __name__ == '__main__':
    main()