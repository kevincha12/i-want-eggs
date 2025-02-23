class Store:
    #as a note,
    #address is a string for the street address
    #city is a string for the city
    #zipcode is a string for the zipcode (not an int because zipcodes could have a dash)
    #longitude is a float for the longitude
    #latitude is a float for the latitude
    #eggs is a dictionary with the key as the egg name and the value as the price :)
    def __init__(self, address, city, zipcode, longitude, latitude, eggs):
        self.address = address
        self.city = city
        self.zipcode = zipcode
        self.longitude = longitude
        self.latitude = latitude
        self.eggs = eggs