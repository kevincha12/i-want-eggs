from get_pricing import PriceFilter
from db import DBHandler
#this serves as a short python script to bring all the other files together.
all_stores_with_prices = PriceFilter()
stores = all_stores_with_prices.load_stores()

db_inst = DBHandler()
db_inst.open_conn()
db_inst.new_transaction()
db_inst.create_tables()
for store in stores:
    store_pkey = db_inst.add_store(store.address, store.city, store.zipcode, store.longitude, store.latitude)
    eggs = store.eggs
    for egg in eggs:
        egg_pkey = db_inst.add_egg(egg)
        db_inst.add_store_egg_relation(store_pkey, egg_pkey)
    db_inst.commit()
db_inst.commit()
db_inst.close_transaction()
db_inst.close_conn()