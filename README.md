# VDownload - A Powerful Geospatial Data Downloader

## Installation: 
- Using pip install: 
  ``` bash 
  pip install vdownload --upgrade
  ```
    
- Visit vdownload on [PyPI](https://pypi.org/project/vdownload/)

## Usage:

### OSM data:
#### Downnload OSM data by country/ region
  ``` bash 
  > osmdownload <country or region name>
  ```
Ex: `> osmdownload vietnam` 

#### Show OSM info (.pbf)
  ``` bash 
  > osminfo <OSM file>
  ```
Ex: `> osminfo vietnam.osm.pbf` 

#### Convert OSM daata to GeoJSON
  ``` bash 
  > osm2geojson -i <path_to_osm_file.osm.pbf> -o <output_file.geojson>
  ```
Ex: `> osm2geojson -i vietnam.osm.pbf -o vietnam.geojson` 

### Google Open Buildings:
#### Download Google Open Buildings by country:
  ``` bash 
  > openbuildings <country name or iso3 code>
  ```
Ex: `> openbuildings vietnam` or `> openbuildings vnm`

### PMTIles:
#### Download PMTiles by country:
  ``` bash 
  > pmtiles extract <url> --country <country name or iso3 code> ouput.pmtiles
  > pmtiles extract <url> --bbox= ouput.pmtiles
  ```
Ex: `> pmtiles extract  https://build.protomaps.com/20241027.pmtiles --country VNM vietnam.pmtiles` or `> openbuildings vnm`
  

#### Serve PMTiles:
  ``` bash 
  > pmtiles serve .
    # serves this directory at http://localhost:8080/TILESET/{z}/{x}/{y}.mvt 
    # the .pmtiles extension is added automatically
    # TileJSON at http://localhost:8080/TILESET.json
    pmtiles serve . --bucket=https://example.com
    pmtiles serve / --bucket=s3://BUCKET_NAME
    pmtiles serve PREFIX --bucket=s3://BUCKET_NAME
  > 
  ```
Ex: `> pmtiles serve .  --bucket=https://map-api-new.sovereignsolutions.net/sovereign/v20240410/vietnam_pmtiles` 


