# import modules
import os
import sqlite3
from datetime import date, datetime
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# login credentials
username = ''
password = ''
url = ''

# directories
areacode = ''
geojson_dir = r''
output_dir = r''

# query keywords
start_date = None
end_date = None
file_name = None
product_type = None
platform_name = None
orbit_direction = None
polarisation_mode = None
cloud_cover_percentage = None
sensor_operational_mode = None

# post-search modes
printProducts = True
writeToDB = False
downloadProducts = False
getGeoJSON = False

# connect to the API
api = SentinelAPI(username, password, url)

# read geojson
geojson = os.path.join(geojson_dir, '%s.geojson' % areacode)
footprint = geojson_to_wkt(read_geojson(geojson))

raw_query = ''
if file_name is not None:
    raw_query = raw_query + 'filename:%s AND ' % file_name
if product_type is not None:
    raw_query = raw_query + 'producttype:%s AND ' % product_type
if platform_name is not None:
    raw_query = raw_query + 'platformname:%s AND ' % platform_name
if orbit_direction is not None:
    raw_query = raw_query + 'orbitdirection:%s AND ' % orbit_direction
if polarisation_mode is not None:
    raw_query = raw_query + 'polarisationmode:%s AND ' % polarisation_mode
if cloud_cover_percentage is not None:
    raw_query = raw_query + 'cloudcoverpercentage:%s AND ' % cloud_cover_percentage
if sensor_operational_mode is not None:
    raw_query = raw_query + 'sensoroperationalmode:%s AND ' % sensor_operational_mode
raw_query = raw_query[:-5]

# search by polygon, time, and SciHub query keywords
products = api.query(footprint, date = (start_date, end_date), raw = raw_query)

# print results from the search
if printProducts:
    print "%d products found." % len(products)
    for product in products:
        print product

# write to database
if writeToDB:
    conn = sqlite3.connect('sentinel')
    c = conn.cursor()
    products_new = dict(products)
    for product in products:
        c.execute('SELECT * FROM downloads where productid = ?', (product,)) 
        temp = c.fetchone()
        if temp is None:
            if products[product]['filename'].startswith('S1A'):
                attr_platformname = 'Sentinel-1A'
            elif products[product]['filename'].startswith('S1B'):
                attr_platformname = 'Sentinel-1B'
            attr_dateacquired = str(products[product]['beginposition']).split()[0]
            attr_producttype = products[product]['producttype']
            attr_orbitdirection = products[product]['orbitdirection']
            attr_polarisationmode = products[product]['polarisationmode']
            attr_sensoropmode = products[product]['sensoroperationalmode']
            attr_productid = product
            attr_datedownloaded = str(datetime.today()).split()[0]
            parameters = (attr_platformname, areacode, attr_dateacquired,
                          attr_producttype, attr_orbitdirection,
                          attr_polarisationmode, attr_sensoropmode,
                          attr_productid, attr_datedownloaded)
            c.execute("INSERT INTO downloads VALUES (NULL,?,?,?,?,?,?,?,?,?)", parameters)
    else:
        products_new.pop(product)
        
    conn.commit()
    conn.close()

# download all results from the search
if downloadProducts:
    api.download_all(products, output_dir)

# GeoJSON FeatureCollection containing footprints and metadata of the scenes
if getGeoJSON:
    api.to_geojson(products)
