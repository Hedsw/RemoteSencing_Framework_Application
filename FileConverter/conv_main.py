import sys,os,time,requests
from glob import glob
from flask import Flask, render_template, request
from converter import threadrunner as ThreadNC4
from converter import fileconvert_class

app = Flask(__name__, template_folder='../templates')
app.config["DEBUG"] = True

@app.route('/', methods=['GET'])
def main():
    return render_template('index.html')

class fileconverter:
    @app.route('/converter/tifftonc4', methods=['POST','GET'])
    def tiffconvtiff2nc4():
        # url_itmes는 GET이나 POST로 데이터 송수신할 때 사용 함. 
        # url_items = "http://localhost:5001/download/trmm_rt" 
        # # 이거 이렇게 하지말고, 유저가 각 마이크로서비스 쓸 수 있게 만들자. 버튼 만들고 이럴 것도 없이 그냥.. Python으로 부르면 바로 할 수 있도록.
        if request.method == 'POST':
            #response = requests.get(url_items)
            #print(response.text)
            print("NC4 Converter POST Method starts")    

            # This is CONVERTER WIHTOUT THREAD 
            os.system('rm -rf ../storage/nc4file/*1')
            lists = glob('../storage/nc4file/*.nc4')
            for i in range(len(lists)):
                tmp = lists[i]
                splited = tmp.split('/')
                #print(splited[-1], " Splited")
                filename = splited[-1].split('.')
                #print(filename[0], " File name")
                
                fileconvert_class.nc4converter(i, lists, filename[0])
                
            # THIS IS COVERTER WITH THREAD    
            # When we use Thread, our virtual machine's power is not enough to run large amount of thread again.    
            # ThreadNC4.threadstarter()
            
        
        # 다이렉트로 URL 쏘면 바로 여기로 온다. 
        elif request.method == 'GET':
            # response = requests.get(url_items)
            #print(response.text)
            print("NC4 Starter GET Method")    
            
            # This is CONVERTER WIHTOUT THREAD 
            os.system('rm -rf ../storage/nc4file/*1')
            lists = glob('../storage/nc4file/*.nc4')
            for i in range(len(lists)):
                tmp = lists[i]
                splited = tmp.split('/')
                #print(splited[-1], " Splited")
                filename = splited[-1].split('.')
                #print(filename[0], " File name")
                
                fileconvert_class.nc4converter(i, lists, filename[0])
                
                
            # THIS IS COVERTER WITH THREAD    
            # When we use Thread, our virtual machine's power is not enough to run larege amount of thread again.
            #ThreadNC4.threadstarter()
            
            #print("NC4 Starter GET Method")    
    
    
    
    
    
    
    @app.route('/converter/mergeIRnc4totif', methods=['POST','GET'])
    def mergedirconvtiff2nc4():
        # url_itmes는 GET이나 POST로 데이터 송수신할 때 사용 함. 
        # url_items = "http://localhost:5001/download/trmm_rt" 
        # # 이거 이렇게 하지말고, 유저가 각 마이크로서비스 쓸 수 있게 만들자. 버튼 만들고 이럴 것도 없이 그냥.. Python으로 부르면 바로 할 수 있도록.
        if request.method == 'POST':
            #response = requests.get(url_items)
            #print(response.text)
            print("NC4 Converter POST Method starts")    

            # This is CONVERTER WIHTOUT THREAD 
            os.system('rm -rf ../storage/nc4file/*1')
            lists = glob('../storage/nc4file/*.nc4')
            for i in range(len(lists)):   
                #fileconvert_class.nc4converter(i, lists)
                #print(lists[i])
                tmp = lists[i]
                print(tmp.split('/'))
                print(tmp, " Splited")
                fileconvert_class.nc4converter(i, lists, filename[0])
                
            # THIS IS COVERTER WITH THREAD    
            # When we use Thread, our virtual machine's power is not enough to run large amount of thread again.    
            # ThreadNC4.threadstarter()
            
        
        # 다이렉트로 URL 쏘면 바로 여기로 온다. 
        elif request.method == 'GET':
            # response = requests.get(url_items)
            #print(response.text)
            print("NC4 Starter GET Method")    
            
            # This is CONVERTER WIHTOUT THREAD 
            os.system('rm -rf ../storage/nc4file/*1')
            lists = glob('../storage/nc4file/*.nc4')
            for i in range(len(lists)):
                tmp = lists[i]
                splited = tmp.split('/')
                #print(splited[-1], " Splited")
                filename = splited[-1].split('.')
                #print(filename[0], " File name")
                
                fileconvert_class.nc4converter(i, lists, filename[0])

            # This is CONVERTER WIHT THREAD 
            # When we use Thread, our virtual machine's power is not enough to run larege amount of thread again.
            #ThreadNC4.threadstarter()
            
            #print("NC4 Starter GET Method")    

        return render_template('index.html')
#Convert Port Number

#class fileconverter():
#    def __init(self, downloadmethod, controlfile):
#        self.url_items = 
        
app.run(host='0.0.0.0', port=5002)

#1 Bash가 File Converter 5002
#2 Bash가 File Downloader 5001
