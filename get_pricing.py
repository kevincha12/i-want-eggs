import location_reference_creation as LRC
from store import Store
from scraper import Scraper

class PriceFilter:
    def __init__(self):
        self.stores = self.load_stores()

    def load_stores(self):
        target_list = self.load_target()
        walmart_list = self.load_walmarts()
        target_list.extend(walmart_list)
        return target_list

    def load_target(self):
        target_stores = []
        target_df = LRC.load_target_csvs()
        #again, super unoptimal but for now this is a good query to just enforce and load.
        target_optimized_url = 'https://www.target.com/s?searchTerm=eggs&tref=typeahead%7Cterm%7Ceggs%7C%7C%7Chistory&facetedValue=4pd1f&ignoreBrandExactness=true&moveTo=product-list-grid'
        for index, row in target_df.iterrows():
            full_address = row['Address.FormattedAddress']
            address_elements = [addr_elem.strip() for addr_elem in full_address.split(',')]
            #to explain, the city should be the second to last element and 
            #the zipcode should be the last element after the split
            address = address_elements[0]
            city = address_elements[-2]
            zipcode = address_elements[-1].split(' ')[1]
            longitude = row['Address.Longitude']
            latitude = row['Address.Latitude']
            eggs = self.get_eggs(target_optimized_url, longitude, latitude)
            target_stores.append(Store(address, city, zipcode, longitude, latitude, eggs))
        return target_stores

    def load_walmarts(self):
        walmart_stores = []
        walmart_df = LRC.load_walmart_csvs()
        #yeah it doesn't feel great but this is an optimized URI usage and then we just need to deal with long/lat so walmart picks up on the correct warehouse
        walmart_optimized_url = 'https://www.walmart.com/search?q=egg&facet=facet_product_type%3AEggs%7C%7Cfood_form%3AWhole%7C%7Cnumber_of_pieces%3A12%7C%7Cnumber_of_pieces%3A18'
        for index, row in walmart_df.iterrows():
            address = row['street_address']
            city = row['city']
            zipcode = row['zip_code']
            longitude = row['longitude']
            latitude = row['latitude']
            eggs = self.get_eggs(walmart_optimized_url, longitude, latitude)
            walmart_stores.append(Store(address, city, zipcode, longitude, latitude, eggs))
        return walmart_stores
    
    def get_eggs(self, url, store_long, store_lat):
        instanced_scraper = Scraper(url, store_lat, store_long)
        instanced_scraper.scrape()
        return instanced_scraper.read_walmart()