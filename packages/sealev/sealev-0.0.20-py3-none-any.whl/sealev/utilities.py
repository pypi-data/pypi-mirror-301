#from dashImport import printLog
#import bs4 as bs
#import BeautifulSoup4 as bs
# per farlo prendere in requirements bs4==0.0.1
#import base64
import xml.etree.ElementTree as ET
#from dashImport import app,html,dcc, dire0
import json,platform
import requests
from urllib.request import urlopen
#from plotly.subplots import make_subplots
#import plotly.graph_objects as go
from datetime import datetime,timedelta
#import numpy as np
#import uuid
import time,os
from math import radians, cos, sin, asin, sqrt
#import pyproj
#import numpy as np
#import pandas as pd
#from pyproj import Proj, transform, CRS, Transformer
from io import StringIO
from urllib.parse import urlparse, parse_qs, urlencode
#
#image_filename = 'data'+os.sep+'gdacs.png'
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#gdacsImg=html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'width':'40px'})

#image_filename = 'data'+os.sep+'noaa.png'
#encoded_image = base64.b64encode(open(image_filename, 'rb').read())
#noaaImg=html.Img(src='data:image/png;base64,{}'.format(encoded_image.decode()),style={'width':'40px'})

dire0=''

def getInfo(title,size='20px',link=''):
    image_filename = 'data'+os.sep+'infoSign1.png'
    encoded_image = base64.b64encode(open(image_filename, 'rb').read())
    img='data:image/png;base64,{}'.format(encoded_image.decode())
    infoImg=html.A(html.Img(src=img,style={'width':size}, title=title),href=link, target='_new')
    return infoImg

def fileage_days(fname):
    x=os.stat(fname)
    secs=(time.time()-x.st_mtime) 
    days=secs/3600/24
    return days


def  tds(w='',fontStyle='',fontSize='',bgcol='',fbol='',fontColor=''):
    if w=='':
        tds={'padding':'2 px'}
    else:
        tds={'padding':'2px','width':format(w)+'px'}
    if bgcol !='':
        tds['backgroundColor']=bgcol
    if fontStyle !='':
        tds['font-style']=fontStyle
    if fontSize!='':
       tds['font-size']=format(fontSize)+'px'
    if fbol!='':
       tds['font-weight']=fbol
    if fontColor!='':
       tds['color']=format(fontColor)
    
    return tds

def downloadFile(url, usecacheIfPresent=False, useget=False,cacheDir='cache',ageMax=1e9):
    if not os.path.exists('data'):
        os.mkdir('data')
    if not os.path.exists('data'+os.sep+cacheDir):
        os.mkdir('data'+os.sep+cacheDir)
    fname=url.replace(':','_')
    fname=fname.replace('/','_')
    fname=fname.replace('&','_')
    fname=fname.replace('?','_')
    fname=fname.replace('=','_')
    fname='data'+os.sep+cacheDir+os.sep+fname
    #if platform.system() == 'Windows':fGIG
    #    usecacheIfPresent=True
    if os.path.exists(fname):
        age=fileage_days(fname)
    else:
        age=1e10
    if os.path.exists(fname) and usecacheIfPresent and age<ageMax: # usecacheIfPresent:
        #print('using cache ',fname)
        with open(fname,'r', errors='ignore',encoding='utf-8') as f:
            resp=f.read()
    else:
        try:
            if useget:
                    resp=requests.get(url,verify=False)
                    resp=resp.text
            else:
                #resp=urlopen(url)
                #resp = resp.read().decode("utf-8")
                print(url)
                try:
                    with urlopen(url) as response:
                        resp = response.read().decode("utf-8")
                except Exception as e:
                    import pycurl
                    from io import BytesIO

                    c=pycurl.Curl()
                    c.setopt(pycurl.URL,url)
                    c.setopt(pycurl.SSL_VERIFYPEER, 0)   
                    c.setopt(pycurl.SSL_VERIFYHOST, 0)    
                    buffer=BytesIO() #StringIO()
                    c.setopt(c.WRITEDATA,buffer)
                    c.perform()
                    resp =buffer.getvalue().decode()
        except:
            return ''
        if usecacheIfPresent:
            with open(fname,'w',encoding='utf-8') as f:
                f.write(resp)
    return resp

def getListDevicesbyDBs():
    listDB=getList('DB')
    data={}
    for elem in listDB:
        db=elem['value']
        #print('getListDevicesbyDBs: ',db)
        data[db ]=getListDevices(db)
    return data

def getListNOA(testo,baseURL):
    if testo=='':
        return []
    trs=testo.split("<table class='defTable'>")[1].split('<tr>')
    list=[]
    for sens in trs[2:]:
        p=sens.split('>')
        ID=p[1].split('<')[0]
        name=p[4].split('<')[0] 
        lat=p[9].split('<')[0]
        lon=p[11].split('<')[0]
        location=p[13].split('<')[0]
        country=p[15].split('<')[0].split('(')[0]        
        link=baseURL+'/Default.aspx?mode=txt&ID='+ID
        list.append((ID,name,lon,lat,location,link,country))
    return list


def getListNOA_combo(data, extended=False):
    list=[]
    for elem0 in data:
        ID,name,lon,lat,location,link,country=elem0
        elem={'label':location+', '+name,'value':ID}
        
        if extended:
            elem['lon']=float(lon)
            elem['lat']=float(lat)
            elem['location']=location
            elem['deviceID']=name
            elem['country']=country
            elem['link']=link
        list.append(elem)
    return list

def getListDevices(URLtype,latestData='False'):
    latency=2880
    url=''
    if URLtype=='GLOSS @vliz':
        url = "http://www.vliz.be/sls/service.php?query=stationlist&format=json"
    elif URLtype=='SeaLevelDB':
        url="https://webcritech.jrc.ec.europa.eu/worldsealevelinterface/?list=true&format=txt"
    elif URLtype=='JRC_TAD':
        url='https://webcritech.jrc.ec.europa.eu/TAD_Server/api/Groups/GetGeoJSON?test=false&includeLatestData='+latestData
    elif URLtype=='NOA_TAD':
        #url='http://83.212.99.53/tad_server//api/Groups/GetGeoJSON?group=&maxLatency='+format(latency)+'&test=false'
        url='http://83.212.99.53/TAD_Server'
        url='http://antares.gein.noa.gr/tad_server'
        resp=downloadFile(url,True,ageMax=30)
        return getListNOA(resp,url)
    elif URLtype=='ISPRA_TAD':
        url='https://tsunami.isprambiente.it/Tad_Server//api/Groups/GetGeoJSON?group=&maxLatency='+format(latency)+'&test=false'
    elif URLtype=='NOAA TC':
        url='https://tidesandcurrents.noaa.gov/mdapi/latest/webapi/stations.json?type=1minute&expand=sensors'
    elif URLtype=='DART':
        url='https://www.ndbc.noaa.gov/kml/marineobs_as_kml.php?sort=pgm'        
        return getListDART(url)
    elif URLtype=='BIG':
        url='https://srgi.big.go.id/api/pasut/stations'
        #return getListBIG(url)
    elif URLtype=='INCOIS':
        urlList=[('https://tsunami.incois.gov.in/itews/homexmls/TideStations.xml','Tidal Gauges'),('https://tsunami.incois.gov.in/itews/homexmls/BprStations.xml?currentTime=1668750632823','Tsunami Buoys')]
        return getListINCOIS(urlList)
    if url=='':
        return ''
    else:
        #print(url)
        dataJson = downloadFile(url,True,False,'cache',30)
        if dataJson=='':
           dataJson = downloadFile(url,False,False,'cache',30)
           if dataJson=='':
                return []
        #print('imported devices names ',URLtype)
