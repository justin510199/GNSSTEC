import numpy
import math
import statistics
import calendar

def readOfile(ofile):
    Ofile = open(ofile,'r')
    i=0
    for line in Ofile.readlines():
        i+=1
        if 'END OF HEADER' in line:
            break
    Ofile.close()
    Ofile = open(ofile,'r')
    lines = Ofile.readlines()
    alltimedata=[]
    LC=[]
    satLC=[]
    satnum = []
    moresatnum = []
    allsatnum=[]
    satcount=[]
    i-=1
    gg = i+1
    ccc=lines[gg].split(',')
    timefind = ccc[0][0:12]
    count = 0

    for linecount in lines:
        if timefind in linecount:
            count+=1
    for j in range(count):
        i+=1
        a=lines[i].split(',')
        sat=int(a[0][30:32])
        satcount.append(sat)
        if sat<13:
            for k in range(sat):
                i +=1
                data = lines[i].split(',')
                if len(data[0])!=63:
                    continue
                satnum.append(int(a[0][33+k*3:35+k*3]))
                LC.append(float(data[0][1:14]))
                LC.append(float(data[0][17:30]))
                LC.append(float(data[0][34:46]))
                LC.append(float(data[0][50:62]))
                satLC.append(LC)
                LC=[]
        if sat>=13:
            i+=1
            aa = lines[i].split(',')
            moresat = sat-12
            for g in range(moresat):
                moresatnum.append(int(aa[0][33+g*3:35+g*3]))
            for h in range(12):
                i +=1
                data = lines[i].split(',')
                if len(data[0])!=63:
                    continue
                satnum.append(int(a[0][33+h*3:35+h*3]))
                LC.append(float(data[0][1:14]))
                LC.append(float(data[0][17:30]))
                LC.append(float(data[0][34:46]))
                LC.append(float(data[0][50:62]))
                satLC.append(LC)
                LC=[]
            for h in range(moresat):
                i +=1
                data = lines[i].split(',')
                if len(data[0])!=63:
                    continue
                LC.append(float(data[0][1:14]))
                LC.append(float(data[0][17:30]))
                LC.append(float(data[0][34:46]))
                LC.append(float(data[0][50:62]))
                satLC.append(LC)
                LC=[]
                satnum.append(moresatnum[h])
        allsatnum.append(satnum)
        satnum = []
        moresatnum = []
        alltimedata.append(satLC)
        satLC = []
    Ofile.close()
    # satec & srtec
    B1 = 1575.42*10**6
    B2 = 1227.6*10**6
    m = B1/B2
    c = 2.998*10**8
    A = c*((B1**2*B2**2)/(B1**2-B2**2))/40.3
    B = -c*B2/40.3*(m**2/(m**2-1))
    sartecall=[]
    for d in range(count):
        sartecsat = []
        for s in range(len(alltimedata[d])):
            L1 = alltimedata[d][s][0]
            L2 = alltimedata[d][s][1]
            C1 = alltimedata[d][s][2]
            P2 = alltimedata[d][s][3]
            sartec=[]
            sartec.append(A*(P2-C1)/10**25)
            sartec.append(B*(L2-B2/B1*L1)/10**16)
            sartecsat.append(sartec)
        sartecall.append(sartecsat)
    #find all satellite
    temp=[]
    for d in range(count):
        temp.extend(allsatnum[d])
        allsatcount = list(set(temp))
    #Slant TEC calculation
    allSATEC = []
    for k in range(len(allsatcount)):
        c = allsatcount[k]
        Di=[]
        Pi=[]
        for d in range(count):
            if c in allsatnum[d]:
                q = allsatnum[d].index(c)
                Di.append(sartecall[d][q][0])
                Pi.append(sartecall[d][q][1])
        temp=list(map(lambda x: x[0]-x[1], zip(Di, Pi)))
        offset = sum(temp)/len(temp)
        SATEC = numpy.array([i+offset for i in Pi])
        aaaa = abs(SATEC)
        SATECmedian = abs(statistics.median(aaaa))     
        allSATEC.append(SATECmedian)
    return [allSATEC,allsatcount]

