import snappy
from snappy import ProductIO
from snappy import HashMap
import os, gc   
from snappy import GPF

#import sys
#sys.path.append('<snappy-dir>') 

GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
HashMap = snappy.jpy.get_type('java.util.HashMap')

path = "../"
for folder in os.listdir(path):
    gc.enable()   
    output = path + folder + "\\"  
    timestamp = folder.split("_")[4] 
    date = timestamp[:8]
    print(output, "  <--->  " ,data)

    sentinel_1 = ProductIO.readProduct(output + "\\S1B.SAFE")    
    print(sentinel_1)

    """
    pols = ['VH','VV'] 
    for p in pols:  
        polarization = p    
        
        ### CALIBRATION
        parameters = HashMap() 
        parameters.put('outputSigmaBand', True) 
        parameters.put('sourceBands', 'Intensity_' + polarization) 
        parameters.put('selectedPolarisations', polarization) 
        parameters.put('outputImageScaleInDb', False)  

        calib = output + date + "_calibrate_" + polarization 
        target_0 = GPF.createProduct("Calibration", parameters, sentinel_1) 
        ProductIO.writeProduct(target_0, calib, 'BEAM-DIMAP')
    """