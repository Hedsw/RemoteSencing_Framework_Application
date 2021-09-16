import os
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt
from datetime import date
from glob import glob

class API:
    def info():
        link = 'https://apihub.copernicus.eu/apihub'
        loginId = 'kannsky'
        password = 'dbsgur1004!'

        return SentinelAPI(loginId, password, link)
