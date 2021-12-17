# connect to the API
import os, collections
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from glob import glob
from xml.etree.ElementTree import parse
#from downloadmethod.sentinelAPI import API
from filechecker.zipreleaser import unzipper

class sentinel1:
    def sentinel_1(jsondirectory, from_period, to_period):
        filenames = []
        tree = parse('../XMLfiles/sentinel.xml')
        root = tree.getroot()
        getINFO = root.findall("DOWNLOAD")
        USERID = [x.findtext("USERID") for x in getINFO]
        PASSWORD = [x.findtext("PASSWORD") for x in getINFO]
        USERID = str(USERID[0])
        PASSWORD = str(PASSWORD[0])
        #print(type(USERID), type(PASSWORD) , " What is typed?")
        #print(USERID, PASSWORD)
        # barot, masterproject@201
        
        api = SentinelAPI(USERID, PASSWORD, "https://scihub.copernicus.eu/dhus/")
        # download single scene by known product id
        product_id = '22e7af63-07ad-4076-8541-f6655388dc5e'
        # This is to download directly through product_id
        # api.download(product_id)
        # search by polygon, time, and SciHub query keywords
        
        footprint = geojson_to_wkt(read_geojson(jsondirectory))
        periodFrom_TEST = "20190622"
        periodTo_TEST = "20190624"
        print("Footprint is done and searching files now.. ")
        tiles = ['35VMD', '35VLD', '35VLE']

        products = api.query(footprint,
                            #date = (periodFrom_TEST, periodTo_TEST), # We can choose specific date also.
                            date = ("NOW-5DAYS", "NOW"), # "NOW-XXDAYS", "NOW" -> download files from before 10 days to Now
                            platformname = 'Sentinel-1')
        
        if len(products) == 0:
            print("There is no files on the period and conditions")
        
        if len(products) > 4:
            print("CAN NOT DOWNLOAD OVER 4 FILE CONCURRENTLY So that only downloading top 4 sentinel files")
            print(type(products))
            #print(products)
            list_productID = []
            
            product1 = products.popitem()
            product2 = products.popitem()
            product3 = products.popitem()
            product4 = products.popitem()
            
            print(product1)
            
            list_productID.append(product1[0])
            list_productID.append(product2[0])
            list_productID.append(product3[0])
            list_productID.append(product4[0])

            
            for i in range(len(list_productID)):
                api.download(list_productID[i], "../storage/sentinelfiles/")
            
            #return False
        
        """
        HTTP status 403 Forbidden: User quota exceeded: MediaRegulationException : 
        An exception occured while creating a stream: Maximum number of 4 concurrent flows achieved by the user "kannsky"        
        """
        #products_df = api.to_dataframe(products)
        #products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
        #products_df_sorted = products_df_sorted.head(5)
        # API Reference -> download_all(products, directory_path=’.’, max_attempts=10, checksum=True, n_concurrent_dl=None, lta_retry_delay=None, fail_fast=False, nodefilter=None)
        
        
        #api.download_all(test2, "../storage/sentinelfiles/", 10, True, 4)
            
        """
        # convert to Pandas DataFrame
        products_df = api.to_dataframe(products)

        # sort and limit to first 5 sorted products
        products_df_sorted = products_df.sort_values(['cloudcoverpercentage', 'ingestiondate'], ascending=[True, True])
        products_df_sorted = products_df_sorted.head(5)

        # download sorted and reduced products
        api.download_all(products_df_sorted.index)
        """
        return True
    
# To extract files, use unzip()
    #unzip() 

'''
https://sentinelsat.readthedocs.io/en/v1.10/

'''