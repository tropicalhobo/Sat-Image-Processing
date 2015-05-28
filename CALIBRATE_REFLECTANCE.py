import os
import gdal
from gdalconst import *
import numpy as np
import time
from math import pi, sin
import sys

def setcwd():
    
    cwd = os.getcwd()
    return cwd

def findDistance(cwd):
    fn = None
    workdir = os.listdir(cwd)
    for f in workdir:
        if 'EARTH-SUN_DISTANCE_AU.txt' in f:
            fn = f
        else:
            pass

    if fn == None:
        print 'Cannot find earth-sun distance txt file.'
        sys.exit(1)
    else:
        return fn

def findMTL(cwd):
    """Finds and metadata file and returns its name string."""
    listdir = os.listdir(cwd)
    fn = None
    for f in listdir:
        if '_MTL.txt' in f:
            fn = f

    if fn == None:
        print 'Cannot find metadata file.'
        sys.exit(1)
    else:
        return fn

def calibrateReflectance(cwd,dist,sunElev):
    caList = [] 
    eSun = {1:1997,2:1812,3:1533,4:1039,5:230.8,7:84.90,8:1362}
    dist = findDistance(cwd)
    
    for i in workspace:
        #ignore thermal bands for all Landsats
        if 'B10_RADIANCE' in i:
            pass
        elif 'B11_RADIANCE' in i:
            pass
        elif 'VCID_1_RADIANCE' in i:
            pass
        elif 'VCID_2_RADIANCE' in i:
            pass
        elif 'B6_RADIANCE' in i:
            pass
        elif 'RADIANCE' in i:
            caList.append(i)

    for j,k in zip(caList,sorted(eSun)): 
        ds = gdal.Open(j, GA_ReadOnly)
        cols, rows = ds.RasterXSize, ds.RasterYSize
        geotrans, proj = ds.GetGeoTransform(), ds.GetProjection()
        driver = ds.GetDriver()

        data = ds.ReadAsArray(0,0,cols,rows)
        print j, eSun[k]
        reflectance = (pi*data*dist**2)/(eSun[k]*sin(sunElev))

        output = driver.Create(modifyName(j),cols,rows,1,GDT_Float32)
        band = output.GetRasterBand(1)
        band.WriteArray(reflectance)
        band.FlushCache()
        ds = None
        output = None
        band = None
       
def earthSunDist(txtfile, doy):
    txt = open(txtfile,'r')
    distance = 0
    for i in txt:
        if doy in i:
            line = i.strip().split('\t')
            distance = float(line[1])
        else:
            'Cannot find date of year.'
    return distance
    
def retrieveDOY(fN):
    s = fN.strip().split('_')
    return s[0][13:16]
               
def collectSunElev(f):
    txt = open(f, 'r')
    for i in txt:
        if 'SUN_ELEVATION' in i:
            value = i.strip().split('=')
            return (pi/180)*float(value[1])
        else:
            pass
    close.txt()
    
def modifyName(nom):
    """Returns modified input file name string."""
    fn = nom.strip().split('_RADIANCE.TIF')
    return fn[0]+'_REFLECTANCE.TIF'
              
def main():
    start = time.time()

    wSpace = os.listdir('C:\\Users\\G Torres\\Desktop\\GEOG 213 DATA PROCESSING\\1995292')
    mtl = 'LT51140531995292CLT00_MTL.txt'
    ersun = 'EARTH-SUN_DISTANCE_AU.txt'
    sunElevation = collectSunElev(mtl)
    doy = retrieveDOY(mtl)
    distance = earthSunDist(ersun, doy)
    print 'Sun elevation: %s\nDay of year: %s\nDistance: %s' % (
        sunElevation, doy, distance)
    calibrateReflectance(wSpace,distance,sunElevation)
 
    print 'Script run time: %f' % (time.time()-start)
    
if __name__=='__main__':
    main()