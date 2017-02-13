# spark-submit --packages org.apache.spark:spark-streaming-kafka-0-8_2.11:2.1.0 user_spark_streaming.py

from elasticsearch import Elasticsearch


class ElasticsearchQueries():
    def  __init__(self):
        return None
    # insert/update document based on its presence in the index
    def gen_notification(self,latitude,longitude):
        es = Elasticsearch("http://elastic:changeme@xxxxxxx:9200")
        INDEX_NAME = 'healthlivetest'
        q = {}
        query = {}
        bool = {}
        must = {}
        match_all = {}
        filter = {}
        geo_distance = {}
        location = {}
        location['lat'] = latitude
        location['lon'] = longitude
        geo_distance['distance'] = "10km"
        geo_distance['location'] = location
        filter['geo_distance'] = geo_distance
        must['match_all'] = match_all
        bool['must'] = must
        bool['filter'] = filter
        query['bool'] = bool
        q['query'] = query

        res = es.search(index = INDEX_NAME, size=1000, body=q)
        countDict = {}
        countDict['Cold & Flu'],countDict['Diarrhea'],countDict['Bronchitis'],countDict['Swine Flu'],countDict['Asthma'],countDict['Conjunctivitis'],countDict['HIV/AIDS'],countDict['Cancer'],countDict['Heart Disease'],countDict['Malaria'],countDict['Hay Fever'],countDict['Tuberculosis'] = (0,)*12

        for i in res['hits']['hits']:
            countDict['Cold & Flu'] += i['_source']['Cold & Flu']
            countDict['Diarrhea'] += i['_source']['Diarrhea']
            countDict['Bronchitis'] += i['_source']['Bronchitis']
            countDict['Swine Flu'] += i['_source']['Swine Flu']
            countDict['Asthma'] += i['_source']['Asthma']
            countDict['Conjunctivitis'] += i['_source']['Conjunctivitis']
            countDict['HIV/AIDS'] += i['_source']['HIV/AIDS']
            countDict['Cancer'] += i['_source']['Cancer']
            countDict['Heart Disease'] += i['_source']['Heart Disease']
            countDict['Malaria'] += i['_source']['Malaria']
            countDict['Hay Fever'] += i['_source']['Hay Fever']
            countDict['Tuberculosis'] += i['_source']['Tuberculosis']

        result = []
        threshold = 100
        for key, value in countDict.iteritems():
            if value>threshold:
                result.append(key)
        return result
