import os
import pandas as pd
import geopandas as gpd
from shapely.geometry import LineString
import json
import argparse

from tqdm import tqdm  # Import tqdm for progress bar

# Initialize tqdm with Pandas
tqdm.pandas()

def convert_tsv_to_shapefile(tsv_file, country_code=None):
    # Load the TSV file
    data = pd.read_csv(tsv_file, sep='\t', header=None, names=['country', 'GeoJSON'])

    # Extract unique countrys and save to CSV without header, as a comma-separated single row
    country_codes = data['country'].unique()
    output_csv = os.path.join(os.path.dirname(tsv_file), 'country_codes.csv')
    
    with open(output_csv, 'w') as f:
        f.write(','.join(country_codes))  # Write countrys in a single line, comma-separated
    
    print(f"Distinct countrys saved to {output_csv}")
    
    # If country_code is specified, filter the DataFrame
    if country_code:
        filtered_data = data[data['country'] == country_code]
        if filtered_data.empty:
            print(f"No data found for country: {country_code}")
            return
    else:
        # If not specified, group by country to create shapefiles for each unique country
        for country_ in country_codes:
            convert_tsv_to_shapefile(tsv_file, country_code=country_)
        return

    # Function to convert GeoJSON to LineString
    def extract_line_string(geojson_str):
        geojson = json.loads(geojson_str)
        coordinates = geojson['geometry']['coordinates']
        return LineString(coordinates)

    # Create a GeoDataFrame with filtered data and convert GeoJSON to geometry
    filtered_data['geometry'] = filtered_data['GeoJSON'].progress_apply(extract_line_string)  # Use tqdm for progress bar
    
    # Create GeoDataFrame, drop the 'GeoJSON' column to avocountry adding it to the shapefile
    gdf = gpd.GeoDataFrame(filtered_data.drop(columns=['GeoJSON']), geometry='geometry')

    # Set the coordinate reference system (CRS) to WGS 84
    gdf.crs = "EPSG:4326"

    # Generate output shapefile name
    output_shapefile = os.path.join(os.path.dirname(tsv_file), f"{country_code}.shp")

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

    # Call the conversion function with the provcountryed arguments
    convert_tsv_to_shapefile(args.input, args.country)

if __name__ == "__main__":
    main()  # Run the main function
