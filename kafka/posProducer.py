import random
import sys
import six
import pickle
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer
from kafka import KafkaProducer
from datetime import datetime, timedelta
from faker import Faker
from faker.providers import BaseProvider

fake = Faker()

class DiseaseDrug(BaseProvider):

    diseaseDrugDict = {'Cold & Flu':['Benadryl','diphenhydramine','Coricidin HBP Cold & Flu','chlorpheniramine','Tylenol Cold','Banophen'],
                       'Diarrhea':['Lomotil','loperamide','Imodium','Anti-Diarrheal','Imodium A-D','Florastor','Kaopectate'],
                       'Bronchitis':['Azithromycin Dose Pack','Mucinex','Augmentin','Levaquin','Zithromax','doxycycline','Amoxil'],
                       'Swine Flu':['Tamiflu','Oseltamivir','Relenza','zanamivir','peramivir'],
                       'Asthma':['Singulair','Montelukast','Prednisone','Aerobid','Dulera','Atrovent'],
                       'Conjunctivitis':['Ophthalmic','Cromolyn','Cycloplegic','Natamycin','Phenylephrine'],
                       'HIV/AIDS':['Truvada','Atripla','Norvir','Isentress','Prezista','Stribild','Complera','Epzicom','Reyataz','Epivir'],
                       'Cancer':['Carboplatin','Adriamycin','Cytoxan','Adrucil','Etoposide','Paraplatin','Fluorouracil','Cosmegen'],
                       'Heart Disease':['Amiodarone','Disopyramide','Dofetilide','Mexiletine','Moricizine','Procainamide','Quinidine','Tocainide'],
                       'Malaria':['Antimalarial ','Atovaquone','Chloroquine','Hydroxychloroquine','Primaquine','Proguanil','Quinine'],
                       'Hay Fever':['Antihistamines','Ephedrine','Guaifenesin','Hydroxyzyne','Meclizine','Orphenadrine','Phenylephrine'],
                       'Tuberculosis':['Cycloserine','Ethionamide','Isoniazid','Rifamycins']
                      }

    def diseaseDrug(self):
        disease,drugList = random.choice(self.diseaseDrugDict.items())
        drug = random.choice(drugList)
        return disease,drug

# adding new provider drug to faker instance
fake.add_provider(DiseaseDrug)



class Producer(object):

    def __init__(self, addr):
        self.producer = KafkaProducer(bootstrap_servers=addr)

    def produce_msgs(self,source_symbol):

        start = '2017-01-10 09:48:49'
        timestamp = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        msg_cnt = 0
        pkl_file = open('pharmacyPickle.pkl', 'rb')
        pharmacyLocDict = pickle.load(pkl_file)
        pkl_file.close()
        while True:
            str_fmt = "{};{};{};{};{};{};{}"
            for i in range(0,10):
                pharmacy_field,(lat_field,lon_field ) = random.choice(pharmacyLocDict.items())
                timestamp_field = str(timestamp)
                disease,drug = fake.diseaseDrug()
                disease_field = str(disease)
                drug_field = str(drug)

                message_info = str_fmt.format(source_symbol,
                                              pharmacy_field,
                                              timestamp_field,
                                              drug_field,
                                              disease_field,
                                              lat_field,
                                              lon_field)
                print message_info
                self.producer.send('posTest',key=source_symbol,value=message_info)
                msg_cnt += 1
            timestamp += timedelta(seconds=1)


if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])+':9092'
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key)
