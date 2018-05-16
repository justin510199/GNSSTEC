# -*- coding: utf-8 -*-
import Justintec
import scipy.io as sio
from mpl_toolkits.basemap import Basemap
import glob
import os
import shutil
import matplotlib.pyplot as plt
from subprocess import call
import numpy
import numpy as np
import traceback
import time
import datetime
try:
    allvtec=[]
    alllat = []
    alllon=[]
    ddccbb = sio.loadmat('dcbP1C1.mat')
    ddccbb2 = sio.loadmat('dcbP1P2.mat')
    dcb =ddccbb['dcb1'].flatten().tolist()
    dcb2 = ddccbb2['dcb2'].flatten().tolist()
    #GPS
    os.chdir("D:/gps")
    a = sorted(glob.glob("D:/gps/" + '*'+'.18*'))
    datanum = int(len(a)/2)
    if 3<=int(a[0][14:16])<=9:
        aaaaa = np.array([15.36,5.49,4.83,0.66,-0.1,4.2,4.07,2.3,-5.92,-6.15,-7.13,-5.82,-7.34,-4.44])*0.3+13.5
        beidcb = aaaaa.tolist()
    else:
        aaaaa = np.array([15.36,5.49,4.83,0.66,-0.1,4.2,4.07,2.3,-5.92,-6.15,-7.13,-5.82,-7.34,-4.44])*0.3+3
        beidcb = aaaaa.tolist()
    if int(a[0][14:16])%2 == 1:
        for k in range(datanum):
            nfile = a[2*k]
            ofile = a[2*k+1]
            recxyz123 = Justintec.recxyz(ofile)
            temp = Justintec.readOfile(ofile)
            temp2 = Justintec.readNfileeve(nfile)
            slanttec1 = temp[0]
            tecsat = temp[1]
            navisat = temp2[1]
            navixyz = temp2[0]
            navixyz123 =[]
            navidcb1 = []
            navidcb2 = []
            for g in range(len(tecsat)):
                if tecsat[g] in navisat:
                    c = navisat.index(tecsat[g])
                    navixyz123.append(navixyz[c])
                    navidcb1.append(dcb[tecsat[g]-1])
                    navidcb2.append(dcb2[tecsat[g]-1])
                if tecsat[g] not in navisat:
                    slanttec1[g] = 1000000000
            slanttec=list(filter(lambda x: x<999999999,slanttec1)) 
            Seall = Justintec.slantfunctionG(recxyz123,navixyz123,navidcb1,navidcb2)
            Se = Seall[0]
            e = Seall[1]
            bias = Seall[2]
            latlon = Justintec.latlon(recxyz123,navixyz123,e)
            vtecG = Justintec.vtecG(slanttec,Se,bias)
            allvtec.extend(vtecG)
            alllat.extend(latlon[0])
            alllon.extend(latlon[1])
    if int(a[0][14:16])%2 == 0:
        for k in range(datanum):
            nfile = a[2*k]
            ofile = a[2*k+1]
            recxyz123 = Justintec.recxyz(ofile)
            temp = Justintec.readOfile(ofile)
            temp2 = Justintec.readNfileodd(nfile)
            slanttec1 = temp[0]
            tecsat = temp[1]
            navisat = temp2[1]
            navixyz = temp2[0]
            navixyz123 =[]
            navidcb1 = []
            navidcb2 = []
            for g in range(len(tecsat)):
                if tecsat[g] in navisat:
                    c = navisat.index(tecsat[g])
                    navixyz123.append(navixyz[c])
                    navidcb1.append(dcb[tecsat[g]-1])
                    navidcb2.append(dcb2[tecsat[g]-1])
                if tecsat[g] not in navisat:
                    slanttec1[g] = 1000000000
            slanttec=list(filter(lambda x: x<999999999,slanttec1))        
            Seall = Justintec.slantfunctionG(recxyz123,navixyz123,navidcb1,navidcb2)
            Se = Seall[0]
            e = Seall[1]
            bias = Seall[2]
            latlon = Justintec.latlon(recxyz123,navixyz123,e)
            vtecG = Justintec.vtecG(slanttec,Se,bias)
            allvtec.extend(vtecG)
            alllat.extend(latlon[0])
            alllon.extend(latlon[1])

    #Beidou
    os.chdir("D:/bei")
    aa = sorted(glob.glob("D:/bei/" + '*'+'.18*'))
    datanum = int(len(aa)/2)
    for k in range(datanum):
        nfile = aa[2*k]
        ofile = aa[2*k+1]
        recxyz123 = Justintec.recxyz(ofile)
        temp = Justintec.readOfileb(ofile)
        temp2 = Justintec.readNfileb(nfile)
        slanttec1 = temp[0]
        tecsat = temp[1]
        navisat = temp2[1]
        navixyz = temp2[0]
        navixyz123 =[]
        beibias=[]
        for g in range(len(tecsat)):
            if tecsat[g] in navisat:
                c = navisat.index(tecsat[g])
                navixyz123.append(navixyz[c])
                beibias.append(beidcb[tecsat[g]-1])
            if tecsat[g] not in navisat:
                slanttec1[g] = 1000000000
        slanttec=list(filter(lambda x: x<999999999,slanttec1))
        Seall = Justintec.slantfunction(recxyz123,navixyz123)
        Se = Seall[0]
        e = Seall[1]
        latlon = Justintec.latlon(recxyz123,navixyz123,e)
        vtec = Justintec.vtec(slanttec,Se,beibias)
        allvtec.extend(vtec)
        alllat.extend(latlon[0])
        alllon.extend(latlon[1])

    tecplotall = Justintec.remove3std(allvtec,alllat,alllon)

    allvtecplot = tecplotall[0]
    alllatplot = tecplotall[1]
    alllonplot = tecplotall[2]


    os.chdir("D:/gpsteqc/newfigure")
    #coast = numpy.loadtxt('CoastXYTW.dat')
    #coastT = coast.T
    #loncoast = coastT[0]
    #latcoast = coastT[1]
    ut = a[0][14:16]
    day = int(a[0][11:14])
    year = int(a[0][17:19])+2000
    date = Justintec.JulianDate_to_MMDDYYY(year,day)
    titletime = str(date[2])+'-'+str(date[0])+'-'+str(date[1])+' UT '+ut+':30'
    figtime = str(date[2])+str(date[0]).zfill(2)+str(date[1]).zfill(2)+'UT'+ut+'30.png'

    fig = plt.figure()


    m = Basemap(llcrnrlon=111.,llcrnrlat=17.,urcrnrlon=132,urcrnrlat=30.,\
                rsphere=(6378137.00,6356752.3142),\
                resolution='l',area_thresh=1000.,projection='lcc',\
                lat_1=23.5,lon_0=121.)
    m.drawcoastlines()
    m.drawcountries()
    #m.drawmapboundary(fill_color='#99ffff')
    #m.fillcontinents(color='#cc9966',lake_color='#99ffff')
    m.drawparallels(np.arange(18,30,2),labels=[1,0,0,0])
    m.drawmeridians(np.arange(111,132,3),labels=[0,0,0,1])
    #m.drawparallels(np.arange(5,42,5),labels=[1,0,0,0])
    #m.drawmeridians(np.arange(100,143,5),labels=[0,0,0,1])
    cm = plt.cm.get_cmap('jet')
    x, y = m(alllonplot, alllatplot)
    plt.scatter(x, y, c=allvtecplot, s=6.5, cmap=cm, vmin=0, vmax=70)

    clb = plt.colorbar()
    clb.ax.set_title('TECu',fontsize=13)
    #plt.plot(loncoast, latcoast, 'k-', linewidth = 0.5)
    plt.title(titletime,fontsize=16)
    #plt.xlabel('Longitude',fontsize=14)
    #plt.ylabel('Latitude',fontsize=14)
    plt.savefig(figtime,dpi=500,format = 'png')
    if 0 <= int(ut) <= 9:
        webpath = "Y://GPS_tec_addbeidou//"
        shutil.copy(figtime,webpath)
except:
    os.chdir("D:/gpsteqc")
    now = datetime.datetime.now()
    time1 = now - datetime.timedelta(hours=11)
    datatimenow = time1.strftime("%Y%m%d%H")
    log=open("errorlogplotfiletest.txt",'a')
    traceback.print_exc(file=log)
    log.flush()
    log.write(datatimenow)
    log.close()