def readOfileb(ofile):
    Ofile = open(ofile,'r')
    i=0
    for line in Ofile.readlines():
        i+=1
        if 'END OF HEADER' in line:
            break
    Ofile.close()
    Ofile = open(ofile,'r')
    lines = Ofile.readlines()
    alltimedata=[]
    LC=[]
    satLC=[]
    satnum = []
    moresatnum = []
    allsatnum=[]
    satcount=[]
    i-=1
    gg = i+1
    ccc=lines[gg].split(',')
    timefind = ccc[0][0:12]
    count = 0

    for linecount in lines:
        if timefind in linecount:
            count+=1
    for j in range(count):
        i+=1
        a=lines[i].split(',')
        sat=int(a[0][30:32])
        satcount.append(sat)
        if sat<13:
            for k in range(sat):
                i +=1
                data = lines[i].split(',')
                if len(data[0])!=63:
                    continue
                if float(data[0][17:30]) < 1000000:
                    continue
                satnum.append(int(a[0][33+k*3:35+k*3]))
                LC.append(float(data[0][1:14]))
                LC.append(float(data[0][17:30]))
                LC.append(float(data[0][34:46]))
                LC.append(float(data[0][50:62]))
                satLC.append(LC)
                LC=[]
        if sat>=13:
            i+=1
            aa = lines[i].split(',')
            moresat = sat-12
            for g in range(moresat):
                moresatnum.append(int(aa[0][33+g*3:35+g*3]))
            for h in range(12):
                i +=1
                data = lines[i].split(',')
                if len(data[0])!=63:
                    continue
                if float(data[0][17:30]) < 1000000:
                    continue
                satnum.append(int(a[0][33+h*3:35+h*3]))
                LC.append(float(data[0][1:14]))
                LC.append(float(data[0][17:30]))
                LC.append(float(data[0][34:46]))
                LC.append(float(data[0][50:62]))
                satLC.append(LC)
                LC=[]
            for h in range(moresat):
                i +=1
                data = lines[i].split(',')
                if len(data[0])!=63:
                    continue
                if float(data[0][17:30]) < 1000000:
                    continue
                LC.append(float(data[0][1:14]))
                LC.append(float(data[0][17:30]))
                LC.append(float(data[0][34:46]))
                LC.append(float(data[0][50:62]))
                satLC.append(LC)
                LC=[]
                satnum.append(moresatnum[h])
        allsatnum.append(satnum)
        satnum = []
        moresatnum = []
        alltimedata.append(satLC)
        satLC = []
    Ofile.close()
    # satec & srtec
    B1 = 1561.089*10**6
    B2 = 1207.14*10**6
    m = B1/B2
    c = 2.998*10**8
    A = c*((B1**2*B2**2)/(B1**2-B2**2))/40.3
    B = -c*B2/40.3*(m**2/(m**2-1))
    sartecall=[]
    for d in range(count):
        sartecsat = []
        for s in range(len(alltimedata[d])):
            L1 = alltimedata[d][s][0]
            L2 = alltimedata[d][s][1]
            C1 = alltimedata[d][s][2]
            P2 = alltimedata[d][s][3]
            sartec=[]
            sartec.append(A*(P2-C1)/10**25)
            sartec.append(B*(L2-B2/B1*L1)/10**16)
            sartecsat.append(sartec)
        sartecall.append(sartecsat)
    #find all satellite
    temp=[]
    for d in range(count):
        temp.extend(allsatnum[d])
        allsatcount = list(set(temp))
    #Slant TEC calculation
    allSATEC = []
    for k in range(len(allsatcount)):
        c = allsatcount[k]
        Di=[]
        Pi=[]
        for d in range(count):
            if c in allsatnum[d]:
                q = allsatnum[d].index(c)
                Di.append(sartecall[d][q][0])
                Pi.append(sartecall[d][q][1])
        temp=list(map(lambda x: x[0]-x[1], zip(Di, Pi)))
        offset = sum(temp)/len(temp)
        SATEC = numpy.array([i+offset for i in Pi])
        aaaa = abs(SATEC)
        SATECmedian = abs(statistics.median(aaaa))     
        allSATEC.append(SATECmedian)
    return [allSATEC,allsatcount]



def recxyz(ofile):
    Ofile = open(ofile,'r')
    i=0
    for line in Ofile.readlines():
        i+=1
        if 'APPROX POSITION XYZ' in line:
            break
    Ofile.close()
    Ofile = open(ofile,'r')
    lines = Ofile.readlines()
    a=lines[i-1].split()
    recxyz=[float(a[0]),float(a[1]),float(a[2])]
    Ofile.close()
    return recxyz