#        data=json.loads(dataJson)
        data=json.loads(dataJson)
        #printLog(data)
        return data

def extractXML(testo,tag):
    if tag in testo:
        res=testo.split('<'+tag+'>')[1].split('</'+tag+'>')[0]
    else:
        res=''
    return res

def creation_date(path_to_file):
    """
    Try to get the date that a file was created, falling back to when it was
    last modified if that isn't possible.
    See http://stackoverflow.com/a/39501288/1709587 for explanation.
    """
    if platform.system() == 'Windows':
        from pathlib import Path
        p = Path("path_to_file").resolve()
        #printLog(p)
        #printLog('path_to_file ',path_to_file,os.path.getctime(path_to_file),datetime.datetime.fromtimestamp(os.path.getctime(path_to_file)))
        return datetime.fromtimestamp(os.path.getmtime(path_to_file))
    else:
        stat = os.stat(path_to_file)
        try:
            return datetime.fromtimestamp(stat.st_birthtime)
        except AttributeError:
            # We're probably on Linux. No easy way to get creation dates here,
            # so we'll settle for when its content was last modified.
            return datetime.fromtimestamp(stat.st_mtime)
def elapsedHours(d1):
    now=datetime.now()
    #printLog(d1,now)
    age=(now-d1).days*24+(now-d1).seconds/3600
    #printLog(age)
    return int(age)

def getListBIG(stations, extended=False):
    #resp=downloadFile(url,True,True,'cacheMeas')
    #stations=json.loads(resp)
    list=[]
    for sta in stations['features']:
        lon,lat=sta['geometry']['coordinates']
        IDstation=sta['properties']['KODE_STS']
        location=sta['properties']['NAMA_STS']
        elem={'label':location,'value':IDstation}
        if extended:
            elem['deviceID']=IDstation
            elem['lon']=lon
            elem['lat']=lat
            elem['country']='Indonesia'
            elem['location']=location
        list.append(elem)
    list=sorted(list, key=lambda i: i['label'])
    return list

def getListINCOIS(urlList):
    list=[]
#    return list
    for url,group in urlList:
        try:
            xmlstr=downloadFile(url,True)
            if xmlstr=='':
                return list
            root=ET.fromstring(xmlstr)
            stations=root.findall('station')
            for station in stations:
                lat=float(station.findall('latitude')[0].text)
                lon=float(station.findall('longitude')[0].text)
                rep=station.findall('date')[0].text
                latency=0
                if rep=='Not Reporting': latency=1e6
                country=station.findall('country')[0].text
                owner=station.findall('owner')[0].text            
                location=station.findall('statrealName')[0].text
                ID=location.upper()
                list.append([ID,location,lat,lon,latency,country,owner,group])
        except Exception as ex:
            print('error reading INCOIS',ex)
    return list

def getListINCOIS_combo(data,GROUP,groupID, extended=False):
    list=[]
    for elem0 in data:
        ID,location,lat,lon,latency,country,owner,group=elem0
        if group in GROUP or group in groupID:
            elem={'label':location,'value':ID}
        
            if extended:
                elem['lon']=float(lon)
                elem['lat']=float(lat)
                elem['location']=location
                elem['deviceID']=ID
                elem['country']=country
                elem['owner']=owner
                elem['latency']=latency
            list.append(elem)
    return list

def tsINC(timestamp):
    import datetime
    d=datetime.datetime(1970, 1, 1) + datetime.timedelta(milliseconds=timestamp)
    return datetime.datetime(d.year+1900,d.month,d.day,d.hour,d.minute,d.second)

#def read_INCOIS_BPR():
    # <input type="hidden"  id="wLevel" value="[2829.424, 2829.36, 2829.295, 2829.249, 2829.2, 2829.165, 2829.14, 2829.12, 2829.115, 2829.121, 2829.138, 2829.155, 2829.19, 2829.23, 2829.28, 2829.329, 2829.394, 2829.771, 2829.849, 2829.924, 2829.994, 2830.064, 2830.123, 2830.184, 2830.229, 2830.277, 2830.312, 2830.343, 2830.363, 2830.378, 2830.378, 2830.371, 2830.361, 2830.341, 2830.316, 2830.286, 2830.246, 2830.206, 2830.151, 2830.102, 2830.047, 2829.994, 2829.939, 2829.891, 2829.841, 2829.801, 2829.761, 2829.726, 2829.707, 2829.681, 2829.672, 2829.662, 2829.666, 2829.671, 2829.686, 2829.71, 2829.745, 2829.784, 2829.829, 2829.878, 2829.933, 2829.997, 2830.066, 2830.125, 2830.189, 2830.258, 2830.323, 2830.381, 2830.441, 2830.495, 2830.54, 2830.579, 2830.606, 2830.628, 2830.644, 2830.643, 2830.638, 2830.622, 2830.592, 2830.558, 2830.509, 2830.456, 2830.39, 2830.315, 2830.225, 2830.136, 2830.043, 2829.944, 2829.839]" />
 
    # <input type="hidden"  id="tims"value="[2022-11-20-07-00, 2022-11-20-07-15, 2022-11-20-07-30, 2022-11-20-07-45, 2022-11-20-08-00, 2022-11-20-08-15, 2022-11-20-08-30, 2022-11-20-08-45, 2022-11-20-09-00, 2022-11-20-09-15, 2022-11-20-09-30, 2022-11-20-09-45, 2022-11-20-10-00, 2022-11-20-10-15, 2022-11-20-10-30, 2022-11-20-10-45, 2022-11-20-11-00, 2022-11-20-12-15, 2022-11-20-12-30, 2022-11-20-12-45, 2022-11-20-13-00, 2022-11-20-13-15, 2022-11-20-13-30, 2022-11-20-13-45, 2022-11-20-14-00, 2022-11-20-14-15, 2022-11-20-14-30, 2022-11-20-14-45, 2022-11-20-15-00, 2022-11-20-15-15, 2022-11-20-15-30, 2022-11-20-15-45, 2022-11-20-16-00, 2022-11-20-16-15, 2022-11-20-16-30, 2022-11-20-16-45, 2022-11-20-17-00, 2022-11-20-17-15, 2022-11-20-17-30, 2022-11-20-17-45, 2022-11-20-18-00, 2022-11-20-18-15, 2022-11-20-18-30, 2022-11-20-18-45, 2022-11-20-19-00, 2022-11-20-19-15, 2022-11-20-19-30, 2022-11-20-19-45, 2022-11-20-20-00, 2022-11-20-20-15, 2022-11-20-20-30, 2022-11-20-20-45, 2022-11-20-21-00, 2022-11-20-21-15, 2022-11-20-21-30, 2022-11-20-21-45, 2022-11-20-22-00, 2022-11-20-22-15, 2022-11-20-22-30, 2022-11-20-22-45, 2022-11-20-23-00, 2022-11-20-23-15, 2022-11-20-23-30, 2022-11-20-23-45, 2022-11-21-00-00, 2022-11-21-00-15, 2022-11-21-00-30, 2022-11-21-00-45, 2022-11-21-01-00, 2022-11-21-01-15, 2022-11-21-01-30, 2022-11-21-01-45, 2022-11-21-02-00, 2022-11-21-02-15, 2022-11-21-02-30, 2022-11-21-02-45, 2022-11-21-03-00, 2022-11-21-03-15, 2022-11-21-03-30, 2022-11-21-03-45, 2022-11-21-04-00, 2022-11-21-04-15, 2022-11-21-04-30, 2022-11-21-04-45, 2022-11-21-05-00, 2022-11-21-05-15, 2022-11-21-05-30, 2022-11-21-05-45, 2022-11-21-06-00]" />

