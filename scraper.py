from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright


class Scraper:
    def __init__(self, url, lat, long):
        self.url = url
        self.html = None
        # idk how ethical this is but I'm mimicking a real browser :)
        self.ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36'
        self.lat = lat
        self.long = long

    #static scraping using requests - works if page statically loads
    def static_scrape(self):
        headers = {'User-Agent': self.ua, "X-Geo-Location": f"{self.lat}; {self.long}"}
        self.html = requests.get(self.url, headers=headers).text

    #dynamic scraping using playwright - works if page dynamically loads
    #but much much slower (ONLY USE IF STATIC DOESN'T WORK)
    def dynamic_scrape(self):
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(user_agent=self.ua, geolocation={"latitude" : self.lat, 
                                          "longitude": self.long}, permissions=["geolocation"]) 
            page = context.new_page()
            page.goto(self.url)
            self.html = page.content()

    #read contents and actually receive the egg prices and stuff
    def read(self):
        return BeautifulSoup(self.html, "html.parser")

def main():
    #debugging to make sure this actually works :crying:
    url = 'https://www.walmart.com/search?q=egg&facet=facet_product_type%3AEggs%7C%7Cfood_form%3AWhole%7C%7Cnumber_of_pieces%3A12%7C%7Cnumber_of_pieces%3A18'
    lat = 38.0372329
    long = -78.5706529
    scraper = Scraper(url, lat, long)
    scraper.dynamic_scrape()
    with open ("output.html", "w") as f:
        f.write(scraper.read().prettify())

if __name__ == "__main__":
    main()