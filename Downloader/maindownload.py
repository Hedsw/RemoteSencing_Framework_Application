import sys,os,time,requests
from flask import Flask, render_template, request
from downloader import threadcontroller 
from downloader import xmlcontroller
from downloader import downloadClass #여기에 import할 때는 클래스를 임포트 하는 것
#from downloader import mergedirdownload # Merged IR Parsing
from sentinel_1_downloader import sentinel1 
from sentinel_2_downloader import sentinel2 

app = Flask(__name__, template_folder='../templates') 
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

# Bring URL information from XML 
# TRMM_RT Downloader

"""
No meaning on __init__ function. The method is to classify download type and related files. 
"""


# Classifier Abstract Compnent -> Nasa filedownloader (This are concrete components)
#                             -> Sentinel Downlaoder 


class classifier: # why this called to classifier
    def __init__(self, downloadmethod, controlfile):
        self.downloadmethod = "wget"
        self.controlfile = "xml"
    def nasafile(self, methodcheck):
        if methodcheck == "GET" or methodcheck == "POST":
            return True
        else: 
            return False 
        pass
    def sentinelfile(self, downloadmethod, controlfile):
        self.downloadmethod = downloadmethod
        self.controlfile = controlfile
        pass
    def typecheckprinter(self):
        print(self.downlaodmethod, self.controlfile)    
    

class nasafiledownloader(classifier):       
    @app.route('/download/merged_ir', methods =['GET', 'POST'])
    def MergedIR_downloader():
        typechecker = classifier("wget", 'merged_ir.xml')
        #year_test = '1998'
        if typechecker.nasafile(request.method) == False:
            print("Reqest Method is wrong")
        
        try:
            if request.method == 'POST':
                period = request.form['periodfrom']
                period1 = request.form['periodto']
                lists = request.form['lists']
                yearfrom, monthfrom, yearto, monthto = parser.parse_nasa(period, period1)
                url = xmlcontroller.xml_merged_ir_file(yearfrom, yearto) # XMLFiels/Merged_IR.xml
                
                yearcount = int(yearto) - int(yearfrom)
                #print(yearcount, " Year Count")
                # 1998 + yearcount + 1 
                for i in range(0, yearcount+1):
                    for j in range(1, 2):
                        url = xmlcontroller.xml_merged_ir_file(yearfrom, yearto)
                        url = str(url)
                        tmp_year = int(yearfrom) + i
                         
                        if j < 10: # 0 ~ 9
                            j = "00" + str(j)
                            url += str(tmp_year) + "/" + str(j)
                        elif j > 9 and j < 100: # 10 ~ 99
                            j = "0" + str(j)
                            url += str(tmp_year) + "/" + str(j)

                        #print(url)
                        mergedIRsignal = downloadClass.download_mergedir(url, yearfrom, yearto, monthfrom, monthto)

                #print(yearfrom, monthfrom, yearto, monthto)
                
                #여기까지가 이제 URL을 가져온거고.. 그 다음부터는.. 뒤에 슬러쉬 슬러쉬 붙이면서 가야함.. 마지막에
                # URL 들어왔을 때. https://disc2.gesdisc.eosdis.nasa.gov/data/MERGED_IR/GPM_MERGIR.1/2008/347/merg_2008121200_4km-pixel.nc4
                # 이런식으로 들어온다 하면... 뒤에 부분 파싱 해야함. 2008이 있는지.. 01이 있는지..이런식으로 연, 달 별로 파싱 해서 다운로드 시작해야함
        except OSError:
            print("OS Error")

        return render_template('index.html')

    
    @app.route('/download/modis', methods =['GET', 'POST'])
    def Modis_downloader():
        pass

    @app.route('/download/trmm_rt', methods =['GET', 'POST'])
    def tr_rt_downloader():
        typechecker = classifier("wget", "trmm_rt.xml")
        #typechecker.nasafile()
        #print(typechecker.downloadmethod)
        #print(tr_rt_downloader().controlfile)
        url = xmlcontroller.xml_trmm_rt_file() # XMLFiles/trmm_rt 
        if typechecker.nasafile(request.method) == False:
            print("Request Method is wrong")
            
        try: 
            if request.method == 'POST':
                period = request.form['periodfrom']
                period1 = request.form['periodto']
                lists = request.form['lists']
                yearfrom, monthfrom, yearto, monthto = parser.parse_nasa(period, period1)
                #print(yearfrom, monthfrom, yearto, monthto)
                #url = url + "/" + lists + "/" + yearfrom + "/" + monthfrom
                months = []
                trmmsignal = False
                for i in range(int(monthfrom), int(monthto)+1):
                    url = xmlcontroller.xml_trmm_rt_file()
                    # 0 - 238 case or 0 - 12 case have to separate
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
                        
                    if "3B42RT" in url:
                        print(url + " 3B43RT exists")
                    print(url + "3B43RT is done ")
                    
                    trmmsignal = downloadClass.download_trmm(url)
                    #trmmsignal = True
                DownloadResult = {
                "sendtype": "POST",
                "FileDownloadType": "3B42RT.7",
                "Result": trmmsignal
                }        
                #if trmmsignal == True:
                    #nc4convstarter()
                    #ㅇㅏ래꺼 실행시켜야한다.
                    #response = requests.post("http://0.0.0.0:5002/converter/tifftonc4", data=DownloadResult)
                    #print(response.text)
                #else:
                #    pass
            elif request.method == 'GET':
                pass
        except OSError:
            print("OS Error")
            
        return render_template('index.html')
        
class sentineldownloader(classifier):
    def __init__(self, downloadmethod, controlfile):
        self.downloadmethod = "API"
        self.controlfile = "json"
         
    @app.route('/download/sentinel1', methods =['GET', 'POST'])
    def Sendtinel1_downloader():
        typechecker = classifier("API", "polygoninformation.json")
        print(typechecker.downloadmethod)
        polydir = parser.parse_sentinel("polygoninformation.json")
        # Polygon File should be used to get GPS address. API Query is used to set options liks platformname, date, cloudcoverpercentage
        if request.method == 'POST':
            sentinel_1(polydir)

        return render_template('index.html')
    
    @app.route('/download/sentinel2', methods =['GET', 'POST'])
    def Sendtinel2_downloader():
        typechecker = classifier("API", "polygoninformation.json")
        print(typechecker.downloadmethod)
        polydir = parser.parse_sentinel("polygoninformation.json")
        # Polygon File should be used to get GPS address. API Query is used to set options liks platformname, date, cloudcoverpercentage
        if request.method == 'POST':
            sentinel_1(polydir)

        return render_template('index.html')
    
class parser: 
    # Parse date and month. Parsing will be used in TRMM_RT
    def parse_nasa(period1, period2):
        tmp = period1.split('-')
        tmp2 = period2.split('-')
        # year and month return
        #print(tmp[0],tmp[1])
        return tmp[0], tmp[1], tmp2[0], tmp2[1]
    def parse_sentinel(json):
        jsondir = "/home/ubuntu/RemoteSensing_v1/Downloader/sentinel_folder/" + json
        return jsondir

# Here is Download Port Number
app.run(host='0.0.0.0', port=5004)   

