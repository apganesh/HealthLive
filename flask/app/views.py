from flask import Flask, jsonify, redirect, render_template, request, url_for
from app import app
from utils.ElasticsearchQueries import ElasticsearchQueries

esQueries = ElasticsearchQueries()
'''
@app.route('/')
def index():
  return render_template("base.html")
'''
@app.route('/')
def realtime():
 return render_template("maps.html")

@app.route('/getDiseases')
def get_diseases():
    # /getDiseases?lat=123&lng=456
    lat = request.args.get('lat')
    lng = request.args.get('lng')    
    prevelant_diseases = esQueries.gen_notification(lat,lng)
    # Do stuff with your lat and lng here and populate the above array
    return ', '.join(prevelant_diseases)