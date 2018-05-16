# -*- coding: utf-8 -*-
import glob
import os
import shutil
import subprocess
import time
import datetime
from time import gmtime
from subprocess import call
import numpy
import traceback

try:
    teqcfile = 'D:/gpsteqc/teqcstation.txt'
    station = numpy.genfromtxt(teqcfile,dtype='str').tolist()
    now = datetime.datetime.now()
    time1 = now - datetime.timedelta(hours=11)
    time2 = now - datetime.timedelta(hours=12)
    yy = time1.strftime("%Y")
    doy = time1.strftime("%j")
    doy2 = time2.strftime("%j")
    ymd = time1.strftime("%Y.%m.%d")
    ymd2 = time1.strftime("%Y%m%d")
    hr = int(time1.strftime("%H"))
    hr2 = int(time2.strftime("%H"))
    subprocess.call('net use Z: \\\\gpsnas1\\GPS /user:gps Gps1111@', shell=True)
    rnxpth = "Z://1Hz_GPS_Data//"+yy+"//"+ymd+"//"
    mypath = "D:/gpsteqc"
    movepath = "D:/gps"
    movepath2 = "D:/bei"
    for k in range(len(station)):
        tfile = rnxpth+station[k]+ymd2+str(hr).zfill(2)+'00s.T02'
        boo = os.path.isfile(tfile)
        if boo == True:
            shutil.copy(tfile,mypath)



    os.chdir("D:/gpsteqc")
    a = sorted(glob.glob("D:/gpsteqc/" + '*'+'00s.T02'))
    for k in a:
        subprocess.run(["D:/gpsteqc/runpkr00.exe","-g","-d",k])
        os.remove(k)
    aa = sorted(glob.glob("D:/gpsteqc/" + '*'+'00s.tgd'))

    for k in aa:
        subprocess.run("D:/gpsteqc/teqc.exe +relax +obs "+k[11:15]+doy+str(hr).zfill(2)+"b."+yy[2:4]+"o +nav -,-,-,-,"+k[11:15]+doy+str(hr).zfill(2)+"."+yy[2:4]+"b -R -E -G -J -S -O.obs L1L7C1C7 "+k)
        subprocess.run("D:/gpsteqc/teqc.exe +obs "+k[11:15]+doy+str(hr).zfill(2)+"."+yy[2:4]+"o +nav "+k[11:15]+doy+str(hr).zfill(2)+"."+yy[2:4]+"n -R -S -E -J -C -O.obs L1L2C1P2 "+k)
        os.remove(k)

    aaa = sorted(glob.glob("D:/gpsteqc/" + '*'+doy+str(hr).zfill(2)+'.18o'))
    for k in aaa:
        shutil.move(k,movepath)

    aaa = sorted(glob.glob("D:/gpsteqc/" + '*'+doy+str(hr).zfill(2)+'.18n'))
    for k in aaa:
        shutil.move(k,movepath)

    aaa = sorted(glob.glob("D:/gpsteqc/" + '*'+doy+str(hr).zfill(2)+'.18b'))
    for k in aaa:
        shutil.move(k,movepath2)

    aaa = sorted(glob.glob("D:/gpsteqc/" + '*'+doy+str(hr).zfill(2)+'b.18o'))
    for k in aaa:
        shutil.move(k,movepath2)


    os.chdir("D:/gps")
    aaaa = sorted(glob.glob("D:/gps/" + '*'+doy2+str(hr2).zfill(2)+'*'))
    for k in aaaa:
        os.remove(k)

    os.chdir("D:/bei")
    aaaa = sorted(glob.glob("D:/bei/" + '*'+doy2+str(hr2).zfill(2)+'*'))
    for k in aaaa:
        os.remove(k)

    os.chdir("D:/gpsteqc")
    aaaa = sorted(glob.glob("D:/gpsteqc/" + '*'+doy2+str(hr).zfill(2)+'*'))
    for k in aaaa:
        os.remove(k)
except:
    os.chdir("D:/gpsteqc")
    now = datetime.datetime.now()
    time1 = now - datetime.timedelta(hours=11)
    datatimenow = time1.strftime("%Y%m%d%H")
    log=open("errorlogcopyfile.txt",'a')
    traceback.print_exc(file=log)
    log.flush()
    log.write(datatimenow)
    log.close()
