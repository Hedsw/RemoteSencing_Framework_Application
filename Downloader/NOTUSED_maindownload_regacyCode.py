import sys,os,time,requests
from flask import Flask, render_template, request
from trmmdownloader import threadcontroller 
from trmmdownloader import xmlcontroller
from trmmdownloader import trmmdownload
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

class classifier:
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
        pass

    @app.route('/download/trmm_rt', methods =['GET', 'POST'])
    def tr_rt_downloader():
        typechecker = classifier("wget", "trmm_rt.xml")
        #typechecker.nasafile()
        #print(typechecker.downloadmethod)
        #print(tr_rt_downloader().controlfile)
        url = xmlcontroller.xml_trmm_rt_file() #XMLFiles/trmm_rt 
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
                    
                    trmmsignal = trmmdownload.download(url)
                    #trmmsignal = True
                DownloadResult = {
                "sendtype": "POST",
                "FileDownloadType": "3B42RT.7",
                "Result": trmmsignal
                }        
                if trmmsignal == True:
                    #nc4convstarter()
                    #ㅇㅏ래꺼 실행시켜야한다.
                    response = requests.post("http://0.0.0.0:5002/converter/tifftonc4", data=DownloadResult)
                    print(response.text)
                else:
                    pass
            elif request.method == 'GET':
                pass
        except OSError:
            print("OS Error")
        return render_template('index.html')
    @app.route('/download/modis', methods =['GET', 'POST'])
    def Modis_downloader():
        pass


        
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
app.run(host='0.0.0.0', port=5001)   
          
    
        
import sys,os,time,requests
from flask import Flask, render_template, request
from trmmdownloader import threadcontroller 
from trmmdownloader import xmlcontroller
from trmmdownloader import trmmdownload
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

class classifier:
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
    @app.route('/download/modis', methods =['GET', 'POST'])
    def Modis_downloader():
        pass
    
    @app.route('/download/merged_ir', methods =['GET', 'POST'])
    def MergedIR_downloader():
        pass

    @app.route('/download/trmm_rt', methods =['GET', 'POST'])
    def tr_rt_downloader():
        typechecker = classifier("wget", "trmm_rt.xml")
        #typechecker.nasafile()
        #print(typechecker.downloadmethod)
        #print(tr_rt_downloader().controlfile)
        url = xmlcontroller.xml_trmm_rt_file() #XMLFiles/trmm_rt 
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
                    
                    trmmsignal = trmmdownload.download(url)
                    #trmmsignal = True
                DownloadResult = {
                "sendtype": "POST",
                "FileDownloadType": "3B42RT.7",
                "Result": trmmsignal
                }        
                if trmmsignal == True:
                    #nc4convstarter()
                    #ㅇㅏ래꺼 실행시켜야한다.
                    response = requests.post("http://0.0.0.0:5002/converter/tifftonc4", data=DownloadResult)
                    print(response.text)
                else:
                    pass
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
app.run(host='0.0.0.0', port=5001)   





