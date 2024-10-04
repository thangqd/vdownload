# VDownload - A Powerful Geospatial Data Downloader

## Installation: 
- Using pip install (Windows/ Linux):
  ``` bash 
  pip install vdownload
  ```
- Show information of installed vdownload: 
  ``` bash 
  pip show vdownload
  ```
- Install the latest vertion of vdownload:
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


