import random
import pickle
import faker
from faker import Faker
# first, import a similar Provider or use the default one
from faker.providers import BaseProvider

fake = Faker()

class GeoLocation(BaseProvider):

    user_list = [(40.76,-73.97),(40.67,-73.94),(48.85,2.35),(28.61,77.20),(41.88,-87.64),(39.90,116.40)]
    def geoloc(self):
        lat,lon = random.choice(self.user_list)
        latitude = random.uniform(lat - 0.08, lat + 0.08)
        longitude = random.uniform(lon - 0.08, lon + 0.08)
        return latitude,longitude

fake.add_provider(GeoLocation)
userLocDict = {}
N = 1000
for i in range(0,N):
    lat,lon = fake.geoloc()
    userLocDict[fake.ean8()] = (lat,lon)
    output = open('userPickle.pkl', 'wb')
    # Pickle dictionary using protocol 0.
    pickle.dump(userLocDict, output)
    output.close()    