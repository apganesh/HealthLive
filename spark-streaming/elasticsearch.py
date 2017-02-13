from elasticsearch import Elasticsearch
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.streaming.kafka import KafkaUtils
import json,os
from datetime import datetime



# check if an index is present or not in elasticsearch, if not present create index and mapping
def check_create_index():
# connect to the elasticsearch instance
    es = Elasticsearch("http://elastic:changeme@xxxxxxx:9200")

    INDEX_NAME = 'healthlivetest'
    if es.indices.exists(INDEX_NAME):
        print("deleting index...")
        res = es.indices.delete(index = INDEX_NAME)

    os.system('curl -X PUT --user elastic:changeme xxxxxxx:9200/healthlivetest/')


    bb= """curl -X PUT --user elastic:changeme xxxxxxx:9200/healthlivetest/healthlivetest/_mapping -d '{
        "healthlivetest": {
            "properties": {
                "location": {
                    "type" : "geo_point"
                },
                "date": {
                    "type" : "date",
                    "doc_values" : true,
                    "format" : "yyyy-MM-dd HH:mm:ss.SSS"
                }
            }
        }
    }'
    """

    os.system(bb)

# insert/update document based on its presence in the index
def create_index(data):
    # connect to the elasticsearch instance
    es = Elasticsearch("http://elastic:changeme@xxxxxxx:9200")

    INDEX_NAME = 'healthlivetest'


    d = {}
    d['date'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
    d['pharmacyID'] = data[0][0]
    d['Disease'] = data[0][3]
    d['Cold & Flu'] = data[1] if data[0][3] == 'Cold & Flu' else 0
    d['Diarrhea'] = data[1] if data[0][3] == 'Diarrhea' else 0
    d['Bronchitis'] = data[1] if data[0][3] == 'Bronchitis' else 0
    d['Swine Flu'] = data[1] if data[0][3] == 'Swine Flu' else 0
    d['Asthma'] = data[1] if data[0][3] == 'Asthma' else 0
    d['Conjunctivitis'] = data[1] if data[0][3] == 'Conjunctivitis' else 0
    d['HIV/AIDS'] = data[1] if data[0][3] == 'HIV/AIDS' else 0
    d['Cancer'] = data[1] if data[0][3] == 'Cancer' else 0
    d['Heart Disease'] = data[1] if data[0][3] == 'Heart Disease' else 0
    d['Malaria'] = data[1] if data[0][3] == 'Malaria' else 0
    d['Hay Fever'] = data[1] if data[0][3] == 'Hay Fever' else 0
    d['Tuberculosis'] = data[1] if data[0][3] == 'Tuberculosis' else 0

    location = {}
    location['lat'] = data[0][1]
    location['lon'] = data[0][2]
    d['location'] = location

    # get the details about the document with id = pharmacyID
    res = es.get(index=INDEX_NAME, doc_type=INDEX_NAME, id=data[0][0], ignore=404)

    #if the document with id do not exist, create it
    if not res['found']:
        es.index(index=INDEX_NAME, doc_type=INDEX_NAME, id=data[0][0], body=d, refresh=True)
    else:
        #update the document
        disease = res['_source']['Disease']
        prevCount = res['_source'][disease]
        runningCount = prevCount + data[1]
        qq = {}
        doc = {}
        doc[disease] = runningCount
        qq['doc'] = doc
        es.update(index=INDEX_NAME, doc_type=INDEX_NAME,id=data[0][0], body=qq)

    return d

# create tuple of the format((timestamp, name, lat, lon), availability)
def parseStream(item):
    p = item.split(";")
    res = []
    res.append(((p[1],p[5],p[6],p[4]),1))
    return res

if __name__=='__main__':
    sc = SparkContext(appName="Pos_Spark-Streaming")
    ssc = StreamingContext(sc, 1)
    kafkaStream = KafkaUtils.createStream(ssc,"xxxxxx:2181", "spark-streaming-group", {"posTest": 1})
    posStream = kafkaStream.map(lambda x:x[1])
    posDataRDD = posStream.flatMap(lambda x: parseStream(x)).reduceByKey(lambda a,b: (int(a)+int(b)))
    es = Elasticsearch("http://xxxxxxx:9200")
    INDEX_NAME = 'healthlivetest'
    check_create_index()
    result = posDataRDD.map(lambda s: create_index(s))
    result.pprint()

    ssc.start()             # Start the computation
    ssc.awaitTermination()  # Wait for the computation to terminate