"""
# Legacy Code
class parser: 
    # Parse date and month. Parsing will be used in TRMM_RT
    def parse_nasa(period1, period2):
        tmp = period1.split('-')
        tmp2 = period2.split('-')
        return tmp[0], tmp[1], tmp2[0], tmp2[1]
    def parse_sentinel(json):
        jsondir = "/home/ubuntu/RemoteSensing_v1/Downloader/sentinel_folder/" + json
        return jsondir
class parser: 
    # Parse date and month. Parsing will be used in TRMM_RT
    def parse_nasa(period1, period2):
        tmp = period1.split('-')
        tmp2 = period2.split('-')
        return tmp[0], tmp[1], tmp2[0], tmp2[1]
    def parse_sentinel(json):
        jsondir = "/home/ubuntu/RemoteSensing_v1/Downloader/sentinel_folder/" + json
        return jsondir

class nasafiledownloader(classifier):
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



class nasa_mergedIR_downloader(AbstractDownloader):
    @app.route('/download/mergedirTest', methods = ['GET', 'POST'], endpoint = 'downloadAPI_mergedIR')
    def downloadAPI_mergedIR():
        try:
            if request.method == 'POST':
                #print("Working?")
                period1 = request.form['periodfrom']
                period2 = request.form['periodto']
                lists = request.form['lists']
                if nasa_mergedIR_downloader.printInfo(period1, period2) is None:
                    print("Invalid URL")
                    return False
                yearfrom, monthfrom, yearto, monthto, url = nasa_mergedIR_downloader.parser(period1, period2)
                
                #print(yearfrom, monthfrom, yearto, monthto, url)
                # To Run download... 다운로드 돌리려면 아래꺼 실행..
                signal = downloadClass.download_mergedir(url, yearfrom, yearto, monthfrom, monthto)
                nasa_mergedIR_downloader.downloadstatuschecker(signal)
                
                #여기까지가 이제 URL을 가져온거고.. 그 다음부터는.. 뒤에 슬러쉬 슬러쉬 붙이면서 가야함.. 마지막에
                # URL 들어왔을 때. https://disc2.gesdisc.eosdis.nasa.gov/data/MERGED_IR/GPM_MERGIR.1/2008/347/merg_2008121200_4km-pixel.nc4
                # 이런식으로 들어온다 하면... 뒤에 부분 파싱 해야함. 2008이 있는지.. 01이 있는지..이런식으로 연, 달 별로 파싱 해서 다운로드 시작해야함
            else:  # GET 
                pass
        except OSError:
            print("OS Error")
        return render_template('index.html')
    
    #Overriding
    def parser(period1, period2):
        tmp1 = period1.split('-')
        tmp2 = period2.split('-')
        # year and month return
        yearfrom, monthfrom, yearto, monthto = tmp1[0], tmp1[1], tmp2[0], tmp2[1]
        url = nasa_mergedIR_downloader.printInfo(yearfrom, yearto) # XMLFiels/Merged_IR.xml
        yearcount = int(yearto) - int(yearfrom)

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
                print(url)
        return yearfrom, monthfrom, yearto, monthto, url
    
        #Overriding
    def printInfo(fromP, toP):
        if fromP == None or toP == None:
            print("invalid Period")
            return False
        tree = parse('../XMLfiles/merged_ir.xml')
        root = tree.getroot()
        merged_ir = root.findall("DATA")
        year = [x.findtext("YEAR") for x in merged_ir]
        
        # types = [x.findtext("TYPES") for x in trmm]
        # year = [x.findtext("START_YEAR") for x in trmm]
        #print(year)
        find_year_link = [x.findtext("LINK") for x in merged_ir]
        
        return find_year_link[0]
    
    def downloadstatuschecker(signal):
        if signal == False:
            print("Downloading is failure. Check Further procedure. 1. Check Thread is not broken. 2. Check URL is not broken.")
        else:
            print("Download is successful")
            
    
class copernicus_sentinel_2(AbstractDownloader):
    @app.route('/download/sentinel2', methods =['GET', 'POST'])
    def Sendtinel2_downloader():
        typechecker = classifier("API", "polygoninformation.geoson")
        print(typechecker.downloadmethod)
        polydir = parser.parse_sentinel("polygoninformation.geojson")
        # Polygon File should be used to get GPS address. API Query is used to set options liks platformname, date, cloudcoverpercentage
        if request.method == 'POST':
            sentinel2.sentinel_2(polydir)

        return render_template('index.html')    
    
    #Overriding
    def parser(json):
        if len(json) == 0:
            print(" No Json File")
            return       
        jsondir = "/home/ubuntu/RemoteSensing_v1/Downloader/sentinel_folder/" + json
        return jsondir
    
    #Overriding
    def downloadstatuschecker(signal):
        # TO DO: Sentinel 형식에 맞게 변경시켜야함 
        if signal == False:
            print("Downloading is failure. Check Further procedure. 1. Check Thread is not broken. 2. Check URL is not broken.")
        else:
            print("Download is successful")
            
    #Overriding
    def printInfo(fromP, toP):
        #TODO: 이거 날짜 두개 입력받아서, URl 출력하도록 만들어야함 URL은 XML 파일로 하는 것이 좋을듯.. 파싱해서 가져오는거지. mergedIR처럼

        pass 
"""        
    
        
