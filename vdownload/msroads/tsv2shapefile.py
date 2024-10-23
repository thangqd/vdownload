import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import json
import argparse

from tqdm import tqdm  # Import tqdm for progress bar

# Initialize tqdm with Pandas
tqdm.pandas()

def convert_tsv_to_shapefile(tsv_file, target_id=None):
    # Load the TSV file
    data = pd.read_csv(tsv_file, sep='\t', header=None, names=['ID', 'GeoJSON'])
    
    # If target_id is specified, filter the DataFrame
    if target_id:
        filtered_data = data[data['ID'] == target_id]
        if filtered_data.empty:
            print(f"No data found for ID: {target_id}")
            return
    else:
        # If not specified, group by ID to create shapefiles for each unique ID
        ids = data['ID'].unique()
        for id_ in ids:
            convert_tsv_to_shapefile(tsv_file, target_id=id_)
        return

    # Function to convert GeoJSON to LineString
    def extract_line_string(geojson_str):
        geojson = json.loads(geojson_str)
        coordinates = geojson['geometry']['coordinates']
        return LineString(coordinates)

    # Create a GeoDataFrame with filtered data and convert GeoJSON to geometry
    filtered_data['geometry'] = filtered_data['GeoJSON'].progress_apply(extract_line_string)  # Use tqdm for progress bar
    
    # Create GeoDataFrame, drop the 'GeoJSON' column to avoid adding it to the shapefile
    gdf = gpd.GeoDataFrame(filtered_data.drop(columns=['GeoJSON']), geometry='geometry')

    # Set the coordinate reference system (CRS) to WGS 84
    gdf.crs = "EPSG:4326"

    # Generate output shapefile name
    output_shapefile = os.path.join(os.path.dirname(tsv_file), f"{target_id}.shp")

    # Save to shapefile without the 'GeoJSON' field
    gdf.to_file(output_shapefile, driver='ESRI Shapefile')
    print(f"Shapefile saved to {output_shapefile}")

def main():
    # Set up argument parsing
    parser = argparse.ArgumentParser(description='Convert TSV from MS road detections to Shapefile.')
    parser.add_argument('input', type=str, help='Path to the input TSV file.')
    parser.add_argument('-country', type=str, help='ISO3 Country Code (optional). E.g -country IND')

    # Parse the arguments
    args = parser.parse_args()

    # Call the conversion function with the provided arguments
    convert_tsv_to_shapefile(args.input, args.country)

if __name__ == "__main__":
    main()  # Run the main function
