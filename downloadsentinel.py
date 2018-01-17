# import modules
import os
from datetime import date
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# login credentials
username = ''
password = ''

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

# output modes
downloadProducts = False
printProducts = True
getGeoJSON = False

# connect to the API
api = SentinelAPI(username, password, 'https://scihub.copernicus.eu/dhus')

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

# download all results from the search
if downloadProducts:
    api.download_all(products, output_dir)

# print results from the search
if printProducts:
    print "%d products found." % len(products)
    for product in products:
        print product

# GeoJSON FeatureCollection containing footprints and metadata of the scenes
if getGeoJSON:
    api.to_geojson(products)