def read_INCOIS(code,tmin,tmax, extended=False):
    tminS=tmin.strftime('%Y%m%d')
    tmaxS=tmax.strftime('%Y%m%d')
    url0='https://tsunami.incois.gov.in/itews/JSONS/$CODE_1.json'
    url=url0.replace('$CODE',code)
    delta=(tmax-tmin).days+1
    #print(url)
    with requests.get(url, verify=False) as resp:
        json=resp.json()
    
    if json==[]:
        return
    list={'x':[], 'y':[]}
    avgDelta=0.0
    firstSensor=''
    indexSensors=[]
    for n in range(len(json)):
        d=json[n]
        if d['name'] in ['PRS','ENC', 'RAD']:
            if not d['name'] in indexSensors:
                indexSensors.append([n,d['name'],len(d['data'])])
    index=sorted(indexSensors, key=lambda x: x[2], reverse=True)
    for j in range(len(json[index[0][0]]['data'])):
        tim=tsINC(json[index[0][0]]['data'][j][0])
        list['x'].append(tim)
        for k in range(len(index)):
            timS=tsINC(json[index[k][0]]['data'][j][0])
            if timS>=tim:
                sens=index[k][1]
                if not sens in list:
                    list[sens]=[]
                list[sens].append(json[index[k][0]]['data'][j][1])
            if len(list['x'])>1:
                avgDelta +=(tim-tim0).seconds
            tim0=tim
    if len(list['x'])>0:            
        avgDelta /=(len(list['x'])-1)
    list['y']=list[index[0][1]].copy()
    return list,avgDelta

    

def read_BIG(code,tmin,tmax, extended=False):
    tminS=tmin.strftime('%Y%m%d')
    tmaxS=tmax.strftime('%Y%m%d')
    url0='https://srgi.big.go.id/tides_data/pasut_$ID?date=$DAY1&datestart=$DAY&status=auto'
    url0=url0.replace('$ID',code)
    delta=(tmax-tmin).days+1
    list={'x':[], 'y':[]}
    avgDelta=0
    for j in range(delta):
        date= (tmin +timedelta(days=j)).strftime('%Y-%m-%d')
        date1=(tmin+timedelta(days=j+1)).strftime('%Y/%m/%d')
        url=url0.replace('$DAY1',date1)
        url=url.replace('$DAY',date)
        #print(url)
        if (datetime.utcnow()-tmin).days<3:
            resp=downloadFile(url,False,True)
        else: 
            resp=downloadFile(url,True,True,'cacheMeas')
        measures=json.loads(resp)

        for meas in measures['results']:
            ts=meas['ts']
            found=False
            if 'RAD1' in meas:
                value=meas['RAD1'];found=True
            elif 'PRS1' in meas:
                value=meas['PRS1'];found=True
            elif 'ENC1' in meas:
                value=meas['ENC1'];found=True
            if found:
                tim=datetime.strptime(ts,'%Y-%m-%d %H:%M:%S')
                list['x'].append(tim)
                list['y'].append(float(value))
                if len(list['x'])>1:
                    avgDelta +=(tim-tim0).seconds
                tim0=tim
            if extended:
                #print(meas.keys())
                for key in meas.keys():
                    if not key in['station','Residu','latency','ts', 'ts2']:
                        if not key in list:
                            list[key]=[]
                        list[key].append(float(meas[key]))
        if len(list['x'])>0:            
            avgDelta /=(len(list['x'])-1)

    return list,avgDelta

def getListDART(url):
    # dovrebbe leggere da una cache
    import requests,pycountry
    fname='data'+os.sep+'cache'+os.sep+'backupDART.txt'
    if os.path.exists(fname):
        dcrea=creation_date(fname)
        ageDays=elapsedHours(dcrea)/24        
        if ageDays<30:
            with open(fname, errors='ignore') as f:
                rows=f.read().split('\n')
            list=[]
            for r in rows:
                if r=='':continue
                elem=r.split('\t')
                name,desc,cou,lon,lat,link,startYear,endYear=elem
                lon=float(lon)
                lat=float(lat)
                startYear=int(startYear)
                endYear=int(endYear)
                elem=name,desc,cou,lon,lat,link,startYear,endYear
                list.append(elem)
            return list

    kml=downloadFile(url)
    if kml=='':
       return []
    testo=''
    vbTab='\t'
    buoys=kml.split('<Folder>\n\t<name>Tsunami</name>')[1].split('</Folder>')[0].split('<Placemark')
    list=[]
    for buoy in buoys:
        if not 'name' in buoy: continue
        name=extractXML(buoy,'name')
        desc=extractXML(buoy,'Snippet')
        desc=desc.replace("'", ' ')
        if ',' in desc:
            iso2=desc.split(',')[1].strip()
            if iso2=='AK': iso2='US'
            if iso2=='Virgin Is': iso2='US'
            if iso2=='NY': iso2='US'
            if iso2=='OR': iso2='US'
            if iso2=='WA': iso2='US'
            if iso2=='BC': iso2='CA'
            if iso2=='HI': iso2='US'
            if iso2=='New Guinea': iso2='PG'
            try:
                cou=pycountry.pycountry.countries.lookup(iso2).name
            except:
                print('iso2 not found: ',iso2)
                cou='Off-shore'
        else:
            if ' IN' in desc:
                cou='India'
            else:
                cou='Off-Shore'
        coordinates=extractXML(buoy,'coordinates')
        lon,lat,dummy=coordinates.split(',')

        link='https://www.ndbc.noaa.gov/station_page.php?station='+name
        resp=urlopen(link).read().decode()
        try:
            p=resp.split('<label for="startyear">')[1].split('Year</option>')[1].split('</select>')[0].split('option')
            if len(p)>0:
                startYear=int(p[1].split('"')[1].split('"')[0])
            p=resp.split('<label for="endyear">')[1].split('Year</option>')[1].split('</select>')[0].split('option')
            if len(p)>0:
                endYear=int(p[-2].split('"')[1].split('"')[0])
        except:
            startYear=2000
            endYear=datetime.utcnow().year
        elem=[name,desc,cou,lon,lat,link,startYear,endYear]
        list.append(elem)
    with open(fname,'w') as f:
        for elem in list:
            name,desc,cou,lon,lat,link,startYear,endYear=elem
            lon=format(lon)
            lat=format(lat)
            startYear=format(startYear)
            endYear=format(endYear)
            elem=name,desc,cou,lon,lat,link,startYear,endYear
            f.write('\t'.join(elem)+'\n')
        

    return list
    #tminS=tmin.strftime('%Y%m%d')
    #tmaxS=tmax.strftime('%Y%m%d')
    #url='https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&begin_date=$BEGINDATE&end_date=$ENDDATE&datum=MSL&station='+format(code)+'&time_zone=GMT&units=metric&format=json'
    #url=url.replace('$BEGINDATE',tminS)
    #url=url.replace('$ENDDATE',tmaxS)
    #if (datetime.utcnow()-tmin).days<3:
    #    resp=downloadFile(url,False,True)
    #else: 
    #    resp=downloadFile(url,True,True,'cacheMeas')

