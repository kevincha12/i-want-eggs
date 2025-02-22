from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright


class Scraper:
    #static scraping using requests - works if page statically loads
    def static_scrape(self):
        self.html = requests.get(self.url).text

    #dynamic scraping using playwright - works if page dynamically loads
    #but much much slower (ONLY USE IF STATIC DOESN'T WORK)
    def dynamic_scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(self.url)
            self.html = page.content()
            browser

    # read contents and actually receive the egg prices and stuff
    def read(self):
        self.soup = BeautifulSoup(self.html, "html.parser")