def slantfunction(recxyz123,navixyz123):
    h1 = 450
    h2 = 200
    Re = 6371
    slantfun=[]
    eve=[]
    for k in range(len(navixyz123)):
        recxyz = numpy.array(recxyz123)
        navixyz = numpy.array(navixyz123[k])
        temp = navixyz - recxyz
        temp2 = recxyz[0]*temp[0]+recxyz[1]*temp[1]+recxyz[2]*temp[2]
        temp3 = math.sqrt(recxyz[0]**2+recxyz[1]**2+recxyz[2]**2)
        temp4 = math.sqrt(temp[0]**2+temp[1]**2+temp[2]**2)
        e = math.asin(temp2/(temp3*temp4))
        temp5 = math.sqrt(Re**2*(math.sin(e)**2)-Re**2+(Re+h1)**2)
        temp6 = math.sqrt(Re**2*(math.sin(e)**2)-Re**2+(Re+h2)**2)
        slantfun.append((temp5-temp6)/(h1-h2))
        eve.append(e)
    return [slantfun,eve]

def slantfunctionG(recxyz123,navixyz123,navidcb1,navidcb2):
    h1 = 450
    h2 = 200
    Re = 6371
    slantfun=[]
    eve=[]
    bias=[]
    for k in range(len(navixyz123)):
        recxyz = numpy.array(recxyz123)
        navixyz = numpy.array(navixyz123[k])
        temp = navixyz - recxyz
        temp2 = recxyz[0]*temp[0]+recxyz[1]*temp[1]+recxyz[2]*temp[2]
        temp3 = math.sqrt(recxyz[0]**2+recxyz[1]**2+recxyz[2]**2)
        temp4 = math.sqrt(temp[0]**2+temp[1]**2+temp[2]**2)
        e = math.asin(temp2/(temp3*temp4))
        temp5 = math.sqrt(Re**2*(math.sin(e)**2)-Re**2+(Re+h1)**2)
        temp6 = math.sqrt(Re**2*(math.sin(e)**2)-Re**2+(Re+h2)**2)
        slantfun.append((temp5-temp6)/(h1-h2))
        eve.append(e)
        bias.append(navidcb2[k]-navidcb1[k])
    return [slantfun,eve,bias]	

def vtecG(allSATEC,Se,bias):
    a = numpy.array(allSATEC)
    b = numpy.array(Se)
    c = numpy.array(bias)
    kkk = a/b+c
    return kkk

def vtec(allSATEC,Se,beibias):
    a = numpy.array(allSATEC)
    b = numpy.array(Se)
    c = numpy.array(beibias)
    jjj = a/b+c
    return jjj

def latlon(recxyz123,navixyz123,e):
    h1 = 450
    h2 = 200
    Re = 6371
    r= math.sqrt(recxyz123[0]**2+recxyz123[1]**2+recxyz123[2]**2)
    h = (h1+h2)/2
    latallsat=[]
    lonallsat=[]
    for k in range(len(navixyz123)):
        theta = math.acos(r/(r+h)*math.cos(e[k]))-math.pi/4
        I = math.sqrt(r**2+(r+h)**2-2*r*(r+h)*math.cos(theta))
        recxyz = numpy.array(recxyz123)
        navixyz = numpy.array(navixyz123[k])
        temp = navixyz - recxyz
        R = math.sqrt(temp[0]**2+temp[1]**2+temp[2]**2)
        X = recxyz[0]+I/R*temp[0]
        Y = recxyz[1]+I/R*temp[1]
        Z = recxyz[2]+I/R*temp[2]
        lon = math.atan2(Y,X)*180/math.pi
        lat = math.asin(Z/(r+h))*180/math.pi
        latallsat.append(lat)
        lonallsat.append(lon)
    return [latallsat,lonallsat]