def read_NOAA(code,tmin,tmax):
    tminS=tmin.strftime('%Y%m%d')
    tmaxS=tmax.strftime('%Y%m%d')
    url='https://tidesandcurrents.noaa.gov/api/datagetter?product=water_level&application=NOS.COOPS.TAC.WL&begin_date=$BEGINDATE&end_date=$ENDDATE&datum=MSL&station='+format(code)+'&time_zone=GMT&units=metric&format=json'
    url=url.replace('$BEGINDATE',tminS)
    url=url.replace('$ENDDATE',tmaxS)
    if (datetime.utcnow()-tmin).days<3:
        resp=downloadFile(url,False,True)
    else: 
        resp=downloadFile(url,True,True,'cacheMeas')
    #resp=requests.get(url)
    #json=resp.json()
    jsonf=json.loads(resp)
    if not 'data'in jsonf:
        #print(jsonf)
        return [],0
    samples=jsonf['data']
    list={'x':[], 'y':[]}
    avgDelta=0
    for dat in samples:
        tim = datetime.strptime(dat['t'],'%Y-%m-%d %H:%M')
        try:
            if dat['v'] !='':
                measure_Float = float(dat['v'])
        except:
            print('*** error',dat)
            #print(tim,calg[0]._LastDateTimeAcquired)
        if dat['v']!='':
            list['x'].append(tim)
            list['y'].append(measure_Float)
            if len(list['x'])>1:
                avgDelta +=(tim-tim0).seconds
            tim0=tim
            
    avgDelta /=(len(list['x'])-1)
    return list, avgDelta
            
    
import xml.etree.ElementTree as ET
def read_GLOSS(code,tmin,tmax):

#  1)  collect the data into the "samples" collection
    URL='https://www.ioc-sealevelmonitoring.org/service.php?query=data&format=xml&code=$CODE&timestart=$TMIN&timestop=$TMAX'
    URL=URL.replace('$CODE',code )
    tminS=tmin.strftime('%Y-%m-%dT%H:%M:%S')
    tmaxS=tmax.strftime('%Y-%m-%dT%H:%M:%S')    
    URL=URL.replace('$TMIN',tminS )
    URL=URL.replace('$TMAX',tmaxS )
    print(URL)
    #xmlstr=downloadFile(URL,True)
    mode=2
    if mode==1:
        xmlbin=urlopen(URL).read()
        xmlstr=xmlbin.decode()
    
        #fname='temp_'+format(uuid.uuid1().int)+'.xml'
        fname='temp_.xml'
        with open(fname,'w') as f:
            f.write(xmlstr)
        #    
        time.sleep(.1)    
        #print('opening ',fname)
        tree = ET.parse(fname)        
        os.remove(fname)    
        root=tree.getroot()
    else:
        if (datetime.utcnow()-tmin).days>3:
            xmlstr=downloadFile(URL,True,False,'cacheMeas')
        else:
            xmlstr=downloadFile(URL,False,False,'cacheMeas')
            if xmlstr=='':
                xmlstr=downloadFile(URL,False,True,'cacheMeas')
        root=ET.fromstring(xmlstr)
    
    samples=root.findall('sample')
    #print('len(samples)',len(samples))
    if len(samples)==0:
        return [],0
    #
    sensors=[]
    for j in range(len(samples)):
        samp=samples[j]
        sens=samp.findall('sensor')[0].text
        if not sens in sensors:
            sensors.append(sens)
    if 'prs' in sensors:
        sens0='prs'
    else:
        if 'rad' in sensors:
            sens0='rad'
        else:
            if 'bat' in sensors:
                sens0='bat'
            else:
                sens0=sensors[0]

    list={'x':[], 'y':[]}
    avgDelta=0
    n=-1
    for j in range(len(samples)):
        samp=samples[j]
        try:
            tiSt=samp.findall('stime')[0].text
            sens=samp.findall('sensor')[0].text
            if sens==sens0:
                tim=datetime.strptime(tiSt,'%Y-%m-%d %H:%M:%S')
                try:
                    measure_Float = float(samp.findall('slevel')[0].text)
                except:
                    print('*** error',samp)
                list['x'].append(tim)
                list['y'].append(measure_Float)
                if len(list['x'])>1:
                    avgDelta +=(tim-tim0).seconds
                tim0=tim
            
        except Exception as e:
            samp=samp
            print(e)
    if len(list['x'])>1:
        avgDelta /=(len(list['x'])-1)
    else:
        avgDelta=0.0
        list=[]
    return list, avgDelta

def haversine(lon1, lat1, lon2, lat2):
    #Calculate the great circle distance in kilometers between two points 
    #on the earth (specified in decimal degrees)
    #
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a)) 
    r = 6371000 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r
