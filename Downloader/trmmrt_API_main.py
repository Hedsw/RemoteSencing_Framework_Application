# Abstract Method
from abc import ABC, abstractmethod
import sys,os,time,requests
from xml.etree.ElementTree import parse
from flask import Flask, render_template, request
from downloader import threadcontroller_trmmRT
from downloader import threadcontroller_mergedIR 
from downloader import xmlcontroller
from downloader import downloadclass_nasa_trmm #여기에 import할 때는 클래스를 임포트 하는 것
from downloader import downloadclass_nasa_mergedir
from sentinel_1_downloader import sentinel1 
from sentinel_2_downloader import sentinel2 

app = Flask(__name__, template_folder='../templates') 
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')
# https://dev.to/takaakit/uml-diagram-for-gof-design-pattern-examples-in-python-4j40#strategy

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

class nasa_trmmRT_API():
    @app.route('/downloads/trmmRT', methods = ['GET', 'POST'], endpoint = 'downloadAPI_trmmRT')
    def downloadAPI_trmmRT():
        try:
            if request.method == 'POST':
                # Sub Class
                from_period = request.form['periodfrom']
                to_period = request.form['periodto']
                url = ""
                print(from_period, to_period, " Work?")
                context = Context(nasa_trmmRT_downloader())
                context.do_commonlogic_printInfo(from_period, to_period)
                signal = context.do_commonlogic_download(from_period, to_period, url)
                context.do_commonlogic_downloadstatuschecker(signal)
            else:
                print("GET")
                pass
        except OSError:
            print("OS ERORR. Check your AWS EC2 machine ")
        return render_template('index.html')

# https://www.gleek.io/blog/class-diagram-arrows.html
class nasa_trmmRT_downloader(AbstractDownloader):
    def download(self, from_period, to_period, url):
        try:
            months = []
            trmmsignal = False
            lists = request.form['lists']
            tmp1 = from_period.split('-')
            tmp2 = to_period.split('-')
            # year and month return
            yearfrom, monthfrom, yearto, monthto = tmp1[0], tmp1[1], tmp2[0], tmp2[1]
            
            if yearfrom == None or yearto == None:
                return "invalid Period"
            tree = parse('../XMLfiles/trmm_rt.xml')
            root = tree.getroot()
            trmm = root.findall("DATA")
            _listUrl = []
            for i in range(int(monthfrom), int(monthto)+1):
                # 0 - 238 case or 0 - 12 case have to separate
                url = [x.findtext("LINK") for x in trmm]
                url = url[0]
                if "3B42RT.7" in lists:
                    if i < 10:
                        j = "00" + str(i)
                        url = url + "/" + lists + "/" + yearfrom + "/" + j
                    else:
                        j = "0" + str(i)
                        url = url + "/" + lists + "/" + yearfrom + "/" + j            
                else:
                    if i < 10:
                        j = "0" + str(i)
                        url = url + "/" + lists + "/" + yearfrom + "/" + j
                    else:
                        url = url + "/" + lists + "/" + yearfrom + "/" + str(i)
                    
                if nasa_trmmRT_downloader.filelistcheckers(url):
                    _listUrl.append(url)
            print(yearfrom, monthfrom, yearto, monthto, url)
            # 테스트 용
            # 진짜 돌릴 때 아래 코드 
            #바로 아랫줄 돌리면 쓰레드 돌아간다
            #print(_listUrl, " Merged URL List")
            for url in _listUrl:
                downloadclass_nasa_trmm.download_trmm(url)
            #nasa_trmmRT_downloader.downloadstatuschecker(trmmsignal)
            
        except OSError:
            print("API someting problem during download method")
            
        return render_template('index.html')

    def filelistcheckers(url):
        if "3B42RT" in url:
            print(url + " 3B43RT exists")
            return True 
        elif "3B42RT.7" in url:
            print (url + "3B42RT.7")
            return True 
        elif "3B42RT_daily.007" in url:
            print (url + "3B42RT.7")
            return True 
        else:
            print("InValid File Type")
            return False

    #Overriding
    def printInfo(self, fromP, toP):
        if fromP == None or toP == None:
            return "invalid Period"
        tree = parse('../XMLfiles/trmm_rt.xml')
        root = tree.getroot()
        trmm = root.findall("DATA")
        link = [x.findtext("LINK") for x in trmm]
        print(link, " <-- Target URL")
        return link[0]
            
    #Overriding
    def downloadstatuschecker(self, signal):
        if signal == False:
            print("NASA TRMM RT Downloading is failure. Check Further procedure. 1. Check Thread is not broken. 2. Check URL is not broken.")
        else:
            print("NASA TRMM RT Downloading is successful")
        return signal 

    
    #Overriding    
    def dbinsert(self):
        pass    

# Here is Download Port Number
app.run(host='0.0.0.0', port=5002)   






       