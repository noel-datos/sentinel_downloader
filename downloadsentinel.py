# import modules
import os
from datetime import date
from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt

# connect to the API
api = SentinelAPI('noel.datos', 'datos2018', 'https://cophub.copernicus.eu/dhus')

# read geojson
geojson_dir = r'C:\Users\jeromepogi\Desktop\Sentinel1 PH\Sentinel 1A\s1a geojson'
geojson = os.path.join(geojson_dir, 'C1.geojson')
footprint = geojson_to_wkt(read_geojson(geojson))

# query keywords
start_date = 'NOW-26DAYS'
end_date = 'NOW'
file_name = 'S1A*'
product_type = 'SLC'
platform_name = 'Sentinel-1'
orbit_direction = 'Descending'
polarisation_mode = None
cloud_cover_percentage = None
sensor_operational_mode = None

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
products = api.query(footprint,
                     date = (start_date, end_date),
                     raw = raw_query)

### download all results from the search
##api.download_all(products)

for product in products:
    print product

### GeoJSON FeatureCollection containing footprints and metadata of the scenes
##api.to_geojson(products)