def read_DART(ID, tmin,tmax):
    
    URL='https://www.ndbc.noaa.gov/station_page.php?station='+ID+'&startyear='+format(tmin.year)+'&startmonth='+format(tmin.month)+'&startday='+format(tmin.day)+'&endyear='+format(tmax.year)+'&endmonth='+format(tmax.month)+'&endday='+format(tmax.day)
    #print(URL)
    #resp=requests.get(URL).text
    if (datetime.utcnow()-tmin).days<3:
        resp=downloadFile(URL,False)
    else:
        resp=downloadFile(URL)
    list={'x':[], 'y':[]}
    avgDelta=0
    if '#yr  mo dy hr mn  s -      m'  in resp:
        data=resp.split('#yr  mo dy hr mn  s -      m')[1].split('</textarea')[0].split('\n')
    else:
        return [],0
    try:
        for j in range(len(data)-1,0,-1):
            d=data[j]
            if d=='' or d=='\n': continue
            #2022 08 07 11 45 00 1 4737.192
            #01234567890123456789012
            datTime=datetime.strptime(d[:18],'%Y %m %d %H %M %S')
            if '9999' in d[21:] or 'a' in d[21:]:continue
            lev    =float(d[21:])
            
            list['x'].append(datTime)
            list['y'].append(lev)
            #print(datTime,lev)
            if len(list['x'])>1:
                avgDelta +=(datTime-ts0).seconds
            ts0=datTime
    except Exception as e:
        print(e)
    #print(len(list['x']),len(data))
    if len(list['x'])>1:
        avgDelta /=(len(list['x'])-1)
    return list,avgDelta

def read_NOA(type,ID,tmin,tmax,nmaxData, extended=False):
    tminS=tmin.strftime('%Y-%m-%dT%H:%M:%S')
    tmaxS=tmax.strftime('%Y-%m-%dT%H:%M:%S')    

    url='http://antares.gein.noa.gr/TAD_Server/Default.aspx?mode=json&ID='+ID+'&tMin='+tminS+'&tMax='+tmaxS
    if (datetime.utcnow()-tmin).days<3:
        dataJson=downloadFile(url,False,False,'cacheMeas')
    else:
        dataJson=downloadFile(url,True,False,'cacheMeas')
    data=json.loads(dataJson)
    list={'x':[], 'y':[]}
    avgDelta=0.0
    for j in range(len(data['fields'][0]['values'])):
        t=data['fields'][0]['values'][j]
        v=data['fields'][1]['values'][j]
        ts=datetime.utcfromtimestamp(float(t.split('(')[1].split(')')[0])/1000)
        list['x'].append(ts)
        list['y'].append(v)
        if extended:
            for field in data['fields'][2:]:
                key=field['dbName']
                if not key in list:
                    list[key]=[]
                list[key].append(field['values'][j])
        if j>0:
            avgDelta +=(ts-ts0).seconds
        ts0=ts
    avgDelta /=(len(list['x'])-1)
    #print('avgDelta',avgDelta)
    return list,avgDelta




def readTAD_server(type,ID,tmin,tmax,nmaxData, extended=False):
    tminS=tmin.strftime('%Y-%m-%dT%H:%M:%SZ')
    tmaxS=tmax.strftime('%Y-%m-%dT%H:%M:%SZ')

    if type=='JRC_TAD':
        url='https://webcritech.jrc.ec.europa.eu/TAD_server/api/Data/Get/'+format(ID) +'?tMin='+tminS+'&tMax='+tmaxS+'&nRec='+format(nmaxData)+'&mode=json'
        timeLabel='Timestamp'
    elif type=='ISPRA_TAD':
        url='https://tsunami.isprambiente.it/TAD_server/api/Data/Get/'+format(ID) +'?tMin='+tminS+'&tMax='+tmaxS+'&nRec='+format(nmaxData)+'&mode=json'
        timeLabel='Date'
    elif type=='NOA_TAD':
        url='http://83.212.99.53/TAD_server/api/Data/Get/'+format(ID) +'?tMin='+tminS+'&tMax='+tmaxS+'&nRec='+format(nmaxData)+'&mode=json'
        url='http://83.212.99.53/TAD_Server/Default.aspx?mode=json&ID='+ID+'&tMin='+tminS+'&tMax='+tmaxS
        #print(url)
        timeLabel='Date'
    #print(url)

    #resp=urlopen(url)
    #dataJson = resp.read().decode("utf-8")
    if (datetime.utcnow()-tmin).days<3:
        dataJson=downloadFile(url,False,False,'cacheMeas')
    else:
        dataJson=downloadFile(url,True,False,'cacheMeas')
    data=json.loads(dataJson)
    #print(len(data))
    list={'x':[], 'y':[]}
    avgDelta=0
    for j in range(len(data)):
        v=data[j]
        ts=v[timeLabel]
        if '.' in ts:
            ts1=datetime.strptime(ts,'%Y-%m-%dT%H:%M:%S.%fZ')
        else:
            ts1=datetime.strptime(ts,'%Y-%m-%dT%H:%M:%SZ')
        va=v['Values']['inp1']            
        list['x'].append(ts1)
        list['y'].append(va)
        if extended:
            for key in v['Values']:
                if not key in list:
                    list[key]=[]
                list[key].append(v['Values'][key])
        if j>0:
            avgDelta +=(ts1-ts0).seconds
        ts0=ts1
    avgDelta /=(len(data)-1)
    #print('avgDelta',avgDelta)
    return list,avgDelta

def getValues(type,ID,tmin,tmax,nmaxData=500000,extended=False):
    #print('type=',type)

    if type=='GLOSS @vliz':
        list,avgDelta= read_GLOSS(ID,tmin,tmax)
    elif type=='BIG':
        list,avgDelta= read_BIG(ID,tmin,tmax, extended)
    elif type=='DART':
        list,avgDelta= read_DART(ID,tmin,tmax)
    elif type=='NOAA TC':
        list,avgDelta= read_NOAA(ID,tmin,tmax)
    elif type=='NOA_TAD':
        devlist=getListDevices(type,False)
        for dev in devlist:
            if dev[1]==ID:
                ID=dev[0]
                break
        list,avgDelta=read_NOA(type,ID,tmin,tmax,nmaxData,extended)
    elif type=='INCOIS':
        list,avgDelta=read_INCOIS(ID,tmin,tmax, extended)

    elif type in ['JRC_TAD','ISPRA_TAD']:
        list,avgDelta=readTAD_server(type,ID,tmin,tmax,nmaxData,extended)
    else:
        print('error, database not existing. Use the command getDBs() to retrieve valid databases')
        return [],''
    return list,avgDelta

