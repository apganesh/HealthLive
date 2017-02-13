import random
import pickle
import faker
from faker import Faker
# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

fake = Faker()

class GeoLocation(BaseProvider):

    city_list = [(40.7616909474115,-73.97884368896484),(40.6781784,-73.9441579),(48.856614,2.3522219),(28.6139391,77.209021),(41.880553298809645,-87.64755249023438),(39.904211,116.40739499999995)]
    def geoloc(self):
        lat,lon = random.choice(self.city_list)
        latitude = random.uniform(lat - 0.05, lat + 0.05)
        longitude = random.uniform(lon - 0.05, lon + 0.05)
        return latitude,longitude

fake.add_provider(GeoLocation)
pharmacyLocDict = {}
N = 1000
for i in range(0,N):
    lat,lon = fake.geoloc()
    pharmacyLocDict[fake.ean8()] = (lat,lon)
    output = open('pharmacyPickle.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(pharmacyLocDict, output)
    output.close()    