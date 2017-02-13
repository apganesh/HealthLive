# bash spawn_kafka_streams.sh 172.31.1.4 1 new
import random
import sys
import six
import pickle
import time
from datetime import datetime
from kafka.client import SimpleClient
from kafka.producer import KeyedProducer
from kafka import KafkaProducer
from datetime import datetime, timedelta


class Producer(object):

    def __init__(self, addr):
        self.producer = KafkaProducer(bootstrap_servers=addr)

    def produce_msgs(self,source_symbol):

        start = '2017-01-10 09:55:49'
        timestamp = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")
        msg_cnt = 0
        pkl_file = open('userPickle.pkl', 'rb')
        userLocDict = pickle.load(pkl_file)
        pkl_file.close()
        while True:
            str_fmt = "{};{};{};{}"
            for i in range(0,100):
                user_field,(lat_field,lon_field ) = random.choice(userLocDict.items())
                timestamp_field = str(timestamp)
                message_info = str_fmt.format(source_symbol,
                                              user_field,                      
                                              lat_field,
                                              lon_field)
                print message_info
                self.producer.send('userTest',key=source_symbol,value=message_info)
                msg_cnt += 1
            time.sleep(1)
            timestamp += timedelta(seconds=1)


if __name__ == "__main__":
    args = sys.argv
    ip_addr = str(args[1])+':9092'
    partition_key = str(args[2])
    prod = Producer(ip_addr)
    prod.produce_msgs(partition_key)