# def getEventDetail(noaa_id,eventsGDACS):
#     #print('requested id=',EventId)
#     ev=eventsGDACS[eventsGDACS['noaa_id']==noaa_id].sort_values(by='Amplitude',ascending=False)
#     #print(ev)
#     EventDate=pd.to_datetime(ev['EventDate'].values[0]).strftime('%d-%m-%Y %H:%M:%S')
#     EventLocation=ev['EventLocation'].values[0]
#     EventLat=float(ev['EventLat'].values[0])
#     EventLon=float(ev['EventLon'].values[0])
#     Mag=float(ev['Magnitude'].values[0])
#     if Mag>0:
#         Magnitude='M'+format(ev['Magnitude'].values[0])
#     else:
#         Magnitude='n.a.'
#     Depth=format(ev['Depth'].values[0])+' km'
#     GTSName='' #ev['GTSName'].values[0]
#     PlaceMax=ev['Place'].values[0]
#     Lon=ev['Lon'].values[0]
#     Lat=ev['Lat'].values[0]
#     ArrivalTime=ev['ArrivalTime'].values[0]
#     Amplitude=format(ev['Amplitude'].values[0])+' m'
#     gdacs_link=ev['gdacs_link'].values[0]
#     noaa_link=ev['noaa_link'].values[0]
#     gts_link=ev['gts_link'].values[0]
#     url='https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/tsunamis/events/'+format(noaa_id)+'/info'
#     noaaJson=downloadFile(url,True)
#     if noaaJson !='':
#         js=json.loads(noaaJson)
#         #print(js)
#         if 'comments' in js:
#             comments=js['comments']
#             comments=html.Div([html.B('Comments'),' (',html.Em('source NOAA'), ')',html.Br(),convert_html_to_dash(comments)], style={'height':'200px', 'width':'100%',"overflow": "scroll"})
#             #comments=html.Div([html.B('Comments'),' (',html.Em('source NOAA'), ')',html.Br(),comments], style={'height':'200px', 'width':'100%',"overflow": "scroll"})
#         else:
#             comments=''
#     else:
#         comments=''
#     Period=format(ev['Period'].values[0])+' min'
#     if PlaceMax=='n.a.': 
#         AmplPer=''
#     else:
#         AmplPer=format(Amplitude)+' ('+format(Period)+')'
#     if noaa_id>100000:
#         linkGDACS='https://www.gdacs.org/report.aspx?eventtype=EQ&eventid='+format(noaa_id)
#     else:
#         linkGDACS=''

#     rows=[]
#     row=html.Tr([html.Td('Event ID',style=tds(150)),html.Td(noaa_id,id='evID',style=tds(250))]);rows.append(row)
#     row=html.Tr([html.Td('Date of event',style=tds(150)),html.Td(html.B(EventDate),style=tds(250))]);rows.append(row)
#     row=html.Tr([html.Td('Location',style=tds(150)),html.Td(html.B(EventLocation),style=tds(250))]);rows.append(row)
#     row=html.Tr([html.Td('Magnitude',style=tds(150)),html.Td(html.B(Magnitude),style=tds(250))]);rows.append(row)
#     row=html.Tr([html.Td('Depth',style=tds(150)),html.Td(html.B(Depth),style=tds(250))]);rows.append(row)
#     row=html.Tr([html.Td('Lat/Lon',style=tds(150)),html.Td(html.B(format(EventLat)+'/'+format(EventLon)),style=tds(250))]);rows.append(row)
#     row=html.Tr([html.Td('Place of max height',style=tds(250)),html.Td(html.B(PlaceMax,id='PlaceMax'),style=tds(150))]);rows.append(row)
#     row=html.Tr([html.Td('Amplitude (period)',style=tds(250)),html.Td(html.B(AmplPer),style=tds(250))]);rows.append(row)
#     if gdacs_link != None:
#         row=html.Tr([html.Td('GDACS Report',style=tds(250)),html.Td(html.A(gdacsImg,href=gdacs_link,target='_GDACS'),style=tds(150))]);rows.append(row)
#     if noaa_link != None:
#         row=html.Tr([html.Td('NOAA Report',style=tds(250)),html.Td(html.A(noaaImg,href=noaa_link,target='_NOAA'),style=tds(150))]);rows.append(row)
#     if comments !='':
#         row=html.Tr(html.Td(comments,colSpan=2));rows.append(row)


#     tab=html.Center(html.Table(rows))
#     title=format(Magnitude)+' '+ EventLocation    
    
#     #dat=pd.to_datetime(ev['EventDate'].values[0])
#     dat=datetime.strptime(EventDate,'%d-%m-%Y %H:%M:%S')
#     return tab,title,dat,Mag,EventLon,EventLat,PlaceMax

# def getFigure(values, definition, title='', log_x=False, log_y=False,limitsX=[], limitsY=[],dat=None):
#     fig = make_subplots(specs=[[{"secondary_y": True}]])

#     # Add traces
#     for q in definition:
#         xf,yf, caption=q
#         if caption=='': caption=yf
#         fig.add_trace(go.Scatter(x=values[xf], y=values[yf], name=caption))
#         if title !='':
#             fig.update_layout(title={'text': title,'xanchor': 'center','yanchor': 'top'},title_x=0.5)
#         if log_x:
#             fig.update_layout(xaxis_type="log")
#         if log_y:
#             fig.update_layout(yaxis_type="log")
#         if limitsY !=[]:
#             fig.update_yaxes(range=limitsY)
#         if limitsX !=[]:
#             fig.update_xaxes(range=limitsX)
#     if not dat==None:
#         if limitsY==[]:
#             ymin=1e8;ymax=-1e8
#             for d in fig.data:
#                 ymin,ymax=min(min(d['y']),ymin),max(max(d['y']),ymax)
#                 delta=ymax-ymin
#             ymax+=delta*0.1;ymin -=delta*0.1
#             fig.update_yaxes(range=[ymin,ymax])
#             ymax+=delta;ymin -=delta
#         else:
#             ymin,ymax=limitsY
#         fig.add_trace(go.Scatter(x=[dat,dat], y=[ymin,ymax], name='EQ',mode='lines',line=dict(width=2,color='red',dash='dash')))
#         #line=dict(width=2,color='navy',dash='dash')
#     return fig

def getMaxDistances():
    listNmax=[]
    for n in range(100,1000,100):
        listNmax.append({'label':format(n) +' km','value':n})
    for n in range(1000,10000,1000):
        listNmax.append({'label':format(n) +' km','value':n})
    for n in range(10000,30000,5000):
        listNmax.append({'label':format(n) +' km','value':n})
    return listNmax