def readNfileeve(nfile):
    Nfile = open(nfile,'r')
    g=0
    for line in Nfile.readlines():
        g+=1
        if 'END OF HEADER' in line:
            break
    Nfile.close()
    Nfile = open(nfile,'r')
    lines = Nfile.readlines()
    c = int((len(lines)-g)/8)
    i=g-1
    navisatfind=[]
    for k in range(c):
        i+=1
        a=lines[i].split(',')
        navisatfind.append(int(a[0][0:2]))
        for h in range(4):
            i+=1
        i+=1
        i+=2
    Nfile.close()
    aaa = list(set(navisatfind))
    aaa.sort(key=navisatfind.index)
    navi=[]
    navisat=[]
    hr=[]
    for m in range(len(aaa)):
        count = 0
        temp321=[]
        if aaa[m] < 10:
            strf = ' '+str(aaa[m])
        else:
            strf = str(aaa[m])
        
        for linef in lines:
            count +=1
            if strf in linef[0:2]:
                break
        count -=1
        a=lines[count].split(',')
        navisat.append(int(a[0][0:2]))
        hr.append(int(a[0][12:14]))
        for g in range(4):
            count+=1
            a=lines[count].split(',')
            temp321.append(float(a[0][3:18])*10**int(a[0][19:22]))
            temp321.append(float(a[0][22:37])*10**int(a[0][38:41]))
            temp321.append(float(a[0][41:56])*10**int(a[0][57:60]))
            temp321.append(float(a[0][60:75])*10**int(a[0][76:79]))
        count+=1
        a=lines[count].split(',')
        temp321.append(float(a[0][3:18])*10**int(a[0][19:22]))
        navi.append(temp321)

    u =3.986005*10**14
    OmegaE=7.292115167*10**(-5)
    navihr = int(nfile[14:16])
    navixyz = []

    for k in range(len(navisat)):
        v = hr[k] - navihr
        if v == 2:
            tk = -5400
        elif v == -22:
            tk = -5400
        else:
            tk = -1800   
        IODE = navi[k][0]
        Crs = navi[k][1]
        deltan = navi[k][2]
        M0 = navi[k][3]
        Cuc = navi[k][4]
        e = navi[k][5]
        Cus = navi[k][6]
        sqrta = navi[k][7]
        toe = navi[k][8]
        Cic = navi[k][9]
        Omega0 = navi[k][10]
        Cis = navi[k][11]
        i0 = navi[k][12]
        Crc = navi[k][13]
        w = navi[k][14]
        Omegadot = navi[k][15]
        IDOT = navi[k][16]
        aa = sqrta**2
        n1 = math.sqrt(u/aa**3)
        n = n1 + deltan
        Mk = M0 + n*tk
        Ek = Mk
        error = 1
        while error<0.00000000001:
            E0 = Ek
            Ek = Ek-(Ek-Mk-e*math.sin(Ek))/(1-e*math.cos(Ek))
            error = abs(Ek-E0)
        cosfk = (math.cos(Ek)-e)/(1-e*math.cos(Ek))
        sinfk = math.sqrt(1-e**2)*math.sin(Ek)/(1-e*math.cos(Ek))
        fk = math.atan2(sinfk,cosfk)
        Qk = w+fk
        uk = Qk+Cus*math.sin(2*Qk)+Cuc*math.cos(2*Qk)
        rk = aa*(1-e*math.cos(Ek))+Crs*math.sin(2*Qk)+Crc*math.cos(2*Qk)
        ik = i0+IDOT*tk+Cis*math.sin(2*Qk)+Cic*math.cos(2*Qk)
        Omegak = Omega0+(Omegadot-OmegaE)*tk-OmegaE*toe
        xk = rk*math.cos(uk)
        yk = rk*math.sin(uk)
        X = xk*math.cos(Omegak)-yk*math.cos(ik)*math.sin(Omegak)
        Y = xk*math.sin(Omegak)+yk*math.cos(ik)*math.cos(Omegak)
        Z = yk*math.sin(ik)
        tempxyz = [X,Y,Z]
        navixyz.append(tempxyz)
    return[navixyz,navisat]

