from abc import ABC, abstractmethod
import sys,os,time,requests
from glob import glob
from flask import Flask, render_template, request

app = Flask(__name__, template_folder='../templates')
app.config["DEBUG"] = True
    
class nasa_trmm_schedular():
    @app.route('/download/sentinel1', methods =['GET', 'POST'], endpoint = 'nasa_trmm_schedularAPI')
    def nasa_trmm_schedularAPI(self):
        print("TRMM Schedular")    

        #return 0
            
class nasa_mergedIR_schedular():
    @app.route('/download/sentinel1', methods =['GET', 'POST'], endpoint = 'nasa_mergedIR_schedularAPI')
    def nasa_mergedIR_schedularAPI(self):
        print("MergedIR Schedular")    

        #return 0

class copernicus_sentinel1_schedular():
    @app.route('/download/sentinel1', methods =['GET', 'POST'], endpoint = 'copernicus_sentinel1_schedularAPI')
    def copernicus_sentinel1_schedularAPI(self):
        print("Sentinel 1 Schedular")    

        #return 0    
    
class copernicus_sentinel2_schedular():
    @app.route('/download/sentinel1', methods =['GET', 'POST'], endpoint = 'copernicus_sentinel_2_schedularAPI')
    def copernicus_sentinel_2_schedularAPI(self):
        print("Sentinel 2 Schedular")    

        #return 0  

# Convert Port Number
app.run(host='0.0.0.0', port=5004)