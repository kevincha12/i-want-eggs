import location_reference_creation as LRC
import store

class PriceFilter:
    def __init__(self):
        self.stores = self.load_stores()
        #egg_prices are stored in a dictionary; key is the store name, value is the price
        self.egg_prices = self.parse_egg_prices()

    def parse_egg_prices(self):
        # TODO: implement, but basically should egg_prices
        # should be a dictionary of address keys and price values in a list
        # basically, String -> List<String>
        
        pass

    def load_stores(self):
        target_list = self.load_target()
        walmart_list = self.load_walmarts()
        target_list.extend(walmart_list)
        return target_list

    def load_target(self):
        target_stores = []
        target_df = LRC.load_target_csvs()
        for index, row in target_df.iterrows():
            full_address = row['Address.FormattedAddress']
            address_elements = [addr_elem.strip() for addr_elem in full_address.split(',')]
            target_stores.append(store.Store(address=address_elements[0],
                                             city=address_elements[1],
                                             zipcode=address_elements[-1].split(' ')[1],
                                             longitude=row['Address.Longitude'],
                                             latitude=row['Address.Latitude'],
                                             eggs=None))
        return target_stores
        

    def load_walmarts(self):
        walmart_stores = []
        walmart_df = LRC.load_walmart_csvs()
        for index, row in walmart_df.iterrows():
            walmart_stores.append(store.Store(address=row['street_address'],
                                              city=row['city'],
                                              zipcode=row['zip_code'],
                                              longitude=row['longitude'],
                                              latitude=row['latitude'],
                                              eggs=None))
        return walmart_stores

if __name__ == '__main__':
    pf = PriceFilter()
    print(pf.stores)