def readNfileb(nfile):
    Nfile = open(nfile,'r')
    g=0
    for line in Nfile.readlines():
        g+=1
        if 'END OF HEADER' in line:
            break
    Nfile.close()
    Nfile = open(nfile,'r')
    lines = Nfile.readlines()
    c = int((len(lines)-g)/8)
    i=g-1
    navisatfind=[]
    for k in range(c):
        i+=1
        a=lines[i].split(',')
        navisatfind.append(int(a[0][0:2]))
        for h in range(4):
            i+=1
        i+=1
        i+=2
    Nfile.close()
    aaa = list(set(navisatfind))
    aaa.sort(key=navisatfind.index)
    navi=[]
    navisat=[]
    hr=[]
    for m in range(len(aaa)):
        count = 0
        temp321=[]
        if aaa[m] < 10:
            strf = ' '+str(aaa[m])
        else:
            strf = str(aaa[m])
        
        for linef in lines:
            count +=1
            if strf in linef[0:2]:
                break
        count -=1
        a=lines[count].split(',')
        navisat.append(int(a[0][0:2]))
        hr.append(int(a[0][12:14]))
        for g in range(4):
            count+=1
            a=lines[count].split(',')
            temp321.append(float(a[0][3:18])*10**int(a[0][19:22]))
            temp321.append(float(a[0][22:37])*10**int(a[0][38:41]))
            temp321.append(float(a[0][41:56])*10**int(a[0][57:60]))
            temp321.append(float(a[0][60:75])*10**int(a[0][76:79]))
        count+=1
        a=lines[count].split(',')
        temp321.append(float(a[0][3:18])*10**int(a[0][19:22]))
        navi.append(temp321)

    u =3.986005*10**14
    OmegaE=7.292115167*10**(-5)
    navihr = int(nfile[14:16])
    navixyz = []

    for k in range(len(navisat)):
        v = hr[k] - navihr
        if v == 0:
            tk = 1800
        elif v == -22:
            tk = 5400
        else:
            tk = -1800   
        IODE = navi[k][0]
        Crs = navi[k][1]
        deltan = navi[k][2]
        M0 = navi[k][3]
        Cuc = navi[k][4]
        e = navi[k][5]
        Cus = navi[k][6]
        sqrta = navi[k][7]
        toe = navi[k][8]
        Cic = navi[k][9]
        Omega0 = navi[k][10]
        Cis = navi[k][11]
        i0 = navi[k][12]
        Crc = navi[k][13]
        w = navi[k][14]
        Omegadot = navi[k][15]
        IDOT = navi[k][16]
        aa = sqrta**2
        n1 = math.sqrt(u/aa**3)
        n = n1 + deltan
        Mk = M0 + n*tk
        Ek = Mk
        error = 1
        while error<0.00000000001:
            E0 = Ek
            Ek = Ek-(Ek-Mk-e*math.sin(Ek))/(1-e*math.cos(Ek))
            error = abs(Ek-E0)
        cosfk = (math.cos(Ek)-e)/(1-e*math.cos(Ek))
        sinfk = math.sqrt(1-e**2)*math.sin(Ek)/(1-e*math.cos(Ek))
        fk = math.atan2(sinfk,cosfk)
        Qk = w+fk
        uk = Qk+Cus*math.sin(2*Qk)+Cuc*math.cos(2*Qk)
        rk = aa*(1-e*math.cos(Ek))+Crs*math.sin(2*Qk)+Crc*math.cos(2*Qk)
        ik = i0+IDOT*tk+Cis*math.sin(2*Qk)+Cic*math.cos(2*Qk)
        Omegak = Omega0+(Omegadot-OmegaE)*tk-OmegaE*toe
        xk = rk*math.cos(uk)
        yk = rk*math.sin(uk)
        X = xk*math.cos(Omegak)-yk*math.cos(ik)*math.sin(Omegak)
        Y = xk*math.sin(Omegak)+yk*math.cos(ik)*math.cos(Omegak)
        Z = yk*math.sin(ik)
        tempxyz = [X,Y,Z]
        navixyz.append(tempxyz)
    return[navixyz,navisat]

def remove3std(allvtec,alllat,alllon):

    for k in range(len(allvtec)):
        if allvtec[k] > 500:
            allvtec[k] = 1000
            alllat[k] = 1000
            alllon[k] = 1000
    aa=list(filter(lambda x: x<999,allvtec))
    bb=list(filter(lambda x: x<999,alllat))
    cc=list(filter(lambda x: x<999,alllon))
    std = statistics.stdev(aa)*5+statistics.mean(aa)
    for k in range(len(aa)):
        if aa[k] >=std:
            aa[k] = 1000
            bb[k] = 1000
            cc[k] = 1000
    
    a=list(filter(lambda x: x<999,aa))
    b=list(filter(lambda x: x<999,bb))
    c=list(filter(lambda x: x<999,cc))

    return[a,b,c]