def getList(what,data=[], db=None, groupID=None, extended=False, GROUP='', invertDict=False):
    list=[]
    if what=='DB':
        dbs=['JRC_TAD', 'NOA_TAD', 'ISPRA_TAD', 'GLOSS @vliz', 'NOAA TC', 'DART', 'INCOIS']  #,'BIG']
        for db in dbs:
            list.append({'label':db,'value':db})
        return list
    elif what=='GROUPS':
        listInv=[]
        if db in ['GLOSS @vliz', 'NOAA TC', 'DART', 'NOA_TAD','BIG']:
            list.append({'label':db,'value':db})
            listInv=list
        elif db=='INCOIS':
            for gr in ['Tidal Gauges','Tsunami Buoys']:
                list.append({'label':gr,'value':gr})
                listInv=list
        else:
            for group in data:
                Name=group['properties']['Name']
                Color=group['properties']['Color']
                groupID=group['properties']['Id']
                list.append({'label':Name,'value':groupID})
                list
                #print(groupID,Name)
        return list
    elif what=='DEVICES':
        print('groupid=', groupID)
        if groupID==None or db==None:
            return []

        if db=='INCOIS':
            list=getListINCOIS_combo(data,GROUP,groupID,extended)
            return list
        else:
            if groupID=='GLOSS @vliz' or GROUP=='GLOSS @vliz':
                list=getListGLOSS(data,extended)
            elif groupID=='BIG' or GROUP=='BIG':
                list=getListBIG(data,extended)
            elif groupID=='NOA_TAD' or GROUP=='NOA_TAD':
                list=getListNOA_combo(data,extended)
            elif groupID=='NOAA TC' or GROUP=='NOAA TC':
                list=getlistNOAA_TC(data,extended)
            elif groupID=='DART' or GROUP=='DART':
                list=getlistoptionsDART(data,extended)
            else:
                for group in data:
                    #print(group['properties']['Id'],groupID,group['properties']['Name'])
                    if format(groupID)==format(group['properties']['Id']) or GROUP==group['properties']['Name']:
                        for device in group['features']:
                            #print(device)
                            ID=device['id']
                            NAME=device['properties']['Name']
                            try:
                                Location=device['properties']['Location']+' ('+device['properties']['Country']+')'
                            except Exception as e:
                                Location=''
                                print(e)
                            elem={'label':NAME+' '+Location,'value':ID}
                            if extended:
                                elem['deviceID']=NAME
                                elem['location']=device['properties']['Location']
                                lon,lat=device['geometry']['coordinates']
                                elem['lon']=lon
                                elem['lat']=lat
                                elem['country']=device['properties']['Country']
                                elem['sensor']=device['properties']['Sensor']
                                elem['region']=device['properties']['Region']
                                elem['GroupColor']=device['properties']['GroupColor']
                                elem['Provider']=device['properties']['Provider']
                                elem['latencyMin']=-1
                                if 'Latency' in device['properties']:
                                    if 'Seconds' in device['properties']['Latency']:
                                        if device['properties']['Latency']['Seconds']!=None:
                                            elem['latencyMin']=device['properties']['Latency']['Seconds']/60
                                
                                    
                            list.append(elem)
                        break
            
#{'type': 'Feature', 'id': '208', 'geometry': {'type': 'Point', 'coordinates': [99.585453, -2.037654]}, 'properties': {'Name': 'IDSL-303', 'Sensor': 'RAD', 'Location': 'Mentawai Tua Pejat', 'Country': 'Indonesia', 'Region': 'West Sumatra', 'Provider': 'JRC-MMAF', 'LastData': {'Date': '03 Jul 2022 02:06:38', 'Value': 1.712382}, 'Latency': {'Literal': '1 Days', 'Seconds': 100214, 'Color': '#FF0000'}, 'GroupColor': '#D20950'}},                    
            return list

def getlistNOAA_TC(stations,extended=False):
        list=[]
        for station in stations['stations']:
            #print('station=',station)
            #print(format(station['lat']) + "," + format(station['lng']) + "," + station['name'] + " " + format(station['id']))
            ID = station['id']
            location=station['name']
            elem={'label':location,'value':ID}
            if extended:
                elem['lon']=station['lng']
                elem['lat']=station['lat']
                elem['Provider']=station['affiliations']
                elem['deviceID']=ID
                elem['location']=location
                elem['country']='USA'
                #print(station)
            #print(elem)
            list.append(elem)
        return list

def getlistoptionsDART(stations,extended=False):
        list=[]
        for station in stations:
            name,desc,cou,lon,lat,link,startYear,endYear=station
            #print(format(station['lat']) + "," + format(station['lng']) + "," + station['name'] + " " + format(station['id']))
            ID = name
            location=(desc.split('-')[0]+' - '+desc.split('-')[1]).strip()
            elem={'label':location,'value':ID}
            if extended:
                elem['lon']=lon
                elem['lat']=lat
                elem['country']=cou
                elem['deviceID']=ID
                elem['location']=location
                elem['sensor']='BPR'
            list.append(elem)
        return list

def getListGLOSS(stations,extended=False):
        import pycountry
        list=[]
        n=-1
        for station in stations:
            n+=1
            #if not 'ioc' in station: continue
            #print(station)
            n +=1
            try:
                cou=pycountry.pycountry.countries.lookup(station['country']).name
            except:
                cou=station['country']
            elem={'label':station['Code']+' - '+station['Location']+' ('+cou+') ','value':station['Code']}
            if extended:
                elem['lat']=station['lat']
                elem['lon']=station['lon']
                elem['country']=cou
                elem['deviceID']=station['Code']
                elem['location']=station['Location']
                elem['sensor']=station['sensor']
            if not elem in list:
                #if n<3: print(elem)
                list.append(elem)
        return list

def extractLabel(opt,value):
    for elem in opt:
        #print(elem,value)
        if elem['value']==value:
            return elem['label']
    return ''
def interpData(x0,vv,x=[]):
    nseconds=[]
    for k in range(len(x0)):
    #		printLog(x0[k],values[k])
        nseconds.append((x0[k]-x0[0]).days*24*3600+(x0[k]-x0[0]).seconds)
    if len(x)==0:
        x=np.linspace(0,nseconds[-1],1+len(vv))
    #print(len(x),len(nseconds),len(vv))
    try:
        ynew=np.interp(x,nseconds,vv)
    except Exception as e:
        print(e)
    dnew=[]
    for k in range(len(x)):
        day=int(x[k]/3600/24)
        secs=x[k]-day*3600*24
        dnew.append(x0[0]+timedelta(days=day)+timedelta(seconds=secs))
    return dnew, ynew
def movAverage(x,y,n):
    n2=int(n/2)
    res=[];xres=[]
    for j in range(n2,len(y)-n2):
        sum=0
        for i in range(j-n2,j+n2):
            sum +=y[i]
        res.append(sum/(n2*2))
       # print('mov ave',x[j],sum/n2)
        xres.append(x[j])
    return xres,res

def powspec(x0,y0):       
    freq=[];period_min=[];pow=[]
    if len(x0)<10:
        return freq, period_min,pow,[],[]
    xvalue, signal=interpData(x0,y0)    
    #xvalue,signal=x0,y0
    npoi = len(xvalue)    
    dt = (xvalue[-1] - xvalue[0]).seconds + (xvalue[-1] - xvalue[0]).days*24*3600
    #print(type(signal),len(signal), type(xvalue), len(xvalue))
    coeff=np.fft.fft(signal)
    
    f=open('outpowspec.csv','w')
    for k in range(int(npoi/2)):
        freq.append ( k / dt)
        if k != 0:
            period=dt/k/60
            period_min.append ( period)
            pows=float((coeff[k].real ** 2 + coeff[k].imag ** 2) ** 0.5 * 2 / npoi)
            pow.append ( pows )      
            f.write(format(period)+','+format(pows)+'\n')
    f.close()
    pmin=int(period_min[-1])+1
    pmax=int(period_min[0])
    pernew=np.linspace(pmax,pmin,(pmax-pmin)+1)
    pernew    =np.flip(pernew)
    period_min=np.flip(period_min)
    pow       =np.flip(pow)
    pownew=np.interp(pernew,period_min,pow)
    perS,powS=movAverage(pernew,pownew,6)
    return freq, period_min,pow,perS,powS

