# todo  sl.plot(db,devID)
#       det=sl.search(lat,lon,[dist_KM=10])
#       values_enriched=sl.TSdetModel(values, n30,n300, rmsMult, thresh)

from sealev.utilities import getListDevices,getValues,haversine

from datetime import datetime,timedelta
fmtime='%Y-%m-%d %H:%M:%S'

class seaLevelDB():
    """description of class"""

    def __init__(self):
        return
    
    def getDBs(self):
        #get the list of databases
        dbs=['GLOSS @vliz','NOAA TC','JRC_TAD','DART','IDSL_REP_bilance','IDSL_REP_pyt_any',
        'NOA_TAD','ISPRA_TAD','BIG','INCOIS']
        return dbs
    
    def __convertList(self,db,list):
        if list==[]:return []
        flist=[]
        listdevs=[]
        if db=='GLOSS @vliz':
            for sta in list:
                id=sta['Code']
                if id in listdevs:continue
                listdevs.append(id)
                name=sta['Location']
                country=sta['country']
                lat=sta['Lat']
                long=sta['Lon']
                group=''
                elem={'location':name,
                      'id':id,
                      'lat':lat,
                      'lon':long,
                      'country':'',
                      'group':group}                
                flist.append(elem)
                        
        elif db=='NOAA TC':
            for sta in list['stations']:
                name=sta['name']
                id  =sta['id']
                lat =sta['lat']
                long=sta['lng']
                group=''                
                elem={'location':name,
                      'id':id,
                      'lat':lat,
                      'lon':long,
                      'country':'',
                      'group':''}                
                flist.append(elem)
        elif db=='DART':
            #  ('21413', 'Station 21413 - SOUTHEAST TOKYO - 700NM ESE of Tokyo, JP', 'Japan', 152.085, 30.492, 'https://www.ndbc.noaa.gov/station_page.php?station=21413', 2000, 2024)
                for sta in list:    
                    id,name,country,long,lat,url,y0,y1=sta
                    elem={'location':name,
                          'id':id,
                          'lat':lat,
                          'lon':long,
                          'country':country,
                          'group':''}                
                    flist.append(elem)
                    
        elif db=='NOA_TAD':
            for sta in list:
                id,name,lon,lat,location,link,country=sta
                lon=float(lon)
                lat=float(lat)
                elem={'location':location,
                        'id':name,
                        'lat':lat,
                        'lon':lon,
                        'country':country,
                        'group':''}                
                flist.append(elem)                
                
        elif db=='JRC_TAD' or db=='ISPRA_TAD':
        #{'properties': {'Name': 'CNRS', 'Color': '#0C50FF', 'Id': 13}, 'type': 'FeatureCollection',
        # 'features': [{'type': 'Feature', 'id': '107', 'geometry': {'type': 'Point', 'coordinates': [35.50945, 33.900068]}, 'properties': {'Name': 'CNRS-01', 'Sensor': 'RAD', 'Location': 'Beirut', 'Country': 'Lebanon', 'Region': 'Lebanon', 'Provider': 'CNRS', 'GroupColor': '#0C50FF'}}]}
            exclude=['X_DART','X_GLOSS','X_India','X_NOAA','Test']
            for group in list:
                if group['properties']['Name'] in exclude:continue
                for sta in group['features']: 
                    prop=sta['properties']
                    id=prop['Name']
                    location=prop['Location']
                    long,lat=sta['geometry']['coordinates']
                    country=prop['Country']
                    
                    elem={'location':location,
                          'id':id,
                          'lat':lat,
                          'lon':long,
                          'country':country,
                          'group':group['properties']['Name']
                         }                
                    flist.append(elem)
        elif db=='BIG':
            for sta in list['features']: 
                prop=sta['properties']
                id=prop['CODE']
                location=prop['NAMA_STS']
                long,lat=sta['geometry']['coordinates']
                country=''
                if id!=None:
                    elem={'location':location,
                        'id':id,
                        'lat':lat,
                        'lon':long,
                        'country':country,
                        'group':''
                        }                
                    flist.append(elem)
        elif db=='INCOIS':
            for sta in list:
                id,location,lat,lon,latency,country,owner,group=sta
                elem={'location':location,
                    'id':id,
                    'lat':lat,
                    'lon':lon,
                    'country':country,
                    'group':group
                    }                
                flist.append(elem)
        flist=sorted(flist, key=lambda i: i['id'])
        return flist                
    
    def getDevs(self,db,maxdelayMin=-1,ld='False'):
        # get the list of devices
        # maxdelayMin= max delay in minutes
        print('Generating device list for database '+db+'. If cache is older than 30 days it will take more time')        
        devlist=getListDevices(db,ld)
        #print('devlist=',devlist)
        list=self.__convertList(db,devlist)
        return list
    
    def to_csv(selv,values,outFile):
        columns=values.keys()
        testo='\t'.join(list(columns))+'\n'
        for j in range(len(values['x'])):
            first=True
            for col in list(columns):
                if not first:
                    testo+='\t'
                first=False            
                if col=='x':
                    testo+=values[col][j].strftime(fmtime)
                else:
                    testo+=format(values[col][j])
            testo+='\n'                    
        with open(outFile,'w') as f:
            f.write(testo)

            #def getDetails(self,db,idDevice):
            #    if db=='' or group=='' or idDevice=='':
            #        return 'error in parameters'
            #    # 1. retrieve details
            #    detailsTable,details=getDetailsDevice(DB,GROUP,idDevice)
            #    return details
    
    
    def getLevel(self,db,idDevice,tmin='',tmax='', nmax=10000):
        # get the sea level of device 
            # 2. retrieve data
        if tmax=='':
            tmax=datetime.utcnow()
        else:
            tmax=datetime.strptime(tmax,fmtime)
        if tmin=='':
            tmin =tmax - timedelta(days=1)
        else:
            tmin=datetime.strptime(tmin,fmtime)
        values, avgDelta1=getValues(db,idDevice, tmin, tmax, nmax, True)

        return values
   
    def getDetails(self,db,devID):
       devices=self.getDevs(db)
       det= list(filter(lambda dev: dev['id'] == devID, devices))[0]
       if det['country']=='':
           try:
               import reverse_geocoder, pycountry
               cc=reverse_geocoder.search((det['lat'],det['lon']))[0]['cc']
               cou=pycountry.pycountry.countries.lookup(cc).name
               det['country']=cou
           except Exception as e:
                print(e)
       return det

    def plot(self,db,devID,tmin='',tmax='',title=None,xlab=None,ylab=None,xmin=None,ymin=None,ymax=None,show=True):       
        det=self.getDetails(db,devID)
        if xlab==None:xlab='Date/Time'
        if ylab==None:ylab='Level (m)'
        if title==None: title=det['location']+', '+det['country']+' (id='+det['id']+' lat/lon='+format(det['lat'])+'/'+format(det['lon'])+')'
        values=self.getLevel(db,devID,tmin,tmax)
        import matplotlib.pyplot as plt
        plt.plot(values['x'],values['y'])
        plt.xlabel(xlab)
        plt.ylabel(ylab)        
        plt.title(title)
        if show:
            plt.show()
        return plt

    def search(self,db,word='',pointDistKM=None):
        devs=self.getDevs(db)
        list=[]
        for dev in devs:
            found=False
            if word!='':
                if word in dev['id'] or word in dev['location'] or word in dev['group']:
                    list.append(dev)
                    found=True
            if not found and pointDistKM!=None:
                latP,lonP,dist=pointDistKM
                
                di=haversine(dev['lon'],dev['lat'],lonP,latP)/1000
                #print(lonP,latP,dev['lon'],dev['lat'],di,dist)
                if di<=dist:
                    list.append(dev)
        return list

    def mapDevs(self,listDevs):         
        lons  =list(x['lon'] for x in listDevs) 
        lats  =list(x['lat'] for x in listDevs)
        places=list(x['location'] for x in listDevs)

        import matplotlib.pyplot as plt
        import cartopy.crs as ccrs
        fig = plt.figure()
        ax = fig.add_subplot(1, 1, 1,
                             projection=ccrs.PlateCarree())
        ax.scatter(lons, lats,s =100)
        ax.stock_img()
        ax.coastlines()
        ax.gridlines()
        ax.set_extent([min(lons)-0.5,max(lons)+0.5,min(lats)-0.5,max(lats)+0.5])
        for x, y, text in zip(lons, lats, places):
            plt.text(x, y, text, fontsize=6)
            
        fig.show()    
    
if __name__ == '__main__':
    sdb=seaLevelDB()
    #print (sdb.getDBs())
    #print(sdb.getDevs('JRC_TAD',60*24,'True'))
    #print(sdb.getLevel('NOAA TC','1611400','2024-10-04 10:00:00','2024-10-04 15:00:00'))

    dbs=sdb.getDBs()
    dbs=['INCOIS']
    for db in dbs:
        devs=sdb.getDevs(db)
        print('****************')
        print('**' +db +' **')
        for dev in devs:
            print(dev['id'],dev['location'],dev['lon'],dev['lat'])
        