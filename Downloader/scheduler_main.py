# Abstract Method
from abc import ABC, abstractmethod
import sys,os,time,requests
from xml.etree.ElementTree import parse
from flask import Flask, render_template, request
"""
from downloader import threadcontroller_trmmRT
from downloader import threadcontroller_mergedIR 
from downloader import xmlcontroller
from downloader import downloadclass_nasa_trmm #여기에 import할 때는 클래스를 임포트 하는 것
from downloader import downloadclass_nasa_mergedir
from sentinel_1_downloader import sentinel1 
from sentinel_2_downloader import sentinel2 
"""
app = Flask(__name__, template_folder='../templates') 
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')
# https://dev.to/takaakit/uml-diagram-for-gof-design-pattern-examples-in-python-4j40#strategy
"""
class Context():
    #strategy: AbstractDownloader 
    def __init__(self, strategy):
        self._strategy = strategy
        
    #strategy: Strategy  ## the strategy interface
    def do_commonlogic_download(self, from_period, to_period, url):
        self._strategy.download(from_period, to_period, url)
        
    def do_commonlogic_printInfo(self, fromP, toP):
        print("URL, ID and Password are described in below")
        self._strategy.printInfo(fromP, toP) 
        print("Printinfo function is finished")
        #self._strategy.printInfo(fromP, toP)
        
    def do_commonlogic_downloadstatuschecker(self, signal):
        print("Download Status Checker is in processing.. ")
        self._strategy.downloadstatuschecker(signal)
        print("Download Status Checker is finished")

    def do_commonlogic_dbInsert(self):
        print("DB Insert function is in processing")
        self._strategy.dbinsert()
        print("DB Insert function is finished")
        
class AbstractDownloader(ABC):
    # 타입 체커 하나 더 넣으면 좋을듯.. 그리고... 마이크로서비스 하나 더 만들어서 총 3개 운영해야 함.. 하나는 어답터 나머지 두개는 다운로더, 컨버터 이렇게
    @abstractmethod
    def download(from_period, to_period, url):
        pass
    
    @abstractmethod
    def printInfo(fromP, toP):
        pass
    
    @abstractmethod
    def downloadstatuschecker(signal):
        pass
    
    @abstractmethod
    def dbinsert():
        pass
"""
class main_schedular_trmmRT():
    @app.route('/schedulars/trmmrt', methods = ['GET', 'POST'], endpoint = 'trmmrtschedular')
    def trmmrtschedular():
        try:
            if request.method == 'POST':
                # Downloader 
                downloadRT_response = requests.get("http://0.0.0.0/downloads/trmmRT")
                if downloadRT_response.status_code != 404 or downloadRT_response.status_code != 403:
                    return ("DOWNLOAD CONNECTION ERROR trmmRT")

                print("Download Success")

                # File Professor
                processorRT_response = request.get("http://0.0.0.0/processors/trmmRT")
                if processorRT_response.status_code != 404 or downloadRT_response.status_code != 403:
                    return ("PROCESSOR CONNECTION ERROR trmmRT")
            else:
                print("GET")
                pass
        except OSError:
            print("OS ERORR. Check your AWS EC2 machine")
        return render_template('index.html')

class main_schedular_sentinel1():
    @app.route('/schedulars/sentinel1', methods = ['GET', 'POST'], endpoint = 'sentinel1_schedular')
    def sentinel1_schedular():
        try:
            if request.method == 'POST':
                # Downloader 
                downloadSenti_response = requests.get("http://0.0.0.0/downloads/sentinel1")
                if downloadSenti_response.status_code != 404 or downloadSenti_response.status_code != 403:
                    return ("DOWNLOAD CONNECTION ERROR sentinel1")
                
                print("Download Success")
                
                # File Professor
                processorSenti_response = request.get("http://0.0.0.0/processors/sentinel1")
                if processorSenti_response.status_code != 404 or processorSenti_response.status_code != 403:
                    return ("PROCESSOR CONNECTION ERROR sentinel1 ")
            else:
                print("GET")
                pass
            
        except OSError:
            print("OS ERORR. Check your AWS EC2 machine ")
        return render_template('index.html')
    
# Here is Download Port Number
app.run(host='0.0.0.0', port=5002)   






       