def numpydt64to_datetime(date):
    """
    Converts a numpy datetime64 object to a python datetime object 
    Input:
      date - a np.datetime64 object
    Output:
      DATE - a python datetime object
    """
    timestamp = ((date - np.datetime64('1970-01-01T00:00:00'))
                 / np.timedelta64(1, 's'))
    return datetime.utcfromtimestamp(timestamp)   

def xnumpydt64to_datetime(dt64):
    unix_epoch = np.datetime64(0, 's')
    one_second = np.timedelta64(1, 's')
    seconds_since_epoch = (dt64 - unix_epoch) / one_second
    return datetime.utcfromtimestamp(seconds_since_epoch)


def showPlot(DBNAME,idDevice,dat,width=''):
    nmaxData=1000
    tmin=dat-timedelta(days=1)
    tmax=dat+timedelta(days=2)
    values, avgDelta1=getValues(DBNAME,idDevice, tmin, tmax, nmaxData)  
    if values['x']==[]:
        return ''
    label=DBNAME+'/'+idDevice
    fig=getFigure(values,[('x','y','Level')],'Original measured data '+label,False,False,[],[],dat)
    if width=='':
        grafico=dcc.Graph(id='plotOnTheFly', figure=fig)
    else:
        grafico=dcc.Graph(id='plotOnTheFly', figure=fig, style={'width':format(width)+'px'})
    return grafico

def convert_html_to_dash(el,style = None):
    CST_PERMITIDOS =  {'div','span','a','hr','br','p','b','i','u','s','h1','h2','h3','h4','h5','h6','ol','ul','li',
                        'em','strong','cite','tt','pre','small','big','center','blockquote','address','font','img',
                        'table','tr','td','caption','th','textarea','option'}
    def __extract_style(el):
        if not el.attrs.get("style"):
            return None
        return {k.strip():v.strip() for k,v in [x.split(": ") for x in el.attrs["style"].split(";")]}

    if type(el) is str:
        return convert_html_to_dash(bs.BeautifulSoup(el,'html.parser'))
    if type(el) == bs.element.NavigableString:
        return str(el)
    else:
        name = el.name
        style = __extract_style(el) if style is None else style
        contents = [convert_html_to_dash(x) for x in el.contents]
        if name.title().lower() not in CST_PERMITIDOS:        
            return contents[0] if len(contents)==1 else html.Div(contents)
        return getattr(html,name.title())(contents,style = style)

def spikeRemoval(x,y,th=20):       
    totAverage = 0.
    rms = 0.
    npoi=len(y)
    x1=[];y1=[]
    totAverage=np.average(y)
    for k  in range(len(y)):
        rms += (y[k] - totAverage) ** 2 / npoi
    rms = rms ** 0.5
    skip=0
    i0 = -1
    skip = 0
    for k in range(npoi):
        #print(k,x[k],y[k],totAverage,(abs(y[k]) - totAverage),th / 20 * 3 * rms ,(abs(y[k]) - totAverage) < th / 20 * 3 * rms)
        if abs(y[k] - totAverage) < th / 20 * 3 * rms:
            i0 += 1
            x1.append(x[k])
            y1.append(y[k])
        else:
            skip +=1
    #print('skip=',skip)
    return x1,y1
def spikeRemoval0(x,y,avgDelta):
    npoi=len(x)
    delta=int(npoi/20)
    vy=[]
    for j in range(npoi):
        if j<delta:
            vy.append(y[j])
        else:
            avg=np.average(vy[(j-delta):j-1])
            
            if abs(y[j]-y[j-1])>5*abs(vy[j-1]-avg) and abs(y[j]-y[j-1])>0.2:
                vy.append(vy[j-1])
                y[j]=vy[j-1]
            else:
                vy.append(y[j])
            #print(j,x[j],vy[j],y[j],avg,y[j]-y[j-1],y[j]-avg,abs(y[j]-y[j-1])>5*abs(y[j]-avg))
    return vy

def interpDataGen(x0,vv,nmax):
	d0=np.array(x0).min()
	dd=[]
	for k in range(len(x0)):
		dd.append((x0[k]-d0).total_seconds())
	x=np.linspace(0,np.max(dd),nmax)
	ynew=np.interp(x,dd,vv)
	#printLog (len(x),len(y))
	dnew=[]
	#printLog('===============================')
	for k in range(len(x)):
		dnew.append(d0+timedelta(seconds=x[k]))
	ynew=np.array(ynew)
	
	return dnew, ynew

def decodeUploadedData(decoded,nmaxData):
    from dateutil.parser import parse
    lines=decoded.split('\n')
    for line in lines:
        if line[0] in '*%$#@!':
            continue
        break
    line0=line
    if '\t' in line0:
        sep='\t'
    elif ',' in line0:
        sep=','
    else:
        return {},0,'Please use a file with tab or comma separations'
    nfields=len(line0.split(sep))
    values={'x':[],'y':[]}
    avgDelta=0
    for line in decoded.split('\n'):
        if line.strip()=='':
            continue
        if line[0] in '*%$#@!':
            continue
        #print(line)
        x=parse(line.split(sep)[0])
        y=float(line.split(sep)[1])
        values['x'].append(x)
        values['y'].append(y)
        if len(values['x'])>1:
             avgDelta +=(x-tim0).seconds
        tim0=x
        
    if len(values['x'])>1:
        avgDelta /=(len(values['x'])-1)
    else:
        avgDelta=0
    if len(values['x'])>nmaxData: 
        xnew,ynew=interpDataGen(values['x'],values['y'],nmaxData)
        values['x']=xnew
        values['y']=ynew
        avgDelta=(xnew[-1]-xnew[0]).total_seconds()/len(xnew)
    return values,avgDelta,''


def updateStatistics(section, testo=''):
    fnameStat=dire0+os.sep+'_logs'+os.sep+'_logsstats.txt'
    if not os.path.exists(dire0+os.sep+'_logs'):
        os.makedirs(dire0+os.sep+'_logs')
    
    now=datetime.now().strftime('%Y-%m-%d')
    if os.path.exists(fnameStat):
        f=open(fnameStat,'r')
        stat=f.read().split('\n')
        f.close()
    else:
        stat=[]
    found=False
    
    for j in range(len(stat)):
        
        fields=stat[j].split('\t')
        if fields[0]==now and fields[1]==section:
            n=int(fields[2])+1
            stat[j]='\t'.join([now,section,str(n), testo])
            found=True
            break
    if not found:
        n=1
        stat.append('\t'.join([now,section,str(n)]))

    with open(fnameStat, "w") as outfile:
        outfile.write("\n".join(stat))

#dataList=getListDevicesbyDBs()