def readNfileodd(nfile):
    Nfile = open(nfile,'r')
    g=0
    for line in Nfile.readlines():
        g+=1
        if 'END OF HEADER' in line:
            break
    Nfile.close()
    Nfile = open(nfile,'r')
    lines = Nfile.readlines()
    c = int((len(lines)-g)/8)
    i=g-1
    navisatfind=[]
    for k in range(c):
        i+=1
        a=lines[i].split(',')
        navisatfind.append(int(a[0][0:2]))
        for h in range(4):
            i+=1
        i+=1
        i+=2
    Nfile.close()
    aaa = list(set(navisatfind))
    aaa.sort(key=navisatfind.index)
    navi=[]
    navisat=[]
    hr=[]
    for m in range(len(aaa)):
        count = 0
        temp321=[]
        if aaa[m] < 10:
            strf = ' '+str(aaa[m])
        else:
            strf = str(aaa[m])
        
        for linef in lines:
            count +=1
            if strf in linef[0:2]:
                break
        count -=1
        a=lines[count].split(',')
        navisat.append(int(a[0][0:2]))
        hr.append(int(a[0][12:14]))
        for g in range(4):
            count+=1
            a=lines[count].split(',')
            temp321.append(float(a[0][3:18])*10**int(a[0][19:22]))
            temp321.append(float(a[0][22:37])*10**int(a[0][38:41]))
            temp321.append(float(a[0][41:56])*10**int(a[0][57:60]))
            temp321.append(float(a[0][60:75])*10**int(a[0][76:79]))
        count+=1
        a=lines[count].split(',')
        temp321.append(float(a[0][3:18])*10**int(a[0][19:22]))
        navi.append(temp321)

    u =3.986005*10**14
    OmegaE=7.292115167*10**(-5)
    navihr = int(nfile[14:16])
    navixyz = []

    for k in range(len(navisat)):
        v = hr[k] - navihr
        if v == 2:
            tk = -5400
        elif v == -22:
            tk = -5400
        else:
            tk = 1800   
        IODE = navi[k][0]
        Crs = navi[k][1]
        deltan = navi[k][2]
        M0 = navi[k][3]
        Cuc = navi[k][4]
        e = navi[k][5]
        Cus = navi[k][6]
        sqrta = navi[k][7]
        toe = navi[k][8]
        Cic = navi[k][9]
        Omega0 = navi[k][10]
        Cis = navi[k][11]
        i0 = navi[k][12]
        Crc = navi[k][13]
        w = navi[k][14]
        Omegadot = navi[k][15]
        IDOT = navi[k][16]
        aa = sqrta**2
        n1 = math.sqrt(u/aa**3)
        n = n1 + deltan
        Mk = M0 + n*tk
        Ek = Mk
        error = 1
        while error<0.00000000001:
            E0 = Ek
            Ek = Ek-(Ek-Mk-e*math.sin(Ek))/(1-e*math.cos(Ek))
            error = abs(Ek-E0)
        cosfk = (math.cos(Ek)-e)/(1-e*math.cos(Ek))
        sinfk = math.sqrt(1-e**2)*math.sin(Ek)/(1-e*math.cos(Ek))
        fk = math.atan2(sinfk,cosfk)
        Qk = w+fk
        uk = Qk+Cus*math.sin(2*Qk)+Cuc*math.cos(2*Qk)
        rk = aa*(1-e*math.cos(Ek))+Crs*math.sin(2*Qk)+Crc*math.cos(2*Qk)
        ik = i0+IDOT*tk+Cis*math.sin(2*Qk)+Cic*math.cos(2*Qk)
        Omegak = Omega0+(Omegadot-OmegaE)*tk-OmegaE*toe
        xk = rk*math.cos(uk)
        yk = rk*math.sin(uk)
        X = xk*math.cos(Omegak)-yk*math.cos(ik)*math.sin(Omegak)
        Y = xk*math.sin(Omegak)+yk*math.cos(ik)*math.cos(Omegak)
        Z = yk*math.sin(ik)
        tempxyz = [X,Y,Z]
        navixyz.append(tempxyz)
    return[navixyz,navisat]


def JulianDate_to_MMDDYYY(y,jd):
    month = 1
    day = 0
    while jd - calendar.monthrange(y,month)[1] > 0 and month <= 12:
        jd = jd - calendar.monthrange(y,month)[1]
        month = month + 1
    return [month,jd,y]







        


    
    
